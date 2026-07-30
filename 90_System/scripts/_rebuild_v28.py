import sys
# Read the v27 file and extract the core simulator + tests
# Then create v28 as a new file with only the needed changes
base = r"D:\Obsidian\phase1_workspace\sdi_v27_multiscale.py"

with open(base, "r", encoding="utf-8") as f:
    content = f.read()

# Fix the corrupted parts
# Fix 1: def corruption
content = content.replace("def # v28: N=2000 test\nv27_multi_scale_test(factors=[1, 2, 3, 4, 7]",
                          "def v27_multi_scale_test(factors=[1, 2, 3, 4, 7]")

# Fix 2: find and fix indentation at line 675 area
lines = content.split("\n")
# Check around line 675
for i in range(670, min(685, len(lines))):
    if "Results saved" in lines[i] and not lines[i].startswith(" "):
        # This should be inside if __name__ block
        lines[i] = "    " + lines[i].strip()
        print(f"Fixed line {i+1}")

content = "\n".join(lines)

# Fix 3: update version strings
content = content.replace("v27 Real C.elegans xN Multi-Scale Test", 
                          "v28 Real C.elegans xN Multi-Scale Test")
content = content.replace("v28 Real C.elegans xN", "v28 Real C.elegans xN")
content = content.replace("BCM_ETA=0.15", "BCM_ETA=0.25")
content = content.replace("OUT_DIR   = \"D:/Obsidian/phase1_workspace/v27_results\"",
                          "OUT_DIR   = \"D:/Obsidian/phase1_workspace/v28_results\"")

# Also update the scaling epsilon comment
if "v27_results" in content:
    content = content.replace("v27_results", "v28_results")

out_path = r"D:\Obsidian\phase1_workspace\sdi_v28_multiscale.py"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(content)

import py_compile
try:
    py_compile.compile(out_path, doraise=True)
    print("v28 built, syntax OK, size:", len(content))
except py_compile.PyCompileError as e:
    print(f"Syntax error: {e}")
