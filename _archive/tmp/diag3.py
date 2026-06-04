import json

fpath = r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html"
with open(fpath, "r", encoding="utf-8") as f:
    html = f.read()

# Entries array at 15469, closes at 23942
# Find the last } before the closing ]
close_bracket = 23942
# Find the last } before this position
last_brace = html.rfind('}', 15000, close_bracket)
print(f"Last entry ends at: {last_brace}")
print(f"Context: ...{html[last_brace-80:close_bracket+5]}...")

# New entries to insert
new_entries = [
    {"id":48,"dim":"TCC","cat":"论文","title":"From Compute to Complexity: A Physical Theory of Intelligence Emergence","ver":"V26","status":"撰写中","date":"2026-06-04","desc":"CST理论核心论文：智能涌现的物理理论及其对AGI的启示","priority":"高","link":"papers/TCC/From Compute to Complexity- A Physical Theory of Intelligence Emergence and Its Implications for AGI.md"},
    {"id":49,"dim":"TCC","cat":"论文","title":"5类通信-4类计算拓扑完备映射与PTM算法","ver":"v2","status":"撰写中","date":"2026-06-03","desc":"B2核心论文：5通信+4计算原语拓扑完备映射，含FFT-AllReduce图同构定理","priority":"高","link":"papers/TCC/5类通信-4类计算拓扑完备映射与PTM算法.md"},
    {"id":50,"dim":"iNEST","cat":"论文","title":"FEP-STDP Deep Fusion: Physics-Grounded Self-Evolving Neural Architecture","ver":"draft-v1","status":"撰写中","date":"2026-06-03","desc":"FEP-STDP深度融合：面向绿色安全可扩展智能的物理自演化神经架构","priority":"高","link":"papers/iNEST/FEP-STDP Deep Fusion- Physics-Grounded Self-Evolving Neural Architecture.md"},
    {"id":51,"dim":"TCC","cat":"专利","title":"面向网络中心计算的软件定义互连系统架构及调度方法","ver":"申请稿-v1","status":"撰写中","date":"2026-06-04","desc":"P0优先级：覆盖TCC+SDI系统架构，海河实验室重大专项","priority":"高","link":"TCC_3_专利撰写/面向网络中心计算的软件定义互连系统架构及调度方法.md"},
    {"id":52,"dim":"TCC","cat":"专利","title":"面向晶圆级大模型推理的高维最优扇出互连拓扑结构","ver":"构思-v1","status":"规划中","date":"2026-06-04","desc":"P0优先级：针对晶圆级高维互连拓扑的关键卡位专利","priority":"高","link":"TCC_3_专利撰写/面向晶圆级大模型推理的高维最优扇出互连拓扑结构.md"},
    {"id":53,"dim":"TCC","cat":"专利","title":"面向万亿参数大模型的网内原语AI梯度归约通信加速系统","ver":"构思-v1","status":"规划中","date":"2026-06-04","desc":"P0优先级：针对AllReduce等集合通信的直接工程专利","priority":"高","link":"TCC_3_专利撰写/面向万亿参数大模型的网内原语AI梯度归约通信加速系统.md"},
]

# Insert new entries after the last existing entry (before ])
insert_pos = last_brace + 1
insert_json = ""
for ne in new_entries:
    insert_json += ",\n    " + json.dumps(ne, ensure_ascii=False)

html = html[:insert_pos] + insert_json + html[insert_pos:]
print(f"Inserted at position {insert_pos}")

with open(fpath, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Final size: {len(html)}")
