import json, os
os.chdir(r"D:\Obsidian\home\work\.openclaw\workspace")
data = json.load(open("dashboard/data.json", encoding="utf-8"))
v31 = json.load(open("simulation/data/v31_results/v31_results.json"))
ratio = v31["sc_fc_coupling"]["on_off_ratio"]
data["simulation"]["versions"]["V31"] = {
    "name": "C.elegans SC-FC Coupling",
    "species": "C.elegans", "N": 279,
    "sigma": "SC=6.98 -> FC=2.69", "status": "complete",
    "finding": "FC {:.0f}x stronger on SC edges".format(ratio)
}
data["simulation"]["last_updated"] = "2026-06-19"
data["simulation"]["key_findings"].append(
    "V31: FC on SC edges is {:.0f}x stronger than off (C.elegans heat kernel)".format(ratio)
)
with open("dashboard/data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
js = "window.DASHBOARD_DATA = " + json.dumps(data, indent=2, ensure_ascii=False) + ";"
with open("dashboard/data.js", "w", encoding="utf-8") as f:
    f.write(js)
print("Dashboard updated with V31 (FC {:.0f}x on SC)".format(ratio))
