#!/usr/bin/env python3
"""Run the daily pipeline with a bounded execution window and pause on timeout."""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
PIPELINE = VAULT / "90_System" / "scripts" / "pipeline_v3.py"
LOGS = VAULT / "logs"
STATE = VAULT / "state"
STATUS_NOTE = VAULT / "60_MOC" / "07_Pipeline_Status.md"
PAUSE_FILE = STATE / "pipeline_pause.json"
DEFAULT_TIMEOUT_MINUTES = 20
TIMEZONE = ZoneInfo("Asia/Shanghai")


def now():
    return datetime.now(TIMEZONE)


def write_json_atomic(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def write_status(status, detail, started, timeout_minutes, log_path, exit_code=None):
    STATE.mkdir(parents=True, exist_ok=True)
    STATUS_NOTE.parent.mkdir(parents=True, exist_ok=True)
    finished = now()
    payload = {
        "schema": "pipeline-guard-v1",
        "status": status,
        "started": started.isoformat(timespec="seconds") if started else None,
        "finished": finished.isoformat(timespec="seconds"),
        "timeout_minutes": timeout_minutes,
        "detail": detail,
        "log": str(log_path.relative_to(VAULT)).replace("\\", "/") if log_path else None,
        "exit_code": exit_code,
        "requires_confirmation": status == "timeout",
    }
    write_json_atomic(STATE / "pipeline_guard_status.json", payload)

    headline = {
        "running": "科研管线运行中",
        "completed": "科研管线已完成",
        "failed": "科研管线执行失败",
        "timeout": "科研管线已超时并暂停",
        "paused": "科研管线等待人工确认",
    }[status]
    lines = [f"# {headline}", "", f"> 更新时间：{finished:%Y-%m-%d %H:%M %Z}", ""]
    lines.extend([
        f"- 状态：`{status}`",
        f"- 允许时长：{timeout_minutes} 分钟",
        f"- 详情：{detail}",
    ])
    if started:
        lines.append(f"- 启动时间：{started:%Y-%m-%d %H:%M:%S %Z}")
    if exit_code is not None:
        lines.append(f"- 退出码：`{exit_code}`")
    if log_path:
        relative = str(log_path.relative_to(VAULT)).replace("\\", "/")
        lines.append(f"- 运行日志：[打开日志](http://127.0.0.1:8899/home/work/.openclaw/workspace/{relative})")
    if status == "timeout":
        lines.extend([
            "",
            "## 需要确认",
            "",
            "当前进程已被终止，后续自动任务已暂停。请先检查运行日志；确认后在 Codex 对话中输入“继续科研管线”，系统会以新的受控窗口重新运行。",
        ])
    elif status == "paused":
        lines.extend(["", "自动运行已暂停，等待人工确认。"])
    STATUS_NOTE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def terminate_process_tree(process):
    if process.poll() is None:
        subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                       capture_output=True, text=True, timeout=30)


def run_pipeline(timeout_minutes, resume):
    if PAUSE_FILE.exists() and not resume:
        paused = json.loads(PAUSE_FILE.read_text(encoding="utf-8"))
        write_status("paused", "Previous timeout requires confirmation.", None,
                     timeout_minutes, None)
        print("[PAUSED] Pipeline requires explicit --resume.")
        return 2
    if resume and PAUSE_FILE.exists():
        PAUSE_FILE.unlink()

    LOGS.mkdir(parents=True, exist_ok=True)
    started = now()
    log_path = LOGS / f"pipeline_guard_{started:%Y%m%d_%H%M%S}.log"
    command = [sys.executable, "-X", "utf8", str(PIPELINE)]
    try:
        with log_path.open("w", encoding="utf-8") as log_file:
            process = subprocess.Popen(command, cwd=VAULT, stdout=log_file,
                                       stderr=subprocess.STDOUT, text=True)
            try:
                exit_code = process.wait(timeout=timeout_minutes * 60)
            except subprocess.TimeoutExpired:
                terminate_process_tree(process)
                detail = f"Exceeded the {timeout_minutes}-minute limit; process tree was stopped."
                pause = {
                    "status": "timeout",
                    "timed_out_at": now().isoformat(timespec="seconds"),
                    "log": str(log_path.relative_to(VAULT)).replace("\\", "/"),
                    "timeout_minutes": timeout_minutes,
                }
                write_json_atomic(PAUSE_FILE, pause)
                write_status("timeout", detail, started, timeout_minutes, log_path, 124)
                print(f"[TIMEOUT] {detail}")
                return 124
    except OSError as error:
        write_status("failed", str(error), started, timeout_minutes, log_path, 1)
        raise

    status = "completed" if exit_code == 0 else "failed"
    detail = "Pipeline completed within the time limit." if exit_code == 0 else "Pipeline exited with a non-zero code."
    write_status(status, detail, started, timeout_minutes, log_path, exit_code)
    print(f"[{status.upper()}] {detail}")
    return exit_code


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", action="store_true", help="Clear a timeout pause and run again.")
    parser.add_argument("--timeout-minutes", type=int, default=DEFAULT_TIMEOUT_MINUTES)
    args = parser.parse_args()
    if args.timeout_minutes < 1:
        raise SystemExit("timeout-minutes must be positive")
    raise SystemExit(run_pipeline(args.timeout_minutes, args.resume))


if __name__ == "__main__":
    main()
