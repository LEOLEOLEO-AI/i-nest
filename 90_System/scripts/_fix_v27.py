import sys
path = r"D:\Obsidian\phase1_workspace\sdi_v27_multiscale.py"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

old = '''    n_types = {}
    for b in range(factor):
        offset = b * N0
        for i, nt in data["n_types"].items():
            n_types[offset + int(i)] = nt'''

new = '''    n_types_raw = data["n_types"]
    node_list = list(data["nodes"])
    node_to_idx = {n: i for i, n in enumerate(node_list)}
    n_types = {}
    for b in range(factor):
        offset = b * N0
        for node_name, nt in n_types_raw.items():
            idx = node_to_idx.get(node_name, 0)
            n_types[offset + idx] = nt'''

code = code.replace(old, new)
with open(path, "w", encoding="utf-8") as f:
    f.write(code)
print("Fixed n_types mapping")
