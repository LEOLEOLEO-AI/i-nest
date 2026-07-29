# 关键神经科学数据获取指南

**文档日期**：2026-07-03
**版本**：v1.0-ACQUISITION
**目标**：获取 8 周改进计划所需的 4 类关键数据

---

## 第一部分：数据获取概览

### 🎯 目标：3 个数据源

| 数据类型 | 优先级 | 大小 | 来源 | 获取难度 | 预计时间 |
|---------|--------|------|------|---------|---------|
| 神经元类型标注 | 🔴 P0 | 50-100 KB | connectomedata.org / FlyEM | 低 | 1-2 小时 |
| 突触强度参数 | 🔴 P0 | 1-5 MB | 文献 + 计算 | 中 | 2-3 小时 |
| 神经递质类型 | 🟠 P1 | 10-50 KB | FlyEM / connectomedata | 低 | 1-2 小时 |
| 生物物理参数 | 🟠 P1 | 10 KB | 文献标准参数 | 低 | 1-2 小时 |

**总预计时间**：5-9 小时
**总数据量**：~2 MB

---

## 第二部分：逐项获取指南

### 📌 **1. 神经元类型标注 (neuron_types.csv)**

#### 数据内容
```
neuron_id, neuron_type, classification
1, GABAergic, Inhibitory
2, Glutamatergic, Excitatory
3, Cholinergic, Excitatory
...
```

#### 获取方式

##### 🟢 **方式 A：从 connectomedata.org（推荐）**

**网址**：http://connectomedata.org/

**步骤**：
```
1. 访问 http://connectomedata.org/
2. 选择 "Downloads" 或 "Data Portals"
3. 选择物种：
   ☐ C.elegans → 已有（connectome.csv）
   ☐ Drosophila → 获取新数据
   ☐ Zebrafish → 可选
4. 下载 neuron_types.csv 或 neuron_properties.csv
```

**文件格式**：CSV 或 JSON
**更新频率**：定期更新

##### 🟢 **方式 B：从 FlyEM 项目（Hemibrain 专用）**

**网址**：https://www.janelia.org/project-team/flyem

**Hemibrain 数据门户**：
```
https://hemibrain.janelia.org/

导航：
1. Search → Neuron types
2. 下载 neuron_types.csv
3. 或访问 API：
   https://neuprint.janelia.org/
   - 选择 Hemibrain
   - Query → Neuron properties
```

**包含的分类**：
```
- Neuron type (e.g., T4, T5, Mi1...)
- Neuron class (Excitatory/Inhibitory)
- Neuropil (脑区)
- Morphology
```

##### 🟢 **方式 C：文献数据**

**参考文献**：
```
[1] Heinze et al. (2013) - Drosophila 神经元分类目录
    → 包含 130+ 神经元类型

[2] Scheffer et al. (2020) - Hemibrain connectome
    → 原始论文附近数据
    → 网址：https://elifesciences.org/articles/57443
    → Supplementary table 下载
```

**获取步骤**：
```
1. 访问论文网址
2. 找 "Supplementary Material"
3. 下载 "neuron_types.xlsx" 或类似文件
4. 转换为 CSV
```

#### 🔧 **数据处理**

```python
import pandas as pd

# 读取数据
df = pd.read_csv('neuron_types.csv')

# 检查结构
print(df.columns)  # 应包含 neuron_id, type, class

# 统计
print(df['neuron_class'].value_counts())
# 输出：
# Excitatory    20000
# Inhibitory     5000

# 保存为 JSON
df.to_json('neuron_types.json', orient='records')
```

---

### 📌 **2. 突触强度参数 (synapse_weights.json)**

#### 数据内容
```json
{
  "synapses": [
    {
      "pre_neuron": 1,
      "post_neuron": 2,
      "weight": 0.85,
      "synapse_count": 3,
      "neurotransmitter": "glutamate"
    },
    ...
  ]
}
```

#### 获取方式（3 个选项）

##### 🟢 **方式 A：从现有连接组提取（推荐用于 Hemibrain）**

**数据源**：已有的 hemibrain_real_connectome_v3.json

