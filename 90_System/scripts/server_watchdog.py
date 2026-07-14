import subprocess, time, socket
from pathlib import Path

PORT = 8899
SERVER = r"D:\Obsidian\home\work\.openclaw\workspace\90_System\scripts\vault_server.py"
PYTHON = r"C:\Users\LEO\AppData\Local\Programs\Python\Python310\python.exe"

def is_running():
    try:
        s = socket.socket(); s.settimeout(3)
        s.connect(("127.0.0.1", PORT)); s.close()
        return True
    except:
        return False

print(f"Watchdog: port {PORT}")
started = False

while True:
    if not is_running():
        print(f"[{time.strftime('%H:%M:%S')}] Down, restarting...")
        subprocess.Popen(
            [PYTHON, "-X", "utf8", SERVER],
            creationflags=subprocess.CREATE_NO_WINDOW,
            cwd=str(Path(SERVER).parent)
        )
        time.sleep(5)
    elif not started:
        print(f"[{time.strftime('%H:%M:%S')}] Server running")
        started = True
    time.sleep(15)
