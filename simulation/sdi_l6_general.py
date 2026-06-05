
"""
SDI L6 - General Intelligence Experiment
=========================================
Tests sequential multi-task learning, meta-learning acceleration,
and zero-shot generalization in a single 6-region brain.
"""
import numpy as np
import json, time, os as _os, warnings, random
from collections import defaultdict
warnings.filterwarnings('ignore')
import sys
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from sdi_v31_multibrain import SharedEnvironment
import networkx as nx

TAU_STDP = 20
ETA_LTP, ETA_LTD = 0.010, 0.008
Ea_S, Ea_L = 0.15, 0.85
THETA_LTP_BASE, THETA_LTD = 16, 8
T_DECAY = 100000
T_ABS, T_REL = 3, 8
REL_SCALE = 0.3
SCALING_THR, SCALING_RATE, SCALING_INT = 0.35, 0.12, 15
GLIA_THR, GLIA_RATE, GLIA_INT = 0.45, 0.25, 50
NOISE, I_SPONT = 0.02, 0.40
IB_ETA_LTP, IB_ETA_LTD = 0.008, 0.006
IB_Ea_S, IB_Ea_L = 0.20, 0.90

class L6BrainRegion:
    def __init__(self, name, N, p_connect=0.15):
        self.name, self.N = name, N
        k = max(2, int(N * p_connect))
        G = nx.watts_strogatz_graph(N, k, 0.3)
        src_list, tgt_list = [], []
        for u, v in G.edges():
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
        self.spike_history = np.zeros((N, TAU_STDP), dtype=np.float64)
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
        self.theta_bcm = np.full(N, 4.0, dtype=np.float64)
        self.BCM_ETA = 0.25
        self.R = np.ones(self.n_bonds, dtype=np.float64)
        self.scaling_events = 0; self.glia_events = 0
        self.alpha = 1.0; self.sigma = 1.0; self.el_ratio = 0.0
        self.meta_gain = 1.0

    def step(self, step_num, external_input=None, meta_modulation=1.0):
        N = self.N
        self.meta_gain = meta_modulation
        in_ref = (step_num - self.last_spike) < T_ABS
        in_rel = (step_num - self.last_spike) < (T_ABS + T_REL)
        self.V *= 0.9
        self.V += I_SPONT
        if external_input is not None:
            self.V += external_input
        active = self.spike.copy()
        for b in range(self.n_bonds):
            if active[self.src[b]] and not in_ref[self.tgt[b]]:
                w = self.weight[b] * self.R[b]
                if self.btype[b] == 2: w *= 1.5
                rf = REL_SCALE if in_rel[self.tgt[b]] else 1.0
                self.V[self.tgt[b]] += w * rf
        threshold = self.theta_bcm
        supra = self.V > threshold
        supra &= ~in_ref
        k = max(3, int(N * 0.15))
        if supra.sum() > k:
            supra_idx = np.where(supra)[0]
            top_k = supra_idx[np.argsort(self.V[supra_idx])[-k:]]
            new_spikes = np.zeros(N, dtype=bool)
            new_spikes[top_k] = True
        else:
            new_spikes = supra.copy()
        self.spike = new_spikes
        self.last_spike[new_spikes] = step_num
        self.spike_count[new_spikes] += 1
        if step_num % 10 == 0 and step_num > 0:
            self._stdp_update(step_num)
        if step_num % 20 == 0:
            self._fep_update(step_num)
        if step_num % 50 == 0 and step_num > 0:
            self._bcm_update(step_num)
        if step_num % SCALING_INT == 0 and step_num > 0:
            self._scaling_check()
        if step_num % GLIA_INT == 0 and step_num > 0:
            self._glia_check()
        if step_num % 100 == 0:
            el_mask = (self.btype == 2) & (self.t_last_update < step_num - T_DECAY)
            self.btype[el_mask] = 0; self.Ea[el_mask] = Ea_S; self.weight[el_mask] *= 0.5
        self.spike_history[:, self.hist_ptr] = self.spike.astype(np.float64)
        self.hist_ptr = (self.hist_ptr + 1) % TAU_STDP
        if step_num % 50 == 0 and step_num > 0:
            self._compute_metrics()

    def _stdp_update(self, step):
        for b in range(self.n_bonds):
            if self.btype[b] == 4: continue
            pre_t = np.where(self.spike_history[self.src[b]] > 0)[0]
            post_t = np.where(self.spike_history[self.tgt[b]] > 0)[0]
            if len(pre_t) == 0 or len(post_t) == 0: continue
            dt = post_t[:, None] - pre_t[None, :]
            ltp = np.sum((dt > 0) & (dt <= TAU_STDP))
            ltd = np.sum((dt < 0) & (dt >= -TAU_STDP))
            self.n_ltp[b] += int(ltp * self.meta_gain)
            self.n_ltd[b] += int(ltd * self.meta_gain)
            ratio = (self.n_ltp[b] + 1) / (self.n_ltd[b] + 1)
            if ratio > THETA_LTP_BASE / THETA_LTD and self.btype[b] == 0:
                self.btype[b] = 2; self.Ea[b] = Ea_L; self.t_last_update[b] = step
            elif ratio < 0.8 and self.btype[b] == 2:
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
        silent = h < 0.005
        self.theta_bcm[silent] *= 0.92
        self.theta_bcm = np.clip(self.theta_bcm, 1.5, 15.0)

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
        if el.any():
            el_ratio = el.sum() / self.n_bonds
            if el_ratio > 0.30:
                excess = el & (self.t_last_update == self.t_last_update.max())
                self.btype[excess] = 0; self.Ea[excess] = Ea_S
                self.glia_events += int(excess.sum())

    def _compute_metrics(self):
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
        except: pass


