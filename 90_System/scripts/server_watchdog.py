import subprocess, time, socket, os

PORT = 8899
BAT = r"D:\Obsidian\home\work\.openclaw\workspace\90_System\scripts\start_server.bat"

def is_running():
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect(("127.0.0.1", PORT))
        s.close()
        return True
    except:
        return False

print("Watchdog: monitoring port " + str(PORT))
while True:
    if not is_running():
        print("Down! Restarting...")
        subprocess.Popen(["cmd.exe", "/c", BAT], creationflags=subprocess.CREATE_NO_WINDOW)
        time.sleep(5)
    time.sleep(30)
