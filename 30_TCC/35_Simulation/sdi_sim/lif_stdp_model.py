"""
LIF 神经元 + STDP 学习模型
Leaky Integrate-and-Fire + Spike-Timing-Dependent Plasticity
"""

import numpy as np
from scipy import stats
import json

class LIFNeuron:
    """
    Leaky Integrate-and-Fire 神经元模型
    """
    
    def __init__(self, tau_m=20.0, tau_syn=5.0, V_rest=-70.0, 
                 V_reset=-70.0, V_threshold=-50.0, delay=1.0):
        """
        参数初始化
        tau_m: 膜时间常数 (ms)
        tau_syn: 突触时间常数 (ms)
        V_rest: 静息电位 (mV)
        V_reset: 复位电位 (mV)
        V_threshold: 放电阈值 (mV)
        delay: 轴突传导延迟 (ms)
        """
        self.tau_m = tau_m
        self.tau_syn = tau_syn
        self.V_rest = V_rest
        self.V_reset = V_reset
        self.V_threshold = V_threshold
        self.delay = delay
        
        # 状态变量
        self.V = V_rest  # 膜电位
        self.I_syn = 0.0  # 突触电流
        self.last_spike_time = -np.inf
        self.refractory_period = 2.0  # 不应期 (ms)
    
    def integrate_step(self, I_input, dt=0.1):
        """
        单个时间步长的积分
        dt: 时间步长 (ms)
        """
        # 不应期检查
        if self.last_spike_time > -np.inf and \
           (self.last_spike_time + self.refractory_period) > self.V:
            self.V = self.V_reset
            return False
        
        # 突触电流衰减
        self.I_syn *= np.exp(-dt / self.tau_syn)
        self.I_syn += I_input
        
        # 膜电位动力学 (欧拉方法)
        dV_dt = (self.V_rest - self.V + self.I_syn) / self.tau_m
        self.V += dV_dt * dt
        
        # 放电检查
        if self.V >= self.V_threshold:
            self.V = self.V_reset
            self.last_spike_time = self.V
            return True
        
        return False
    
    def receive_spike(self, weight):
        """接收突触输入"""
        self.I_syn += weight

class STDPRule:
    """
    Spike-Timing-Dependent Plasticity 学习规则
    """
    
    def __init__(self, tau_plus=20.0, tau_minus=20.0, 
                 A_plus=0.001, A_minus=-0.001, w_min=0.0, w_max=1.0):
        """
        参数初始化
        tau_plus: 正 STDP 时间窗 (ms)
        tau_minus: 负 STDP 时间窗 (ms)
        A_plus: 正强化幅度
        A_minus: 负强化幅度
        w_min, w_max: 权重范围
        """
        self.tau_plus = tau_plus
        self.tau_minus = tau_minus
        self.A_plus = A_plus
        self.A_minus = A_minus
        self.w_min = w_min
        self.w_max = w_max
    
    def update_weight(self, w, t_pre, t_post):
        """
        更新突触权重
        w: 当前权重
        t_pre: 前脉冲时间
        t_post: 后脉冲时间
        """
        dt = t_post - t_pre  # 时间差
        
        if dt > 0:  # 后脉冲在前脉冲之后（长期增强）
            dw = self.A_plus * np.exp(-dt / self.tau_plus)
        else:  # 后脉冲在前脉冲之前（长期抑制）
            dw = self.A_minus * np.exp(dt / self.tau_minus)
        
        w_new = w + dw
        return np.clip(w_new, self.w_min, self.w_max)

