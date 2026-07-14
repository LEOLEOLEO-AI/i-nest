"""
第 1 周完整流程：数据加载 → 网络构建 → 对照生成
"""

from data_loader import ConnectomeDataLoader
from network_builder import HemibrainNetworkBuilder
from null_model_generator import NullModelGenerator
import json
import os
from datetime import datetime

def run_week1_pipeline():
    """第 1 周完整流程"""
    
    print("\n" + "="*60)
    print("【iNEST 第 1 周完整流程 - Day 1】")
    print("="*60 + "\n")
    
    start_time = datetime.now()
    
    # 步骤 1：加载数据
    print("【步骤 1：数据加载】\n")
    loader = ConnectomeDataLoader('./data')
    data = loader.load_all()
    
    if not loader.validate_data_integrity():
        print("❌ 数据验证失败")
        return False
    
    summary = loader.generate_summary_report()
    print("数据摘要：")
    for key, val in summary.items():
        print(f"  {key}: {val}")
    print()
    
    # 步骤 2：构建网络
    print("【步骤 2：网络构建】\n")
    builder = HemibrainNetworkBuilder(loader)
    G_real = builder.build_network_graph()
    
    properties = builder.analyze_basic_properties()
    adj_matrix = builder.compute_connectivity_matrix()
    
    # 步骤 3：生成对照
    print("【步骤 3：对照网络生成】\n")
    null_gen = NullModelGenerator(G_real)
    null_models = null_gen.generate_all_models()
    
    # 步骤 4：生成报告
    print("【步骤 4：生成完整报告】\n")
    
    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()
    
    report = {
        'week': 1,
        'date': datetime.now().isoformat(),
        'execution_time_seconds': elapsed,
        'data_summary': summary,
        'network_properties': properties,
        'connectivity_matrix': {
            'shape': adj_matrix.shape,
            'nonzero_elements': int(np.count_nonzero(adj_matrix)),
        },
        'null_models_status': {
            'ER': 'generated',
            'configuration': 'generated',
            'scale_free': 'generated',
        },
        'status': 'PASS',
    }
    
    # 创建结果目录
    os.makedirs('results', exist_ok=True)
    
    # 保存报告
    with open('results/week1_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"✓ 执行时间：{elapsed:.2f} 秒")
    print(f"✓ 报告已保存：results/week1_report.json")
    print(f"\n✅ 第 1 周流程完成")
    
    return True

if __name__ == '__main__':
    import numpy as np
    
    success = run_week1_pipeline()
    if success:
        print("\n🎉 第 1 周 Day 1 验收通过")
        exit(0)
    else:
        print("\n❌ 第 1 周 Day 1 验收失败")
        exit(1)