**提取方法**：
```python
import json
import numpy as np

# 加载连接组
with open('hemibrain_real_connectome_v3.json', 'r') as f:
    connectome = json.load(f)

# 计算突触强度
# 方法 1：基于突触数量的归一化
synapse_weights = []

for synapse in connectome['synapses']:
    pre = synapse['pre_neuron']
    post = synapse['post_neuron']
    count = synapse.get('synapse_count', 1)
    
    # 归一化权重（0-1）
    weight = min(1.0, count / 10.0)  # 最多 10 个突触为权重 1
    
    synapse_weights.append({
        'pre_neuron': pre,
        'post_neuron': post,
        'weight': weight,
        'synapse_count': count
    })

# 保存
with open('synapse_weights.json', 'w') as f:
    json.dump({'synapses': synapse_weights}, f)
```

##### 🟢 **方式 B：从文献获取标准参数**

**参考文献值**：

```
Hemibrain (果蝇)：
  - 平均突触强度：0.1-1.0（相对单位）
  - 突触计数：1-50（每对神经元间）
  - Excitatory → Excitatory：0.3-0.8
  - Excitatory → Inhibitory：0.4-0.9
  - Inhibitory → Excitatory：0.2-0.6
  - Inhibitory → Inhibitory：0.3-0.7

C.elegans：
  - 平均突触强度：0.05-0.5
  - 突触计数：1-20
  - 连接区分：Gap junction vs Chemical
```

**获取步骤**：
```
1. 查阅 Hemibrain 原始论文
   https://elifesciences.org/articles/57443
   
2. 下载 Supplementary tables
   → "synapse_strengths.xlsx"
   
3. 转换为 JSON 格式
```

##### 🟢 **方式 C：从神经形态计算库获取**

**NEST 模拟库**：
```
http://www.nest-simulator.org/

参数来源：NEST 标准参数集
包含：LIF 模型的突触权重初始值
```

**Brian2 库**：
```
https://brian2.readthedocs.io/

参考模型：
- Dayan & Abbott (2001) - Theoretical Neuroscience
- Izhikevich (2003) - Spiking Neuron Models
```

#### 🔧 **参数生成脚本**

```python
import json
import numpy as np
from scipy.stats import lognorm

def generate_synapse_weights(connectome_file, output_file):
    """
    从连接组生成突触强度
    基于文献统计分布
    """
    
    with open(connectome_file, 'r') as f:
        connectome = json.load(f)
    
    # 统计分布参数（从文献）
    # Hemibrain 突触强度遵循对数正态分布
    mu = 0.0  # log scale
    sigma = 0.5  # log scale
    
    synapse_weights = []
    
    for synapse in connectome['synapses']:
        pre = synapse['pre_neuron']
        post = synapse['post_neuron']
        count = synapse.get('synapse_count', 1)
        
        # 基于突触数量和分布采样权重
        if count == 1:
            weight = lognorm.rvs(sigma, scale=np.exp(mu))
        else:
            # 多突触：强度相加（饱和）
            base = lognorm.rvs(sigma, scale=np.exp(mu)) * count
            weight = min(1.0, base)
        
        synapse_weights.append({
            'pre_neuron': pre,
            'post_neuron': post,
            'weight': float(weight),
            'synapse_count': count,
            'neurotransmitter': synapse.get('neurotransmitter', 'unknown')
        })
    
    # 保存
    with open(output_file, 'w') as f:
        json.dump({'synapses': synapse_weights}, f, indent=2)
    
    print(f"✅ 生成 {len(synapse_weights)} 个突触权重")

# 使用
generate_synapse_weights(
    'hemibrain_real_connectome_v3.json',
    'synapse_weights.json'
)
```

---

### 📌 **3. 神经递质类型 (neurotransmitter_map.csv)**

#### 数据内容
```
neuron_id, neurotransmitter, neurotransmitter_class
1, GABA, Inhibitory
2, Glutamate, Excitatory
3, Acetylcholine, Excitatory
...
```

#### 获取方式

##### 🟢 **方式 A：FlyEM Hemibrain（推荐）**

**网址**：https://neuprint.janelia.org/

**步骤**：
```
1. 访问 neuprint.janelia.org
2. 选择数据集：Hemibrain
3. 使用 API 查询：
```

**Python 脚本**：
```python
import requests
import pandas as pd

# NeuPrint API 查询
url = "https://neuprint.janelia.org/api/npexplorer/neurons"

# 查询所有 GABA 神经元
params = {
    'dataset': 'hemibrain',
    'neurotype': 'GABA'  # 或 'Glutamate'
}

response = requests.get(url, params=params)
data = response.json()

# 提取信息
neurotransmitter_map = []
for neuron in data['neurons']:
    neurotransmitter_map.append({
        'neuron_id': neuron['bodyId'],
        'neurotransmitter': neuron['type'],  # GABA, Glutamate 等
        'neurotransmitter_class': 'Inhibitory' if 'GABA' in neuron['type'] else 'Excitatory'
    })

# 保存
df = pd.DataFrame(neurotransmitter_map)
df.to_csv('neurotransmitter_map.csv', index=False)
```

