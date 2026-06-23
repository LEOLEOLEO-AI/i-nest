import sys
path = r'D:\Obsidian\home\work\.openclaw\workspace\simulation\sdi_l6_general.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Switch WS to BA graph
old_ws = '''        k = max(2, int(N * p_connect))
        G = nx.watts_strogatz_graph(N, k, 0.3)
        src_list, tgt_list = [], []
        for u, v in G.edges():
            if random.random() < 0.5:
                src_list.append(u); tgt_list.append(v)
            else:
                src_list.append(v); tgt_list.append(u)'''

new_ba = '''        # Barabasi-Albert scale-free graph: naturally power-law degree
        # distribution, creating hub neurons essential for self-organized criticality.
        m = max(2, int(N * p_connect * 0.5))
        G = nx.barabasi_albert_graph(N, m)
        src_list, tgt_list = [], []
        for u, v in G.edges():
            if random.random() < 0.5:
                src_list.append(u); tgt_list.append(v)
            else:
                src_list.append(v); tgt_list.append(u)'''

c = c.replace(old_ws, new_ba)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('L6: Switched to Barabasi-Albert scale-free initialization')
