# 仿真报告 · 跨物种连接组临界性交叉仿真（秀丽线虫/果蝇/猕猴）

- 实验 `celegans_cross_species_criticality` · 运行 `20260919-225713-s0`
- 证据等级 **[仿真]**
- 状态 **ok**
- 随机种子 `0` · 配置哈希 `adf102b95bbe` · 结果哈希 `04ed44050b5c`
- git `26c65f7c3` · Python 3.10.11
- 耗时 5.65s

## 配置

```json
{
  "species": [
    "celegans",
    "celegans_elec",
    "macaque"
  ],
  "gain_lo": 0.02,
  "gain_hi": 1.5,
  "gain_n": 10,
  "n_trials": 400
}
```

## 结果

```json
{
  "evidence": "[仿真]",
  "note": "所有数值为仿真观测量，不构成实测结论或普适定律",
  "seed": 0,
  "species_loaded": {
    "celegans": {
      "n": 300,
      "edges": 2276,
      "species": "C. elegans"
    },
    "celegans_elec": {
      "n": 300,
      "edges": 1096,
      "species": "C. elegans"
    },
    "macaque": {
      "n": 82,
      "edges": 3312,
      "species": "Macaque (RM)"
    }
  },
  "species_skipped": {},
  "gains": [
    0.02,
    0.1844,
    0.3489,
    0.5133,
    0.6778,
    0.8422,
    1.0067,
    1.1711,
    1.3356,
    1.5
  ],
  "per_species": {
    "celegans": {
      "graph": {
        "n_nodes": 300,
        "n_edges": 2276,
        "density": 0.025373467112597546,
        "avg_clustering": 0.32808686282354205,
        "avg_path_len_scc": 3.4807444754344563,
        "modularity": 0.5448670085712591,
        "n_communities": 9,
        "small_world_sigma": 11.979113889524866,
        "degree_mean": 19.54,
        "degree_std": 18.554291507177883,
        "degree_max": 136.0
      },
      "critical_gain": 1.0067,
      "sigma_at_critical": 0.995452633493628,
      "dynamic_range_decades": 2.0612066740870043,
      "sigma_by_gain": [
        {
          "gain": 0.02,
          "sigma": 0.47643979057591623,
          "mean_size": 1.91,
          "tau": 3.6509183510433165
        },
        {
          "gain": 0.1844,
          "sigma": 0.9913984044040169,
          "mean_size": 116.2575,
          "tau": 1.295816824774924
        },
        {
          "gain": 0.3489,
          "sigma": 0.9946207638515331,
          "mean_size": 185.9,
          "tau": 1.2299113350074948
        },
        {
          "gain": 0.5133,
          "sigma": 0.9952139942807232,
          "mean_size": 208.9425,
          "tau": 1.2150877394244481
        },
        {
          "gain": 0.6778,
          "sigma": 0.995277003731167,
          "mean_size": 211.73,
          "tau": 1.2162745743862025
        },
        {
          "gain": 0.8422,
          "sigma": 0.9953388645474037,
          "mean_size": 214.54,
          "tau": 1.2126133208242038
        },
        {
          "gain": 1.0067,
          "sigma": 0.995452633493628,
          "mean_size": 219.9075,
          "tau": 1.2104985131916748
        },
        {
          "gain": 1.1711,
          "sigma": 0.995452633493628,
          "mean_size": 219.9075,
          "tau": 1.2104985131916748
        },
        {
          "gain": 1.3356,
          "sigma": 0.995452633493628,
          "mean_size": 219.9075,
          "tau": 1.2104985131916748
        },
        {
          "gain": 1.5,
          "sigma": 0.995452633493628,
          "mean_size": 219.9075,
          "tau": 1.2104985131916748
        }
      ]
    },
    "celegans_elec": {
      "graph": {
        "n_nodes": 300,
        "n_edges": 1096,
        "density": 0.01221850613154961,
        "avg_clustering": 0.20756046586900284,
        "avg_path_len_scc": 4.522854904009403,
        "modularity": 0.7038610656074273,
        "n_communities": 41,
        "small_world_sigma": 12.465499856765662,
        "degree_mean": 6.213333333333333,
        "degree_std": 10.05125973309924,
        "degree_max": 113.0
      },
      "critical_gain": 1.0067,
      "sigma_at_critical": 0.9954176785959767,
      "dynamic_range_decades": 2.2516655848676708,
      "sigma_by_gain": [
        {
          "gain": 0.02,
          "sigma": 0.18200408997955012,
          "mean_size": 1.2225,
          "tau": 9.264407779898221
        },
        {
          "gain": 0.1844,
          "sigma": 0.9665467926737475,
          "mean_size": 29.8925,
          "tau": 1.5931937035729136
        },
        {
          "gain": 0.3489,
          "sigma": 0.9875703054597433,
          "mean_size": 80.4525,
          "tau": 1.3538583687780603
        },
        {
          "gain": 0.5133,
          "sigma": 0.9932666733999933,
          "mean_size": 148.515,
          "tau": 1.2527964926430923
        },
        {
          "gain": 0.6778,
          "sigma": 0.9944297451608411,
          "mean_size": 179.525,
          "tau": 1.231147071090869
        },
        {
          "gain": 0.8422,
          "sigma": 0.9952337261537362,
          "mean_size": 209.8075,
          "tau": 1.2092424997359228
        },
        {
          "gain": 1.0067,
          "sigma": 0.9954176785959767,
          "mean_size": 218.23,
          "tau": 1.2064875895768528
        },
        {
          "gain": 1.1711,
          "sigma": 0.9954176785959767,
          "mean_size": 218.23,
          "tau": 1.2064875895768528
        },
        {
          "gain": 1.3356,
          "sigma": 0.9954176785959767,
          "mean_size": 218.23,
          "tau": 1.2064875895768528
        },
        {
          "gain": 1.5,
          "sigma": 0.9954176785959767,
          "mean_size": 218.23,
          "tau": 1.2064875895768528
        }
      ]
    },
    "macaque": {
      "graph": {
        "n_nodes": 82,
        "n_edges": 3312,
        "density": 0.4986449864498645,
        "avg_clustering": 0.7471200164686104,
        "avg_path_len_scc": 1.5173140620295091,
        "modularity": 0.5389313652315243,
        "n_communities": 6,
        "small_world_sigma": 1.5265371042482356,
        "degree_mean": 1.204094163775366,
        "degree_std": 0.3252904994484525,
        "degree_max": 1.9220546563
      },
      "critical_gain": 1.5,
      "sigma_at_critical": 0.9729455529252621,
      "dynamic_range_decades": 1.5517732321500437,
      "sigma_by_gain": [
        {
          "gain": 0.02,
          "sigma": 0.03614457831325301,
          "mean_size": 1.0375,
          "tau": 39.47186775703903
        },
        {
          "gain": 0.1844,
          "sigma": 0.2248062015503876,
          "mean_size": 1.29,
          "tau": 6.815815007168007
        },
        {
          "gain": 0.3489,
          "sigma": 0.4152046783625731,
          "mean_size": 1.71,
          "tau": 3.8291150520467903
        },
        {
          "gain": 0.5133,
          "sigma": 0.5815899581589958
```

## 复现命令

```bash
cd D:\Obsidian\vault\90_System && python -m sim_platform.run celegans_cross_species_criticality --seed 0
```

> 所有数值均为 **[仿真]**，不构成实测结论（AGENTS.md §0.1）。