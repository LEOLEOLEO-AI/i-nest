---
title: MetaNet | 多组学网络分析（四）：拓扑性质读懂网络结构，拓扑指标与关键节点识别
tags:
- scale-free-networks
- small-world-networks
- tools
- topology
- tutorial
---
- **笔记本**: 我的剪贴板
- **时间**: 2026-01-19 23:57

---

原文链接: https://mp.weixin.qq.com/s/5-JZlGLMuBT-u8JQZVFfAA

01
 
MetaNet 介绍

## 本次关注的是“网络本身长什么样、结构有什么特征”，也就是用数学指标来量化网络。MetaNet 提供了节点层面和整体层面的拓扑统计：节点层面包括度数、加权度数、介数中心性、接近中心性、特征向量中心性等，可用于鉴定关键节点 / keystone 物种；整体层面则包含平均路径长度、网络密度、聚类系数、模块度、负边比例等，用来描述整个系统的连通性和复杂度。
## 还介绍如何进行模块/社区划分，比较不同模块的组成和功能，或将模块特征与环境因子、表型指标关联，从而找到“功能模块”。此外，通过在不同组条件下重复计算这些指标，可以系统比较 Case vs Control 或不同时间点网络结构的差异，判断疾病、处理或环境改变对系统稳定性与鲁棒性的影响。
## 拓扑性质的分析结果往往以表格和摘要指标的形式呈现，是进一步做统计比较、机器学习建模以及撰写结果小结（如“疾病组网络更加稀疏、聚类系数下降”）的重要数据来源。

02
 拓扑性质分析流程

1.基础准备 & 示例网络指标
1.1 基础准备

Sys.setenv(LANGUAGE = "en")options(stringsAsFactors = FALSE)rm(list=ls())setwd("D:/Gongzuo/fuxian/metanet/5")library(remotes)library(d3r)library(igraph)library(MetaNet)library(kableExtra)library(ggkegg)library(ggfx)library(ggraph)library(dplyr)library(pcutils)library(tidyr)library(ggplot2)
1.2 用内置 toy 网络看整体拓扑指标
计算网络整体拓扑指标 + 点/边指标。

只算网络层面的指标load("data.rdata")这个网络有多少点、多少边、稠密度、平均路径长度、直径、是否 small-world、有多“中心化”等。
2.随机网络 + 节点指标可视化

c_net_update()：给这个图补齐 MetaNet 需要的属性（颜色、形状、分组等）go <- erdos.renyi.game(30, 0.25)go <- c_net_update(go)par(mfrow = c(1, 2))plot(go, vertex_size_range = c(5, 20), legend = F, main = "Same size")

为每个节点计算拓扑指标go <- c_net_index(go)head(get_v(go))

需要画图数据添加作者微信：15623525389再用 Degree 映射点大小：

度数越大的点越大，一眼能看出“关键节点”。go <- c_net_set(go, vertex_size = "Degree")plot(go, vertex_size_range = c(5, 20), legend = F, main = "Size map to degree")
含义：教你如何把拓扑结果映射到绘图属性（大小、颜色等），后面会反复用到。
3.与随机网络比较 + 小世界 / 标度无标度

生成一个“保持度分布”的随机网络（null model）rand_net(co_net) -> random_net

重复构造 30 次随机网络，算每次的网络指标。算真实网络的指标，把真实网络和随机网络比较rand_net_par(co_net, reps = 30) -> randpnet_par(co_net) -> parscompare_rand(pars, randp, index = c("Average_path_length", "Clustering_coefficient"))如果你的网络路径长度接近随机，但聚集系数远大于随机 → small-world 特性。

拟合度分布是不是“幂律” → 是否接近无标度网络data("c_net", package = "MetaNet")fit_power(co_net)smallworldness(co_net)##给出一个 small-world 指数： 40.76805

生物学解读：微生物共现网络往往 small-world + 近似无标度，意味着有少数 hub 节点，系统具有较高鲁棒性但对 hub 敏感。
4.模块检测与模块网络操作
4.1 构造一个玩具模块网络

生成一个有 3 个模块、每个模块 30 个节点的“合成网络”，用于展示模块。test_module_net <- module_net(module_number = 3, n_node_in_module = 30)plot(test_module_net, mark_module = T)

需要画图数据添加作者微信：15623525389
4.2 在真实 co_net 上做模块检测

用 fast greedy 算法做社区划分，每个节点多了一列 module 表示属于哪个模块module_detect(co_net, method = "cluster_fast_greedy") -> co_net_moduget_v(co_net_modu)[, c("name", "module")] %>% head()

plot(co_net_modu,     plot_module = T, mark_module = T,     legend_position = c(-1.8, 1.6, 1.1, 1.3), edge_legend = F)table(V(co_net_modu)$module)

4.3 按模块大小筛选 / 提取子网络

只保留编号为 10 的模块，且模块节点数 ≥ 30co_net_modu2 <- filter_n_module(co_net_modu, n_node_in_module = 30, keep_id = 10)plot(co_net_modu2, plot_module = T, mark_module = T, ...)
圆圈布局：

把不同模块组织成“套娃圆圈”的布局，把这个坐标coors用到子网co_net_modu2 上，模块结构更加一目了然g_layout_circlepack(co_net_modu, group = "module") -> coorsplot(co_net_modu2, coors = coors, plot_module = T, mark_module = T, edge_legend = F)
提取单个或主成分：

