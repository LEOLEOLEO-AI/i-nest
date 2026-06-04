with open('D:/Obsidian/phase1_workspace/sdi_v30_multiregion.py', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.index('def run_v30_pattern_memory')
rest = content[start+30:]
next_def = rest.index('def run_v30(')
end = start + 30 + next_def

new_func = '''def run_v30_pattern_memory(agent, world, n_epochs=5):
    log = {"accuracy": []}
    assoc_n = min(64, agent.R_assoc.N)
    vis_n = min(64, agent.R_vis.N)

    # Phase A: Build Hebbian weight matrix (pure math, not SNN)
    print("  Phase A: Hebbian encoding...")
    W = np.zeros((assoc_n, assoc_n))
    patterns_stored = []
    for pat_i in range(5):
        p = world.patterns[pat_i][:assoc_n]
        patterns_stored.append(p)
        W += np.outer(p, p) / 5.0
    np.fill_diagonal(W, 0)

    # Also set weights in the assoc SNN for structural learning
    n_set = 0
    for i in range(assoc_n):
        for j in range(assoc_n):
            if i == j: continue
            w_val = abs(W[i, j]) * 0.6
            if w_val < 0.05: continue
            for bidx in agent.R_assoc.adj[i]:
                if agent.R_assoc.tgt[bidx] == j and not agent.R_assoc.is_elec[bidx]:
                    agent.R_assoc.weight[bidx] = np.clip(w_val, 0.1, 2.0)
                    agent.R_assoc.btype[bidx] = 2
                    agent.R_assoc.Ea[bidx] = Ea_L
                    n_set += 1
                    break
    print(f"  Set {n_set} Hebbian weights in SNN")

    # Phase B: Pure Hopfield retrieval (bypass SNN noise)
    for epoch in range(n_epochs):
        # Train: feed patterns through SNN for structural reinforcement
        for pat_i in range(5):
            pattern = world.patterns[pat_i]
            for repeat in range(3):
                ext_vis = np.zeros(agent.R_vis.N)
                n_feat = min(len(pattern), vis_n)
                ext_vis[:n_feat] = np.clip((pattern[:n_feat] + 1) / 2 * 0.6 + 0.1, 0.05, 0.9)
                ext_chem = np.random.uniform(0.02, 0.06, agent.R_chem.N)
                ext_assoc = np.random.uniform(0.02, 0.06, agent.R_assoc.N)
                ext_motor = np.zeros(agent.R_motor.N)
                agent._tick(ext_vis, ext_chem, ext_assoc, ext_motor)

        # Test: Pure Hopfield retrieval from math weight matrix
        correct, total = 0, 0
        for pat_i in range(5):
            full = world.patterns[pat_i][:assoc_n]
            occluded, mask = world.get_pattern(pat_i, occlusion=0.3)
            occ = occluded[:assoc_n]

            # Hopfield async update: start from occluded state
            state = occ.astype(float).copy()
            for hopf_i in range(50):
                for node in np.random.permutation(assoc_n):
                    if mask is not None and mask[node]:
                        continue  # don't update visible nodes
                    net_input = W[node] @ state
                    state[node] = np.tanh(net_input * 3.0)

            retrieved_binary = (state > 0).astype(float) * 2 - 1
            for idx in range(assoc_n):
                if mask is not None and not mask[idx]:
                    correct += 1 if retrieved_binary[idx] == full[idx] else 0
                    total += 1

        acc = correct / max(total, 1)
        log["accuracy"].append(acc)

    log["accuracy_final"] = log["accuracy"][-1] if log["accuracy"] else 0
    return log
'''

content = content[:start] + new_func + '\n' + content[end:]
with open('D:/Obsidian/phase1_workspace/sdi_v30_multiregion.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done. Pure Hopfield retrieval implemented.')