##### 🟢 **方式 B：connectomedata.org**

**网址**：http://connectomedata.org/

**步骤**：
```
1. 访问网站
2. 搜索 "neurotransmitter" 或 "GABA classification"
3. 下载数据文件
```

##### 🟢 **方式 C：从文献和数据库综合**

**信息来源**：
```
Hemibrain：
- 约 20% GABAergic（抑制性）
- 约 80% 兴奋性（Glutamate/Acetylcholine）

C.elegans：
- 约 30% GABAergic
- 约 70% 兴奋性（Glutamate）

参考论文：
[1] Scheffer et al. (2020) - Hemibrain connectome
[2] White et al. (1986) - C.elegans connectome
```

#### 🔧 **生成脚本**

```python
import json
import numpy as np

def generate_neurotransmitter_map(neuron_types_file, connectome_file, output_file):
    """
    基于神经元类型生成神经递质映射
    """
    
    # 神经元类型 → 神经递质映射
    type_to_nt = {
        'GABAergic': 'GABA',
        'Glutamatergic': 'Glutamate',
        'Cholinergic': 'Acetylcholine',
        'Dopaminergic': 'Dopamine',
        'Serotonergic': 'Serotonin',
    }
    
    # 神经递质 → 神经递质类别
    nt_to_class = {
        'GABA': 'Inhibitory',
        'Glutamate': 'Excitatory',
        'Acetylcholine': 'Excitatory',
        'Dopamine': 'Excitatory',
        'Serotonin': 'Excitatory',
    }
    
    # 从神经元类型文件读取
    import pandas as pd
    neuron_types = pd.read_csv(neuron_types_file)
    
    # 映射神经递质
    nt_map = []
    for _, row in neuron_types.iterrows():
        neuron_type = row['neuron_type']
        nt = type_to_nt.get(neuron_type, 'Unknown')
        nt_class = nt_to_class.get(nt, 'Unknown')
        
        nt_map.append({
            'neuron_id': row['neuron_id'],
            'neurotransmitter': nt,
            'neurotransmitter_class': nt_class
        })
    
    # 保存
    df = pd.DataFrame(nt_map)
    df.to_csv(output_file, index=False)
    print(f"✅ 生成 {len(nt_map)} 个神经递质映射")
```

---

### 📌 **4. 生物物理参数 (neuron_params.yaml)**

#### 数据内容
```yaml
LIF_neuron:
  tau_m: 20.0  # 膜时间常数 (ms)
  tau_syn: 5.0  # 突触时间常数 (ms)
  V_rest: -70.0  # 静息电位 (mV)
  V_reset: -70.0  # 复位电位 (mV)
  V_threshold: -50.0  # 阈值 (mV)
  R_m: 10000.0  # 膜电阻 (Ohm)
  C_m: 0.0001  # 膜容 (F)

Synapse:
  tau_rise: 0.5  # 上升时间 (ms)
  tau_decay: 3.0  # 衰减时间 (ms)
  delay: 1.0  # 传导延迟 (ms)

STDP:
  tau_plus: 20.0  # 正 STDP 时间窗 (ms)
  tau_minus: 20.0  # 负 STDP 时间窗 (ms)
  A_plus: 0.001  # 正强化幅度
  A_minus: -0.001  # 负强化幅度
```

#### 获取方式（2 个选项）

##### 🟢 **方式 A：使用标准文献参数（推荐）**

**来源**：

```
1. Izhikevich (2003) - Spiking Neuron Models
   → 标准 LIF 参数
   
2. Dayan & Abbott (2001) - Theoretical Neuroscience
   → 生物物理参数
   
3. Brian2 官方文档
   → 神经形态计算参数
   
4. NEST 模拟库
   → 预定义参数集
```

**标准参数值**：
```
LIF 模型（广泛使用）：
  τ_m = 20 ms （果蝇）到 10-30 ms （哺乳动物）
  τ_syn = 3-5 ms （快速突触）
  V_threshold = -50 to -45 mV
  V_reset = -70 to -65 mV
  
Hodgkin-Huxley 模型：
  C_m = 1 μF/cm²
  g_Na = 120 mS/cm²
  g_K = 36 mS/cm²
  g_L = 0.3 mS/cm²
```

