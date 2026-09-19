# 仿真报告 · 跨物种连接组临界性交叉仿真（秀丽线虫/果蝇/猕猴）

- 实验 `celegans_cross_species_criticality` · 运行 `20260919-225644-s0`
- 证据等级 **[仿真]**
- 状态 **ok**
- 随机种子 `0` · 配置哈希 `602905f36c86` · 结果哈希 `0f4a6389b400`
- git `26c65f7c3` · Python 3.10.11
- 耗时 6.65s

## 配置

```json
{
  "species": [
    "celegans",
    "celegans_elec",
    "hemibrain",
    "macaque"
  ],
  "gain_lo": 0.25,
  "gain_hi": 3.0,
  "gain_n": 8,
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
  "species_skipped": {
    "hemibrain": "ValueError: hemibrain 边表已损坏(715 字节)：文件内容是云存储报错页（AccessDenied），不是数据。需重新下载（原文件可能来自需要鉴权的 GCS 链接）。"
  },
  "gains": [
    0.25,
    0.6429,
    1.0357,
    1.4286,
    1.8214,
    2.2143,
    2.6071,
    3.0
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
      "critical_gain": 0.25,
      "sigma_at_critical": 3.9163909959534102,
      "dynamic_range_decades": 0.13143344871338758,
      "sigma_by_gain": [
        {
          "gain": 0.25,
          "sigma": 3.9163909959534102,
          "mean_size": 162.4825,
          "tau": 1.244681252218883
        },
        {
          "gain": 0.6429,
          "sigma": 6.45479995747546,
          "mean_size": 211.6425,
          "tau": 1.2160283977781057
        },
        {
          "gain": 1.0357,
          "sigma": 7.895649307095028,
          "mean_size": 219.9075,
          "tau": 1.2104985131916748
        },
        {
          "gain": 1.4286,
          "sigma": 7.895649307095028,
          "mean_size": 219.9075,
          "tau": 1.2104985131916748
        },
        {
          "gain": 1.8214,
          "sigma": 7.895649307095028,
          "mean_size": 219.9075,
          "tau": 1.2104985131916748
        },
        {
          "gain": 2.2143,
          "sigma": 7.895649307095028,
          "mean_size": 219.9075,
          "tau": 1.2104985131916748
        },
        {
          "gain": 2.6071,
          "sigma": 7.895649307095028,
          "mean_size": 219.9075,
          "tau": 1.2104985131916748
        },
        {
          "gain": 3.0,
          "sigma": 7.895649307095028,
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
      "critical_gain": 0.25,
      "sigma_at_critical": 2.343784869448784,
      "dynamic_range_decades": 0.6875395087502856,
      "sigma_by_gain": [
        {
          "gain": 0.25,
          "sigma": 2.343784869448784,
          "mean_size": 44.81,
          "tau": 1.4992179818653009
        },
        {
          "gain": 0.6429,
          "sigma": 3.327384787785404,
          "mean_size": 178.475,
          "tau": 1.2293524372710922
        },
        {
          "gain": 1.0357,
          "sigma": 4.12786967877927,
          "mean_size": 218.23,
          "tau": 1.2064875895768528
        },
        {
          "gain": 1.4286,
          "sigma": 4.12786967877927,
          "mean_size": 218.23,
          "tau": 1.2064875895768528
        },
        {
          "gain": 1.8214,
          "sigma": 4.12786967877927,
          "mean_size": 218.23,
          "tau": 1.2064875895768528
        },
        {
          "gain": 2.2143,
          "sigma": 4.12786967877927,
          "mean_size": 218.23,
          "tau": 1.2064875895768528
        },
        {
          "gain": 2.6071,
          "sigma": 4.12786967877927,
          "mean_size": 218.23,
          "tau": 1.2064875895768528
        },
        {
          "gain": 3.0,
          "sigma": 4.12786967877927,
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
      "critical_gain": 0.6429,
      "sigma_at_critical": 0.7937007874015748,
      "dynamic_range_decades": 1.7424855635838028,
      "sigma_by_gain": [
        {
          "gain": 0.25,
          "sigma": 0.30141843971631205,
          "mean_size": 1.41,
          "tau": 5.460137319746987
        },
        {
          "gain": 0.6429,
          "sigma": 0.7937007874015748,
          "mean_size": 3.175,
          "tau": 2.335810432888503
        },
        {
          "gain": 1.0357,
          "sigma": 1.3359167404782994,
          "mean_size": 11.29,
          "tau": 1.6372162304176152
        },
        {
          "gain": 1.4286,
          "sigma": 1.7941875197972759,
          "mean_size": 31.57,
          "tau": 1.3703078663896586
        },
        {
          "gain": 1.8214,
          "sigma": 2.262113437173607,
          "mean_size": 55.0525,
          "tau": 1.2829770481484415
        },
        {
          "gain": 2.2143,
          "sigma": 2.7128334997859893,
          "mean_size": 70.09,
          "tau": 1.2461096419588467
        },
        {
          "gain": 2.6071,
          "sigma": 3.168398677373642,
          "mean_size": 74.095,
          "tau": 1.2410272187003932
        },
```

## 复现命令

```bash
cd D:\Obsidian\vault\90_System && python -m sim_platform.run celegans_cross_species_criticality --seed 0
```

> 所有数值均为 **[仿真]**，不构成实测结论（AGENTS.md §0.1）。