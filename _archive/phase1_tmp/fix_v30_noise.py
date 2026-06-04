with open('D:/Obsidian/phase1_workspace/sdi_v30_multiregion.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the Hebbian drive line and increase strength
old_drive = 'hebb_drive = W_hebb @ h_current * 0.5'
new_drive = 'hebb_drive = W_hebb @ h_current * 1.5'
content = content.replace(old_drive, new_drive)

# Reduce noise in step function for assoc region during retrieval
old_noise = 'v += dv + np.random.normal(0, 0.5, self.N)  # noise'
new_noise = 'noise_level = 0.5 if self.name != \"assoc\" else 0.1\n        v += dv + np.random.normal(0, noise_level, self.N)  # noise'
content = content.replace(old_noise, new_noise)

with open('D:/Obsidian/phase1_workspace/sdi_v30_multiregion.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated: Hebbian drive x3, assoc noise reduced')
