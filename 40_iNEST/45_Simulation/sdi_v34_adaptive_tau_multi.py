"""
SDI V34 - Adaptive Tau Multi-Brain Cooperation (v33 tau + v31 multi-brain) & Collective Intelligence Simulation
======================================================================
Based on V31 + V33 adaptive tau mechanism single-brain multi-region architecture.
Each brain has vis/chem/assoc/motor regions.
Brains interact via shared environment and inter-brain SDI bonds.

Experiments:
  2-1: Dual-brain resource competition (with adaptive tau)
  V34 adds: adaptive tau vs fixed tau comparison
  2-2: Dual-brain signal cooperation  
  2-3: N-brain mixed population (N=3,5,10)

Principles: STDP + FEP + BCM drive self-organization.
Inter-brain bonds follow the same physical rules.
"""

import numpy as np
import json, time, os as _os, warnings, random
from collections import defaultdict
warnings.filterwarnings('ignore')
import networkx as nx

# ============================================================
# Global Constants
# ============================================================
TAU_STDP = 20
ETA_LTP = 0.010
ETA_LTD = 0.008
Ea_S, Ea_L = 0.15, 0.85
THETA_LTP_BASE = 16  # Lower threshold for young network E-L consolidation
THETA_LTD = 8
T_DECAY = 25000
T_ABS = 3
T_REL = 8
REL_SCALE = 0.3
SCALING_THR = 0.35
SCALING_RATE = 0.12
SCALING_INT = 15
GLIA_THR = 0.45
GLIA_RATE = 0.25
GLIA_INT = 50
NOISE_LEVEL = 0.02
I_SPONT = 0.40          # Spontaneous depolarizing current applied to ALL neurons (leak + background)
# I_SPONT applied to ALL neurons each step (universal leak/background drive)
RESOURCE_DECAY = 0.995
SIGNAL_DECAY = 0.9
IB_ETA_LTP = 0.008
IB_ETA_LTD = 0.006
IB_Ea_S = 0.20
IB_Ea_L = 0.90
IB_THETA_LTP_BASE = 30



# ============================================================
# V34: Adaptive Tau Configuration (from V33)
# ============================================================
class TauConfig:
    def __init__(self, enabled=True, tau_base=20.0, alpha_tau=1.0,
                 tau_min=5.0, tau_max=50.0):
        self.enabled = enabled
        self.tau_base = tau_base
        self.alpha_tau = alpha_tau
        self.tau_min = tau_min
        self.tau_max = tau_max