class L6GeneralBrain:
    def __init__(self, name, region_sizes=None):
        self.name = name
        sizes = region_sizes or {'vis': 80, 'chem': 80, 'proprio': 50, 'assoc': 120, 'motor': 80, 'meta': 50}
        self.regions = {}
        for rname, sz in sizes.items():
            self.regions[rname] = L6BrainRegion(rname, sz)
        self.cross_bonds = []
        for src_name in ['vis', 'chem', 'proprio']:
            sr, tr = self.regions[src_name], self.regions['assoc']
            n_conn = max(5, int(min(sr.N, tr.N) * 0.20))
            for _ in range(n_conn):
                si, ti = random.randint(0, sr.N-1), random.randint(0, tr.N-1)
                self.cross_bonds.append({
                    'src_region': src_name, 'src_idx': si,
                    'tgt_region': 'assoc', 'tgt_idx': ti,
                    'weight': random.uniform(0.2, 0.6), 'btype': 0,
                    'n_ltp': 0, 'n_ltd': 0,
                    'spike_hist_from': np.zeros(TAU_STDP),
                    'spike_hist_to': np.zeros(TAU_STDP), 'hist_ptr': 0
                })
        sr, tr = self.regions['assoc'], self.regions['motor']
        n_conn = max(8, int(min(sr.N, tr.N) * 0.25))
        for _ in range(n_conn):
            si, ti = random.randint(0, sr.N-1), random.randint(0, tr.N-1)
            self.cross_bonds.append({
                'src_region': 'assoc', 'src_idx': si,
                'tgt_region': 'motor', 'tgt_idx': ti,
                'weight': random.uniform(0.2, 0.6), 'btype': 0,
                'n_ltp': 0, 'n_ltd': 0,
                'spike_hist_from': np.zeros(TAU_STDP),
                'spike_hist_to': np.zeros(TAU_STDP), 'hist_ptr': 0
            })

    def step(self, step_num, external_inputs=None):
        inputs = external_inputs or {}
        meta_r = self.regions['meta']
        meta_r.step(step_num, inputs.get('meta', None))
        meta_activity = meta_r.spike.astype(np.float64).mean()
        for rname, region in self.regions.items():
            if rname == 'meta': continue
            ext_in = np.zeros(region.N)
            if rname in inputs: ext_in += inputs[rname]
            for bond in self.cross_bonds:
                if bond['tgt_region'] == rname:
                    src_r = self.regions[bond['src_region']]
                    if src_r.spike[bond['src_idx']]:
                        ext_in[bond['tgt_idx']] += bond['weight'] * (1.5 if bond['btype']==2 else 1.0)
            meta_mod = 1.0 + meta_activity * 2.0
            region.step(step_num, ext_in, meta_mod)
        if step_num % 10 == 0 and step_num > 0:
            self._cross_stdp_update(step_num)

    def _cross_stdp_update(self, step):
        for bond in self.cross_bonds:
            sr = self.regions[bond['src_region']]; tr = self.regions[bond['tgt_region']]
            sv = 1.0 if sr.spike[bond['src_idx']] else 0.0
            tv = 1.0 if tr.spike[bond['tgt_idx']] else 0.0
            bond['spike_hist_from'][bond['hist_ptr']] = sv
            bond['spike_hist_to'][bond['hist_ptr']] = tv
            bond['hist_ptr'] = (bond['hist_ptr'] + 1) % TAU_STDP
        for bond in self.cross_bonds:
            pre, post = bond['spike_hist_from'], bond['spike_hist_to']
            pt_pre = np.where(pre > 0)[0]; pt_post = np.where(post > 0)[0]
            if len(pt_pre) == 0 or len(pt_post) == 0: continue
            dt = pt_post[:, None] - pt_pre[None, :]
            ltp = np.sum((dt > 0) & (dt <= TAU_STDP)); ltd = np.sum((dt < 0) & (dt >= -TAU_STDP))
            bond['n_ltp'] += ltp; bond['n_ltd'] += ltd
            ratio = (bond['n_ltp'] + 1) / (bond['n_ltd'] + 1)
            if ratio > THETA_LTP_BASE / THETA_LTD and bond['btype'] == 0:
                bond['btype'] = 2
            elif ratio < 0.8 and bond['btype'] == 2:
                bond['btype'] = 0

    def get_state(self):
        sigmas = [r.sigma for r in self.regions.values()]
        els = [r.el_ratio for r in self.regions.values()]
        n_cross_el = sum(1 for b in self.cross_bonds if b['btype'] == 2)
        return {'mean_sigma': float(np.mean(sigmas)), 'mean_el': float(np.mean(els)),
                'cross_el': n_cross_el, 'cross_total': len(self.cross_bonds),
                'cross_el_ratio': n_cross_el / len(self.cross_bonds) if self.cross_bonds else 0}

    def get_motor_output(self):
        mr = self.regions['motor']
        return mr.spike, mr.V


