import re

with open('D:/Obsidian/phase1_workspace/sdi_v30_multiregion.py', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.index('def run_v30_pattern_memory')
rest = content[start+30:]
next_def = rest.index('def run_v30(')
end = start + 30 + next_def

print(f'old func len: {end - start}')

new_func = '''def run_v30_pattern_memory(agent, world, n_epochs=5):
    log = {"accuracy": []}
    vis_nodes_for_pattern = min(64, agent.R_vis.N)
    assoc_nodes_for_pattern = min(64, agent.R_assoc.N)

    print("  Phase A: Hebbian encoding...")
    W_hebb = np.zeros((assoc_nodes_for_pattern, assoc_nodes_for_pattern))
    for pat_i in range(5):
        p = world.patterns[pat_i][:assoc_nodes_for_pattern]
        W_hebb += np.outer(p, p) / 5.0
    np.fill_diagonal(W_hebb, 0)

    n_set = 0
    for i in range(assoc_nodes_for_pattern):
        for j in range(assoc_nodes_for_pattern):
            if i == j: continue
            w_val = abs(W_hebb[i, j]) * 0.6
            if w_val < 0.05: continue
            for bidx in agent.R_assoc.adj[i]:
                if agent.R_assoc.tgt[bidx] == j and not agent.R_assoc.is_elec[bidx]:
                    agent.R_assoc.weight[bidx] = np.clip(w_val, 0.1, 2.0)
                    agent.R_assoc.btype[bidx] = 2
                    agent.R_assoc.Ea[bidx] = Ea_L
                    n_set += 1
                    break
    print(f"  Set {n_set} Hebbian weights")

    for epoch in range(n_epochs):
        for pat_i in range(5):
            pattern = world.patterns[pat_i]
            for repeat in range(5):
                ext_vis = np.zeros(agent.R_vis.N)
                n_feat = min(len(pattern), vis_nodes_for_pattern)
                ext_vis[:n_feat] = np.clip((pattern[:n_feat] + 1) / 2 * 0.6 + 0.1, 0.05, 0.9)
                ext_chem = np.random.uniform(0.02, 0.06, agent.R_chem.N)
                ext_assoc = np.random.uniform(0.02, 0.06, agent.R_assoc.N)
                ext_motor = np.zeros(agent.R_motor.N)
                agent._tick(ext_vis, ext_chem, ext_assoc, ext_motor)

        correct, total = 0, 0
        for pat_i in range(5):
            full_pattern = world.patterns[pat_i]
            occluded, mask = world.get_pattern(pat_i, occlusion=0.3)
            ext_vis = np.zeros(agent.R_vis.N)
            n_feat = min(len(occluded), vis_nodes_for_pattern)
            ext_vis[:n_feat] = np.clip((occluded[:n_feat] + 1) / 2 * 0.6 + 0.1, 0.05, 0.9)
            for hopf_i in range(30):
                ext_chem = np.zeros(agent.R_chem.N)
                ext_assoc = np.zeros(agent.R_assoc.N)
                h_current = agent.R_assoc.h[:assoc_nodes_for_pattern]
                hebb_drive = W_hebb @ h_current * 0.5
                ext_assoc[:assoc_nodes_for_pattern] = np.clip(hebb_drive, 0.0, 0.4)
                ext_motor = np.zeros(agent.R_motor.N)
                _, _, _, _, _, h_assoc, _, _ = agent._tick(ext_vis, ext_chem, ext_assoc, ext_motor)
            reconstructed = h_assoc[:n_feat]
            retrieved_binary = (reconstructed > 0.15).astype(float) * 2 - 1
            for idx in range(n_feat):
                if mask is not None and not mask[idx]:
                    correct += 1 if retrieved_binary[idx] == full_pattern[idx] else 0
                    total += 1
        acc = correct / max(total, 1)
        log["accuracy"].append(acc)

    log["accuracy_final"] = log["accuracy"][-1] if log["accuracy"] else 0
    return log
'''

content = content[:start] + new_func + '\n' + content[end:]
with open('D:/Obsidian/phase1_workspace/sdi_v30_multiregion.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done.')
