# TCC 产品化子工程（`tcc`）设计说明

**Domain**: TCC
**Source**: raw\imports\2026-07-28-tcc-productized-subproject-design.md
**Compiled**: 2026-08-01

## Summary
> 面向后续长期维护：在 `cim-design` 仓库内新建一个“产品化子工程”作为主力代码归宿，顶层包名为 `tcc`。DRBE 与推理（infer）作为两个 workload 共享同一套 TCC 核心层（L1/L2/L3 + RTC + metrics）。 - 在仓库内新增 **产品化子工程**：`src/tcc/`，作为后续主力开发与维护入口。 - 保持现有 DRBE MVP 主链体验不丢：仍支持一键运行 `IQ 回放 → FFT → DBF → 拓扑页切换 → 指标输出`。 - 固化 TCC 核心层边界：将 **L1/L2/L3、RTC 原语、指标体系（含 `τ_commit/τ_apply/τ_resume`）** 抽到 `tcc/core`，供不同 workload 复用。 - 建立 workload 分层：`tcc/workloads/drbe` 与 `tcc/workloads/infer` 分别承载 DRBE 与推理相关实现，互不相互依赖（只能依赖 `tcc/core`）。

## Keywords
TCC, topology, 互连, 拓扑

---
*Auto-compiled by wiki_compiler.py*


## Related Concepts

[[Network_Topology_Design]]
