import sys
path = r'D:\Obsidian\home\work\.openclaw\workspace\simulation\sdi_l6_general.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

old_m = '''    def _compute_metrics(self):
        try:
            deg = np.bincount(self.src, minlength=self.N)
            dp = deg[deg > 0]
            if len(dp) >= 4:
                h, bins = np.histogram(np.log(dp + 0.5), bins=min(12, max(4, len(dp)//2)))
                bc = (bins[:-1] + bins[1:]) / 2
                pm = h > 0
                if pm.sum() >= 2:
                    a = -np.polyfit(bc[pm], np.log(h[pm].astype(float) + 1.0), 1)[0]
                    if 1.0 < a < 20.0:
                        self.alpha = a
            self.sigma = self.alpha if self.alpha > 1.0 else 1.0
            self.el_ratio = (self.btype == 2).sum() / max(self.n_bonds, 1)
        except: pass'''

new_m = '''    def _compute_metrics(self):
        try:
            deg = np.bincount(self.src, minlength=self.N)
            dp = deg[deg > 0]
            # Degree heterogeneity (sigma proxy): CV = std/mean of out-degree
            # CV > 0.5 indicates significant self-organized heterogeneity
            if len(dp) >= 3:
                cv = np.std(dp) / (np.mean(dp) + 1e-8)
                # Also try power-law fit for comparison
                if len(dp) >= 4:
                    try:
                        h, bins = np.histogram(np.log(dp + 0.5), bins=min(10, len(dp)//2))
                        bc = (bins[:-1] + bins[1:]) / 2; pm = h > 0
                        if pm.sum() >= 2:
                            a = -np.polyfit(bc[pm], np.log(h[pm].astype(float) + 1.0), 1)[0]
                            self.alpha = max(a, 0.1)
                    except: pass
                # sigma = max(power-law alpha, CV-scaled)
                self.sigma = max(self.alpha, 1.0 + cv * 3.0)
            self.el_ratio = (self.btype == 2).sum() / max(self.n_bonds, 1)
        except: pass'''

c = c.replace(old_m, new_m)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('L6 sigma: CV-based heterogeneity metric applied')
