"""
SDI (Software-Defined Interconnect) 硬件仿真模型
模拟 SDI 架构相比传统芯片的优势
"""

import numpy as np
import json
from dataclasses import dataclass

@dataclass
class HardwareMetrics:
    """硬件性能指标"""
    area_mm2: float  # 面积 mm²
    power_mw: float  # 功耗 mW
    latency_ns: float  # 延迟 ns
    throughput_gops: float  # 吞吐量 GOPS
    bandwidth_gbps: float  # 带宽 Gbps
    leakage_power_mw: float  # 漏电功耗 mW

class TraditionalChip:
    """传统芯片架构（对标）"""
    
    def __init__(self, n_neurons=31431, n_synapses=100000):
        self.n_neurons = n_neurons
        self.n_synapses = n_synapses
    
    def estimate_metrics(self):
        """估计传统芯片的性能"""
        
        # 传统架构：基于寄存器堆 + 乘法器阵列
        # 参考：SpiNNaker, Loihi, IBM TrueNorth 等
        
        # 面积估算（28nm 工艺）
        neuron_area = 0.1  # mm² 每个神经元
        synapse_area = 0.05  # mm² 每个突触
        total_neuron_area = self.n_neurons * neuron_area
        total_synapse_area = self.n_synapses * synapse_area
        routing_area = (total_neuron_area + total_synapse_area) * 0.3
        area = total_neuron_area + total_synapse_area + routing_area
        
        # 功耗估算
        active_power = (total_neuron_area * 50) + (total_synapse_area * 20)
        leakage = active_power * 0.3
        total_power = active_power + leakage
        
        # 延迟
        latency = 50  # ns
        
        # 吞吐量
        freq_ghz = 1.0
        parallelism = 64
        throughput = freq_ghz * 1000 * parallelism
        
        # 带宽
        spike_rate = 20
        total_spikes_per_s = self.n_neurons * spike_rate
        data_width = 32
        bandwidth = (total_spikes_per_s * data_width) / 1e9
        
        return HardwareMetrics(
            area_mm2=area,
            power_mw=total_power,
            latency_ns=latency,
            throughput_gops=throughput,
            bandwidth_gbps=bandwidth,
            leakage_power_mw=leakage
        )

class SDIChip:
    """SDI 芯片架构"""
    
    def __init__(self, n_neurons=31431, n_synapses=100000):
        self.n_neurons = n_neurons
        self.n_synapses = n_synapses
    
    def estimate_metrics(self):
        """估计 SDI 芯片的性能"""
        
        traditional = TraditionalChip(self.n_neurons, self.n_synapses)
        trad_metrics = traditional.estimate_metrics()
        
        # SDI 优化因子
        logic_reduction = 0.6
        routing_reduction = 0.8
        
        sdi_area = trad_metrics.area_mm2 * (logic_reduction + routing_reduction) / 2
        
        # 功耗优势
        duty_cycle = 0.05
        power_reduction = 0.7
        sdi_power = trad_metrics.power_mw * power_reduction * duty_cycle
        sdi_leakage = sdi_power * 0.1
        sdi_total_power = sdi_power + sdi_leakage
        
        # 延迟和吞吐量
        sdi_latency = trad_metrics.latency_ns * 0.5
        sdi_throughput = trad_metrics.throughput_gops * 2.0
        sdi_bandwidth = trad_metrics.bandwidth_gbps * 1.5
        
        return HardwareMetrics(
            area_mm2=sdi_area,
            power_mw=sdi_total_power,
            latency_ns=sdi_latency,
            throughput_gops=sdi_throughput,
            bandwidth_gbps=sdi_bandwidth,
            leakage_power_mw=sdi_leakage
        )

class HardwareComparison:
    """硬件对标分析"""
    
    def __init__(self, n_neurons=31431, n_synapses=100000):
        self.traditional = TraditionalChip(n_neurons, n_synapses)
        self.sdi = SDIChip(n_neurons, n_synapses)
    
    def compare(self):
        """生成对标报告"""
        
        trad_metrics = self.traditional.estimate_metrics()
        sdi_metrics = self.sdi.estimate_metrics()
        
        # 计算优势比
        area_improvement = (trad_metrics.area_mm2 - sdi_metrics.area_mm2) / trad_metrics.area_mm2 * 100
        power_improvement = (trad_metrics.power_mw - sdi_metrics.power_mw) / trad_metrics.power_mw * 100
        latency_improvement = (trad_metrics.latency_ns - sdi_metrics.latency_ns) / trad_metrics.latency_ns * 100
        throughput_improvement = (sdi_metrics.throughput_gops - trad_metrics.throughput_gops) / trad_metrics.throughput_gops * 100
        
        report = {
            'traditional_chip': {
                'area_mm2': float(trad_metrics.area_mm2),
                'power_mw': float(trad_metrics.power_mw),
                'latency_ns': float(trad_metrics.latency_ns),
                'throughput_gops': float(trad_metrics.throughput_gops),
                'bandwidth_gbps': float(trad_metrics.bandwidth_gbps),
                'leakage_power_mw': float(trad_metrics.leakage_power_mw),
            },
            'sdi_chip': {
                'area_mm2': float(sdi_metrics.area_mm2),
                'power_mw': float(sdi_metrics.power_mw),
                'latency_ns': float(sdi_metrics.latency_ns),
                'throughput_gops': float(sdi_metrics.throughput_gops),
                'bandwidth_gbps': float(sdi_metrics.bandwidth_gbps),
                'leakage_power_mw': float(sdi_metrics.leakage_power_mw),
            },
            'improvements': {
                'area_reduction_percent': float(area_improvement),
                'power_reduction_percent': float(power_improvement),
                'latency_reduction_percent': float(latency_improvement),
                'throughput_increase_percent': float(throughput_improvement),
            }
        }
        
        return report
    
    def print_report(self):
        """打印对标报告"""
        report = self.compare()
        
        print("\n【硬件对标分析报告】")
        print("="*60)
        
        print("\n传统芯片架构：")
        for key, val in report['traditional_chip'].items():
            print(f"  {key}: {val:.2f}")
        
        print("\nSDI 芯片架构：")
        for key, val in report['sdi_chip'].items():
            print(f"  {key}: {val:.2f}")
        
        print("\n性能改善：")
        for key, val in report['improvements'].items():
            print(f"  {key}: {val:.1f}%")
        
        return report

if __name__ == '__main__':
    comparison = HardwareComparison(n_neurons=31431, n_synapses=100000)
    report = comparison.print_report()
    
    # 保存报告
    import os
    os.makedirs('results', exist_ok=True)
    with open('results/hardware_comparison.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\n✅ 报告已保存：results/hardware_comparison.json")
