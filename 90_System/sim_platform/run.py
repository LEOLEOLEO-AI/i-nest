# -*- coding: utf-8 -*-
"""sim_platform.run — 平台 CLI。

    python -m sim_platform.run check            平台自检
    python -m sim_platform.run species          各物种连接组可用性
    python -m sim_platform.run lint             版本蔓延体检
    python -m sim_platform.run list             已登记实验与最近运行
    python -m sim_platform.run run <exp_id>     跑实验（默认实验可省略）
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sim_platform import harness as H  # noqa: E402
from sim_platform import species as S  # noqa: E402


def cmd_check() -> int:
    print("=== 平台自检 ===")
    ok = True
    print(f"  平台目录: {H.PLATFORM_CODE}")
    print(f"  实验目录: {H.EXPERIMENTS} ({'存在' if H.EXPERIMENTS.exists() else '不存在'})")
    print(f"  注册表  : {H.REGISTRY} ({'存在' if H.REGISTRY.exists() else '尚未创建'})")
    try:
        from sim_platform import metrics as M
        print("  metrics  : 可导入")
    except Exception as e:
        print(f"  metrics  : 导入失败 {e}"); ok = False
    deps = H._deps()
    print(f"  依赖     : {deps}")
    for need in ("numpy", "scipy", "networkx"):
        if need not in deps:
            print(f"  ✗ 缺少必需依赖 {need}"); ok = False
    av = S.available()
    good = [k for k, v in av.items() if v["ok"]]
    print(f"  连接组   : 可用 {len(good)}/{len(av)} -> {good}")
    if not good:
        print("  ✗ 没有任何可用连接组"); ok = False
    reg = H.load_registry()
    print(f"  已登记实验: {len(reg.get('experiments', {}))}")
    print("  结论:", "OK" if ok else "有问题")
    return 0 if ok else 1


def cmd_species() -> int:
    print("=== 各物种连接组可用性 ===")
    for name, v in S.available().items():
        if v["ok"]:
            print(f"  ✓ {name:<16} n={v['n']:<5} edges={v['edges']:<7} {v['species']}")
        else:
            print(f"  ✗ {name:<16} {v['err'][:90]}")
    cm = S.celegans_species_metrics()
    if cm:
        print("\n=== C. elegans 物种级复杂度指标（已有结果）===")
        for f, d in cm.items():
            print(f"  {f}: {json.dumps(d, ensure_ascii=False)[:150]}")
    return 0


def cmd_lint() -> int:
    print("=== 版本蔓延体检（对应实测到的 24 版本并存）===")
    rows = H.lint_version_sprawl()
    if not rows:
        print("  未发现同实验多版本并存")
        return 0
    total = sum(r["count"] for r in rows)
    print(f"  发现 {len(rows)} 组、共 {total} 个多版本文件：")
    for r in rows:
        print(f"    [{r['count']:>3} 个] {r['group']}")
        for f in r["files"][:4]:
            print(f"             {f}")
        if r["count"] > 4:
            print(f"             … 其余 {r['count']-4} 个")
    print("\n  建议：只保留一个规范脚本（登记进 sim_platform 注册表），"
          "其余交给 git 历史，目录里不再并存。")
    return 0


def cmd_list() -> int:
    reg = H.load_registry()
    exps = reg.get("experiments", {})
    print(f"=== 已登记实验 {len(exps)} 个 ===")
    for k, v in exps.items():
        runs = v.get("runs", [])
        last = runs[-1] if runs else None
        print(f"  {k}")
        print(f"      标题: {v.get('title')}")
        print(f"      规范脚本: {v.get('canonical_script')}")
        print(f"      版本事件: {len(v.get('versions', []))}  运行: {len(runs)}")
        if last:
            print(f"      最近: {last['run_id']} seed={last['seed']} "
                  f"hash={last.get('result_hash')} {last.get('evidence')}")
    return 0


def cmd_run(exp_id: str, seed: int) -> int:
    if exp_id in ("", "default", "celegans"):
        from sim_platform.experiments import celegans_cross_species_criticality as E
    else:
        mod = __import__(f"sim_platform.experiments.{exp_id}", fromlist=["*"])
        E = mod
    r = H.run(getattr(E, "EXP_ID", exp_id), E.experiment,
              getattr(E, "DEFAULT_CONFIG", {}), seed=seed,
              title=getattr(E, "TITLE", exp_id))
    print(f"run_id={r.run_id} status={r.manifest['status']} "
          f"config_hash={r.manifest['config_hash']} result_hash={r.manifest['result_hash']}")
    if r.manifest["status"] != "ok":
        print("ERROR:", r.manifest["error"])
        return 1
    print(f"报告 -> {r.out_dir / 'report.md'}")
    return 0


def main() -> int:
    a = sys.argv[1:]
    if not a:
        print(__doc__); return 1
    cmd = a[0]
    if cmd == "check":
        return cmd_check()
    if cmd == "species":
        return cmd_species()
    if cmd == "lint":
        return cmd_lint()
    if cmd == "list":
        return cmd_list()
    if cmd == "run":
        exp = a[1] if len(a) > 1 else "default"
        seed = 0
        if "--seed" in a:
            seed = int(a[a.index("--seed") + 1])
        return cmd_run(exp, seed)
    print(__doc__)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