根据连通分量 components 过滤，只保留主巨型组件co_net_modu3 <- filter_n_module(co_net_modu, n_node_in_module = 30, keep_id = 10, delete = T)plot(co_net_modu3, coors, plot_module = T)table(V(co_net_modu)$components)co_net_modu4 <- c_net_filter(co_net_modu, components == 1)
再做一次模块检测 + 布局：

co_net_modu4 <- module_detect(co_net_modu4)g_layout_circlepack(co_net_modu4, group = "module") -> coorsplot(co_net_modu4, coors, plot_module = T)

需要画图数据添加作者微信：15623525389
4.4 模块树 & 合并模块数
思想：模块太多不好解释 → 合并成合理数量（如 5）便于后续生物学解释。

把很多小模块按层次聚类合并成 5 个大模块p1 <- plot_module_tree(co_net_modu4, label.size = 0.6)co_net_modu5 <- combine_n_module(co_net_modu4, 5)p2 <- plot_module_tree(co_net_modu5, label.size = 0.6)p1 + p2

5.把模块映射回 OTU 丰度 & 环境因子

totu：样本 × OTU 的丰度矩阵data("otutab", package = "pcutils")totu <- t(otutab)只保留正相关边：

c_net_filter(co_net, e_type == "positive", mode = "e") -> co_net_posco_net_pos_modu <- module_detect(co_net_pos, n_node_in_module = 15, delete = T)g_layout_circlepack(co_net_pos_modu, group = "module") -> coors1plot(co_net_pos_modu, coors1, plot_module = T)
先过滤出正相关边的子网络，再做模块检测（模块数、大小重新定义）
5.1 模块 eigengene（代表性丰度）对每个模块计算“模块特征向量”（类似 WGCNA 的 module eigengene）。每个样本在该模块上的综合丰度/代表值。

module_eigen(co_net_pos_modu, totu) -> co_net_pos_modu
## 5.2 模块表达模式（不同样本中的变化）画出模块特征值随样本/分组的变化，同时可以展示与模块相关性高的 OTU。这里回答了哪些模块在不同样本／组别中上升/下降？

plot_eigen = T：加上模块 eigengene 的折线/箱线等。p1 <- module_expression(co_net_pos_modu, totu,                        r_threshold = 0.6,                        facet_param = list(ncol = 4), plot_eigen = T) +  theme(axis.text.x = element_text(size = 5, angle = 90, vjust = 0.5))
## 5.3 与环境因子相关性（ggcor）

提取样本的环境因子 / 理化指标env <- metadata[, 3:8]#从网络对象中取出“模块特征值矩阵”library(ggcor)p2 <- cor_plot(get_module_eigen(co_net_pos_modu), env) + coord_flip()p1 / p2 + patchwork::plot_layout(heights = c(2, 1.4))

## 5.4 模块内部组成 & 节点重要性
## 看每个模块在“门（Phylum）层面”的组成比例（哪个模块富集 Firmicutes，哪个富集 Proteobacteria 等）。根据“节点与模块 eigengene 的相关性”判断模块内关键 OTU，可视作模块 hub 成员。

p3 <- summary_module(co_net_pos_modu, var = "Phylum") +  scale_fill_pc()p4 <- summary_module(co_net_pos_modu, var = "node_eigen_cor") +  scale_color_pc(palette = "col2")p3 + p4

需要画图数据添加作者微信：15623525389
## 6. circlize 圆形 chord 图（links_stat）统计模块之间的边数/强度，画成一个 chord diagram；可以直观看出：哪些模块之间联系最紧密，哪些模块比较独立。

library(MetaNet)library(circlize)circos.clear()windows(width = 8, height = 8)#把外边距去到最小par(mar = c(0, 0, 0, 0))#压缩 track 之间的空隙，为和弦留空间。circos.par(  cell.padding = c(0, 0, 0, 0),  track.margin = c(0.01, 0.01))links_stat(co_net_modu2, group = "module")

7.拓扑角色（Zi–Pi）分析 & Z-P 图

为每个节点计算：Zi、Pi、Kizp_analyse(co_net_modu4) -> co_net_modu4get_v(co_net_modu4)[, c(1, 16:21)] %>% head()利用角色自动着色：

图上会用不同颜色显示不同拓扑角色，帮助快速锁定网络关键节点。co_net_modu6 <- c_net_set(co_net_modu4, vertex_class = "roles")plot(co_net_modu6, coors, mark_module = T, labels_num = 0, group_legend_title = "Roles")
最后用 zp_plot + patchwork 画 Z-P 图：

library(patchwork)library(ggplot2)p1 <- zp_plot(co_net_modu4, mode = 1)p2 <- zp_plot(co_net_modu4, mode = 3)p <- p1 + p2  + plot_layout(ncol = 2)windows(width = 12, height = 6)pggsave("co_net_modu4_zp_mode1_3.png",       plot   = p,       width  = 12,       height = 6,       dpi    = 300)
生物学意义：Zi 高、Pi 低：模块 hub（provincial hub），是模块内部的“核心成员”。Zi 高、Pi 高：network hub（少见），对整个网络结构非常关键。Zi 低、Pi 高：connector，连接多个模块的桥梁物种 / OTU，可能是关键“中介”。

零基础想学生信，看👇这个文章：
零基础也能学的AI生信课（AI助力生信入门班即将开始）

欢迎关注 | 华哥科研平台

往期精彩内容
最详尽的CNS文章空间转录组数据分析教程亲，写的这么辛苦，记得关注、点赞、打赏哟！

## Related Notes

- [[复杂网络|节点重要性|GNN-Based]]
- [[CST理论 × 集合通信硬件化：理论基础]]
- [[具有内在可变性的动态忆阻器内的生成式复杂网络]]
