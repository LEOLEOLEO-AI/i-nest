---
provenance: external
---

# B7: TCC OneFabric 统一内存与网络语义架构

**编号**: B7 | **编码**: P-Memory | **状态**: 🟡 框架完成
**目标**: ASPLOS / ISCA / HPCA | **投稿时间**: 2027 Q2

---

## 核心创新

统一内存与网络语义架构（TCC OneFabric）：将分布式内存访问与网络通信统一为单一语义层，消除传统计算架构中"内存墙"和"网络墙"的双重瓶颈。

### 关键洞察
- 在TCC范式下，内存即网络、网络即内存——两者统一于拓扑空间
- RISC-V指令集扩展 + SDI可重构互连 = 可编程的统一内存-网络语义
- OneFabric抽象层使得分布式系统的数据移动与局部内存访问在编程模型上不可区分

### 技术路线
1. **语义统一层设计**: 定义OneFabric ISA扩展（基于RISC-V）
2. **SDI映射**: 将内存语义操作映射到TCC-16原语 (R6+T6+C4)
3. **原型验证**: FPGA原型 + 基准测试

---

## 关联资源
- [TCC OneFabric 原始笔记](http://127.0.0.1:8899/vault/30_TCC/32_Tech/getnote_20260216_TCC OneFabric%20统一内存与网络语义架构.md)
- [TCC代码实现](http://127.0.0.1:8899/vault/50_Output/54_Code/TCC/TCC OneFabric%20统一内存与网络语义架构.md)
- [RISC-V+SDI方案](http://127.0.0.1:8899/vault/50_Output/54_Code/TCC/统一内存与网络语义架构（Risc-V结合）.md)

---

## 版本历史
| 日期         | 版本   | 变更          |
| ---------- | ---- | ----------- |
| 2026-07-15 | v0.1 | 列入论文计划，框架梳理 |

---

*最后更新: 2026-07-15*

---

## 工程落地方案

👉 **[TCC OneFabric × TCC-16 深度融合工程落地方案 v1.0](http://127.0.0.1:8899/vault/50_Output/54_Code/TCC/TCC OneFabric_TCC16_工程落地方案_v1.0.md)**

核心内容：
- **UMNAS 统一地址空间**: 64-bit 寻址 (Tile ID + Region + Offset)
- **C.MOVE 语义扩展**: DMA → 透明远程访问，OneFabric API (alloc/read/write/sync)
- **SDI Page 表驱动**: C.LINK 原子切换，1.2 µs 拓扑重配置
- **6个 IP 核分解**: OFM-ADDR/DMA/PAGE/SYNC/ROUTE/XFORM，~93K gates/Tile
- **4阶段开发路线**: 2026 Q3 → 2027 Q4 流片准备
- **3项专利 + 2篇论文**: B7 (ASPLOS/ISCA) + B7-S (OSDI/EuroSys)
