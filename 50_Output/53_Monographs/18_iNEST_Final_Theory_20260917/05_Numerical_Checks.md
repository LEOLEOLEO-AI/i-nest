# 解析校核与纯连接数值示例

证据：[仿真]。不是器件实测，也不是智能性能基准。
配置均为[假设]合成示例；单位归一化，不能兑换成真实功率或延迟。
运行环境：Python 3.10.11，NumPy 1.26.4，SciPy 1.15.3。
固定种子 20260918；节点数 5，候选边为完全无向图的 10 条边。
节点线性泄漏为 [0.7,0.9,0.8,1.0,0.6]，三次系数 0.4；输入为节点 0、1，输出固定为节点 3、4。
V-SIM02 验收：每项残差通过下表事先写入脚本的容差；只支持相应解析实现。

| 任务 | 检验 | 数值 | 通过标准 |
|---|---|---|---|
| V-TH12 | implicit response derivative | 2.5098534e-11 | < 1e-7 |
| V-TH13 | two-phase gradient, smallest beta | 1.252643e-07 | < 2e-6; decreasing error |
| V-TH10 | normalized equilibrium noise covariance | 3.6799042e-18 | < 1e-12; stable drift |
| V-TH14 | projected descent inequality slack | 0.06975 | >= -1e-12 |
| V-TH15 | local score x feedback vs enumeration | 6.9388939e-18 | < 1e-12 |
| V-GEO02 | noncommuting frame generators, zero pure-gauge curvature | 0 | < 1e-12 |
| V-GEO02 | basis-change preserves physical state | 5.5511151e-17 | < 1e-12 |

## 只改变二值连接的示例

每个候选均保持 4 条单位电导边；固定节点参数、输入、输出和读出，使用穷举邻居的贪心换边。
这是有中央候选评价器的最小参考算法，不是已经完成的局部硬件自组织实现。
训练输入 24 组、独立同分布留出输入 80 组；标签来自预先固定的同类教师网络。
测试数据只用于记录，既不选候选也不选停止时刻。单一种子和可实现教师不支持外部任务泛化结论。
[仿真] 接受换边：3；训练损失评价调用：100（每次包括全部训练输入）。
[仿真] 初始训练/留出损失：0.009460760439 / 0.006639166446。
[仿真] 最终训练/留出损失：0 / 0。
初始边：[(0, 1), (0, 2), (0, 3), (0, 4)]。
最终边：[(0, 2), (1, 2), (2, 3), (3, 4)]。
验收只要求合法边数与训练损失非增；未预设留出改善和教师图恢复。
没有热噪声、延迟、器件漂移、总表计量或跨种子统计，故 V-EXP03 和 V-EXP04 仍待测。

图：Output/18_iNEST_Final_Theory_20260917/02_Core_Numerical_Examples.png。
