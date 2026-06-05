import sys
path = r'D:\Obsidian\home\work\.openclaw\workspace\simulation\sdi_l6_general.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Increase region sizes
c = c.replace(
    "region_sizes or {'vis': 40, 'chem': 40, 'proprio': 30, 'assoc': 60, 'motor': 50, 'meta': 30}",
    "region_sizes or {'vis': 80, 'chem': 80, 'proprio': 50, 'assoc': 120, 'motor': 80, 'meta': 50}"
)

# Add alpha tracking in init
c = c.replace(
    "self.sigma = 1.0; self.el_ratio = 0.0",
    "self.alpha = 1.0; self.sigma = 1.0; self.el_ratio = 0.0"
)

# Fix _compute_metrics
old_m = '''    def _compute_metrics(self):
        try:
            deg = np.bincount(self.src, minlength=self.N)
            if (deg > 0).sum() > 2:
                dp = deg[deg > 0]
                if len(dp) >= 3:
                    h, bins = np.histogram(np.log(dp + 0.5), bins=min(10, max(3, len(dp)//3)))
                    bc = (bins[:-1] + bins[1:]) / 2
                    pm = h > 0
                    if pm.sum() >= 2:
                        alpha = -np.polyfit(bc[pm], np.log(h[pm].astype(float) + 1.0), 1)[0]
                        if alpha > 1.0 and alpha < 20.0:
                            self.sigma = alpha
            self.el_ratio = (self.btype == 2).sum() / self.n_bonds
        except: pass'''

new_m = '''    def _compute_metrics(self):
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

c = c.replace(old_m, new_m)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print('L6 fixes applied: region sizes 2x, sigma tracking fixed')
