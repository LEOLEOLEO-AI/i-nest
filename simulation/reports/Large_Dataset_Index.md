---
title: 大型仿真数据集索引
date: 2026-06-19
tags: [dataset, connectome, s3, download, large-scale]
status: 待下载 (需服务器+大算力)
---

# 大型仿真数据集索引

> 以下数据集因体积过大(>1GB)或需Docker/SQL环境，暂存链接于此。待构建服务器和大算力后下载使用。

---

## 1. MICrONS Mouse Visual Cortex (功能数据)

| 属性 | 值 |
|------|-----|
| 物种 | Mouse (Mus musculus) |
| 脑区 | Visual Cortex (V1, AL, PM, LM, LI, RL) |
| 数据类型 | 双光子钙成像 + 行为数据 |
| 神经元数 | ~75,000 functional units |
| 数据格式 | MySQL Docker 镜像 / SQL dump |

**S3 地址 (公开, 无需凭证)**:
```
s3://bossdb-open-data/iarpa_microns/minnie/functional_data/two_photon_processed_data_and_metadata/database_v8/
```

**文件列表**:
| 文件 | 大小 | 内容 |
|------|------|------|
| `functional_data_database_container_image_v8.tar` | 96.7 GB | Docker MySQL 数据库镜像 |
| `functional_data_database_sql_dump_v8.sql` | 108.2 GB | SQL dump |
| `two_photon_processed_data_and_metadata_technical_documentation_v8.pdf` | 120 KB | 技术文档 (已下载) |

**下载命令**:
```bash
aws s3 cp s3://bossdb-open-data/iarpa_microns/minnie/functional_data/two_photon_processed_data_and_metadata/database_v8/functional_data_database_container_image_v8.tar . --no-sign-request
```

**使用方式**:
```bash
docker load --input functional_data_database_container_image_v8.tar
docker-compose up -d database
# MySQL: root / microns123
```

**可支撑实验**: 功能活动分析、神经编码、群体动力学

**注意**: 此为功能数据，不含结构连接组。EM电镜重建连接组需从MICrONS Consortium另获取。

**参考**:
- GitHub: https://github.com/cajal/microns-nda-access (v8 branch)
- Explorer: https://www.microns-explorer.org/cortical-mm3

---

## 2. MICrONS EM Connectome (结构数据)

| 属性 | 值 |
|------|-----|
| 物种 | Mouse |
| 脑区 | Visual Cortex |
| 数据类型 | 电镜重建突触连接组 |
| 神经元数 | ~200,000 |
| 突触数 | ~500,000,000 |

**获取方式**: MICrONS Consortium 数据发布 (需申请或从BossDB获取)
- BossDB: https://bossdb.org/
- 数据通道: `bossdb://iarpa_microns/minnie/em/`

---

## 3. FlyWire Drosophila Adult Hemibrain

| 属性 | 值 |
|------|-----|
| 已下载 | ✅ traced-total-connections.csv (82 MB, N=21,739, E=3,550,403) |
| 数据来源 | FlyWire Consortium / neuprint.janelia.org |
| 版本 | v1.2 |

**完整数据获取**:
- neuPrint: https://neuprint.janelia.org/ (需注册)
- 原始地址: `s3://flyem-hemibrain/hemibrain_v1.2.1_edges.csv.gz`

**手动下载**:
```bash
curl -L -o hemibrain_edges.csv.gz "https://storage.googleapis.com/flyem-hemibrain/hemibrain_v1.2.1_edges.csv.gz"
```

---

## 4. IARPA MICrONS Full EM Volume

| 属性 | 值 |
|------|-----|
| 体积 | ~1 mm³ mouse visual cortex |
| 分辨率 | 4nm x 4nm x 40nm |
| 数据量 | ~2 PB (petabytes) |
| 访问 | BossDB API |

```
bossdb://iarpa_microns/minnie/em/
```

---

## 5. Allen Mouse Brain Connectivity Atlas

| 属性 | 值 |
|------|-----|
| 已下载 | ⚠️ allen_mouse_connectivity.json (injection metadata only) |
| 数据类型 | 病毒示踪注射实验元数据 |
| 注入点 | 2,992 |
| 完整矩阵 | 需通过 Allen API 查询 |

**API 访问**:
```
https://api.brain-map.org/api/v2/data/query.json?criteria=model::MouseConnectivity
```

---

## 6. WormWiring C.elegans

| 属性 | 值 |
|------|-----|
| 已下载 | ✅ NeuronConnect.xls (Varshney 2011) |
| 补充数据 | 成虫全突触连接组 (电+化) |

**获取**:
- WormAtlas: https://wormatlas.org/
- WormWiring: https://wormwiring.org/

---

## 总计

| 数据集 | 大小 | 状态 |
|--------|------|------|
| MICrONS Functional DB | 96.7 GB tar | 🔴 待下载 |
| MICrONS SQL Dump | 108.2 GB | 🔴 待下载 |
| MICrONS EM Connectome | ~PB | 🔴 待获取 |
| Hemibrain Full | ~200 MB | ✅ 已下载 |
| Allen Mouse Matrix | ~GB | ⚠️ 需API查询 |
| WormWiring | ~MB | ✅ 已下载 |

---

*创建于 2026-06-19 | 待服务器就绪后推进*
