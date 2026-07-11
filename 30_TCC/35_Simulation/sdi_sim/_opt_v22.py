# optimize_v22.py - add adjacency list to v22 cascade
with open(r"D:\Obsidian\phase1_workspace\sdi_v22_evolution.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add adjacency list in __init__, right before _rebuild
old = '        self._rebuild()\n        dt = time.time()-t0'
new = '        self.adj = [[] for _ in range(self.N)]\n        for j in range(len(self.src)):\n            self.adj[int(self.src[j])].append(j)\n        self._rebuild()\n        dt = time.time()-t0'
code = code.replace(old, new)
print("1. adj init:", "OK" if old in code else "MISS")

# 2. Patch cascade to use adj
old2 = 'out_edges = np.where(self.src == node)[0]\n                for j in out_edges:'
new2 = 'out_edges = self.adj[node]\n                for j in out_edges:'
count = code.count(old2)
code = code.replace(old2, new2)
print(f"2. cascade patch: {count} occurrences replaced" if count else "2. cascade: NOT FOUND")

# 3. Patch _apply_keep to rebuild adj
old3 = '''    def _apply_keep(self, keep):
        for attr in ["src","tgt","btype","weight","n_ltp","n_ltd",
                     "last_active","Ea","R","is_elec"]:
            arr = getattr(self, attr)
            setattr(self, attr, arr[keep])'''
new3 = '''    def _apply_keep(self, keep):
        for attr in ["src","tgt","btype","weight","n_ltp","n_ltd",
                     "last_active","Ea","R","is_elec"]:
            arr = getattr(self, attr)
            setattr(self, attr, arr[keep])
        self.adj = [[] for _ in range(self.N)]
        for j in range(len(self.src)):
            self.adj[int(self.src[j])].append(j)'''
code = code.replace(old3, new3)
print(f"3. _apply_keep patch: {'OK' if old3 in code else 'MISS'}")

# 4. Add adj update after new bond creation in apply_rules
old4 = '                self.is_elec = np.concatenate([self.is_elec, np.zeros(n_add, bool)])\n\n    def _apply_keep'
new4 = '                self.is_elec = np.concatenate([self.is_elec, np.zeros(n_add, bool)])\n                for k in range(n_add):\n                    self.adj[int(ns[k])].append(len(self.src) - n_add + k)\n\n    def _apply_keep'
code = code.replace(old4, new4)
print(f"4. new bonds adj: {'OK' if old4 in code else 'MISS'}")

with open(r"D:\Obsidian\phase1_workspace\sdi_v22_evolution.py", "w", encoding="utf-8") as f:
    f.write(code)
print("Saved")
