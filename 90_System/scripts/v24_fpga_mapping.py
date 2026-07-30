"""v24 FEP-STDP Fusion → FPGA 异步电路映射
==========================================
将 v24 的五个深度融合机制映射到 NCL 异步电路硬件架构

映射层级:
  L1: Python行为级 (本文件 — 扩展 fpga_sim_framework.py)
  L2: Verilog RTL (sdio_bond_core_v24.v — FEP融合版)
  L3: VCK190 原型验证

v24 五机制硬件映射:
  1. FEP盆地追踪 → 硬件直方图比较器 (BRAM查找表)
  2. FEP→STDP速率调制 → 可编程增益乘法器 (DSP)
  3. FEP周期固化 → 定时器+计数比较器 (LUT)
  4. 连通性保持 → 出度计数器+门控 (LUT)
  5. 动态σ → 权重阈值化图重建 (周期性软件协处理)
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional
from collections import deque
import json, os, time

# ============================================================
# v24 FPGA 配置参数
# ============================================================

@dataclass
class V24FPGAConfig:
    """v24 FEP-STDP融合的FPGA实现参数"""
    # 定点数格式: Q8.8 (16-bit, 8整数+8小数)
    DATA_WIDTH: int = 16
    FRAC_BITS: int = 8

    # FEP盆地追踪 (BRAM实现)
    FEP_BASIN_DEPTH: int = 20       # 滑动窗口深度
    FEP_BASIN_THRESH: int = 0x001A  # Q8.8: 0.99 threshold

    # STDP速率调制 (DSP实现)
    FEP_LTP_BOOST_Q: int = 0x0166   # Q8.8: 1.4
    FEP_LTD_SUPPRESS_Q: int = 0x009A # Q8.8: 0.6

    # 周期固化 (定时器+LUT)
    CONSOLIDATE_PERIOD: int = 25    # 固化周期
    CONSOLIDATE_RATE_Q: int = 0x0014 # Q8.8: 0.08

    # 连通性约束
    MIN_OUT_DEG: int = 3

    # 时钟等效 (NCL无全局时钟,此为主流水线等效)
    EQUIV_CLK_MHZ: float = 200.0    # 等效时钟频率

    def q8_8(self, val: float) -> int:
        """浮点 → Q8.8定点"""
        return int(val * (1 << self.FRAC_BITS))

    def from_q8_8(self, val: int) -> float:
        """Q8.8定点 → 浮点"""
        return val / (1 << self.FRAC_BITS)


# ============================================================
# v24 FEP 盆地追踪器 (硬件化)
# ============================================================

class FEPBasinTracker:
    """v24 FEP盆地追踪的硬件实现

    FPGA映射:
      - basin_min: BRAM (1写1读, 双端口)
      - basin_count: 分布式RAM (LUTRAM)
      - F_converged: 1-bit寄存器
      - 比较器: 专用LUT (A < B * 0.99 → 移位+减法)

    每节点资源: ~64 LUT + 32-bit BRAM
    """
    def __init__(self, n_nodes: int, cfg: V24FPGAConfig):
        self.N = n_nodes
        self.cfg = cfg

        # BRAM建模: 存储盆地最小值
        self.basin_min = np.full(n_nodes, 0x7FFF, np.int32)  # Q8.8 max
        self.basin_count = np.zeros(n_nodes, np.uint8)
        self.F_converged = np.zeros(n_nodes, bool)

    def update(self, node_idx: int, F_local_q: int):
        """单周期硬件更新 (组合逻辑+BRAM读写)"""
        if F_local_q == 0:
            return

        # 比较: F_local < basin_min * 0.99
        basin_scaled = (self.basin_min[node_idx] * 99) >> 7  # *99/128 ≈ 0.773
        # 更精确: *0.99 = (val * 253) >> 8
        basin_scaled = (self.basin_min[node_idx] * 253) >> 8

        if F_local_q < basin_scaled:
            # 新盆地: 更新最小值, 重置计数
            self.basin_min[node_idx] = F_local_q
            self.basin_count[node_idx] = 0
            self.F_converged[node_idx] = False
        else:
            # 留在盆地: 增加计数
            if self.basin_count[node_idx] < 255:
                self.basin_count[node_idx] += 1
            if self.basin_count[node_idx] > self.cfg.FEP_BASIN_DEPTH:
                self.F_converged[node_idx] = True

    def is_converged(self, node_idx: int) -> bool:
        return self.F_converged[node_idx]


# ============================================================
# v24 FEP-STDP 融合键核 (扩展 SDIOBondCore)
# ============================================================

@dataclass
class V24BondCore:
    """v24 FEP-STDP深度融合的硬件键核

    相比v0.1的SDIOBondCore, v24增加:
      1. FEP盆地状态输入 → STDP速率调制
      2. 周期固化信号 → 强制E-S→E-L转换
      3. LTP/LTD衰减(不硬复位)
      4. 固化率自适应寄存器
    """
    bond_id: int
    src_node: int
    tgt_node: int

    # 权重 (Q8.8定点)
    weight: int = 0x0080          # 0.5
    # 键类型: 0=E-S, 2=E-L, 4=电气
    bond_type: int = 0
    activation_energy: int = 0x0026  # Ea_S = 0.15 Q8.8

    # STDP计数器 (v24: 衰减不硬复位)
    ltp_count: int = 0
    ltd_count: int = 0
    theta_ltp: int = 15           # Q0

    # v24 FEP调制信号
    fep_converged_src: bool = False
    fep_ltd_suppress: bool = False

    # 固化状态
    last_active_time: int = 0
    resource: int = 0x0100        # 1.0 Q8.8

    # 通道
    is_electrical: bool = False

    def fep_modulated_stdp(self, pre_active: bool, post_active: bool,
                           current_time: int, cfg: V24FPGAConfig) -> bool:
        """v24 FEP-STDP深度融合的单步更新

        返回: True 如果发生E-S→E-L固化
        """
        if self.is_electrical:
            return False

        if pre_active and post_active:
            # LTP: 收敛节点加速
            self.ltp_count += 1
            self.ltd_count = max(0, self.ltd_count - 1)  # v24: 衰减

            boost = cfg.FEP_LTP_BOOST_Q if self.fep_converged_src else 0x0100
            dw = (boost * 0x0002) >> 8  # Q8.8: eta_ltp * boost
            self.weight = min(0x0300, self.weight + dw)  # clamp to 3.0 max

        elif pre_active and not post_active:
            # LTD: 收敛节点抑制
            self.ltd_count += 1
            self.ltp_count = max(0, self.ltp_count - 1)  # v24: 衰减

            suppress = cfg.FEP_LTD_SUPPRESS_Q if self.fep_converged_src else 0x0100
            dw = (suppress * 0x0001) >> 8  # eta_ltd * suppress
            self.weight = max(0x0001, self.weight - dw)  # clamp to 0.01 min

        self.last_active_time = current_time

        # v24: LTP/LTD比值判定固化 (ratio >= 3.0)
        ltd_safe = max(self.ltd_count, 1)
        ltp_ratio = self.ltp_count / ltd_safe
        if ltp_ratio >= 3.0 and self.ltp_count >= 5 and self.bond_type == 0:
            self.bond_type = 2  # E-S → E-L
            self.activation_energy = 0x00D9  # Ea_L = 0.85 Q8.8
            # 部分重置LTP
            self.ltp_count = max(0, self.ltp_count - self.theta_ltp)
            return True
        return False

    def fep_periodic_consolidate(self, converged_src: bool, rate_q: int) -> bool:
        """v24 FEP周期固化: 收敛节点的E-S边直接转E-L"""
        if self.bond_type != 0:  # 只转换E-S
            return False
        if not converged_src:
            return False
        if self.weight < 0x000D:  # min weight = 0.05 Q8.8
            return False
        # 概率固化 (LFSR伪随机)
        if np.random.randint(0, 0x0100) < rate_q:
            self.bond_type = 2
            self.activation_energy = 0x00D9
            return True
        return False

    def compute_fep(self, h_pre: int, h_post: int) -> int:
        """局部自由能 Q8.8定点计算"""
        pred = (h_pre * self.weight) >> 8
        err = pred - h_post
        pe = (err * err) >> 8
        cp = (self.activation_energy * ((self.weight * self.weight) >> 8)) >> 8
        return pe + cp


# ============================================================
# v24 芯片规模估算器
# ============================================================

class V24ChipEstimator:
    """v24 FEP-STDP融合架构的芯片资源估算"""

    # 每节点硬件资源 (v24增加FEP盆地追踪)
    LUTS_PER_NODE = 300      # v0.1: 200 → v24: +100 (盆地追踪+自适应固化)
    BRAM_PER_NODE_KB = 0.15  # 盆地最小値存储
    DSP_PER_NODE = 4         # v0.1: 2 → v24: +2 (FEP调制乘法器)

    # Versal VCK190规格
    TOTAL_LUTS = 899840
    TOTAL_BRAM_KB = 34600
    TOTAL_DSPS = 1968
    UTILIZATION = 0.75

    @classmethod
    def estimate(cls, n_nodes: int, avg_bonds: int = 10) -> dict:
        usable_luts = cls.TOTAL_LUTS * cls.UTILIZATION
        usable_dsps = cls.TOTAL_DSPS * cls.UTILIZATION
        usable_bram = cls.TOTAL_BRAM_KB * cls.UTILIZATION

        n_bonds = n_nodes * avg_bonds
        luts_needed = n_bonds * 200 + n_nodes * 100  # bond核 + 盆地追踪
        dsps_needed = n_bonds * cls.DSP_PER_NODE / avg_bonds
        bram_needed = n_nodes * cls.BRAM_PER_NODE_KB

        max_nodes_lut = int(usable_luts / (200 * avg_bonds + 100))
        max_nodes_dsp = int(usable_dsps / (cls.DSP_PER_NODE))
        max_nodes_bram = int(usable_bram / cls.BRAM_PER_NODE_KB)
        max_nodes = min(max_nodes_lut, max_nodes_dsp, max_nodes_bram)

        power_mw = n_bonds * 0.003 * 0.1  # 3μW/bond × 10%激活率

        return {
            "n_nodes": n_nodes,
            "n_bonds": n_bonds,
            "luts_used": int(luts_needed),
            "luts_util_pct": round(luts_needed / cls.TOTAL_LUTS * 100, 1),
            "dsps_used": int(dsps_needed),
            "bram_kb_used": round(bram_needed, 1),
            "max_nodes_conservative": max_nodes,
            "power_mw": round(power_mw, 2),
            "equiv_clock_mhz": 200,
            "latency_per_spike_ns": 5.0,  # NCL流水线
            "throughput_m_spikes_s": round(200 / 5.0, 1),  # 40M spikes/s
        }


# ============================================================
# v24 Verilog 骨架生成器
# ============================================================

def generate_v24_bond_verilog() -> str:
    """生成 v24 FEP-STDP融合的Verilog IP核"""
    return """\
