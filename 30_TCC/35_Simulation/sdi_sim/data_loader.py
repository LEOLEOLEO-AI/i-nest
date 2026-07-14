"""
Hemibrain 连接组数据加载器
支持：神经元类型、突触强度、神经递质分类、生物物理参数
"""

import json
import pandas as pd
import yaml
import numpy as np
from pathlib import Path

class ConnectomeDataLoader:
    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)
        self.neurons = None
        self.synapses = None
        self.neuron_types = None
        self.neurotransmitter_map = None
        self.params = None
        self.n_neurons = 0
        self.n_synapses = 0
    
    def load_neuron_types(self):
        """加载神经元类型标注"""
        file_path = self.data_dir / 'neuron_types.csv'
        self.neuron_types = pd.read_csv(file_path)
        self.n_neurons = len(self.neuron_types)
        print(f"✓ 加载神经元类型：{self.n_neurons} 个")
        return self.neuron_types
    
    def load_synapse_weights(self):
        """加载突触强度参数"""
        file_path = self.data_dir / 'synapse_weights.json'
        with open(file_path, 'r') as f:
            data = json.load(f)
        self.synapses = data['synapses']
        self.n_synapses = len(self.synapses)
        print(f"✓ 加载突触权重：{self.n_synapses} 个")
        return self.synapses
    
    def load_neurotransmitter_map(self):
        """加载神经递质分类"""
        file_path = self.data_dir / 'neurotransmitter_map.csv'
        self.neurotransmitter_map = pd.read_csv(file_path)
        print(f"✓ 加载神经递质映射：{len(self.neurotransmitter_map)} 个")
        return self.neurotransmitter_map
    
    def load_neural_params(self):
        """加载生物物理参数"""
        file_path = self.data_dir / 'neuron_params.yaml'
        with open(file_path, 'r') as f:
            self.params = yaml.safe_load(f)
        print(f"✓ 加载生物物理参数")
        return self.params
    
    def load_all(self):
        """加载所有数据"""
        print("【加载所有数据】")
        self.load_neuron_types()
        self.load_synapse_weights()
        self.load_neurotransmitter_map()
        self.load_neural_params()
        print(f"✅ 所有数据加载完成\n")
        return {
            'neurons': self.neuron_types,
            'synapses': self.synapses,
            'neurotransmitters': self.neurotransmitter_map,
            'params': self.params
        }
    
    def validate_data_integrity(self):
        """验证数据完整性"""
        print("【数据完整性验证】")
        
        errors = []
        
        # 检查 1：神经元数量一致
        if len(self.neuron_types) != len(self.neurotransmitter_map):
            errors.append("神经元数量不一致")
        else:
            print(f"✓ 神经元数量一致：{len(self.neuron_types)}")
        
        # 检查 2：突触神经元 ID 有效性
        neuron_ids = set(self.neuron_types['neuron_id'].unique())
        synapse_neurons = set()
        for s in self.synapses:
            synapse_neurons.add(s['pre_neuron'])
            synapse_neurons.add(s['post_neuron'])
        
        invalid_ids = synapse_neurons - neuron_ids
        if len(invalid_ids) == 0:
            print(f"✓ 所有突触神经元 ID 有效")
        else:
            errors.append(f"无效的神经元 ID：{len(invalid_ids)} 个")
        
        # 检查 3：权重范围
        weights = [s['weight'] for s in self.synapses]
        if min(weights) >= 0 and max(weights) <= 1:
            print(f"✓ 权重范围有效：[{min(weights):.3f}, {max(weights):.3f}]")
        else:
            errors.append(f"权重范围无效")
        
        # 检查 4：参数完整性
        required_sections = ['LIF_neuron', 'Synapse', 'STDP']
        if all(s in self.params for s in required_sections):
            print(f"✓ 参数配置完整")
        else:
            errors.append("参数配置不完整")
        
        if errors:
            print(f"\n❌ 验证失败：{errors}\n")
            return False
        else:
            print(f"\n✅ 所有验证通过\n")
            return True
    
    def generate_summary_report(self):
        """生成摘要报告"""
        print("【数据摘要报告】")
        
        report = {
            'neurons': {
                'total': self.n_neurons,
                'by_type': self.neuron_types['neuron_type'].value_counts().to_dict(),
                'by_class': self.neuron_types['neuron_class'].value_counts().to_dict(),
            },
            'synapses': {
                'total': self.n_synapses,
                'weight_range': [float(min([s['weight'] for s in self.synapses])),
                                float(max([s['weight'] for s in self.synapses]))],
                'synapse_count_range': [min([s['synapse_count'] for s in self.synapses]),
                                       max([s['synapse_count'] for s in self.synapses])],
            },
            'neurotransmitters': self.neurotransmitter_map['neurotransmitter'].value_counts().to_dict(),
        }
        
        return report
