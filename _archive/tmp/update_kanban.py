import json, re

fpath = r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html"
with open(fpath, "r", encoding="utf-8") as f:
    html = f.read()

# Add new paper and patent entries to DEFAULT_DATA
# Find the closing of entries array
new_entries = [
    {"id":48,"dim":"TCC","cat":"论文","title":"From Compute to Complexity: A Physical Theory of Intelligence Emergence","ver":"V26","status":"撰写中","date":"2026-06-04","desc":"CST理论核心论文：智能涌现的物理理论及其对AGI的启示","priority":"高","link":"papers/TCC/From Compute to Complexity- A Physical Theory of Intelligence Emergence and Its Implications for AGI.md"},
    {"id":49,"dim":"TCC","cat":"论文","title":"5类通信-4类计算拓扑完备映射与PTM算法","ver":"v2","status":"撰写中","date":"2026-06-03","desc":"B2核心论文：5通信+4计算原语拓扑完备映射，含FFT-AllReduce图同构定理","priority":"高","link":"papers/TCC/5类通信-4类计算拓扑完备映射与PTM算法.md"},
    {"id":50,"dim":"iNEST","cat":"论文","title":"FEP-STDP Deep Fusion: Physics-Grounded Self-Evolving Neural Architecture","ver":"draft-v1","status":"撰写中","date":"2026-06-03","desc":"FEP-STDP深度融合：面向绿色安全可扩展智能的物理自演化神经架构，含6机制+5尺度验证+FPGA映射","priority":"高","link":"papers/iNEST/FEP-STDP Deep Fusion- Physics-Grounded Self-Evolving Neural Architecture.md"},
    {"id":51,"dim":"TCC","cat":"专利","title":"面向网络中心计算的软件定义互连系统架构及调度方法","ver":"申请稿-v1","status":"撰写中","date":"2026-06-04","desc":"P0优先级：覆盖TCC+SDI系统架构、原语核和重构控制，海河实验室重大专项","priority":"高","link":"TCC_3_专利撰写/面向网络中心计算的软件定义互连系统架构及调度方法.md"},
    {"id":52,"dim":"TCC","cat":"专利","title":"面向晶圆级大模型推理的高维最优扇出互连拓扑结构","ver":"构思-v1","status":"规划中","date":"2026-06-04","desc":"P0优先级：针对晶圆级高维互连拓扑的关键卡位专利","priority":"高","link":"TCC_3_专利撰写/面向晶圆级大模型推理的高维最优扇出互连拓扑结构.md"},
    {"id":53,"dim":"TCC","cat":"专利","title":"面向万亿参数大模型的网内原语AI梯度归约通信加速系统","ver":"构思-v1","status":"规划中","date":"2026-06-04","desc":"P0优先级：针对AllReduce等集合通信的直接工程专利","priority":"高","link":"TCC_3_专利撰写/面向万亿参数大模型的网内原语AI梯度归约通信加速系统.md"},
]

# Find the last entry in the entries array
# Pattern: last entry ends with }] at the end of the entries array
# Find the closing of DEFAULT_DATA entries
entries_end = html.rfind('}]\n  }\n]')
if entries_end < 0:
    entries_end = html.rfind('"priority":"高"}\n  ]')
if entries_end < 0:
    # Try finding the last entry
    entries_end = html.rfind('"priority":"中"}\n  ]')

print(f"Entries end found at: {entries_end}")

if entries_end > 0:
    # Find the last } before entries closing
    last_entry_end = html.rfind('}', entries_end - 20, entries_end)
    if last_entry_end > 0:
        new_json = ""
        for ne in new_entries:
            new_json += ",\n    " + json.dumps(ne, ensure_ascii=False)
        
        html = html[:last_entry_end + 1] + new_json + html[last_entry_end + 1:]
        print(f"Added {len(new_entries)} new entries")
    else:
        print("Could not find last entry end")
else:
    print("Could not find entries end marker")

with open(fpath, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Final size: {len(html)}")