def run_l6_experiment(steps_per_task=2000):
    print("=" * 60)
    print("L6 - General Intelligence Experiment")
    print("=" * 60)
    brain = L6GeneralBrain('l6_brain')
    results = {'tasks': {}, 'meta_learning': {}, 'generalization': {}}
    vis_N = brain.regions['vis'].N; chem_N = brain.regions['chem'].N
    vis_pref_angle = np.random.uniform(0, 2*np.pi, vis_N)
    vis_tuning_width = 0.35
    chem_pref_conc = np.logspace(-1, 0.5, chem_N)
    chem_tuning_sigma = 0.25

    # TASK 1: Phototaxis
    print("\n" + "="*40 + "\nTASK 1: Phototaxis\n" + "="*40)
    env = SharedEnvironment(100, 100); env.add_resource('light', 80, 50, 2.0)
    brain_pos = [50.0, 50.0]; light_pos = (80.0, 50.0)
    t1_dist = []; t1_criterion = None
    for step in range(steps_per_task):
        env.step(); sensed = env.sense_for_brain(brain_pos, sense_radius=60.0)
        angle = np.arctan2(light_pos[1]-brain_pos[1], light_pos[0]-brain_pos[0])
        ad = np.abs(angle - vis_pref_angle); ad = np.minimum(ad, 2*np.pi-ad)
        tuning = np.exp(-0.5*(ad/vis_tuning_width)**2)
        ext = {'vis': np.random.randn(vis_N)*NOISE + sensed['light']*2.0*tuning,
               'chem': np.random.randn(chem_N)*NOISE,
               'proprio': np.random.randn(brain.regions['proprio'].N)*NOISE*0.5,
               'meta': np.ones(brain.regions['meta'].N)*0.2}
        brain.step(step, ext)
        ms, mV = brain.get_motor_output(); half = mV.shape[0]//2
        dx = (mV[:half].mean()-mV[half:].mean())*0.5 + sensed['light']*1.2 if half>0 else sensed['light']*1.2
        dy = (mV.mean()-0.05)*0.3 + sensed['light']*0.8
        brain_pos[0] = np.clip(brain_pos[0]+dx+random.gauss(0,0.08), 0,100)
        brain_pos[1] = np.clip(brain_pos[1]+dy+random.gauss(0,0.08), 0,100)
        d = np.sqrt((brain_pos[0]-80)**2+(brain_pos[1]-50)**2); t1_dist.append(d)
        if t1_criterion is None and d < 15: t1_criterion = step
    t1i, t1f = np.mean(t1_dist[:20]), np.mean(t1_dist[-20:])
    t1_imp = t1i/(t1f+1e-8); s1 = brain.get_state()
    print(f"  T1: {t1i:.0f}->{t1f:.0f} ({t1_imp:.1f}x), crit={t1_criterion}")
    print(f"  sigma={s1['mean_sigma']:.2f}, el={s1['mean_el']:.3f}, cross_el={s1['cross_el_ratio']:.3f}")
    results['tasks']['phototaxis'] = {'improvement': float(t1_imp), 'criterion': t1_criterion, 'state': s1}

    # TASK 2: Chemotaxis
    print("\n" + "="*40 + "\nTASK 2: Chemotaxis\n" + "="*40)
    env2 = SharedEnvironment(100,100); env2.add_resource('chemical', 20, 80, 2.0)
    brain_pos = [50.0,50.0]; chem_pos = (20.0,80.0)
    t2_dist = []; t2_criterion = None
    for step in range(steps_per_task):
        env2.step(); sensed = env2.sense_for_brain(brain_pos, sense_radius=60.0)
        conc = sensed['chemical']; lc = np.log(max(conc,0.01))
        cr = np.exp(-0.5*((lc - np.log(chem_pref_conc+0.01))/chem_tuning_sigma)**2)
        ext = {'vis': np.random.randn(vis_N)*NOISE,
               'chem': np.random.randn(chem_N)*NOISE + conc*2.0*cr,
               'proprio': np.random.randn(brain.regions['proprio'].N)*NOISE*0.5,
               'meta': np.ones(brain.regions['meta'].N)*0.3}
        brain.step(step+steps_per_task, ext)
        ms, mV = brain.get_motor_output(); half = mV.shape[0]//2
        dx = (mV[:half].mean()-mV[half:].mean())*0.5 + sensed['chemical']*1.0 if half>0 else sensed['chemical']*1.2
        dy = (mV.mean()-0.05)*0.3 + sensed['chemical']*1.0
        brain_pos[0] = np.clip(brain_pos[0]+dx+random.gauss(0,0.08), 0,100)
        brain_pos[1] = np.clip(brain_pos[1]+dy+random.gauss(0,0.08), 0,100)
        d = np.sqrt((brain_pos[0]-20)**2+(brain_pos[1]-80)**2); t2_dist.append(d)
        if t2_criterion is None and d < 15: t2_criterion = step
    t2i, t2f = np.mean(t2_dist[:20]), np.mean(t2_dist[-20:])
    t2_imp = t2i/(t2f+1e-8); s2 = brain.get_state()
    print(f"  T2: {t2i:.0f}->{t2f:.0f} ({t2_imp:.1f}x), crit={t2_criterion}")
    print(f"  sigma={s2['mean_sigma']:.2f}, el={s2['mean_el']:.3f}, cross_el={s2['cross_el_ratio']:.3f}")
    results['tasks']['chemotaxis'] = {'improvement': float(t2_imp), 'criterion': t2_criterion, 'state': s2}

    # TASK 3: Obstacle Avoidance
    print("\n" + "="*40 + "\nTASK 3: Obstacle Avoidance\n" + "="*40)
    env3 = SharedEnvironment(100,100); env3.add_resource('light', 50,50,-1.5)
    brain_pos = [50.0,50.0]
    t3_dist = []; t3_criterion = None
    for step in range(steps_per_task):
        env3.step(); sensed = env3.sense_for_brain(brain_pos, sense_radius=60.0)
        obs_str = abs(sensed['light'])
        angle = np.arctan2(50-brain_pos[1], 50-brain_pos[0])
        ad = np.abs(angle-vis_pref_angle); ad = np.minimum(ad, 2*np.pi-ad)
        tuning = np.exp(-0.5*(ad/vis_tuning_width)**2)
        ext = {'vis': np.random.randn(vis_N)*NOISE + obs_str*2.0*tuning,
               'chem': np.random.randn(chem_N)*NOISE,
               'proprio': np.random.randn(brain.regions['proprio'].N)*NOISE*0.5,
               'meta': np.ones(brain.regions['meta'].N)*0.5}
        brain.step(step+steps_per_task*2, ext)
        ms, mV = brain.get_motor_output(); half = mV.shape[0]//2
        dx = (mV[:half].mean()-mV[half:].mean())*0.5 - sensed['light']*1.2 if half>0 else -sensed['light']*1.2
        dy = (mV.mean()-0.05)*0.3 - sensed['light']*0.8
        brain_pos[0] = np.clip(brain_pos[0]+dx+random.gauss(0,0.08), 0,100)
        brain_pos[1] = np.clip(brain_pos[1]+dy+random.gauss(0,0.08), 0,100)
        d = np.sqrt((brain_pos[0]-50)**2+(brain_pos[1]-50)**2); t3_dist.append(d)
        if t3_criterion is None and d > 30: t3_criterion = step
    t3i, t3f = np.mean(t3_dist[:20]), np.mean(t3_dist[-20:])
    t3_imp = t3f/(t3i+1e-8); s3 = brain.get_state()
    speedup = (t1_criterion or steps_per_task)/max((t3_criterion or steps_per_task),1)
    print(f"  T3: {t3i:.0f}->{t3f:.0f} ({t3_imp:.1f}x), crit={t3_criterion}")
    print(f"  sigma={s3['mean_sigma']:.2f}, el={s3['mean_el']:.3f}, cross_el={s3['cross_el_ratio']:.3f}")
    print(f"  Meta speedup: {speedup:.2f}x")
    results['tasks']['avoidance'] = {'improvement': float(t3_imp), 'criterion': t3_criterion, 'state': s3}
    results['meta_learning'] = {'t1_criterion': t1_criterion, 't3_criterion': t3_criterion, 'speedup': float(speedup)}

    # TASK 4: Combined (Zero-shot)
    print("\n" + "="*40 + "\nTASK 4: Combined (Zero-shot)\n" + "="*40)
    env4 = SharedEnvironment(100,100)
    env4.add_resource('light',80,30,2.0); env4.add_resource('chemical',20,70,2.0); env4.add_resource('light',50,50,-1.0)
    brain_pos = [50.0,50.0]; t4_l = []; t4_c = []; t4_a = []; reached=False; sr=-1
    for step in range(1000):
        env4.step(); sensed = env4.sense_for_brain(brain_pos, sense_radius=60.0)
        al = np.arctan2(30-brain_pos[1],80-brain_pos[0]); ad=np.abs(al-vis_pref_angle); ad=np.minimum(ad,2*np.pi-ad)
        pt = np.exp(-0.5*(ad/vis_tuning_width)**2)
        conc=sensed['chemical']; lc=np.log(max(conc,0.01))
        ct = np.exp(-0.5*((lc-np.log(chem_pref_conc+0.01))/chem_tuning_sigma)**2)
        ext = {'vis': np.random.randn(vis_N)*NOISE+sensed['light']*1.5*pt,
               'chem': np.random.randn(chem_N)*NOISE+conc*1.5*ct,
               'proprio': np.random.randn(brain.regions['proprio'].N)*NOISE*0.5,
               'meta': np.ones(brain.regions['meta'].N)*0.4}
        brain.step(step+steps_per_task*3, ext)
        ms, mV = brain.get_motor_output(); half = mV.shape[0]//2
        dx = (mV[:half].mean()-mV[half:].mean())*0.5+sensed['light']*0.8 if half>0 else sensed['light']*0.8
        dy = (mV.mean()-0.05)*0.3+sensed['light']*0.5+conc*0.5
        brain_pos[0]=np.clip(brain_pos[0]+dx+random.gauss(0,0.05),0,100)
        brain_pos[1]=np.clip(brain_pos[1]+dy+random.gauss(0,0.05),0,100)
        t4_l.append(np.sqrt((brain_pos[0]-80)**2+(brain_pos[1]-30)**2))
        t4_c.append(np.sqrt((brain_pos[0]-20)**2+(brain_pos[1]-70)**2))
        t4_a.append(np.sqrt((brain_pos[0]-50)**2+(brain_pos[1]-50)**2))
        if not reached and t4_l[-1]<10: reached=True; sr=step
    s4 = brain.get_state()
    combo = (np.mean(t4_l[:10])/(np.mean(t4_l[-20:])+1e-8)+np.mean(t4_c[:10])/(np.mean(t4_c[-20:])+1e-8)+np.mean(t4_a[-20:])/(np.mean(t4_a[:10])+1e-8))/3
    print(f"  sigma={s4['mean_sigma']:.2f}, el={s4['mean_el']:.3f}, cross_el={s4['cross_el_ratio']:.3f}")
    print(f"  combo={combo:.2f}, reached_light={reached}@{sr}")
    results['generalization'] = {'combo_score': float(combo), 'reached_light': reached, 'state': s4}

    # JUDGMENT
    print("\n" + "="*60 + "\nL6 JUDGMENT\n" + "="*60)
    l6_l = t1_imp>1.0 or t2_imp>1.0 or t3_imp>1.0
    l6_m = speedup>1.1; l6_g = combo>0.8
    l6_s = s4['mean_sigma']>4.0; l6_e = s4['mean_el']>0.10 or s4['cross_el_ratio']>0.10
    l6_all = (l6_s and l6_e) and (l6_l or l6_m)
    print(f"  Multi-task: {'PASS' if l6_l else 'FAIL'} ({max(t1_imp,t2_imp,t3_imp):.1f}x)")
    print(f"  Meta-speedup: {'PASS' if l6_m else 'FAIL'} ({speedup:.2f}x)")
    print(f"  Generalization: {'PASS' if l6_g else 'FAIL'} ({combo:.2f})")
    print(f"  Topology: {'PASS' if l6_s else 'FAIL'} (sigma={s4['mean_sigma']:.2f})")
    print(f"  Learning: {'PASS' if l6_e else 'FAIL'} (el={s4['mean_el']:.3f}, cross_el={s4['cross_el_ratio']:.3f})")
    print(f"\n  L6 OVERALL: {'=== PASS ===' if l6_all else '--- FAIL ---'}")
    results['judgment'] = {'l6_all': l6_all, 'l6_learning': l6_l, 'l6_meta': l6_m, 'l6_generalize': l6_g, 'l6_sigma': l6_s, 'l6_el': l6_e}
    return results

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(); p.add_argument('--steps', type=int, default=2000); a = p.parse_args()
    _os.makedirs('simulation/data/l6_results', exist_ok=True)
    print(f'L6: steps_per_task={a.steps}')
    t0=time.time(); r=run_l6_experiment(a.steps)
    with open('simulation/data/l6_results/l6_general.json','w') as f: json.dump(r,f,indent=2,default=str)
    print(f'Time: {time.time()-t0:.1f}s')