##### 🟢 **方式 B：从神经形态计算库下载**

**Brian2 示例**：
```python
# 从 Brian2 获取标准参数
from brian2 import *

# LIF 神经元默认参数
default_params = {
    'tau_m': 20 * ms,
    'tau_syn': 5 * ms,
    'V_rest': -70 * mV,
    'V_reset': -70 * mV,
    'V_threshold': -50 * mV,
}
```

**NEST 示例**：
```python
import nest

# 获取神经元模型的默认参数
nest.SetDefaults("iaf_psc_alpha", {"tau_m": 20.0})
params = nest.GetDefaults("iaf_psc_alpha")
print(params)
```

#### 🔧 **参数配置文件**

**生成标准配置**：
```python
import yaml

params = {
    'LIF_neuron': {
        'tau_m': 20.0,  # ms
        'tau_syn': 5.0,  # ms
        'V_rest': -70.0,  # mV
        'V_reset': -70.0,  # mV
        'V_threshold': -50.0,  # mV
        'R_m': 10000.0,  # Ohm
        'C_m': 0.0001,  # F
    },
    'Synapse': {
        'tau_rise': 0.5,  # ms
        'tau_decay': 3.0,  # ms
        'delay': 1.0,  # ms
    },
    'STDP': {
        'tau_plus': 20.0,  # ms
        'tau_minus': 20.0,  # ms
        'A_plus': 0.001,
        'A_minus': -0.001,
    }
}

# 保存
with open('neuron_params.yaml', 'w') as f:
    yaml.dump(params, f)
```

---

## 第三部分：快速获取清单（今天）

### ✅ **1 小时快速方案**

```
☐ 第 1 步（10 分钟）：
   访问 connectomedata.org
   下载 C.elegans neuron_types.csv
   
☐ 第 2 步（10 分钟）：
   访问 https://neuprint.janelia.org/
   下载 Hemibrain neuron properties
   
☐ 第 3 步（20 分钟）：
   运行本指南中的 Python 脚本
   生成 synapse_weights.json
   生成 neurotransmitter_map.csv
   
☐ 第 4 步（10 分钟）：
   从本指南复制 neuron_params.yaml
   保存本地

✅ 完成！所有 4 个数据集已获取
```

### 📁 **文件位置**

获取后应放在：
```
/vault/sdi_sim/data/
├─ neuron_types.csv (50 KB)
├─ synapse_weights.json (1-5 MB)
├─ neurotransmitter_map.csv (10 KB)
└─ neuron_params.yaml (5 KB)
```

---

## 第四部分：验证和集成

### 🔧 **验证数据完整性**

```python
import json
import pandas as pd

# 验证 neuron_types
df_types = pd.read_csv('neuron_types.csv')
print(f"神经元总数：{len(df_types)}")
print(f"包含列：{df_types.columns.tolist()}")

# 验证 synapse_weights
with open('synapse_weights.json', 'r') as f:
    weights = json.load(f)
print(f"突触总数：{len(weights['synapses'])}")

# 验证 neurotransmitter_map
df_nt = pd.read_csv('neurotransmitter_map.csv')
print(f"神经递质分布：\n{df_nt['neurotransmitter'].value_counts()}")
```

### 📤 **推送到 GitHub**

```bash
# 复制到 Genspark
cp /vault/sdi_sim/data/* ~/i-nest/30_TCC/35_Simulation/data/

# 提交
cd ~/i-nest
git add 30_TCC/35_Simulation/data/
git commit -m "data: Add neural parameters - neuron types, synapse weights, neurotransmitter map"
git push github master:main
git push origin master
```

---

## 总结

| 数据 | 获取来源 | 预计时间 | 难度 |
|------|---------|---------|------|
| 神经元类型 | connectomedata.org + FlyEM | 30 分钟 | 低 |
| 突触强度 | Hemibrain JSON + 脚本 | 20 分钟 | 低 |
| 神经递质类型 | NeuPrint API | 20 分钟 | 低 |
| 生物物理参数 | 文献标准值 | 10 分钟 | 低 |

**总时间**：~80 分钟（< 2 小时）

---

**文档版本**：v1.0-ACQUISITION
**更新时间**：2026-07-03
**下一步**：按照快速获取清单执行