class DynamicsSimulator:
    """
    完整的网络动力学仿真器
    """
    
    def __init__(self, network_graph, synapse_weights, neuron_params):
        """
        初始化仿真器
        network_graph: NetworkX 有向图
        synapse_weights: 突触权重字典
        neuron_params: LIF 参数字典
        """
        self.G = network_graph
        self.weights = synapse_weights
        self.params = neuron_params
        
        # 初始化神经元
        self.neurons = {}
        for node in self.G.nodes():
            self.neurons[node] = LIFNeuron(
                tau_m=neuron_params['LIF_neuron']['tau_m'],
                tau_syn=neuron_params['LIF_neuron']['tau_syn'],
                V_threshold=neuron_params['LIF_neuron']['V_threshold'],
                V_reset=neuron_params['LIF_neuron']['V_reset']
            )
        
        # STDP 规则
        self.stdp = STDPRule(
            tau_plus=neuron_params['STDP']['tau_plus'],
            tau_minus=neuron_params['STDP']['tau_minus'],
            A_plus=neuron_params['STDP']['A_plus'],
            A_minus=neuron_params['STDP']['A_minus']
        )
        
        # 记录数据
        self.spike_times = {node: [] for node in self.G.nodes()}
        self.avalanche_sizes = []
        
    def simulate(self, duration=1000.0, dt=0.1, I_ext=10.0, display_interval=100):
        """
        运行仿真
        duration: 仿真总时长 (ms)
        dt: 时间步长 (ms)
        I_ext: 外部输入电流 (nA)
        display_interval: 显示进度的间隔 (ms)
        """
        print(f"\n【开始神经动力学仿真】")
        print(f"  配置：{len(self.G.nodes())} 个神经元，{len(self.G.edges())} 条突触")
        print(f"  时长：{duration} ms，时间步：{dt} ms")
        print(f"  总步数：{int(duration/dt)}\n")
        
        n_steps = int(duration / dt)
        current_time = 0.0
        avalanche_current = 0
        
        for step in range(n_steps):
            current_time = step * dt
            spikes_this_step = []
            
            # 步骤 1：计算突触输入
            for node in self.G.nodes():
                # 外部输入
                I_input = I_ext * 0.1 * np.random.randn()  # 高斯噪声
                
                # 来自前体神经元的输入
                for pred in self.G.predecessors(node):
                    if pred in self.spike_times and self.spike_times[pred]:
                        last_spike = self.spike_times[pred][-1]
                        delay = self.params['Synapse']['delay']
                        
                        if abs(current_time - last_spike - delay) < dt:
                            # 获取突触权重
                            edge_data = self.G[pred][node]
                            w = edge_data.get('weight', 0.5)
                            I_input += w
                
                # 步骤 2：神经元积分
                fired = self.neurons[node].integrate_step(I_input, dt)
                if fired:
                    spikes_this_step.append(node)
                    self.spike_times[node].append(current_time)
            
            # 步骤 3：STDP 学习（可选，简化版）
            for pre in spikes_this_step:
                for post in self.G.successors(pre):
                    if post in spikes_this_step:
                        edge_data = self.G[pre][post]
                        w_old = edge_data.get('weight', 0.5)
                        w_new = self.stdp.update_weight(w_old, current_time, current_time + 1)
                        self.G[pre][post]['weight'] = w_new
            
            # 步骤 4：放电雪崩统计
            if len(spikes_this_step) > 0:
                avalanche_current += len(spikes_this_step)
            else:
                if avalanche_current > 0:
                    self.avalanche_sizes.append(avalanche_current)
                avalanche_current = 0
            
            # 显示进度
            if (step + 1) % int(display_interval / dt) == 0:
                print(f"  进度：{current_time:.1f}/{duration} ms（{100*(step+1)/n_steps:.1f}%）")
        
        print(f"✅ 仿真完成")
        return self.spike_times, self.avalanche_sizes

class AvalancheAnalyzer:
    """
    放电雪崩分析
    """
    
    def __init__(self, avalanche_sizes):
        self.sizes = np.array(avalanche_sizes)
    
    def compute_power_spectrum(self):
        """计算雪崩大小分布的幂律指数"""
        if len(self.sizes) < 10:
            return None
        
        # 排序
        sizes_sorted = np.sort(self.sizes)[::-1]
        
        # 计算幂律指数 α（通过日志回归）
        log_sizes = np.log(sizes_sorted + 1)
        log_ranks = np.log(np.arange(1, len(sizes_sorted) + 1))
        
        # 线性回归
        coeffs = np.polyfit(log_ranks, log_sizes, 1)
        alpha = -coeffs[0]
        
        return alpha
    
    def get_statistics(self):
        """获取统计信息"""
        return {
            'n_avalanches': len(self.sizes),
            'mean_size': float(np.mean(self.sizes)) if len(self.sizes) > 0 else 0,
            'std_size': float(np.std(self.sizes)) if len(self.sizes) > 0 else 0,
            'max_size': int(np.max(self.sizes)) if len(self.sizes) > 0 else 0,
            'alpha': self.compute_power_spectrum(),
        }

