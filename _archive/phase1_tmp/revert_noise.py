with open('D:/Obsidian/phase1_workspace/sdi_v30_multiregion.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Revert noise change
old_noise = 'noise_level = 0.5 if self.name != \"assoc\" else 0.1\n        v += dv + np.random.normal(0, noise_level, self.N)  # noise'
new_noise = 'v += dv + np.random.normal(0, 0.5, self.N)  # noise'
content = content.replace(old_noise, new_noise)

with open('D:/Obsidian/phase1_workspace/sdi_v30_multiregion.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Reverted noise change')
