"""Add topographic visuomotor mapping to drosophila V30 config"""
import json, random, numpy as np
random.seed(42); np.random.seed(42)

with open(r"D:\Obsidian\phase1_workspace\v30_drosophila_config.json") as f:
    cfg = json.load(f)

vis_n = cfg["regions"]["vis"]["N"]  # 100
assoc_n = cfg["regions"]["assoc"]["N"]  # 150
motor_n = cfg["regions"]["motor"]["N"]  # 100

# Rebuild vis->assoc bonds with topographic mapping
# vis[0..49] (left) -> assoc[0..74] (left association)
# vis[50..99] (right) -> assoc[75..149] (right association)
vis_assoc = []
for _ in range(300):
    if random.random() < 0.5:
        # Left pathway: vis 0-49 -> assoc 0-74
        s = random.randint(0, 49)
        t = random.randint(0, 74)
    else:
        # Right pathway: vis 50-99 -> assoc 75-149
        s = random.randint(50, 99)
        t = random.randint(75, 149)
    vis_assoc.append([s, t, random.uniform(0.2, 0.6)])
cfg["cross_bonds"]["vis_to_assoc"] = vis_assoc

# Rebuild chem->assoc with topographic mapping for up/down
chem_n = cfg["regions"]["chem"]["N"]  # 100
chem_assoc = []
for _ in range(300):
    if random.random() < 0.5:
        s = random.randint(0, 49)  # bottom chem
        t = random.randint(0, 74)  # bottom association
    else:
        s = random.randint(50, 99)  # top chem
        t = random.randint(75, 149)  # top association
    chem_assoc.append([s, t, random.uniform(0.2, 0.6)])
cfg["cross_bonds"]["chem_to_assoc"] = chem_assoc

# Rebuild assoc->motor with topographic mapping
# assoc[0..74] (left/bottom) -> motor[0..49] (left/bottom motor)
# assoc[75..149] (right/top) -> motor[50..99] (right/top motor)
assoc_motor = []
for _ in range(400):
    # Mix left-right and up-down pathways
    pathway = random.randint(0, 3)
    if pathway == 0:
        s = random.randint(0, 37); t = random.randint(0, 24)  # L->L
    elif pathway == 1:
        s = random.randint(38, 74); t = random.randint(25, 49)  # BL->D
    elif pathway == 2:
        s = random.randint(75, 112); t = random.randint(50, 74)  # R->R
    else:
        s = random.randint(113, 149); t = random.randint(75, 99)  # T->U
    assoc_motor.append([s, t, random.uniform(0.2, 0.7)])
cfg["cross_bonds"]["assoc_to_motor"] = assoc_motor

# Boost motor feedback
motor_assoc = []
for _ in range(250):
    s = random.randint(0, motor_n-1)
    t = random.randint(0, assoc_n-1)
    motor_assoc.append([s, t, random.uniform(0.1, 0.4)])
cfg["cross_bonds"]["motor_to_assoc"] = motor_assoc

with open(r"D:\Obsidian\phase1_workspace\v30_drosophila_config.json", "w") as f:
    json.dump(cfg, f)

print("Topographic mapping added:")
print("  vis->assoc: {} edges (L->L, R->R)".format(len(vis_assoc)))
print("  chem->assoc: {} edges (B->B, T->T)".format(len(chem_assoc)))
print("  assoc->motor: {} edges (topographic)".format(len(assoc_motor)))