# ============================================================
# BrainRegion: Single functional brain area
# ============================================================
class BrainRegion:
    """Self-organizing network for one functional brain region (vis/chem/assoc/motor)."""

    def __init__(self, name, N, p_connect=0.08, tau_cfg=None):
        self.name = name
        self.N = N
        self.tau_cfg = tau_cfg or TauConfig()
        k = max(2, int(N * p_connect))
        G = nx.watts_strogatz_graph(N, k, 0.3)
        edges = list(G.edges())
        
        # Directed: each edge gets a random direction — creates inherent
        # information flow asymmetry essential for STDP differentiation.
        # (Biological basis: axon→dendrite unidirectionality)
        src_list, tgt_list = [], []
        for u, v in edges:
            if random.random() < 0.5:
                src_list.append(u); tgt_list.append(v)
            else:
                src_list.append(v); tgt_list.append(u)
        self.src = np.array(src_list, np.int32)
        self.tgt = np.array(tgt_list, np.int32)
        self.n_bonds = len(self.src)
        self.weight = np.random.uniform(0.1, 0.5, self.n_bonds).astype(np.float64)
        self.btype = np.zeros(self.n_bonds, dtype=np.int8)
        self.Ea = np.full(self.n_bonds, Ea_S, dtype=np.float64)
        
        self.V = np.zeros(N, dtype=np.float64)
        self.spike = np.zeros(N, bool)
        max_tau = int(self.tau_cfg.tau_max * 2)
        self.spike_history = np.zeros((N, max_tau), dtype=np.float64)
        self.hist_ptr = 0
        self.last_spike = np.full(N, -999, dtype=np.int32)
        self.spike_count = np.zeros(N, np.int32)
        self.n_ltp = np.zeros(self.n_bonds, dtype=np.int32)
        self.n_ltd = np.zeros(self.n_bonds, dtype=np.int32)
        self.t_last_update = np.zeros(self.n_bonds, dtype=np.int32)
        self.F_local = np.full(N, 0.1, dtype=np.float64)
        self.F_history = np.full((N, 20), 0.1, np.float64)
        self.F_ptr = 0
        self.basin_count = np.zeros(N, np.int32)
        self.theta_bcm = np.full(N, 4.0, dtype=np.float64)  # Lower initial threshold for young network
        self.BCM_ETA = 0.25
        self.R = np.ones(self.n_bonds, dtype=np.float64)
        self.scaling_events = 0
        self.glia_events = 0
        # V34: Adaptive tau state
        self.tau_per_neuron = np.full(N, self.tau_cfg.tau_base, dtype=np.float64)
        self.surprise_per_neuron = np.zeros(N, dtype=np.float64)
        self.tau_history = []
        self.sigma = 1.0; self.alpha = 1.0; self.C = 0.0; self.L = 0.0
        self.el_ratio = 0.0; self.k_avg = 0.0; self.F_mean = 0.0

    def step(self, step_num, external_input=None):
        N = self.N
        in_ref = (step_num - self.last_spike) < T_ABS
        in_rel = (step_num - self.last_spike) < (T_ABS + T_REL)
        self.V *= 0.9
        
        # Spontaneous background drive to ALL neurons (leak channels + tonic
        # background synaptic bombardment; Destexhe et al. 2003).
        # Every neuron receives baseline depolarization — this is the physical
        # basis for resting membrane potential fluctuations.
        self.V += I_SPONT
        
        # Apply external sensory input BEFORE spike detection (causal ordering)
        if external_input is not None:
            self.V += external_input
        
        active = self.spike.copy()
        for b in range(self.n_bonds):
            if active[self.src[b]] and not in_ref[self.tgt[b]]:
                w = self.weight[b] * self.R[b]
                if self.btype[b] == 2: w *= 1.5
                rf = REL_SCALE if in_rel[self.tgt[b]] else 1.0
                self.V[self.tgt[b]] += w * rf
        
        # Lateral inhibition (cortical winner-take-all): only top-k
        # neurons fire, creating sparse coding essential for STDP differentiation.
        # k dynamically scales with network size and activity level.
        threshold = self.theta_bcm
        supra = self.V > threshold
        supra &= ~in_ref
        k = max(3, int(N * 0.15))  # Top 15% or at least 3 neurons
        if supra.sum() > k:
            # Sort by V, keep only top-k
            supra_idx = np.where(supra)[0]
            top_k = supra_idx[np.argsort(self.V[supra_idx])[-k:]]
            new_spikes = np.zeros(N, dtype=bool)
            new_spikes[top_k] = True
        else:
            new_spikes = supra.copy()
        self.spike = new_spikes
        self.last_spike[new_spikes] = step_num
        self.spike_count[new_spikes] += 1
        
        if step_num % 10 == 0 and step_num > 0: self._stdp_update(step_num)
        if step_num % 20 == 0:
            self._fep_update(step_num)
            self._update_tau()  # V34: adaptive tau update
        if step_num % 50 == 0 and step_num > 0: self._bcm_update(step_num)
        if step_num % SCALING_INT == 0 and step_num > 0: self._scaling_check()
        if step_num % GLIA_INT == 0 and step_num > 0: self._glia_check()
        
        if step_num % 100 == 0:
            el_mask = (self.btype == 2) & (self.t_last_update < step_num - T_DECAY)
            self.btype[el_mask] = 0; self.Ea[el_mask] = Ea_S; self.weight[el_mask] *= 0.5
        
        max_hist = self.spike_history.shape[1]
        self.spike_history[:, self.hist_ptr % max_hist] = self.spike.astype(np.float64)
        self.hist_ptr += 1
        
        if step_num % 50 == 0 and step_num > 0:
            self._compute_metrics()
            self.tau_history.append({
                "step": step_num,
                "tau_mean": float(self.tau_per_neuron.mean()),
                "tau_std": float(self.tau_per_neuron.std()),
                "surprise_mean": float(self.surprise_per_neuron.mean())
            })


    # V34: Adaptive tau methods
    def _compute_surprise(self):
        fm = self.F_history.mean(axis=1)
        fs = self.F_history.std(axis=1) + 1e-8
        self.surprise_per_neuron = np.abs(self.F_local - fm) / fs

    def _update_tau(self):
        if not self.tau_cfg.enabled:
            self.tau_per_neuron.fill(self.tau_cfg.tau_base)
            return
        self._compute_surprise()
        s = np.clip(self.surprise_per_neuron, 0, 10)
        self.tau_per_neuron = self.tau_cfg.tau_base / (1.0 + self.tau_cfg.alpha_tau * s)
        self.tau_per_neuron = np.clip(self.tau_per_neuron,
                                       self.tau_cfg.tau_min,
                                       self.tau_cfg.tau_max)

    def _get_tau_for_bond(self, b):
        if self.tau_cfg.enabled:
            return int(self.tau_per_neuron[self.src[b]])
        return int(self.tau_cfg.tau_base)

    def _stdp_update(self, step):
        max_hist = self.spike_history.shape[1]
        for b in range(self.n_bonds):
            if self.btype[b] == 4: continue
            tau_b = self._get_tau_for_bond(b)
            window = min(tau_b, max_hist // 2)
            ptr = self.hist_ptr % max_hist
            if ptr >= window:
                pre = self.spike_history[self.src[b], ptr-window:ptr]
                post = self.spike_history[self.tgt[b], ptr-window:ptr]
            else:
                pre = np.concatenate([self.spike_history[self.src[b], ptr-window:],
                                       self.spike_history[self.src[b], :ptr]])
                post = np.concatenate([self.spike_history[self.tgt[b], ptr-window:],
                                        self.spike_history[self.tgt[b], :ptr]])
            pre_t = np.where(pre > 0)[0]
            post_t = np.where(post > 0)[0]
            if len(pre_t) == 0 or len(post_t) == 0: continue
            half = window // 2
            dt = post_t[:, None] - pre_t[None, :]
            dt_s = dt - half
            ltp = np.sum((dt_s > 0) & (dt_s <= half))
            ltd = np.sum((dt_s < 0) & (dt_s >= -half))
            self.n_ltp[b] += ltp; self.n_ltd[b] += ltd
            ratio = (self.n_ltp[b] + 1) / (self.n_ltd[b] + 1)
            if ratio > THETA_LTP_BASE / THETA_LTD and self.btype[b] == 0:
                self.btype[b] = 2; self.Ea[b] = Ea_L; self.t_last_update[b] = step
            elif ratio < 1.0 and self.btype[b] == 2:
                self.btype[b] = 0; self.Ea[b] = Ea_S

    def _fep_update(self, step):
        pred = self.V / (np.abs(self.V).max() + 1e-8)
        act = self.spike.astype(np.float64)
        self.F_local = (pred - act) ** 2 + 0.05
        self.F_history[:, self.F_ptr] = self.F_local
        self.F_ptr = (self.F_ptr + 1) % 20
        if step > 20:
            fm = self.F_history.mean(axis=1); fs = self.F_history.std(axis=1) + 1e-8
            in_b = np.abs(self.F_local - fm) < fs
            self.basin_count[in_b] += 1; self.basin_count[~in_b] = 0

    def _bcm_update(self, step):
        h = self.spike_count / (step + 1)
        s = np.abs(self.F_local - self.F_history.mean(axis=1)) / (self.F_history.std(axis=1) + 1e-8)
        eta = self.BCM_ETA * (1 + 0.8 * np.tanh(s))
        self.theta_bcm += eta * h**2 * (h - self.theta_bcm)
        # Homeostatic plasticity: silent neurons lower their threshold (Turrigiano 1998)
        silent = h < 0.005
        self.theta_bcm[silent] *= 0.95
        self.theta_bcm = np.clip(self.theta_bcm, 2.0, 15.0)

    def _scaling_check(self):
        out_w = np.bincount(self.src, weights=np.abs(self.weight), minlength=self.N)
        over = out_w > SCALING_THR
        if over.any():
            for i in np.where(over)[0]:
                mask = (self.src == i) & (self.btype != 4)
                if mask.any(): self.weight[mask] *= (1 - SCALING_RATE)
            self.scaling_events += int(over.sum())

    def _glia_check(self):
        el = self.btype == 2
        if el.any() and el.sum() / self.n_bonds > GLIA_THR:
            idx = np.where(el)[0]
            hi = np.argsort(self.weight[idx])[-max(1, int(len(idx) * GLIA_RATE)):]
            dg = idx[hi]; self.btype[dg] = 0; self.Ea[dg] = Ea_S
            self.weight[dg] *= 0.5; self.glia_events += len(dg)

    def _compute_metrics(self):
        try:
            G = nx.DiGraph()
            for b in range(min(self.n_bonds, 5000)):
                G.add_edge(int(self.src[b]), int(self.tgt[b]))
            if G.number_of_edges() == 0: return
            C = nx.average_clustering(G.to_undirected())
            try: L = nx.average_shortest_path_length(G.to_undirected())
            except: L = float(self.N)
            n = self.N; p = max(G.number_of_edges()/(n*(n-1)), 0.001) if n>1 else 0.001
            C_rand = max(p, 0.001); L_rand = np.log(n)/np.log(max(n*p, 1.1))
            self.sigma = (C/C_rand)/(L/L_rand) if L_rand>0 else 1.0
            self.C = C; self.L = L
            deg = np.array([d for _,d in G.degree()])
            if len(deg[deg>0])>3:
                dp=deg[deg>0]; h,bins=np.histogram(np.log(dp),bins=min(15,len(dp)//2))
                bc=(bins[:-1]+bins[1:])/2; pm=h>0
                if pm.sum()>1: self.alpha=-np.polyfit(bc[pm],np.log(h[pm]+1),1)[0]
            self.el_ratio=(self.btype==2).sum()/self.n_bonds
            self.k_avg=deg.mean(); self.F_mean=float(self.F_local.mean())
        except: pass

    def get_state(self):
        return dict(sigma=float(self.sigma), alpha=float(self.alpha),
            C=float(self.C), L=float(self.L), el_ratio=float(self.el_ratio),
            k_avg=float(self.k_avg), F_mean=float(self.F_mean),
            scaling_events=int(self.scaling_events), glia_events=int(self.glia_events),
            active=int(self.spike.sum()), mean_V=float(self.V.mean()))



# ============================================================
# Brain: Complete brain instance (4 functional regions)
# ============================================================
class Brain:
    """V34: Complete brain with adaptive tau mechanism."""

    def __init__(self, brain_id, region_sizes=None, tau_cfg=None):
        self.tau_cfg = tau_cfg or TauConfig()
        self.brain_id = brain_id
        sizes = region_sizes or {'vis': 100, 'chem': 100, 'assoc': 150, 'motor': 100}
        self.regions = {}
        self.region_map = {}
        offset = 0
        for rname, rsize in sizes.items():
            self.regions[rname] = BrainRegion(rname, rsize, 0.08, self.tau_cfg)
            self.region_map[rname] = (offset, offset + rsize)
            offset += rsize
        self.total_N = offset
        self.cross_bonds = []
        self._init_cross_region_bonds()

    def _init_cross_region_bonds(self):
        for src, tgt, density in [('vis','assoc',0.05),('chem','assoc',0.05),('assoc','motor',0.08)]:
            sr, tr = self.regions[src], self.regions[tgt]
            n_conn = max(1, int(min(sr.N, tr.N) * density))
            for _ in range(n_conn):
                self.cross_bonds.append(dict(
                    src_region=src, src_idx=random.randint(0, sr.N-1),
                    tgt_region=tgt, tgt_idx=random.randint(0, tr.N-1),
                    weight=random.uniform(0.05, 0.3), btype=0))

    def step(self, step_num, external_inputs=None):
        inputs = external_inputs or {}
        for rname, region in self.regions.items():
            ext_in = np.zeros(region.N)
            if rname in inputs: ext_in += inputs[rname]
            for bond in self.cross_bonds:
                if bond['tgt_region'] == rname and bond['btype'] >= 0:
                    src_r = self.regions[bond['src_region']]
                    if src_r.spike[bond['src_idx']]:
                        ext_in[bond['tgt_idx']] += bond['weight']
            region.step(step_num, ext_in)

    def get_state(self):
        rs = {rn: r.get_state() for rn, r in self.regions.items()}
        return dict(brain_id=self.brain_id, regions=rs,
            total_active=int(sum(r.spike.sum() for r in self.regions.values())),
            mean_sigma=float(np.mean([s['sigma'] for s in rs.values()])),
            mean_el=float(np.mean([s['el_ratio'] for s in rs.values()])))

    def get_motor_output(self):
        motor = self.regions.get('motor')
        if motor is None:
            motor = list(self.regions.values())[-1]
        return motor.spike.copy(), motor.V.copy()


# ============================================================
# SharedEnvironment: Multi-brain shared physical environment
# ============================================================
class SharedEnvironment:
    """Resources, signals, and physics shared by all brains."""

    def __init__(self, width=100.0, height=100.0):
        self.width = width; self.height = height
        self.resources = []
        self.signals = []
        self.global_time = 0

    def add_resource(self, rtype, x=None, y=None, intensity=1.0):
        if x is None: x = random.uniform(10, self.width-10)
        if y is None: y = random.uniform(10, self.height-10)
        self.resources.append(dict(type=rtype, x=x, y=y, intensity=intensity))

    def add_signal(self, source_brain, target_brain, strength=1.0):
        self.signals.append(dict(source=source_brain, target=target_brain,
                                 strength=strength, decay=SIGNAL_DECAY))

    def step(self):
        self.global_time += 1
        for r in self.resources: r['intensity'] *= RESOURCE_DECAY
        self.resources = [r for r in self.resources if r['intensity'] > 0.01]
        for s in self.signals: s['strength'] *= s['decay']
        self.signals = [s for s in self.signals if s['strength'] > 0.01]

    def sense_for_brain(self, brain_pos, sense_radius=30.0):
        sensed = dict(light=0.0, chemical=0.0, signals=[])
        for r in self.resources:
            dist = np.sqrt((brain_pos[0]-r['x'])**2 + (brain_pos[1]-r['y'])**2)
            if dist < sense_radius:
                strength = r['intensity'] * (1 - dist/sense_radius)
                sensed[r['type']] = max(sensed.get(r['type'], 0), strength)
        for s in self.signals: sensed['signals'].append(s)
        return sensed


# ============================================================
# InterBrainBond: Connections between brains
# ============================================================
class InterBrainBond:
    """Manages brain-to-brain SDI bond connections."""

    def __init__(self):
        self.bonds = []

    def create_bond(self, from_brain, to_brain, from_region, to_region,
                    from_idx, to_idx, weight=0.1):
        self.bonds.append(dict(
            from_brain=from_brain, to_brain=to_brain,
            from_region=from_region, to_region=to_region,
            from_idx=from_idx, to_idx=to_idx,
            weight=weight, btype=0, n_ltp=0, n_ltd=0, Ea=IB_Ea_S,
            spike_hist_from=np.zeros(TAU_STDP),
            spike_hist_to=np.zeros(TAU_STDP), hist_ptr=0))

    def random_init(self, brain_a, brain_b, density=0.02):
        ma = brain_a.regions.get('motor', list(brain_a.regions.values())[-1])
        mb = brain_b.regions.get('motor', list(brain_b.regions.values())[-1])
        aa = brain_a.regions.get('assoc', list(brain_a.regions.values())[0])
        ab = brain_b.regions.get('assoc', list(brain_b.regions.values())[0])
        nab = max(1, int(min(ma.N, ab.N) * density))
        nba = max(1, int(min(mb.N, aa.N) * density))
        for _ in range(nab):
            self.create_bond(brain_a.brain_id, brain_b.brain_id,
                           'motor', 'assoc',
                           random.randint(0, ma.N-1), random.randint(0, ab.N-1))
        for _ in range(nba):
            self.create_bond(brain_b.brain_id, brain_a.brain_id,
                           'motor', 'assoc',
                           random.randint(0, mb.N-1), random.randint(0, aa.N-1))

    def step(self, brains, step_num):
        self._propagate(brains)
        if step_num % 10 == 0 and step_num > 0:
            self._stdp_update(step_num)

    def _propagate(self, brains):
        for bond in self.bonds:
            fb = brains.get(bond['from_brain'])
            tb = brains.get(bond['to_brain'])
            if fb is None or tb is None: continue
            fr = fb.regions.get(bond['from_region'])
            tr = tb.regions.get(bond['to_region'])
            if fr is None or tr is None: continue
            fi, ti = bond['from_idx'], bond['to_idx']
            if fi >= fr.N or ti >= tr.N: continue
            sv = 1.0 if fr.spike[fi] else 0.0
            bond['spike_hist_from'][bond['hist_ptr']] = sv
            bond['spike_hist_to'][bond['hist_ptr']] = 1.0 if tr.spike[ti] else 0.0
            bond['hist_ptr'] = (bond['hist_ptr'] + 1) % TAU_STDP
            if sv > 0 and bond['btype'] >= 0:
                w = bond['weight'] * (1.5 if bond['btype'] == 2 else 1.0)
                tr.V[ti] += w * 0.5


    # V34: Adaptive tau methods
    def _compute_surprise(self):
        fm = self.F_history.mean(axis=1)
        fs = self.F_history.std(axis=1) + 1e-8
        self.surprise_per_neuron = np.abs(self.F_local - fm) / fs

    def _update_tau(self):
        if not self.tau_cfg.enabled:
            self.tau_per_neuron.fill(self.tau_cfg.tau_base)
            return
        self._compute_surprise()
        s = np.clip(self.surprise_per_neuron, 0, 10)
        self.tau_per_neuron = self.tau_cfg.tau_base / (1.0 + self.tau_cfg.alpha_tau * s)
        self.tau_per_neuron = np.clip(self.tau_per_neuron,
                                       self.tau_cfg.tau_min,
                                       self.tau_cfg.tau_max)

    def _get_tau_for_bond(self, b):
        if self.tau_cfg.enabled:
            return int(self.tau_per_neuron[self.src[b]])
        return int(self.tau_cfg.tau_base)

    def _stdp_update(self, step):
        for bond in self.bonds:
            pre, post = bond['spike_hist_from'], bond['spike_hist_to']
            pt_pre = np.where(pre > 0)[0]; pt_post = np.where(post > 0)[0]
            if len(pt_pre) == 0 or len(pt_post) == 0: continue
            dt = pt_post[:, None] - pt_pre[None, :]
            ltp = np.sum((dt > 0) & (dt <= TAU_STDP))
            ltd = np.sum((dt < 0) & (dt >= -TAU_STDP))
            bond['n_ltp'] += ltp; bond['n_ltd'] += ltd
            ratio = (bond['n_ltp'] + 1) / (bond['n_ltd'] + 1)
            if ratio > IB_THETA_LTP_BASE / THETA_LTD and bond['btype'] == 0:
                bond['btype'] = 2; bond['Ea'] = IB_Ea_L
            elif ratio < 1.0 and bond['btype'] == 2:
                bond['btype'] = 0; bond['Ea'] = IB_Ea_S

    def get_stats(self):
        n_tot = len(self.bonds)
        n_lock = sum(1 for b in self.bonds if b['btype'] == 2)
        return dict(n_total=n_tot, n_locked=n_lock,
                    lock_ratio=n_lock/n_tot if n_tot > 0 else 0)


# ============================================================
# MultiBrainSimulation: Orchestrator for multi-brain experiments
# ============================================================
class MultiBrainSimulation:
    """Unified framework for multi-brain competition/cooperation/mixed experiments."""

    def __init__(self, n_brains=2, region_sizes=None, env_width=100.0, env_height=100.0, tau_cfg=None):
        self.brains = {}
        self.brain_positions = {}
        self.tau_cfg = tau_cfg or TauConfig()
        for i in range(n_brains):
            bid = 'brain_' + str(i)
            self.brains[bid] = Brain(bid, region_sizes, self.tau_cfg)
            self.brain_positions[bid] = [random.uniform(20, env_width-20),
                                          random.uniform(20, env_height-20)]
        self.env = SharedEnvironment(env_width, env_height)
        self.inter_bonds = InterBrainBond()
        self.n_brains = n_brains
        self.history = []

    def run_exp21_competition(self, n_steps=500):
        """Experiment 2-1: Dual-brain resource competition."""
        assert self.n_brains >= 2
        print("\n" + "="*60)
        print("Experiment 2-1: Dual-brain Resource Competition")
        print("="*60)

        self.env.add_resource('light', 80, 20, 1.5)
        self.env.add_resource('chemical', 20, 80, 1.5)
        self.env.add_resource('light', 50, 50, 1.0)

        bl = list(self.brains.values())
        self.inter_bonds.random_init(bl[0], bl[1], 0.02)
        self.brain_positions = {'brain_0': [30.0, 50.0], 'brain_1': [70.0, 50.0]}

        captures = {'brain_0': {'light': 0, 'chemical': 0},
                    'brain_1': {'light': 0, 'chemical': 0}}

        for step in range(n_steps):
            self.env.step()
            for bid, brain in self.brains.items():
                pos = self.brain_positions[bid]
                sensed = self.env.sense_for_brain(pos)
                ext = {}
                if 'vis' in brain.regions:
                    ext['vis'] = np.random.randn(brain.regions['vis'].N) * NOISE_LEVEL + sensed['light'] * 1.5
                if 'chem' in brain.regions:
                    ext['chem'] = np.random.randn(brain.regions['chem'].N) * NOISE_LEVEL + sensed['chemical'] * 1.5
                brain.step(step, ext)

                ms, mV = brain.get_motor_output()
                half = mV.shape[0] // 2
                dx = (mV[:half].mean() - mV[half:].mean()) * 1.5 if half > 0 else 0
                dy = (mV.mean() - 0.05) * 1.0
                pos[0] = np.clip(pos[0] + dx + random.gauss(0, 0.15), 0, self.env.width)
                pos[1] = np.clip(pos[1] + dy + random.gauss(0, 0.15), 0, self.env.height)

                for r in self.env.resources[:]:
                    dist = np.sqrt((pos[0]-r['x'])**2 + (pos[1]-r['y'])**2)
                    if dist < 8.0 and r['intensity'] > 0.1:
                        captures[bid][r['type']] += 1
                        r['intensity'] *= 0.5

            self.inter_bonds.step(self.brains, step)

            if step % 80 == 0 and len(self.env.resources) < 2:
                self.env.add_resource('light', random.uniform(10, 90), random.uniform(10, 90), 1.2)
                self.env.add_resource('chemical', random.uniform(10, 90), random.uniform(10, 90), 1.2)

        print("\nResource captures:")
        for bid, cap in captures.items():
            print("  " + bid + ": light=" + str(cap['light']) + ", chemical=" + str(cap['chemical']))

        return dict(experiment='2-1_competition', n_steps=n_steps, captures=captures,
            final_positions={bid: [float(p) for p in pos] for bid, pos in self.brain_positions.items()},
            final_states={bid: brain.get_state() for bid, brain in self.brains.items()},
            inter_bonds=self.inter_bonds.get_stats())

    def run_exp22_cooperation(self, n_steps=500):
        """Experiment 2-2: Dual-brain signal cooperation."""
        assert self.n_brains >= 2
        print("\n" + "="*60)
        print("Experiment 2-2: Dual-brain Signal Cooperation")
        print("="*60)

        self.env.add_resource('light', 80, 50, 2.0)
        bl = list(self.brains.values())
        self.brain_positions = {'brain_0': [40.0, 50.0], 'brain_1': [60.0, 50.0]}
        light_src = (80.0, 50.0)

        # Phase 1: Brain A trains alone (200 steps)
        print("Phase 1: Brain A solo phototaxis training...")
        for step in range(400):
            self.env.step()
            ba = self.brains['brain_0']
            pa = self.brain_positions['brain_0']
            s = self.env.sense_for_brain(pa)
            ext = {}
            if 'vis' in ba.regions:
                ext['vis'] = np.random.randn(ba.regions['vis'].N)*NOISE_LEVEL + s['light']*1.5
            ba.step(step, ext)

        # Phase 2: Brain B baseline learning (no cooperation, 100 steps)
        print("Phase 2: Brain B solo baseline...")
        dist_no_coop = []
        bb = self.brains['brain_1']
        pb = self.brain_positions['brain_1']
        for step in range(100):
            self.env.step()
            s = self.env.sense_for_brain(pb)
            ext = {}
            if 'vis' in bb.regions:
                ext['vis'] = np.random.randn(bb.regions['vis'].N)*NOISE_LEVEL + s['light']*1.5
            bb.step(step+200, ext)
            msb, mVb = bb.get_motor_output()
            halfb = mVb.shape[0]//2
            dxb = (mVb[:halfb].mean()-mVb[halfb:].mean())*0.5 + s['light']*0.6 if halfb>0 else s['light']*0.6
            dyb = (mVb.mean()-0.05)*0.3 + s['light']*0.2
            pb[0]=np.clip(pb[0]+dxb+random.gauss(0,0.3),0,self.env.width)
            pb[1]=np.clip(pb[1]+dyb+random.gauss(0,0.3),0,self.env.height)
            dist_no_coop.append(float(np.sqrt((pb[0]-light_src[0])**2+(pb[1]-light_src[1])**2)))

        # Phase 3: Brain B with Brain A signal assistance (100 steps)
        print("Phase 3: Brain B with Brain A signal cooperation...")
        self.inter_bonds = InterBrainBond()
        self.inter_bonds.random_init(bl[0], bl[1], 0.15)
        dist_coop = []
        for step in range(100):
            self.env.step()
            ba = self.brains['brain_0']; pa = self.brain_positions['brain_0']
            s = self.env.sense_for_brain(pa)
            ext = {}
            if 'vis' in ba.regions: ext['vis'] = np.random.randn(ba.regions['vis'].N)*NOISE_LEVEL + s['light']*1.5
            ba.step(step+300, ext)
            bb = self.brains['brain_1']
            s = self.env.sense_for_brain(pb)
            ext = {}
            if 'vis' in bb.regions: ext['vis'] = np.random.randn(bb.regions['vis'].N)*NOISE_LEVEL + s['light']*1.5
            bb.step(step+300, ext)
            self.inter_bonds.step(self.brains, step+300)
            msb, mVb = bb.get_motor_output()
            halfb = mVb.shape[0]//2
            dxb = (mVb[:halfb].mean()-mVb[halfb:].mean())*0.5 + s['light']*0.6 if halfb>0 else s['light']*0.6
            dyb = (mVb.mean()-0.05)*0.3 + s['light']*0.2
            pb[0]=np.clip(pb[0]+dxb+random.gauss(0,0.3),0,self.env.width)
            pb[1]=np.clip(pb[1]+dyb+random.gauss(0,0.3),0,self.env.height)
            dist_coop.append(float(np.sqrt((pb[0]-light_src[0])**2+(pb[1]-light_src[1])**2)))

        avg_no = np.mean(dist_no_coop[-20:])
        avg_co = np.mean(dist_coop[-20:])
        speedup = avg_no / (avg_co + 1e-8)

        print("\nLearning speedup: " + str(round(speedup, 2)) + "x")
        print("  Baseline avg distance: " + str(round(avg_no, 2)))
        print("  Cooperation avg distance: " + str(round(avg_co, 2)))
        print("  Inter-brain lock ratio: " + str(round(self.inter_bonds.get_stats()['lock_ratio'], 3)))

        return dict(experiment='2-2_cooperation', n_steps=n_steps, speedup=float(speedup),
            avg_dist_no_coop=float(avg_no), avg_dist_coop=float(avg_co),
            dist_traj_no_coop=dist_no_coop, dist_traj_coop=dist_coop,
            inter_bonds=self.inter_bonds.get_stats(),
            final_states={bid: brain.get_state() for bid, brain in self.brains.items()})

    def run_exp23_mixed(self, n_brains_list=None, n_steps=500):
        """Experiment 2-3: N-brain mixed population."""
        n_list = n_brains_list or [3, 5, 10]
        results = {}
        for n in n_list:
            print("\n" + "="*60)
            print("Experiment 2-3: N=" + str(n) + " Mixed Population")
            print("="*60)

            sim = MultiBrainSimulation(n_brains=n)
            for _ in range(n):
                sim.env.add_resource('light', random.uniform(10, 90), random.uniform(10, 90), 1.0)
                sim.env.add_resource('chemical', random.uniform(10, 90), random.uniform(10, 90), 1.0)

            bids = list(sim.brains.keys())
            for i in range(n):
                for j in range(i+1, n):
                    sim.inter_bonds.random_init(sim.brains[bids[i]], sim.brains[bids[j]], 0.01)

            brain_captures = {bid: {'light': 0, 'chemical': 0} for bid in bids}
            all_sigmas = []; all_els = []

            for step in range(n_steps):
                sim.env.step()
                for bid, brain in sim.brains.items():
                    pos = sim.brain_positions[bid]
                    sensed = sim.env.sense_for_brain(pos)
                    ext = {}
                    if 'vis' in brain.regions:
                        ext['vis'] = np.random.randn(brain.regions['vis'].N) * NOISE_LEVEL + sensed['light'] * 1.2
                    if 'chem' in brain.regions:
                        ext['chem'] = np.random.randn(brain.regions['chem'].N) * NOISE_LEVEL + sensed['chemical'] * 1.2
                    brain.step(step, ext)

                    ms, mV = brain.get_motor_output()
                    half = mV.shape[0] // 2
                    dx = (mV[:half].mean() - mV[half:].mean()) * 1.5 if half > 0 else 0
                    dy = (mV.mean() - 0.05) * 1.0
                    pos[0] = np.clip(pos[0] + dx + random.gauss(0, 0.15), 0, sim.env.width)
                    pos[1] = np.clip(pos[1] + dy + random.gauss(0, 0.15), 0, sim.env.height)

                    for r in sim.env.resources[:]:
                        dist = np.sqrt((pos[0]-r['x'])**2 + (pos[1]-r['y'])**2)
                        if dist < 8.0 and r['intensity'] > 0.1:
                            brain_captures[bid][r['type']] += 1
                            r['intensity'] *= 0.5

                sim.inter_bonds.step(sim.brains, step)

                if step % 50 == 0 and len(sim.env.resources) < n:
                    for _ in range(2):
                        sim.env.add_resource('light', random.uniform(10, 90), random.uniform(10, 90), 1.0)
                        sim.env.add_resource('chemical', random.uniform(10, 90), random.uniform(10, 90), 1.0)

                if step % 30 == 0:
                    sigs = [brain.get_state()['mean_sigma'] for brain in sim.brains.values()]
                    els = [brain.get_state()['mean_el'] for brain in sim.brains.values()]
                    all_sigmas.append(float(np.mean(sigs))); all_els.append(float(np.mean(els)))

            # Collective metrics
            caps = list(brain_captures.values())
            lc = [c['light'] for c in caps]; cc = [c['chemical'] for c in caps]
            total_l = sum(lc) + 1e-8; total_c = sum(cc) + 1e-8
            profiles = [(l/total_l, c/total_c) for l, c in zip(lc, cc)]
            all_probs = [p[0] for p in profiles] + [p[1] for p in profiles]
            total = sum(all_probs)
            if total > 0:
                probs = [max(p/total, 1e-10) for p in all_probs]
                div_entropy = -sum(p*np.log(p) for p in probs)
            else:
                div_entropy = 0
            col_eff = sum(lc + cc) / n

            result = dict(n_brains=n, n_steps=n_steps,
                total_captures=dict(light=int(sum(lc)), chemical=int(sum(cc))),
                per_brain_captures=brain_captures,
                division_entropy=float(div_entropy),
                collective_efficiency=float(col_eff),
                mean_sigma_final=float(np.mean(all_sigmas[-3:])) if all_sigmas else 0,
                mean_el_final=float(np.mean(all_els[-3:])) if all_els else 0,
                inter_bonds=sim.inter_bonds.get_stats())

            results['N=' + str(n)] = result
            print("  N=" + str(n) + ": total_captures=" + str(result['total_captures']) +
                  ", efficiency=" + str(round(col_eff, 1)) + ", div_entropy=" + str(round(div_entropy, 2)))

        return results



# ============================================================
# Main: Run all V31 experiments
# ============================================================
if __name__ == '__main__':
    _os.makedirs('simulation/data/v31_results', exist_ok=True)
    all_results = {}

    print("="*60)
    print("SDI V34 - Adaptive Tau Multi-Brain Cooperation (v33 tau + v31 multi-brain) Experiments")
    print("="*60)
    t_start = time.time()

    # Experiment 2-1: Competition
    sim21 = MultiBrainSimulation(n_brains=2)
    r21 = sim21.run_exp21_competition(n_steps=800)
    all_results['exp21_competition'] = r21

    # Experiment 2-2: Cooperation
    sim22 = MultiBrainSimulation(n_brains=2)
    r22 = sim22.run_exp22_cooperation(n_steps=800)
    all_results['exp22_cooperation'] = r22

    # Experiment 2-3: Mixed population
    sim23 = MultiBrainSimulation(n_brains=5)
    r23 = sim23.run_exp23_mixed(n_brains_list=[3, 5, 10], n_steps=500)
    all_results['exp23_mixed'] = r23

    elapsed = time.time() - t_start

    # Clean results for JSON (remove large arrays)
    clean = {}
    for k, v in all_results.items():
        if k == 'exp23_mixed':
            clean[k] = {}
            for nk, nv in v.items():
                clean[k][nk] = {kk: vv for kk, vv in nv.items()
                               if kk not in ('per_brain_captures',)}
        else:
            clean[k] = {kk: vv for kk, vv in v.items()
                       if kk not in ('dist_traj_no_coop', 'dist_traj_coop')}

    out_path = 'simulation/data/v31_results/v31_multibrain_results.json'
    with open(out_path, 'w') as f:
        json.dump(clean, f, indent=2, default=str)

    # Summary
    print("\n" + "="*60)
    print("V31 Multi-Brain Experiments - FINAL SUMMARY")
    print("="*60)
    print("Total time: " + str(round(elapsed, 1)) + "s")
    print()
    
    r21 = all_results['exp21_competition']
    print("[2-1 Competition]")
    for bid, cap in r21['captures'].items():
        print("  " + bid + ": light=" + str(cap['light']) + " chem=" + str(cap['chemical']))
    print("  IB lock ratio: " + str(round(r21['inter_bonds']['lock_ratio'], 3)))
    print()

    r22 = all_results['exp22_cooperation']
    print("[2-2 Cooperation]")
    print("  Speedup: " + str(round(r22['speedup'], 2)) + "x")
    print("  IB lock ratio: " + str(round(r22['inter_bonds']['lock_ratio'], 3)))
    print()

    r23 = all_results['exp23_mixed']
    print("[2-3 Mixed Population]")
    for nk, nv in sorted(r23.items()):
        print("  " + nk + ": efficiency=" + str(round(nv['collective_efficiency'], 1)) +
              " div_entropy=" + str(round(nv['division_entropy'], 2)) +
              " sigma=" + str(round(nv['mean_sigma_final'], 2)))
    
    print("\nResults saved: " + out_path)
    print("="*60)


# ============================================================
# V34: Adaptive Tau vs Fixed Tau Comparison
# ============================================================
print()
print("=" * 60)
print("V34 Comparison: Adaptive Tau vs Fixed Tau")
print("=" * 60)

# Run with adaptive tau
sim_v34_adaptive = MultiBrainSimulation(n_brains=2, tau_cfg=TauConfig(enabled=True, tau_base=20.0, alpha_tau=1.0))
r_v34_adaptive = sim_v34_adaptive.run_exp21_competition(n_steps=600)

# Run with fixed tau (baseline)
sim_v34_fixed = MultiBrainSimulation(n_brains=2, tau_cfg=TauConfig(enabled=False, tau_base=20.0))
r_v34_fixed = sim_v34_fixed.run_exp21_competition(n_steps=600)

all_results['v34_adaptive_tau'] = r_v34_adaptive
all_results['v34_fixed_tau'] = r_v34_fixed

print()
print("--- V34 Tau Comparison Summary ---")
print("  Adaptive tau: sigma=" + str(round(r_v34_adaptive.get('mean_sigma', 0), 3)))
print("  Fixed tau:    sigma=" + str(round(r_v34_fixed.get('mean_sigma', 0), 3)))

# Collect tau metrics from all brains
all_tau_means = []
for brain in sim_v34_adaptive.brains.values():
    for region in brain.regions.values():
        all_tau_means.append(float(region.tau_per_neuron.mean()))
if all_tau_means:
    print("  Adaptive tau mean (all regions): " + str(round(sum(all_tau_means)/len(all_tau_means), 2)))
    all_results['v34_tau_stats'] = {
        'tau_mean_all': float(sum(all_tau_means)/len(all_tau_means)),
        'tau_min': float(min(all_tau_means)),
        'tau_max': float(max(all_tau_means))
    }
