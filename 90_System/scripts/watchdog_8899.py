# Preview Server Watchdog — keeps :8899 alive, restarts on failure
# Run: python watchdog_8899.py
import subprocess, time, socket, sys, os

PORT = 8899
SERVER_SCRIPT = r"D:\Obsidian\home\work\.openclaw\workspace\90_System\scripts\vault_server.py"
CHECK_INTERVAL = 30  # seconds

def is_alive():
    try:
        s = socket.create_connection(("127.0.0.1", PORT), timeout=3)
        s.close()
        return True
    except:
        return False

def start_server():
    return subprocess.Popen(
        [sys.executable, SERVER_SCRIPT],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
    )

if __name__ == "__main__":
    print(f"Watchdog started: monitoring port {PORT} every {CHECK_INTERVAL}s")
    proc = start_server()
    time.sleep(3)
    
    failures = 0
    while True:
        if not is_alive():
            failures += 1
            print(f"[{time.strftime('%H:%M:%S')}] Server DOWN (failures: {failures}), restarting...")
            try:
                proc.kill()
            except:
                pass
            proc = start_server()
            time.sleep(3)
        else:
            failures = 0
        time.sleep(CHECK_INTERVAL)
