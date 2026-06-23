import traceback, os
os.chdir(r"D:\Obsidian\phase1_workspace")
try:
    exec(open("sdi_v22_evolution.py", encoding="utf-8").read())
except Exception:
    traceback.print_exc()