// SDIO Bond Core v24 — FEP-STDP 深度融合异步电路 IP 核
// Target: Xilinx Versal ACAP (VCK190)
// Author: iNEST Research Team, Tianjin University
// Date: 2026-06-03
//
// v24新增 (vs v0.1):
//   1. FEP盆地追踪 (BRAM + 比较器)
//   2. FEP调制STDP速率 (DSP乘法器)
//   3. 周期固化逻辑 (定时器)
//   4. LTP/LTD衰减 (不硬复位)
//   5. 连通性约束 (出度计数器)

`timescale 1ns / 1ps

module sdio_bond_core_v24 #(
    parameter DATA_WIDTH = 16,
    parameter FRAC_BITS   = 8,
    parameter THETA_LTP   = 15,
    parameter FEP_LTP_BOOST   = 16'h0166,  // Q8.8: 1.4
    parameter FEP_LTD_SUPPRESS= 16'h009A,  // Q8.8: 0.6
    parameter CONSOLIDATE_PERIOD = 25,
    parameter BASIN_WINDOW = 20,
    parameter MIN_OUT_DEG  = 3
) (
    // NCL 双轨输入
    input  wire pre_data0, pre_data1,
    input  wire post_data0, post_data1,

    // FEP盆地状态输入 (来自盆地追踪器)
    input  wire fep_converged_src,   // 源节点是否收敛
    input  wire fep_converged_tgt,   // 目标节点是否收敛

    // 周期固化使能 (来自全局定时器)
    input  wire consolidate_enable,

    // 控制
    input  wire rst_n,
    input  wire clk_equiv,  // 等效时钟 (仅用于周期固化定时, 非NCL数据路径)

    // 权重输出
    output reg [DATA_WIDTH-1:0] weight_out,

    // 键类型输出
    output reg [2:0] bond_type,

    // 固化事件输出
    output reg consolidate_event,

    // FEP自由能输出
    output reg [DATA_WIDTH-1:0] fep_out,

    // 完成检测
    output wire done
);

    // ===== v24: STDP状态 (衰减式计数器) =====
    reg [7:0] ltp_counter;
    reg [7:0] ltd_counter;
    reg [15:0] last_active_timer;
    reg [DATA_WIDTH-1:0] weight;
    reg [2:0] bond_state;  // 000=E-S, 010=E-L, 100=电

    // ===== v24: FEP调制增益选择 =====
    wire [DATA_WIDTH-1:0] ltp_gain = fep_converged_src ? FEP_LTP_BOOST : 16'h0100;
    wire [DATA_WIDTH-1:0] ltd_gain = fep_converged_src ? FEP_LTD_SUPPRESS : 16'h0100;

    // ===== v24: LTP/LTD 衰减更新 =====
    always @(posedge pre_data or posedge post_data or negedge rst_n) begin
        if (!rst_n) begin
            weight <= {FRAC_BITS{1'b0}, 1'b1, {(FRAC_BITS-1){1'b0}}}; // 0.5
            ltp_counter <= 0;
            ltd_counter <= 0;
            bond_state <= 3'b000;
            consolidate_event <= 0;
        end else begin
            // NCL数据有效检测
            if (pre_data0 ^ pre_data1) begin  // pre valid
                if (post_data0 ^ post_data1) begin  // post also valid
                    // LTP: pre-post共激活
                    ltp_counter <= ltp_counter + 1;
                    ltd_counter <= (ltd_counter > 0) ? ltd_counter - 1 : 0;  // v24: 衰减
                    // DSP: weight += eta_ltp * ltp_gain
                    weight <= weight + ((ltp_gain * 2) >> FRAC_BITS);
                end else begin
                    // LTD: pre-only
                    ltd_counter <= ltd_counter + 1;
                    ltp_counter <= (ltp_counter > 0) ? ltp_counter - 1 : 0;  // v24: 衰减
                    weight <= weight - ((ltd_gain * 1) >> FRAC_BITS);
                end
                last_active_timer <= 0;
            end
        end
    end

    // ===== v24: E-S→E-L固化 (LTP/LTD比值判定) =====
    wire ltp_ratio_ok = (ltp_counter >= (ltd_counter * 3)) && (ltp_counter >= 5);

    always @(posedge clk_equiv) begin
        if (ltp_ratio_ok && bond_state == 3'b000) begin
            bond_state <= 3'b010;  // E-S → E-L
            ltp_counter <= (ltp_counter > THETA_LTP) ? ltp_counter - THETA_LTP : 0;
        end

        // v24: 周期固化 (FEP驱动)
        if (consolidate_enable && fep_converged_src && bond_state == 3'b000
            && weight > {FRAC_BITS{1'b0}, 5'd13}) begin  // weight > 0.05
            bond_state <= 3'b010;
            consolidate_event <= 1;
        end else begin
            consolidate_event <= 0;
        end
    end

    // ===== Output =====
    assign weight_out = weight;
    assign bond_type = bond_state;
    assign done = (pre_data0 ^ pre_data1) & (post_data0 ^ post_data1);

endmodule


// ===== v24 FEP盆地追踪器 (顶层模块) =====
module fep_basin_tracker_v24 #(
    parameter N_NODES = 279,
    parameter DATA_WIDTH = 16,
    parameter FRAC_BITS = 8,
    parameter BASIN_WINDOW = 20
) (
    input  wire clk_equiv,
    input  wire rst_n,
    input  wire [7:0] node_idx,           // 当前计算的节点ID
    input  wire [DATA_WIDTH-1:0] F_local, // 局部自由能
    input  wire F_valid,                   // 自由能有效标志

    output reg fep_converged [0:N_NODES-1], // 每节点收敛标志 (BRAM)
    output reg [DATA_WIDTH-1:0] basin_min [0:N_NODES-1],
    output reg [7:0] basin_count [0:N_NODES-1]
);
    // BRAM: 双端口实现
    // Port A: 读取当前盆地最小值
    // Port B: 写入更新后的值

    reg [DATA_WIDTH-1:0] basin_min_read;
    reg [7:0] basin_count_read;
    reg converged_read;

    always @(posedge clk_equiv or negedge rst_n) begin
        if (!rst_n) begin
            // 初始化所有节点
            integer i;
            for (i = 0; i < N_NODES; i = i + 1) begin
                basin_min[i] <= {DATA_WIDTH{1'b1}};  // 最大值
                basin_count[i] <= 0;
                fep_converged[i] <= 0;
            end
        end else if (F_valid) begin
            // 读取当前值
            basin_min_read = basin_min[node_idx];
            basin_count_read = basin_count[node_idx];

            // 比较: F_local < basin_min * 0.99
            // 硬件实现: basin_min * 253 >> 8
            wire [DATA_WIDTH-1:0] basin_scaled;
            assign basin_scaled = (basin_min_read * 16'd253) >> FRAC_BITS;

            if (F_local < basin_scaled) begin
                basin_min[node_idx] <= F_local;
                basin_count[node_idx] <= 0;
                fep_converged[node_idx] <= 0;
            end else begin
                if (basin_count_read < 255)
                    basin_count[node_idx] <= basin_count_read + 1;
                if (basin_count_read > BASIN_WINDOW)
                    fep_converged[node_idx] <= 1;
            end
        end
    end

endmodule
"""


# ============================================================
# v24 硬件-软件联合仿真
# ============================================================

class V24HwSwCoSim:
    """v24 FEP-STDP融合的硬件-软件联合仿真

    模拟在FPGA上运行v24架构的行为:
      - 软件: 图拓扑管理 + 动态σ计算 (周期性协处理)
      - 硬件: STDP + FEP盆地追踪 + 周期固化 (实时脉冲处理)
    """

    def __init__(self, connectome_path: str = None):
        self.cfg = V24FPGAConfig()

        # 加载连接组
        if connectome_path and os.path.exists(connectome_path):
            with open(connectome_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.N = data["N"]
            self._load_connectome(data)
        else:
            self.N = 100
            self._init_random()

        # v24硬件模块
        self.basin_tracker = FEPBasinTracker(self.N, self.cfg)
        self.bonds: List[V24BondCore] = []
        self._init_bonds()

        # 节点状态 (Q8.8)
        self.h = np.random.randint(13, 38, self.N).tolist()  # 0.05-0.15

        # 周期固化定时
        self.consolidate_timer = 0
        self.consolidate_rate_q = self.cfg.CONSOLIDATE_RATE_Q

        # 统计
        self.t = 0
        self.el_history = []
        self.sigma_history = []

        # 资源估算
        self.estimates = V24ChipEstimator.estimate(self.N)

    def _load_connectome(self, data):
        chem = data["edges_chem"]
        elec = data["edges_elec"]
        self.chem_edges = [(e[0], e[1], e[2]) for e in chem]
        self.elec_edges = [(e[0], e[1], e[2]) for e in elec]
        self.n_types = data["n_types"]

    def _init_random(self):
        self.chem_edges = []
        self.elec_edges = []
        for i in range(self.N):
            targets = np.random.choice(self.N, size=8, replace=False)
            for t in targets:
                if t != i:
                    self.chem_edges.append((i, int(t), np.random.randint(1, 37)))

    def _init_bonds(self):
        bid = 0
        # 化学键
        for src, tgt, w in self.chem_edges:
            w_q = int(min(w / 37.0, 1.0) * 256)
            bond = V24BondCore(bond_id=bid, src_node=src, tgt_node=tgt, weight=w_q)
            self.bonds.append(bond)
            bid += 1
        # 电突触 (双向)
        for src, tgt, w in self.elec_edges:
            for s, t in [(src, tgt), (tgt, src)]:
                bond = V24BondCore(bond_id=bid, src_node=s, tgt_node=t,
                                   weight=0x004D,  # 0.3
                                   bond_type=4, is_electrical=True,
                                   activation_energy=0x0080)  # 0.5
                self.bonds.append(bond)
                bid += 1

    def step(self):
        """v24硬件模拟单步"""
        self.t += 1
        self.consolidate_timer += 1

        # 脉冲输入
        n_seeds = max(1, int(self.N * 0.05))
        seeds = np.random.choice(self.N, size=n_seeds, replace=False)
        for s in seeds: self.h[s] = 256  # 1.0
        self.h = [int(h * 179 // 256) for h in self.h]  # ×0.7 衰减 (Q8.8: 0.7*256=179.2≈0xB3)

        # 遍历所有键: FEP-STDP融合更新
        consolidate_count = 0
        fep_sum = 0
        for bond in self.bonds:
            pre_active = self.h[bond.src_node] > 128  # >0.5
            post_active = self.h[bond.tgt_node] > 0x0080

            # v24: 更新FEP盆地状态
            bond.fep_converged_src = self.basin_tracker.is_converged(bond.src_node)

            # v24: FEP-STDP
            bond.fep_modulated_stdp(pre_active, post_active, self.t, self.cfg)

            # v24: 周期固化
            if self.consolidate_timer >= self.cfg.CONSOLIDATE_PERIOD:
                if bond.fep_periodic_consolidate(
                    self.basin_tracker.is_converged(bond.src_node),
                    self.consolidate_rate_q
                ):
                    consolidate_count += 1

            # FEP计算
            fep_sum += bond.compute_fep(self.h[bond.src_node], self.h[bond.tgt_node])

        # v24: 更新FEP盆地追踪器
        F_local_avg = fep_sum / max(len(self.bonds), 1)
        for i in range(self.N):
            out_bonds = [b for b in self.bonds if b.src_node == i]
            if out_bonds:
                fep_i = sum(b.compute_fep(self.h[b.src_node], self.h[b.tgt_node])
                           for b in out_bonds) // len(out_bonds)
                self.basin_tracker.update(i, fep_i)

        # 周期固化重置
        if self.consolidate_timer >= self.cfg.CONSOLIDATE_PERIOD:
            self.consolidate_timer = 0

        # v24.5: 自适应固化率
        el_ratio = self._compute_el_ratio()
        if el_ratio < 0.15:
            self.consolidate_rate_q = min(0x0033,  # 0.20
                self.consolidate_rate_q + (self.consolidate_rate_q >> 3))  # ×1.125
        elif el_ratio > 0.35:
            self.consolidate_rate_q = max(0x0005,  # 0.02
                self.consolidate_rate_q - (self.consolidate_rate_q >> 3))

        return consolidate_count

    def _compute_el_ratio(self) -> float:
        el = sum(1 for b in self.bonds if b.bond_type == 2)
        total = sum(1 for b in self.bonds if not b.is_electrical)
        return el / max(total, 1)

    def run(self, T: int = 300):
        print(f"\nv24 FPGA Hardware-Software Co-Simulation")
        print(f"  Nodes: {self.N} | Bonds: {len(self.bonds)}")
        print(f"  Q8.8 fixed-point | FEP Basin Tracker | V24BondCore")
        est = self.estimates
        print(f"  VCK190 est: {est['max_nodes_conservative']} nodes, "
              f"{est['luts_util_pct']}% LUT, {est['power_mw']} mW")
        print("-" * 65)

        for step_i in range(T):
            n_consolidated = self.step()

            if self.t % 40 == 0 or self.t < 5:
                el = self._compute_el_ratio()
                converged = self.basin_tracker.F_converged.mean()
                rate = self.cfg.from_q8_8(self.consolidate_rate_q)
                print(f"  t={self.t:4d} EL={el*100:5.1f}% "
                      f"FEP_cv={converged*100:5.1f}% "
                      f"consolidate_rate={rate:.3f} "
                      f"events={n_consolidated}")

        # 结果
        el_final = self._compute_el_ratio()
        print(f"\n  Final: EL={el_final*100:.1f}%")
        return el_final


if __name__ == "__main__":
    # 测试: v24硬件-软件联合仿真
    sim = V24HwSwCoSim(
        connectome_path="D:/Obsidian/phase1_workspace/connectome_v8_data.json"
    )
    sim.run(T=300)

    # 生成 Verilog
    verilog = generate_v24_bond_verilog()
    out_dir = "D:/Obsidian/phase1_workspace/iNEST_4_工程开发/fpga"
    os.makedirs(out_dir, exist_ok=True)
    with open(f"{out_dir}/sdio_bond_core_v24.v", "w") as f:
        f.write(verilog)
    print(f"\nVerilog written to {out_dir}/sdio_bond_core_v24.v")
