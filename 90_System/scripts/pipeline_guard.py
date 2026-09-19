#!/usr/bin/env python3
"""Run the daily pipeline with a bounded execution window and pause on timeout."""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

VAULT = Path(r"D:\Obsidian\vault")
PIPELINE = VAULT / "90_System" / "scripts" / "pipeline_v3.py"
LOGS = VAULT / "logs"
STATE = VAULT / "state"
STATUS_NOTE = VAULT / "60_MOC" / "07_Pipeline_Status.md"
PAUSE_FILE = STATE / "pipeline_pause.json"
LOCK_FILE = STATE / "pipeline_guard.lock"  # 2026-09-06: 单例文件锁, 防止并发 guard 互杀
DEFAULT_TIMEOUT_MINUTES = 75  # 实测最长 56min（graph 12385 节点导出），35min 会误杀触发暂停死锁
TIMEZONE = ZoneInfo("Asia/Shanghai")


def now():
    return datetime.now(TIMEZONE)


# 2026-09-06: 进程级单例锁。
# 故事: 调度任务(iNEST_Daily_Pipeline)与手动调用的 guard 互不知情, MultipleInstances 只对调度器内部生效;
# 两套并发跑会争同一份 state/lock 文件, 系统终结其中一个(0xC000013A)导致 LastTaskResult=failed,
# 进而触发健康告警重复弹出。这里用 OS 文件锁 + pid+host 互相发现, 已存在的 guard 主动让位或直接合入。
class GuardSingleton:
    def __init__(self, path):
        self.path = Path(path)
        self.fd = None

    def acquire(self):
        try:
            self.fd = open(self.path, "x", encoding="utf-8")
        except FileExistsError:
            existing = self._read_existing()
            if existing and self._is_alive(existing):
                return False, existing
            # 锁文件残留(上一次崩溃/cancel): 清掉重试
            try:
                self.path.unlink()
            except OSError:
                return False, self._read_existing()
            try:
                self.fd = open(self.path, "x", encoding="utf-8")
            except FileExistsError:
                return False, self._read_existing()
        self._write_payload({"pid": __import__("os").getpid(), "host": __import__("socket").gethostname(),
                             "started_at": now().isoformat(timespec="seconds")})
        return True, None

    def release(self):
        if self.fd:
            try: self.fd.close()
            except OSError: pass
            try: self.path.unlink(missing_ok=True)
            except OSError: pass

    def _write_payload(self, payload):
        self.fd.seek(0); self.fd.truncate(); self.fd.write(json.dumps(payload)); self.fd.flush()

    def _read_existing(self):
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None

    @staticmethod
    def _is_alive(payload):
        if not isinstance(payload, dict) or "pid" not in payload:
            return False
        try:
            import ctypes
            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            STILL_ACTIVE = 259
            h = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, int(payload["pid"]))
            if not h:
                return False
            try:
                code = ctypes.windll.kernel32.GetExitCodeProcess(h)
            finally:
                ctypes.windll.kernel32.CloseHandle(h)
            return code == STILL_ACTIVE
        except Exception:
            return False


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
        "requires_confirmation": status in ("timeout", "paused"),
    }
    write_json_atomic(STATE / "pipeline_guard_status.json", payload)

    headline = {
        "running": "科研管线运行中",
        "completed": "科研管线已完成",
        "failed": "科研管线执行失败",
        "timeout": "科研管线已超时并暂停",
        "paused": "科研管线等待人工确认",
        "skipped": "科研管线跳过(检测到并发实例)",
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
        lines.append(f"- 运行日志：[打开日志](http://127.0.0.1:8899/vault/{relative})")
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
        try:
            paused = json.loads(PAUSE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            paused = {}
        if paused.get("status") in ("timeout", "paused"):
            write_status("paused", "Previous timeout requires confirmation.", None,
                         timeout_minutes, None)
            print("[PAUSED] Pipeline requires explicit --resume.")
            return 2
        # Stale "cleared" marker from an already-fixed run: remove and continue.
        PAUSE_FILE.unlink(missing_ok=True)
    if resume:
        PAUSE_FILE.unlink(missing_ok=True)

    # 2026-09-06: 单例锁 — 检测到另一个活跃 guard 时, 主动退出避免互杀
    singleton = GuardSingleton(LOCK_FILE)
    acquired, holder = singleton.acquire()
    if not acquired:
        detail = f"Another pipeline guard is already running (pid={holder.get('pid') if holder else '?'} on {holder.get('host') if holder else '?'}); skipping to avoid concurrent corruption."
        write_status("skipped", detail, None, timeout_minutes, None)
        print(f"[SKIPPED] {detail}")
        return 0  # 视为良性结果, 不会触发告警
    try:
        return _run_pipeline_inner(timeout_minutes)
    finally:
        singleton.release()


def _run_pipeline_inner(timeout_minutes):

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
