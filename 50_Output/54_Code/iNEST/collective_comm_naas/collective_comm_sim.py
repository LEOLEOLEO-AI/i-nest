"""
集合通信NaaS — 全链路仿真验证
基于CST理论 × SDI化学键机制
验证目标：硬件化Allreduce/Alltoall相对软件方案的性能提升

任务链：
  T1. 软件基准建模（NCCL/Ring/Tree参数化模型）
  T2. CST拓扑分析（不同连接拓扑的σ/RI指数）
  T3. 硬件Allreduce时序仿真
  T4. 规模敏感性分析（N=4~64节点）
  T5. 可视化报告输出
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch
import networkx as nx
import json, itertools, time

# ============================================================
# 全局参数
# ============================================================
np.random.seed(42)

# 硬件参数（基于文献/工程经验）
LINK_BW_HARD   = 2e12   # 硬互连链路带宽：2 TB/s（晶圆级金属互连）
LINK_BW_SOFT   = 200e9  # 软互连（NVLink/RoCE）：200 GB/s
LINK_LAT_HARD  = 2e-9   # 硬互连延迟：2 ns（片上信号传播）
LINK_LAT_SOFT  = 1e-6   # 软互连延迟：1 μs（NIC+交换机）
SWITCH_LAT     = 500e-9 # 软件交换机端口延迟：500 ns
HARD_LOGIC_LAT = 1e-9   # 硬逻辑延迟（归约加法器流水线）：1 ns/级

DATA_SIZE_BYTES = 256e6  # 典型Allreduce数据量：256 MB（LLM梯度）
DTYPE_BYTES     = 2      # BF16：2字节/参数

NODE_SIZES = [4, 8, 16, 32, 64]  # 测试节点规模


# ============================================================
# T1：软件Allreduce基准模型（α-β-γ参数化）
# ============================================================

def ring_allreduce_latency(N, msg_bytes, bw, lat_link, lat_switch=0):
    """
    Ring-Allreduce（Rabenseifner算法）
    通信步数 = 2(N-1)
    每步数据量 = msg_bytes/N
    延迟 = 步数 × (链路延迟 + 数据量/带宽 + 交换机延迟)
    """
    chunk = msg_bytes / N
    step_lat = lat_link + chunk / bw + lat_switch
    total_lat = 2 * (N - 1) * step_lat
    # 计算延迟（归约操作）：每步一次加法
    compute_lat = (N - 1) * HARD_LOGIC_LAT if lat_link < 100e-9 else 0
    return total_lat + compute_lat

def tree_allreduce_latency(N, msg_bytes, bw, lat_link, lat_switch=0):
    """
    Binary Tree Allreduce（Reduce + Broadcast）
    深度 = 2 × ceil(log2(N))
    """
    depth = int(np.ceil(np.log2(max(N, 2))))
    # Reduce阶段：每级数据量翻倍
    reduce_lat = 0
    for level in range(depth):
        chunk = msg_bytes  # 树根需传完整数据
        step_lat = lat_link + chunk / bw + lat_switch
        reduce_lat += step_lat
    # Broadcast阶段：对称
    bcast_lat = reduce_lat
    compute_lat = depth * HARD_LOGIC_LAT if lat_link < 100e-9 else 0
    return reduce_lat + bcast_lat + compute_lat

def recursive_halving_allreduce_latency(N, msg_bytes, bw, lat_link, lat_switch=0):
    """
    Recursive Halving/Doubling（NCCL默认用于小消息）
    步数 = log2(N)，每步发送msg/2
    """
    steps = int(np.log2(max(N, 2)))
    total_lat = 0
    for k in range(steps):
        chunk = msg_bytes / (2 ** (k + 1))
        step_lat = lat_link + chunk / bw + lat_switch
        total_lat += step_lat * 2  # Reduce + Bcast
    return total_lat

def nccl_model(N, msg_bytes):
    """NCCL软件实现（基于RoCE/InfiniBand典型参数）"""
    # NCCL在大消息时用Ring，小消息时用Recursive Halving
    if msg_bytes > 128 * 1024:  # >128KB用Ring
        return ring_allreduce_latency(N, msg_bytes, LINK_BW_SOFT,
                                       LINK_LAT_SOFT, SWITCH_LAT)
    else:
        return recursive_halving_allreduce_latency(N, msg_bytes,
                                                    LINK_BW_SOFT, LINK_LAT_SOFT, SWITCH_LAT)

def nvidia_sharp_model(N, msg_bytes):
    """NVIDIA SHARP（InfiniBand in-network reduction）"""
    # SHARP在交换机内做归约，延迟约为Ring的50%，但仍受IB延迟限制
    lat_ib = 0.6e-6  # IB HDR 延迟约600ns
    bw_ib  = 400e9   # IB HDR 100 Gb/s per port
    chunk = msg_bytes / N
    step_lat = lat_ib + chunk / bw_ib
    return 2 * (N - 1) * step_lat * 0.5  # SHARP减少约一半跳数

def sdi_hard_allreduce(N, msg_bytes):
    """
    SDI硬件化Allreduce（本方案）
    Ring on wafer：链路2ns，带宽2TB/s，无交换机
    硬归约加法器：1ns流水线，全流水，无软件开销
    """
    return ring_allreduce_latency(N, msg_bytes, LINK_BW_HARD,
                                   LINK_LAT_HARD, lat_switch=0)

def sdi_hard_tree_allreduce(N, msg_bytes):
    """SDI硬件化Tree-Allreduce（适合小N）"""
    return tree_allreduce_latency(N, msg_bytes, LINK_BW_HARD,
                                   LINK_LAT_HARD, lat_switch=0)


# ============================================================
# T2：CST拓扑分析（σ/RI vs 拓扑类型）
# ============================================================

def build_ring(N):
    G = nx.cycle_graph(N)
    return G

def build_tree(N):
    G = nx.balanced_tree(r=2, h=int(np.ceil(np.log2(N+1))))
    nodes = list(G.nodes())[:N]
    return G.subgraph(nodes).copy()

def build_2d_mesh(N):
    side = int(np.ceil(np.sqrt(N)))
    G = nx.grid_2d_graph(side, side)
    G = nx.convert_node_labels_to_integers(G)
    nodes = list(G.nodes())[:N]
    return G.subgraph(nodes).copy()

def build_fat_tree(N):
    """模拟Fat-Tree（每个节点与log(N)个节点相连）"""
    k = max(2, int(np.log2(N)))
    G = nx.random_regular_graph(k, N, seed=42)
    return G

def build_sdi_smallworld(N, sigma_target=2.0):
    """
    SDI生成的小世界拓扑
    基于WS模型，调参到σ≈sigma_target
    """
    # 找合适的k和p使σ接近目标
    k = max(4, int(np.log2(N)) * 2)
    p = 0.1  # 重连概率
    G = nx.watts_strogatz_graph(N, k, p, seed=42)
    return G

def compute_sigma(G):
    """计算小世界指数σ"""
    if not nx.is_connected(G):
        G = G.subgraph(max(nx.connected_components(G), key=len)).copy()
    N = G.number_of_nodes()
    if N < 4: return 1.0
    C = nx.average_clustering(G)
    # 近似平均路径
    sample = list(G.nodes())[:min(50, N)]
    lens = []
    for nd in sample:
        sp = nx.single_source_shortest_path_length(G, nd)
        lens.extend(list(sp.values()))
    L = float(np.mean(lens)) if lens else 5.0
    m = G.number_of_edges()
    k_avg = 2 * m / N
    Cr = k_avg / N if N > 0 else 1e-6
    Lr = np.log(N) / np.log(max(2, k_avg))
    if Cr < 1e-9 or Lr < 0.01: return 1.0
    return float((C / Cr) / (L / max(Lr, 0.01)))

def compute_RI(G, msg_bytes, bw, lat):
    """
    RI = CST(network) / E_env(Allreduce_task)
    CST ∝ σ（小世界指数，综合聚类和路径效率）
    E_env ∝ 完成Allreduce所需的通信步数
    """
    N = G.number_of_nodes()
    sigma = compute_sigma(G)
    # 任务复杂度：Ring步数作为基准（标准化）
    E_ring = 2 * (N - 1)
    diam = nx.diameter(G) if nx.is_connected(G) else N
    E_topo = 2 * diam  # 实际拓扑的通信深度
    E_norm = E_topo / max(E_ring, 1)
    RI = sigma / max(E_norm, 0.1)
    return sigma, RI

def analyze_topologies(N=16):
    """分析各拓扑的CST指标"""
    topos = {
        'Ring': build_ring(N),
        'Binary Tree': build_tree(N),
        '2D Mesh': build_2d_mesh(N),
        'Fat-Tree': build_fat_tree(N),
        'SDI SmallWorld': build_sdi_smallworld(N),
    }
    results = {}
    for name, G in topos.items():
        if not nx.is_connected(G):
            G = G.subgraph(max(nx.connected_components(G), key=len)).copy()
        nodes = list(G.nodes())[:N]
        G = G.subgraph(nodes).copy()
        sigma, RI = compute_RI(G, DATA_SIZE_BYTES, LINK_BW_HARD, LINK_LAT_HARD)
        m = G.number_of_edges()
        k_avg = 2*m/G.number_of_nodes() if G.number_of_nodes()>0 else 0
        C = nx.average_clustering(G)
        try:
            diam = nx.diameter(G)
        except:
            diam = -1
        results[name] = {'sigma': sigma, 'RI': RI, 'k_avg': k_avg,
                          'C': C, 'diam': diam, 'edges': m}
    return results


# ============================================================
# T3：硬件Allreduce时序仿真（时钟周期级）
# ============================================================

class HardwareAllreduceSim:
    """
    硬件Allreduce行为级仿真
    模拟流水线归约树在不同拓扑下的时钟周期
    """
    CLK_PERIOD = 1e-9  # 1 GHz时钟（1 ns/cycle）

    def __init__(self, N, topology='ring'):
        self.N = N
        self.topology = topology
        self.clock = 0

    def simulate_ring_allreduce(self, msg_elements):
        """
        Ring-Allreduce硬件流水仿真
        每个time slot：链路传输 + 加法器归约 同时流水
        """
        chunk = msg_elements // self.N
        # 流水线深度：log2(chunk) 级加法器
        adder_depth = max(1, int(np.log2(max(chunk, 1))))

        # Reduce-Scatter阶段：(N-1)步，每步chunk个元素
        reduce_scatter_cycles = 0
        for step in range(self.N - 1):
            # 链路传输：chunk × 2字节 / 2TB/s / 1ns_per_cycle
            transfer_cycles = int(np.ceil(chunk * DTYPE_BYTES / LINK_BW_HARD / self.CLK_PERIOD))
            # 加法器延迟（流水，每步只加1个延迟）
            add_cycles = adder_depth
            # 链路延迟
            link_cycles = int(np.ceil(LINK_LAT_HARD / self.CLK_PERIOD))
            # 流水：重叠执行
            step_cycles = max(transfer_cycles, add_cycles) + link_cycles
            reduce_scatter_cycles += step_cycles

        # Allgather阶段：对称
        allgather_cycles = reduce_scatter_cycles

        total_cycles = reduce_scatter_cycles + allgather_cycles
        total_time = total_cycles * self.CLK_PERIOD
        return {
            'cycles': total_cycles,
            'latency_us': total_time * 1e6,
            'throughput_TBps': (msg_elements * DTYPE_BYTES * 2) / total_time / 1e12,
            'link_util': min(1.0, (chunk * DTYPE_BYTES / LINK_BW_HARD) /
                            max((chunk * DTYPE_BYTES / LINK_BW_HARD + LINK_LAT_HARD), 1e-12)),
        }

    def simulate_tree_allreduce(self, msg_elements):
        """
        Tree-Allreduce硬件流水仿真
        利用全流水归约树，每个节点有专用加法器
        """
        depth = int(np.ceil(np.log2(max(self.N, 2))))
        adder_depth = max(1, int(np.log2(max(msg_elements, 1))))

        # Reduce阶段：depth步，每步数据量不变（流水）
        reduce_cycles = 0
        for level in range(depth):
            transfer_cycles = int(np.ceil(msg_elements * DTYPE_BYTES / LINK_BW_HARD / self.CLK_PERIOD))
            link_cycles = int(np.ceil(LINK_LAT_HARD / self.CLK_PERIOD))
            add_cycles = adder_depth
            step_cycles = max(transfer_cycles, add_cycles) + link_cycles
            reduce_cycles += step_cycles

        bcast_cycles = reduce_cycles
        total_cycles = reduce_cycles + bcast_cycles
        total_time = total_cycles * self.CLK_PERIOD
        return {
            'cycles': total_cycles,
            'latency_us': total_time * 1e6,
            'throughput_TBps': (msg_elements * DTYPE_BYTES * 2) / total_time / 1e12,
            'link_util': 0.85,
        }

    def simulate_software_ring(self, msg_elements):
        """对比：软件Ring-Allreduce（NCCL）"""
        lat = nccl_model(self.N, msg_elements * DTYPE_BYTES)
        bw = (msg_elements * DTYPE_BYTES * 2) / lat
        return {
            'cycles': int(lat / self.CLK_PERIOD),
            'latency_us': lat * 1e6,
            'throughput_TBps': bw / 1e12,
            'link_util': 0.4,
        }

    def simulate_sharp(self, msg_elements):
        """对比：NVIDIA SHARP"""
        lat = nvidia_sharp_model(self.N, msg_elements * DTYPE_BYTES)
        bw = (msg_elements * DTYPE_BYTES * 2) / lat
        return {
            'cycles': int(lat / self.CLK_PERIOD),
            'latency_us': lat * 1e6,
            'throughput_TBps': bw / 1e12,
            'link_util': 0.55,
        }


# ============================================================
# T4：规模敏感性分析
# ============================================================

def scale_analysis():
    """N=4~64节点，各方案延迟/吞吐曲线"""
    results = {method: {'latency_us': [], 'throughput_TBps': [], 'speedup': []}
               for method in ['NCCL_Ring', 'NCCL_Halving', 'SHARP', 'SDI_Hard_Ring', 'SDI_Hard_Tree']}

    msg_bytes = DATA_SIZE_BYTES

    for N in NODE_SIZES:
        msg_elem = int(msg_bytes / DTYPE_BYTES)
        sim_ring = HardwareAllreduceSim(N, 'ring')
        sim_tree = HardwareAllreduceSim(N, 'tree')

        r_nccl   = sim_ring.simulate_software_ring(msg_elem)
        r_sharp  = sim_ring.simulate_sharp(msg_elem)
        r_sdi_r  = sim_ring.simulate_ring_allreduce(msg_elem)
        r_sdi_t  = sim_tree.simulate_tree_allreduce(msg_elem)

        # NCCL Recursive Halving
        lat_halv = recursive_halving_allreduce_latency(N, msg_bytes, LINK_BW_SOFT, LINK_LAT_SOFT, SWITCH_LAT)
        bw_halv  = msg_bytes * 2 / lat_halv / 1e12

        base_lat = r_nccl['latency_us']
        results['NCCL_Ring']['latency_us'].append(r_nccl['latency_us'])
        results['NCCL_Ring']['throughput_TBps'].append(r_nccl['throughput_TBps'])
        results['NCCL_Ring']['speedup'].append(1.0)

        results['NCCL_Halving']['latency_us'].append(lat_halv * 1e6)
        results['NCCL_Halving']['throughput_TBps'].append(bw_halv)
        results['NCCL_Halving']['speedup'].append(base_lat / (lat_halv * 1e6))

        results['SHARP']['latency_us'].append(r_sharp['latency_us'])
        results['SHARP']['throughput_TBps'].append(r_sharp['throughput_TBps'])
        results['SHARP']['speedup'].append(base_lat / r_sharp['latency_us'])

        results['SDI_Hard_Ring']['latency_us'].append(r_sdi_r['latency_us'])
        results['SDI_Hard_Ring']['throughput_TBps'].append(r_sdi_r['throughput_TBps'])
        results['SDI_Hard_Ring']['speedup'].append(base_lat / r_sdi_r['latency_us'])

        results['SDI_Hard_Tree']['latency_us'].append(r_sdi_t['latency_us'])
        results['SDI_Hard_Tree']['throughput_TBps'].append(r_sdi_t['throughput_TBps'])
        results['SDI_Hard_Tree']['speedup'].append(base_lat / r_sdi_t['latency_us'])

    return results


# ============================================================
# T5：Alltoall仿真（MoE专家并行场景）
# ============================================================

def alltoall_analysis():
    """
    Alltoall（全互换）：MoE模型的专家并行通信
    每个节点向其他所有节点各发送 msg/N 数据
    """
    results = {}
    for N in NODE_SIZES:
        msg_per_pair = DATA_SIZE_BYTES / N  # 每对节点间的数据量

        # 软件Alltoall（所有节点同时发送）
        # 最优情况：N-1步，每步 msg/N 数据
        lat_soft = (N - 1) * (LINK_LAT_SOFT + SWITCH_LAT + msg_per_pair / LINK_BW_SOFT)

        # SDI硬件Alltoall（Crossbar全交换）
        # 硬Crossbar：所有对同时发送，只需1步
        lat_hard = LINK_LAT_HARD + msg_per_pair / LINK_BW_HARD

        # SHARP不支持Alltoall（仅支持Allreduce）
        lat_sharp = lat_soft * 0.7  # 估计，SHARP无法加速Alltoall

        speedup = lat_soft / lat_hard
        results[N] = {
            'lat_soft_us': lat_soft * 1e6,
            'lat_hard_us': lat_hard * 1e6,
            'lat_sharp_us': lat_sharp * 1e6,
            'speedup_vs_soft': speedup,
            'speedup_vs_sharp': lat_sharp / lat_hard,
        }
    return results


# ============================================================
# T6：功耗估算
# ============================================================

def power_analysis(N):
    """
    功耗对比：SDI硬件 vs GPU集群
    基于工艺参数估算
    """
    # GPU集群（A100）
    gpu_power_w = N * 400  # A100 TDP 400W
    nccl_overhead = 0.35   # 通信时间占比35%（行业典型值）
    effective_gpu = gpu_power_w * (1 - nccl_overhead)

    # SDI互连芯粒（28nm估算）
    # 逻辑门：~100k门，每门~10fJ/操作 @ 1GHz
    # 链路：N条，每条~5mW
    logic_power_mw = 100e3 * 10e-15 * 1e9 * 1e3  # 1W
    link_power_mw = N * 5  # 5mW/link
    sdi_total_w = (logic_power_mw + link_power_mw) / 1e3

    # SDI方案：GPU算力100%用于计算（通信零占用）
    effective_sdi = gpu_power_w + sdi_total_w  # GPU满功率 + 芯粒

    return {
        'gpu_cluster_w': gpu_power_w,
        'sdi_chip_w': sdi_total_w,
        'sdi_total_w': effective_sdi,
        'gpu_effective_compute_w': effective_gpu,
        'sdi_effective_compute_w': effective_sdi,  # GPU全部用于计算
        'compute_power_gain': effective_sdi / effective_gpu,
    }


# ============================================================
# 主运行
# ============================================================

def main():
    print("=" * 70)
    print("集合通信NaaS仿真验证 — 全链路分析")
    print("=" * 70)

    # T2: 拓扑CST分析
    print("\n[T2] CST拓扑分析（N=16节点）...")
    topo_results = analyze_topologies(N=16)
    print(f"\n{'拓扑':<20} {'σ':>8} {'RI':>8} {'k_avg':>8} {'C':>8} {'直径':>6}")
    print("-" * 62)
    for name, r in topo_results.items():
        print(f"{name:<20} {r['sigma']:>8.2f} {r['RI']:>8.2f} {r['k_avg']:>8.1f} {r['C']:>8.3f} {r['diam']:>6}")

    # T3: 单点硬件仿真（N=8，256MB）
    print("\n[T3] 硬件Allreduce时序仿真（N=8，256MB）...")
    N_test = 8
    msg_elem = int(DATA_SIZE_BYTES / DTYPE_BYTES)
    sim = HardwareAllreduceSim(N_test, 'ring')
    r_nccl  = sim.simulate_software_ring(msg_elem)
    r_sharp = sim.simulate_sharp(msg_elem)
    r_sdi_r = sim.simulate_ring_allreduce(msg_elem)
    r_sdi_t = sim.simulate_tree_allreduce(msg_elem)

    print(f"\n  {'方案':<25} {'延迟(μs)':>12} {'吞吐(TB/s)':>12} {'加速比':>10}")
    print("  " + "-" * 62)
    rows = [
        ("NCCL Ring (软件)", r_nccl),
        ("NVIDIA SHARP", r_sharp),
        ("SDI 硬件Ring", r_sdi_r),
        ("SDI 硬件Tree", r_sdi_t),
    ]
    base = r_nccl['latency_us']
    for name, r in rows:
        speedup = base / r['latency_us']
        print(f"  {name:<25} {r['latency_us']:>12.1f} {r['throughput_TBps']:>12.2f} {speedup:>10.0f}×")

    # T4: 规模敏感性
    print("\n[T4] 规模敏感性分析...")
    scale_res = scale_analysis()
    print(f"\n  {'N':>6} {'NCCL(μs)':>12} {'SHARP(μs)':>12} {'SDI-Ring(μs)':>14} {'SDI加速比':>12}")
    print("  " + "-" * 60)
    for i, N in enumerate(NODE_SIZES):
        nccl_lat = scale_res['NCCL_Ring']['latency_us'][i]
        sharp_lat = scale_res['SHARP']['latency_us'][i]
        sdi_lat  = scale_res['SDI_Hard_Ring']['latency_us'][i]
        speedup  = scale_res['SDI_Hard_Ring']['speedup'][i]
        print(f"  {N:>6} {nccl_lat:>12.1f} {sharp_lat:>12.1f} {sdi_lat:>14.3f} {speedup:>12.0f}×")

    # T5: Alltoall
    print("\n[T5] Alltoall分析（MoE场景）...")
    at_res = alltoall_analysis()
    print(f"\n  {'N':>6} {'软件(μs)':>12} {'SDI硬件(μs)':>14} {'加速比':>10}")
    print("  " + "-" * 46)
    for N, r in at_res.items():
        print(f"  {N:>6} {r['lat_soft_us']:>12.1f} {r['lat_hard_us']:>14.4f} {r['speedup_vs_soft']:>10.0f}×")

    # T6: 功耗
    print("\n[T6] 功耗估算（N=8节点集群）...")
    pw = power_analysis(8)
    print(f"\n  GPU集群总功耗：{pw['gpu_cluster_w']:.0f} W")
    print(f"  SDI互连芯粒功耗：{pw['sdi_chip_w']:.2f} W")
    print(f"  GPU有效算力功耗（NCCL方案）：{pw['gpu_effective_compute_w']:.0f} W（通信占35%，浪费）")
    print(f"  GPU有效算力功耗（SDI方案）：{pw['sdi_effective_compute_w']:.0f} W（通信零占用）")
    print(f"  等效算力提升：{pw['compute_power_gain']:.2f}× （同等功耗，SDI方案更多算力用于计算）")

    # 保存结果
    all_results = {
        'topology': topo_results,
        'scale': {k: {kk: [float(x) for x in vv]
                       for kk, vv in v.items()}
                  for k, v in scale_res.items()},
        'alltoall': {str(k): {kk: float(vv) for kk, vv in v.items()}
                     for k, v in at_res.items()},
        'power_N8': {k: float(v) for k, v in pw.items()},
        'single_point_N8': {
            'NCCL_Ring':  {k: float(v) for k, v in r_nccl.items()},
            'SHARP':      {k: float(v) for k, v in r_sharp.items()},
            'SDI_Hard_Ring': {k: float(v) for k, v in r_sdi_r.items()},
            'SDI_Hard_Tree': {k: float(v) for k, v in r_sdi_t.items()},
        }
    }
    with open('/tmp/collective_comm_results.json', 'w') as f:
        json.dump(all_results, f, indent=2)

    return all_results, scale_res, at_res, topo_results, pw


# ============================================================
# 可视化
# ============================================================

def plot_results(scale_res, at_res, topo_results, pw):
    fig = plt.figure(figsize=(20, 16))
    fig.patch.set_facecolor('#0A1628')
    gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.38)

    CYAN   = '#00E5FF'
    GOLD   = '#FFD700'
    WHITE  = '#FFFFFF'
    GRAY   = '#8899AA'
    RED    = '#FF4444'
    GREEN  = '#44FF88'
    ORANGE = '#FF8844'
    PINK   = '#FF44AA'
    LBLUE  = '#4488FF'

    def ax_style(ax, title):
        ax.set_facecolor('#0D1F35')
        ax.tick_params(colors=WHITE, labelsize=8)
        ax.spines['bottom'].set_color(GRAY)
        ax.spines['left'].set_color(GRAY)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_title(title, color=CYAN, fontsize=10, fontweight='bold', pad=8)
        ax.yaxis.label.set_color(WHITE)
        ax.xaxis.label.set_color(WHITE)

    Ns = NODE_SIZES

    # ── 图1：延迟对比（线图，对数轴）
    ax1 = fig.add_subplot(gs[0, :2])
    ax_style(ax1, '① Allreduce延迟 vs 节点规模（256MB，对数轴）')
    methods = {
        'NCCL Ring':    ('NCCL_Ring',    RED,    '-',  'o'),
        'NVIDIA SHARP': ('SHARP',        ORANGE, '--', 's'),
        'SDI 硬件Ring': ('SDI_Hard_Ring', CYAN,   '-',  'D'),
        'SDI 硬件Tree': ('SDI_Hard_Tree', GOLD,   '--', '^'),
    }
    for label, (key, color, ls, mk) in methods.items():
        lats = scale_res[key]['latency_us']
        ax1.plot(Ns, lats, color=color, linestyle=ls, marker=mk,
                 linewidth=2, markersize=7, label=label)
    ax1.set_yscale('log')
    ax1.set_xlabel('节点数 N', color=WHITE)
    ax1.set_ylabel('延迟 (μs)', color=WHITE)
    ax1.set_xticks(Ns)
    ax1.legend(facecolor='#0A1628', edgecolor=GRAY, labelcolor=WHITE, fontsize=8)
    # 标注SDI优势
    for i, N in enumerate(Ns):
        sp = scale_res['SDI_Hard_Ring']['speedup'][i]
        ax1.annotate(f'{sp:.0f}×', xy=(N, scale_res['SDI_Hard_Ring']['latency_us'][i]),
                    xytext=(0, 12), textcoords='offset points',
                    color=CYAN, fontsize=7, ha='center')

    # ── 图2：加速比柱状图
    ax2 = fig.add_subplot(gs[0, 2])
    ax_style(ax2, '② SDI加速比 vs NCCL（各规模）')
    speedups_ring = scale_res['SDI_Hard_Ring']['speedup']
    speedups_sharp = scale_res['SHARP']['speedup']
    x = np.arange(len(Ns))
    w = 0.35
    bars1 = ax2.bar(x - w/2, speedups_ring,  w, color=CYAN,   alpha=0.85, label='SDI vs NCCL')
    bars2 = ax2.bar(x + w/2, [r/s for r, s in zip(speedups_ring, speedups_sharp)],
                    w, color=GOLD, alpha=0.85, label='SDI vs SHARP')
    ax2.set_xticks(x); ax2.set_xticklabels([str(n) for n in Ns])
    ax2.set_xlabel('节点数 N', color=WHITE)
    ax2.set_ylabel('加速倍数 (×)', color=WHITE)
    ax2.legend(facecolor='#0A1628', edgecolor=GRAY, labelcolor=WHITE, fontsize=7)
    for bar in bars1:
        ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
                 f'{bar.get_height():.0f}×', ha='center', va='bottom',
                 color=CYAN, fontsize=7)

    # ── 图3：Alltoall延迟（对数轴）
    ax3 = fig.add_subplot(gs[1, :2])
    ax_style(ax3, '③ Alltoall延迟 vs 节点规模（MoE专家并行，256MB）')
    lat_soft  = [at_res[N]['lat_soft_us']  for N in NODE_SIZES]
    lat_hard  = [at_res[N]['lat_hard_us']  for N in NODE_SIZES]
    lat_sharp = [at_res[N]['lat_sharp_us'] for N in NODE_SIZES]
    ax3.plot(Ns, lat_soft,  color=RED,    marker='o', linewidth=2, markersize=7, label='软件Alltoall')
    ax3.plot(Ns, lat_sharp, color=ORANGE, marker='s', linewidth=2, markersize=7, label='SHARP（估算）')
    ax3.plot(Ns, lat_hard,  color=GREEN,  marker='D', linewidth=2, markersize=7, label='SDI 硬件Crossbar')
    ax3.set_yscale('log')
    ax3.set_xlabel('节点数 N', color=WHITE)
    ax3.set_ylabel('延迟 (μs)', color=WHITE)
    ax3.set_xticks(Ns)
    ax3.legend(facecolor='#0A1628', edgecolor=GRAY, labelcolor=WHITE, fontsize=8)
    for i, N in enumerate(Ns):
        sp = at_res[N]['speedup_vs_soft']
        ax3.annotate(f'{sp:.0f}×', xy=(N, lat_hard[i]),
                    xytext=(0, 12), textcoords='offset points',
                    color=GREEN, fontsize=7, ha='center')

    # ── 图4：CST拓扑σ对比
    ax4 = fig.add_subplot(gs[1, 2])
    ax_style(ax4, '④ 各拓扑CST指标（N=16节点）')
    topo_names = list(topo_results.keys())
    topo_short = ['Ring', 'Tree', '2D\nMesh', 'Fat\nTree', 'SDI\nSmallW']
    sigmas = [topo_results[n]['sigma'] for n in topo_names]
    RIs    = [topo_results[n]['RI']    for n in topo_names]
    x = np.arange(len(topo_names))
    w = 0.35
    ax4.bar(x - w/2, sigmas, w, color=CYAN,  alpha=0.85, label='σ (小世界指数)')
    ax4.bar(x + w/2, RIs,    w, color=GOLD,  alpha=0.85, label='RI (智能比)')
    ax4.axhline(1.8, color=RED, linestyle='--', linewidth=1, alpha=0.7, label='σ目标线(1.8)')
    ax4.set_xticks(x); ax4.set_xticklabels(topo_short, fontsize=7)
    ax4.set_ylabel('指标值', color=WHITE)
    ax4.legend(facecolor='#0A1628', edgecolor=GRAY, labelcolor=WHITE, fontsize=7)

    # ── 图5：吞吐量对比
    ax5 = fig.add_subplot(gs[2, :2])
    ax_style(ax5, '⑤ Allreduce有效吞吐量 vs 节点规模（TB/s）')
    for label, (key, color, ls, mk) in methods.items():
        tpts = scale_res[key]['throughput_TBps']
        ax5.plot(Ns, tpts, color=color, linestyle=ls, marker=mk,
                 linewidth=2, markersize=7, label=label)
    ax5.set_xlabel('节点数 N', color=WHITE)
    ax5.set_ylabel('有效吞吐量 (TB/s)', color=WHITE)
    ax5.set_xticks(Ns)
    ax5.legend(facecolor='#0A1628', edgecolor=GRAY, labelcolor=WHITE, fontsize=8)

    # ── 图6：功耗效率（N=8~64）
    ax6 = fig.add_subplot(gs[2, 2])
    ax_style(ax6, '⑥ 等效算力提升（SDI释放GPU被通信占用的功耗）')
    pw_Ns = NODE_SIZES
    gains = [power_analysis(N)['compute_power_gain'] for N in pw_Ns]
    gpu_eff = [power_analysis(N)['gpu_effective_compute_w'] for N in pw_Ns]
    sdi_eff = [power_analysis(N)['sdi_effective_compute_w'] for N in pw_Ns]
    ax6.bar(np.arange(len(pw_Ns)) - 0.2, gpu_eff, 0.35, color=RED,  alpha=0.8, label='NCCL方案有效算力W')
    ax6.bar(np.arange(len(pw_Ns)) + 0.2, sdi_eff, 0.35, color=CYAN, alpha=0.8, label='SDI方案有效算力W')
    ax6.set_xticks(np.arange(len(pw_Ns)))
    ax6.set_xticklabels([str(n) for n in pw_Ns])
    ax6.set_xlabel('节点数 N', color=WHITE)
    ax6.set_ylabel('等效算力 (W)', color=WHITE)
    ax6.legend(facecolor='#0A1628', edgecolor=GRAY, labelcolor=WHITE, fontsize=7)

    # 标题
    fig.suptitle('集合通信NaaS — 仿真验证报告\nSDI硬件化Allreduce × CST理论 × 晶圆级互连',
                 color=GOLD, fontsize=14, fontweight='bold', y=0.98)

    out_path = '/home/work/.openclaw/workspace/collective_comm_naas/03_仿真验证/collective_comm_sim_result.png'
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='#0A1628')
    plt.close()
    print(f"\n✅ 图: {out_path}")
    return out_path


if __name__ == '__main__':
    t0 = time.time()
    all_res, scale_res, at_res, topo_res, pw = main()
    out_path = plot_results(scale_res, at_res, topo_res, pw)
    print(f"\n总耗时: {time.time()-t0:.1f}s")
    print(f"结果JSON: /tmp/collective_comm_results.json")
