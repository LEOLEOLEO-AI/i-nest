# B7: OneFabric-Memory 统一内存与网络语义架构

**编号**: B7 | **编码**: P-Memory | **状态**: 🟡 框架完成
**目标**: ASPLOS / ISCA / HPCA | **投稿时间**: 2027 Q2

---

## 核心创新

统一内存与网络语义架构（OneFabric-Memory）：将分布式内存访问与网络通信统一为单一语义层，消除传统计算架构中"内存墙"和"网络墙"的双重瓶颈。

### 关键洞察
- 在TCC范式下，内存即网络、网络即内存——两者统一于拓扑空间
- RISC-V指令集扩展 + SDI可重构互连 = 可编程的统一内存-网络语义
- OneFabric抽象层使得分布式系统的数据移动与局部内存访问在编程模型上不可区分

### 技术路线
1. **语义统一层设计**: 定义OneFabric ISA扩展（基于RISC-V）
2. **SDI映射**: 将内存语义操作映射到TCC-11原语
3. **原型验证**: FPGA原型 + 基准测试

---

## 关联资源
- [OneFabric-Memory 原始笔记](http://127.0.0.1:8899/home/work/.openclaw/workspace/30_TCC/32_Tech/getnote_20260216_OneFabric-Memory%20统一内存与网络语义架构.md)
- [TCC代码实现](http://127.0.0.1:8899/home/work/.openclaw/workspace/50_Output/54_Code/TCC/OneFabric-Memory%20统一内存与网络语义架构.md)
- [RISC-V+SDI方案](http://127.0.0.1:8899/home/work/.openclaw/workspace/50_Output/54_Code/TCC/统一内存与网络语义架构（Risc-V结合）.md)

---

## 版本历史
| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-07-15 | v0.1 | 列入论文计划，框架梳理 |

---

*最后更新: 2026-07-15*
