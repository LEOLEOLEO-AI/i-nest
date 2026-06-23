# Multi-Scale Renormalization Group for Complex Networks
# =====================================================
# Target: D:\iNEST\Write\Code\MNoB\memai\multiscale.py

from typing import List, Dict, Optional, Set, Tuple
import math, random
from collections import deque

class RenormalizationGroup:
    """Real-space RG for complex networks.
    Implements box-covering and degree-based coarse-graining
    to identify RG fixed points and mesoscopic optimum."""
    def __init__(self, adj: List[List[int]], seed: int = 42):
        self.adj = [set(nbrs) for nbrs in adj]
        self.n = len(adj)
        self.rng = random.Random(seed)
        self.rg_history: List[Dict] = []

    def degree_coarse_grain(self, keep_fraction: float = 0.5) -> List[List[int]]:
        n = self.n; degrees = [(len(self.adj[i]), i) for i in range(n)]
        degrees.sort(reverse=True)
        keep_count = max(1, int(n * keep_fraction))
        keep_nodes = set(d[1] for d in degrees[:keep_count])
        merge_nodes = list(range(n))
        kept_list = list(keep_nodes)
        for i in range(n):
            if i in keep_nodes: merge_nodes[i] = i
            else:
                min_dist, best = float("inf"), i
                for k in kept_list:
                    d = self._bfs_dist(i, k)
                    if d < min_dist: min_dist, best = d, k
                merge_nodes[i] = best
        coarse_adj = [set() for _ in range(keep_count)]
        kept_idx = {node: idx for idx, node in enumerate(kept_list)}
        for u in keep_nodes:
            for v in self.adj[u]:
                vt = merge_nodes[v]
                if vt in keep_nodes and vt != u:
                    coarse_adj[kept_idx[u]].add(kept_idx[vt])
        return [sorted(list(s)) for s in coarse_adj]

    def _bfs_dist(self, src: int, dst: int) -> int:
        if src == dst: return 0
        visited = [-1] * self.n; q = deque([src]); visited[src] = 0
        while q:
            u = q.popleft()
            for v in self.adj[u]:
                if visited[v] == -1:
                    visited[v] = visited[u] + 1
                    if v == dst: return visited[v]
                    q.append(v)
        return self.n

    def rg_flow(self, max_steps: int = 5, keep_fraction: float = 0.5) -> List[Dict]:
        current = [sorted(list(s)) for s in self.adj]
        flow = []
        for step in range(max_steps):
            N = len(current)
            if N < 4: break
            C = self._clustering(current)
            L = self._avg_path(current)
            avg_k = sum(len(s) for s in current) / max(N, 1)
            sigma = self._sigma(C, L, N, max(4, int(avg_k)))
            flow.append({"step": step, "N": N, "avg_degree": round(avg_k, 1),
                        "C": round(C, 4), "L": round(L, 2), "sigma": round(sigma, 2)})
            current = self.degree_coarse_grain(keep_fraction)
        self.rg_history = flow
        return flow

    def _clustering(self, adj: List[List[int]]) -> float:
        n = len(adj); total, cnt = 0.0, 0
        for i in range(n):
            nbrs = set(adj[i]); k = len(nbrs)
            if k < 2: continue
            tri = 0
            nbrs_list = list(nbrs)
            for a in range(k):
                for b in range(a + 1, k):
                    if nbrs_list[b] in adj[nbrs_list[a]] or nbrs_list[a] in adj[nbrs_list[b]]:
                        tri += 1
            total += (2.0 * tri) / (k * (k - 1)); cnt += 1
        return total / max(cnt, 1)

    def _avg_path(self, adj: List[List[int]]) -> float:
        n = len(adj); total, reachable = 0, 0
        for src in range(min(n, 100)):
            dist = [-1] * n; q = deque([src]); dist[src] = 0
            while q:
                u = q.popleft()
                for v in adj[u]:
                    if dist[v] == -1: dist[v] = dist[u] + 1; q.append(v)
            for v in range(n):
                if v != src and dist[v] > 0: total += dist[v]; reachable += 1
        return total / max(reachable, 1)

    def _sigma(self, C: float, L: float, n: int, k: int) -> float:
        rng = random.Random(42)
        p = k / max(n - 1, 1)
        adj_r = [set() for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if rng.random() < p: adj_r[i].add(j); adj_r[j].add(i)
        adj_rl = [sorted(list(s)) for s in adj_r]
        Cr = self._clustering(adj_rl); Lr = self._avg_path(adj_rl)
        if Cr == 0 or Lr == 0: return 0
        return (C / Cr) / (L / Lr)

    def find_fixed_point(self, flow: List[Dict], tol: float = 0.05) -> Optional[int]:
        for i in range(1, len(flow)):
            prev, curr = flow[i - 1]["sigma"], flow[i]["sigma"]
            if prev > 0 and abs(curr - prev) / prev < tol: return i
        return None

    def find_peak_complexity(self, flow: List[Dict]) -> int:
        best_step, best_val = 0, 0.0
        for i, s in enumerate(flow):
            v = s["C"] * s["sigma"] / max(s["N"], 1)
            if v > best_val: best_val, best_step = v, i
        return best_step

    def cross_scale_error(self, orig: List[List[int]], coarse: List[List[int]]) -> float:
        Co = self._clustering(orig); Cc = self._clustering(coarse)
        Lo = max(self._avg_path(orig), 0.001); Lc = max(self._avg_path(coarse), 0.001)
        c_err = abs(Co - Cc); l_err = abs(Lo - Lc) / max(Lo, Lc)
        return 0.5 * c_err + 0.5 * l_err

    def fractal_dimension(self, box_sizes: List[int] = None) -> float:
        if box_sizes is None: box_sizes = list(range(2, min(10, self.n // 4) + 1))
        if len(box_sizes) < 3: return 0.0
        log_l, log_Nb = [], []
        distances = self._all_dists()
        for lb in box_sizes:
            if lb < 2 or lb >= self.n: continue
            uncovered = set(range(self.n)); boxes = []
            while uncovered:
                best_seed, best_cnt = None, -1
                for node in uncovered:
                    cnt = sum(1 for v in uncovered if v != node and distances[node][v] <= lb)
                    if cnt > best_cnt: best_cnt, best_seed = cnt, node
                if best_seed is None: break
                box = {best_seed}
                for v in list(uncovered):
                    if v != best_seed and distances[best_seed][v] <= lb:
                        box.add(v)
                boxes.append(box); uncovered -= box
            Nb = len(boxes)
            if Nb > 0: log_l.append(math.log(lb)); log_Nb.append(math.log(Nb))
        if len(log_l) < 3: return 0.0
        n = len(log_l); sx = sum(log_l); sy = sum(log_Nb)
        sxy = sum(x * y for x, y in zip(log_l, log_Nb)); sxx = sum(x * x for x in log_l)
        denom = n * sxx - sx * sx
        if denom == 0: return 0.0
        return max(0.0, -(n * sxy - sx * sy) / denom)

    def _all_dists(self) -> List[List[int]]:
        n = self.n; dist = [[-1] * n for _ in range(n)]
        for src in range(n):
            q = deque([src]); dist[src][src] = 0
            while q:
                u = q.popleft()
                for v in self.adj[u]:
                    if dist[src][v] == -1: dist[src][v] = dist[src][u] + 1; q.append(v)
        return dist

    def box_cover(self, box_size: int) -> List[List[int]]:
        distances = self._all_dists(); uncovered = set(range(self.n)); boxes = []
        while uncovered:
            best_seed, best_cnt = None, -1
            for node in uncovered:
                cnt = sum(1 for v in uncovered if v != node and distances[node][v] <= box_size)
                if cnt > best_cnt: best_cnt, best_seed = cnt, node
            if best_seed is None: break
            box = {best_seed}
            for v in list(uncovered):
                if v != best_seed and distances[best_seed][v] <= box_size:
                    box.add(v)
            boxes.append(box); uncovered -= box
        coarse = [set() for _ in range(len(boxes))]
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                connected = False
                for u in boxes[i]:
                    for v in self.adj[u]:
                        if v in boxes[j]: connected = True; break
                    if connected: break
                if connected: coarse[i].add(j); coarse[j].add(i)
        return [sorted(list(s)) for s in coarse]


def rg_flow_to_cst(flow: List[Dict]) -> Dict[str, float]:
    if not flow: return {"S_c": 0, "T_c": 0, "Gamma_st": 0, "CST": 0}
    best = max(flow, key=lambda s: s["C"] * s["sigma"])
    S_c = best["C"] * best["sigma"]
    sigmas = [s["sigma"] for s in flow]
    T_c = sum(abs(sigmas[i] - sigmas[i - 1]) for i in range(1, len(sigmas))) / max(len(sigmas) - 1, 1)
    mean_s = sum(sigmas) / len(sigmas)
    var_s = sum((s - mean_s) ** 2 for s in sigmas) / len(sigmas)
    Gamma_st = 1.0 / (1.0 + var_s)
    CST = S_c * (1.0 + T_c) * (1.0 + Gamma_st)
    return {"S_c": round(S_c, 4), "T_c": round(T_c, 4), "Gamma_st": round(Gamma_st, 4), "CST": round(CST, 4)}


if __name__ == "__main__":
    rng = random.Random(42)
    n, k, p = 128, 16, 0.1
    adj = [set() for _ in range(n)]
    for i in range(n):
        for j_off in range(1, k // 2 + 1):
            nb = (i + j_off) % n; adj[i].add(nb); adj[nb].add(i)
    for i in range(n):
        nbrs = sorted(adj[i])
        for j_off in range(1, k // 2 + 1):
            nb = (i + j_off) % n
            if nb in adj[i] and rng.random() < p:
                adj[i].discard(nb); adj[nb].discard(i)
                cands = [v for v in range(n) if v != i and v not in adj[i]]
                if cands: new = rng.choice(cands); adj[i].add(new); adj[new].add(i)
    adj_list = [sorted(list(s)) for s in adj]
    rg = RenormalizationGroup(adj_list)
    flow = rg.rg_flow(5, 0.5)
    print("RG Flow:")
    for s in flow: print(f"  step={s['step']}: N={s['N']:>3} C={s['C']:.4f} L={s['L']:.2f} sigma={s['sigma']:.2f}")
    fp = rg.find_fixed_point(flow)
    print(f"Fixed point: step={fp}")
    pk = rg.find_peak_complexity(flow)
    print(f"Peak complexity: step={pk}")
    cst = rg_flow_to_cst(flow)
    print(f"CST: S_c={cst['S_c']:.4f} T_c={cst['T_c']:.4f} Gamma_st={cst['Gamma_st']:.4f} CST={cst['CST']:.4f}")
    print("Done.")
