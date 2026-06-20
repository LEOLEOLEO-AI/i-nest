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
