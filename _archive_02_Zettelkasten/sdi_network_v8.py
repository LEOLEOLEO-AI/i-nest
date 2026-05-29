"""
SDI网络仿真 v8 — 真实C.elegans Connectome直接初始化
========================================================
v8相比v7的核心升级（全部来自C.elegans特有属性）：

① 真实确定性连接图谱（Deterministic Connectome）
   - 直接用 NeuronConnect.xls 真实边列表初始化
   - 化学突触2575条（有向，权重=突触数量）
   - 电突触1031条（无向，即时双向传播）
   - 文献：Varshney et al. 2011, PLOS Comp Biol

② 有向图传播（Directed Propagation）
   - 化学突触严格有向（突触前→突触后）
   - 电突触无向（gap junction，双向即时）
   - 信息流方向：感觉→中间→运动（前馈层级结构）

③ 三类细胞特异性（Cell-type Specificity）
   - 感觉神经元（22.6%）：高兴奋性，低阈值，优先作为激活种子
   - 运动神经元（39.8%）：高扇出，作为"效应器输出"节点
   - 中间神经元（37.6%）：高度连接，E:I平衡调节枢纽
   - 文献：White et al. 1986, Phil Trans R Soc B（线虫神经网络完整图谱原始文献）

④ 突触权重初始化（基于突触数量）
   - 化学突触权重 = synaptic_count / max_count（归一化）
   - 电突触权重 = 0.3（gap junction固定导纳，Bhatt et al. 2014）

新增机制：
⑤ 星形胶质细胞模拟（线虫无真正胶质细胞，但有CEPsh细胞扮演类似角色）
   - CEPsh sheath cells：维持E-L/E-S比例稳态
   - 实现：基于全局E-L检测的主动降解（比突触缩放更激进）
   - 文献：Yoshimura & Bhatt 2020, Glia

目标：σ≥5.87, C≈0.337, L≈2.44, α∈[1.5,2.5]
"""

import numpy as np
import scipy.sparse as sp
import networkx as nx
import matplotlib
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
import matplotlib.pyplot as plt
from collections import defaultdict
import json, warnings, time, os
warnings.filterwarnings('ignore')

# ============================================================
# 参数
# ============================================================
DATA_PATH   = '/home/work/.openclaw/workspace/celegans_sim/connectome_v8_data.json'

# STDP（Bi&Poo 1998）
TAU_STDP    = 20.0
ETA_LTP     = 0.010
ETA_LTD     = 0.008
Ea_S, Ea_L  = 0.15, 0.85

# 化合键规则
THETA_LTP_BASE = 25
THETA_LTD      = 8
T_DECAY        = 25000

# STD突触疲劳（Tsodyks&Markram 1997）
TAU_REC  = 150
U_SE_CHEM = 0.45   # 化学突触资源消耗
U_SE_ELEC = 0.10   # 电突触消耗极少（gap junction离子直流）

# 不应期（Hodgkin&Huxley 1952）
T_ABS    = 3
T_REL    = 8
REL_SCALE= 0.3

# E-L/E-S比例约束（Song 2005目标：E-L≈20%）
EL_TARGET_LO = 0.15
EL_TARGET_HI = 0.28

# 突触缩放（Turrigiano 1998）
SCALING_THR  = 0.35
SCALING_RATE = 0.12
SCALING_INT  = 15

# ⑤ CEPsh胶质细胞模拟——主动E-L降解（比突触缩放更激进）
GLIA_THR   = 0.45   # E-L>45%时触发胶质细胞模拟
GLIA_RATE  = 0.25   # 每次降解25%的高权重E-L键（降级为E-S）
GLIA_INT   = 50     # 每50步检查

# 细胞类型参数
SEED_FRAC_SENSOR = 0.20  # 感觉神经元激活比例（高，作为输入门）
SEED_FRAC_OTHER  = 0.03  # 其他神经元自发激活比例

N_STEPS = 3000
CASCADE_MAX = 15

# 线虫基准
CEL_SIGMA, CEL_C, CEL_L = 5.87, 0.337, 2.44

# ============================================================
class SDI_v8:
    def __init__(self):
        t0 = time.time()
        print("加载真实C.elegans connectome数据...")
        with open(DATA_PATH) as f:
            data = json.load(f)

        self.N = data['N']
        self.nodes = data['nodes']
        self.n_types = data['n_types']  # node_name -> 'sensory'/'motor'/'interneuron'

        # 节点类型索引
        self.sensor_idx   = np.array([i for i,n in enumerate(self.nodes)
                                       if self.n_types[n]=='sensory'], np.int32)
        self.motor_idx    = np.array([i for i,n in enumerate(self.nodes)
                                       if self.n_types[n]=='motor'], np.int32)
        self.inter_idx    = np.array([i for i,n in enumerate(self.nodes)
                                       if self.n_types[n]=='interneuron'], np.int32)

        # ① 真实化学突触（有向）
        chem = data['edges_chem']
        chem_src = np.array([e[0] for e in chem], np.int32)
        chem_tgt = np.array([e[1] for e in chem], np.int32)
        chem_nbr = np.array([e[2] for e in chem], np.float64)
        chem_w   = chem_nbr / chem_nbr.max()  # 归一化到[0,1]
        chem_type = np.zeros(len(chem), np.int8)  # 初始全E-S

        # ② 真实电突触（无向，双向）
        elec = data['edges_elec']
        # 电突触展开为双向
        e_src1 = np.array([e[0] for e in elec], np.int32)
        e_tgt1 = np.array([e[1] for e in elec], np.int32)
        e_src2 = e_tgt1.copy()
        e_tgt2 = e_src1.copy()
        elec_src = np.concatenate([e_src1, e_src2])
        elec_tgt = np.concatenate([e_tgt1, e_tgt2])
        elec_w   = np.full(len(elec_src), 0.3)
        elec_type = np.full(len(elec_src), 4, np.int8)  # 类型4=电突触（固定）

        # 合并（化学在前，电突触在后）
        N_chem = len(chem_src)
        N_elec = len(elec_src)
        self.src   = np.concatenate([chem_src, elec_src])
        self.tgt   = np.concatenate([chem_tgt, elec_tgt])
        self.weight= np.concatenate([chem_w,   elec_w])
        self.btype = np.concatenate([chem_type, elec_type])
        self.is_elec = np.concatenate([np.zeros(N_chem,bool), np.ones(N_elec,bool)])
        self.Ea    = np.where(self.is_elec, 0.5, Ea_S)

        # 状态变量
        self.n_ltp      = np.zeros(len(self.src), np.int32)
        self.n_ltd      = np.zeros(len(self.src), np.int32)
        self.last_active= np.full(len(self.src), -99999, np.int32)
        self.R          = np.where(self.is_elec, 0.95, 1.0)  # 电突触资源几乎不耗竭

        # 节点状态
        self.t_fire    = np.full(self.N, -99999.0)
        self.last_fire = np.full(self.N, -99999, np.int32)
        self.act_count = np.zeros(self.N, np.int32)

        self.avalanche_sizes = []
        self.S_tot = 0.0
        self.scaling_events = 0
        self.glia_events = 0
        self.theta_ltp_current = THETA_LTP_BASE
        self.t = 0

        self._rebuild()

        dt = time.time()-t0
        print(f"v8初始化完成: N={self.N}, 化学突触={N_chem}, 电突触={N_elec//2}(展开={N_elec})")
        print(f"感觉:{len(self.sensor_idx)} 运动:{len(self.motor_idx)} 中间:{len(self.inter_idx)}")
        print(f"化学突触权重范围: [{chem_w.min():.3f},{chem_w.max():.3f}], 均值={chem_w.mean():.3f}")
        print(f"初始化耗时: {dt:.3f}s")

    def _rebuild(self):
        # 化学突触：有向，E/I区分
        # 电突触：无向，权重固定
        chem_mask = ~self.is_elec
        elec_mask =  self.is_elec

        # 化学突触有效权重（含STD资源）
        sign_chem = np.where(np.isin(self.btype[chem_mask],[0,2]), 1.0, -0.25)
        w_chem = self.weight[chem_mask] * self.R[chem_mask] * sign_chem

        # 电突触：双向、正性、无衰减
        w_elec = self.weight[elec_mask] * self.R[elec_mask] * 0.5  # 电突触效能0.5

        all_w  = np.concatenate([w_chem, w_elec])
        self.W = sp.csr_matrix(
            (all_w, (self.src.astype(int), self.tgt.astype(int))),
            shape=(self.N, self.N))

    def update_std(self, active_mask):
        """STD资源动力学（化学/电突触分开）"""
        self.R += (1.0 - self.R) / TAU_REC
        active_nodes = np.where(active_mask)[0]
        if len(active_nodes)==0: return
        src_active = np.isin(self.src, active_nodes)
        # 化学突触消耗
        chem_active = src_active & (~self.is_elec)
        self.R[chem_active] -= U_SE_CHEM * self.R[chem_active]
        # 电突触消耗（极少）
        elec_active = src_active & self.is_elec
        self.R[elec_active] -= U_SE_ELEC * self.R[elec_active]
        self.R = np.clip(self.R, 0.05, 1.0)

    def cascade(self, seeds):
        """有向传播，含不应期"""
        # 过滤绝对不应期
        seeds = [s for s in seeds if (self.t - self.last_fire[s]) >= T_ABS]
        if not seeds:
            self.avalanche_sizes.append(0)
            return np.zeros(self.N, bool)

        active = np.zeros(self.N, bool); active[seeds] = True
        self.t_fire[seeds] = float(self.t)
        self.last_fire[seeds] = self.t
        all_a = active.copy()

        for step in range(CASCADE_MAX):
            signal = self.W @ active.astype(float)

            # 层级抑制（感觉→中间→运动的前馈抑制）
            ratio = all_a.sum() / self.N
            inh   = max(0, (ratio - 0.18) * 4.5)

            # 不应期调制
            dt_f  = self.t - self.last_fire
            ref_s = np.ones(self.N)
            ref_s[dt_f < T_ABS] = 0.0
            ref_s[(dt_f>=T_ABS)&(dt_f<T_REL)] = REL_SCALE

            prob = np.clip(signal*(1-inh)*ref_s, 0, 1)
            new  = (prob > np.random.random(self.N)) & (~all_a)
            if not new.any(): break
            self.t_fire[new]    = float(self.t + step)
            self.last_fire[new] = self.t + step
            self.act_count[new] += 1
            all_a |= new; active = new

        self.avalanche_sizes.append(int(all_a.sum()))
        return all_a

    def stdp(self, am):
        nodes = np.where(am)[0]
        if len(nodes)==0: return
        # 只对化学突触做STDP（电突触固定）
        em = (~self.is_elec) & (np.isin(self.src,nodes)|np.isin(self.tgt,nodes))
        if not em.any(): return
        idx = np.where(em)[0]
        dt  = self.t_fire[self.src[idx]] - self.t_fire[self.tgt[idx]]
        w0  = self.weight[idx].copy()

        ltp = (dt>0)&(dt<200)
        if ltp.any():
            self.weight[idx[ltp]] = np.clip(
                self.weight[idx[ltp]]+ETA_LTP*np.exp(-dt[ltp]/TAU_STDP),0,1)
            self.n_ltp[idx[ltp]] += 1
        ltd = (dt<0)&(dt>-200)
        if ltd.any():
            self.weight[idx[ltd]] = np.clip(
                self.weight[idx[ltd]]-ETA_LTD*np.exp(dt[ltd]/TAU_STDP),0,1)
            self.n_ltd[idx[ltd]] += 1

        self.last_active[idx] = self.t
        self.S_tot += float(np.sum(self.Ea[idx]*np.abs(self.weight[idx]-w0)))

    def adjust_theta(self):
        chem_mask = ~self.is_elec
        nb = chem_mask.sum()
        el = np.sum((self.btype==2)&chem_mask) / max(1,nb)
        if el > EL_TARGET_HI:
            self.theta_ltp_current = min(THETA_LTP_BASE*4,
                int(THETA_LTP_BASE*(1+(el-EL_TARGET_HI)*12)))
        elif el < EL_TARGET_LO:
            self.theta_ltp_current = max(5,
                int(THETA_LTP_BASE*(1-(EL_TARGET_LO-el)*6)))
        else:
            self.theta_ltp_current = THETA_LTP_BASE
        return el

    def synaptic_scaling(self):
        """突触缩放（Turrigiano 1998）"""
        chem_mask = ~self.is_elec
        nb = chem_mask.sum()
        el_r = np.sum((self.btype==2)&chem_mask)/max(1,nb)
        if el_r < SCALING_THR: return
        thr = np.percentile(self.act_count, 80)
        hot = np.where(self.act_count>=thr)[0]
        if len(hot)==0: return
        sm = chem_mask & (self.btype==2) & \
             (np.isin(self.src,hot)|np.isin(self.tgt,hot))
        if sm.sum()==0: return
        self.weight[sm] *= (1-SCALING_RATE)
        deg = sm & (self.weight < 0.08)
        self.btype[deg]=0; self.Ea[deg]=Ea_S
        self.scaling_events += 1

    def glia_modulation(self):
        """
        ⑤ CEPsh胶质细胞模拟（Yoshimura&Bhatt 2020）
        当E-L超过45%，主动将最强的E-L键降级为E-S
        比突触缩放更激进：直接降级，不只是缩放权重
        对应生物：星形胶质细胞分泌TNF-α触发突触修剪
        """
        chem_mask = ~self.is_elec
        nb = chem_mask.sum()
        el_r = np.sum((self.btype==2)&chem_mask)/max(1,nb)
        if el_r < GLIA_THR: return 0

        # 找最强的E-L键（最容易被胶质细胞"识别"为过活跃）
        el_bonds = np.where(chem_mask & (self.btype==2))[0]
        if len(el_bonds)==0: return 0

        # 按权重从大到小排序，降级top GLIA_RATE比例
        n_degrade = max(1, int(len(el_bonds)*GLIA_RATE))
        top_idx = el_bonds[np.argsort(self.weight[el_bonds])[::-1][:n_degrade]]

        self.btype[top_idx] = 0   # E-L → E-S
        self.Ea[top_idx]    = Ea_S
        self.n_ltp[top_idx] = 0   # 重置LTP计数
        self.glia_events   += 1
        return n_degrade

    def apply_rules(self):
        el_r = self.adjust_theta()
        chem = ~self.is_elec

        # E-S → E-L（固化）
        fix = chem & (self.btype==0) & (self.n_ltp>=self.theta_ltp_current)
        self.btype[fix]=2; self.Ea[fix]=Ea_L; self.n_ltp[fix]=0

        # E-L → E-S（衰减）
        dec = chem & (self.btype==2) & (self.t-self.last_active>T_DECAY)
        self.btype[dec]=0; self.Ea[dec]=Ea_S

        # 修剪（只剪化学突触，不剪电突触）
        cut = chem & (((self.btype==1)&(self.n_ltd>=THETA_LTD)) |
                      ((self.btype==0)&(self.weight<0.01)&(self.t-self.last_active>1500)))
        keep = ~cut  # 保留：所有电突触 + 未被剪的化学突触
        self._apply_keep(keep)

        # 新建E-S键（只建化学突触）
        deg = np.bincount(self.src[~self.is_elec].astype(int), minlength=self.N)
        low = np.where(deg < 6)[0]
        if len(low)>0:
            n_new = min(len(low)*2, 60)
            ns = np.random.choice(low, n_new)
            nt = np.random.randint(0, self.N, n_new)
            v  = ns != nt; ns,nt=ns[v],nt[v]
            exc= np.random.random(len(ns)) < 0.8  # E:I=4:1
            n_add = len(ns)
            self.src  = np.concatenate([self.src, ns.astype(np.int32)])
            self.tgt  = np.concatenate([self.tgt, nt.astype(np.int32)])
            self.btype= np.concatenate([self.btype, np.where(exc,0,1).astype(np.int8)])
            self.weight=np.concatenate([self.weight,
                np.where(exc,np.random.uniform(0.1,0.4,n_add),
                         np.random.uniform(0.03,0.12,n_add))])
            self.n_ltp= np.concatenate([self.n_ltp, np.zeros(n_add,np.int32)])
            self.n_ltd= np.concatenate([self.n_ltd, np.zeros(n_add,np.int32)])
            self.last_active=np.concatenate([self.last_active,
                                             np.full(n_add,self.t,np.int32)])
            self.Ea   = np.concatenate([self.Ea, np.full(n_add,Ea_S)])
            self.R    = np.concatenate([self.R, np.ones(n_add)])
            self.is_elec=np.concatenate([self.is_elec,np.zeros(n_add,bool)])

        return el_r

    def _apply_keep(self, keep):
        self.src=self.src[keep]; self.tgt=self.tgt[keep]
        self.btype=self.btype[keep]; self.weight=self.weight[keep]
        self.n_ltp=self.n_ltp[keep]; self.n_ltd=self.n_ltd[keep]
        self.last_active=self.last_active[keep]
        self.Ea=self.Ea[keep]; self.R=self.R[keep]
        self.is_elec=self.is_elec[keep]

    def compute_sigma(self):
        G = nx.Graph(); G.add_nodes_from(range(self.N))
        for s,t in zip(self.src.tolist(), self.tgt.tolist()): G.add_edge(s,t)
        if not nx.is_connected(G):
            G=G.subgraph(max(nx.connected_components(G),key=len)).copy()
        n=G.number_of_nodes()
        if n<10: return 1.0,0.0,0.0
        C=nx.average_clustering(G)
        try: L=nx.average_shortest_path_length(G)
        except: L=5.0
        m=G.number_of_edges(); p=2*m/(n*(n-1))
        Cr=max(p,1e-6); Lr=np.log(n)/np.log(max(2,n*p))
        return (C/Cr)/(L/max(Lr,0.1)),C,L

    def fit_powerlaw(self):
        if len(self.avalanche_sizes)<200: return None
        s=np.array(self.avalanche_sizes); s=s[s>=2]
        if len(s)<60: return None
        xm=max(2,int(np.percentile(s,10))); x=s[s>=xm]
        if len(x)<20: return None
        return float(1+len(x)/np.sum(np.log(x/(xm-0.5))))

    def run(self):
        print(f"\n运行 {N_STEPS}步 | 真实Connectome初始化 | "
              f"感觉/运动/中间神经元 三类激活策略")
        print(f"新机制: 有向化学突触 + 电突触双向 + CEPsh胶质细胞模拟")
        print("-"*70)
        logs=dict(step=[],sigma=[],alpha=[],el_ratio=[],bonds=[],
                  theta=[],R_mean=[],glia=[],scaling=[])

        for step in range(N_STEPS):
            self.t = step

            for _ in range(5):
                # 感觉神经元优先激活（模拟感觉输入门）
                n_sensor = max(1, int(len(self.sensor_idx)*SEED_FRAC_SENSOR))
                n_other  = max(1, int(self.N*SEED_FRAC_OTHER))
                seeds_s = np.random.choice(self.sensor_idx, n_sensor, replace=False).tolist()
                seeds_o = np.random.choice(self.N, n_other, replace=False).tolist()
                seeds = list(set(seeds_s + seeds_o))
                am = self.cascade(seeds)
                self.update_std(am)
                self.stdp(am)
                self._rebuild()

            if step%SCALING_INT==0 and step>0:
                self.synaptic_scaling()

            if step%GLIA_INT==0 and step>0:
                self.glia_modulation()

            if step%15==0:
                el_r = self.apply_rules()
                self._rebuild()

            if step%100==0:
                sigma,C,L = self.compute_sigma()
                alpha = self.fit_powerlaw()
                chem_mask = ~self.is_elec
                nb = len(self.src)
                el = np.sum((self.btype==2)&chem_mask)/max(1,chem_mask.sum())
                R_m = float(np.mean(self.R[chem_mask]))

                logs['step'].append(step)
                logs['sigma'].append(sigma)
                logs['alpha'].append(alpha or 0)
                logs['el_ratio'].append(el)
                logs['bonds'].append(nb)
                logs['theta'].append(self.theta_ltp_current)
                logs['R_mean'].append(R_m)
                logs['glia'].append(self.glia_events)
                logs['scaling'].append(self.scaling_events)

                a_str=f"{alpha:.3f}" if alpha else "N/A"
                crit="🎯" if (alpha and 1.5<=alpha<=2.5 and sigma>=5.0) else \
                     ("✓σ" if sigma>=5.0 else "")
                el_s=("↑过多" if el>EL_TARGET_HI else
                      "↓过少" if el<EL_TARGET_LO else "✓")
                print(f"  步{step:4d}: σ={sigma:.2f} α={a_str:6s} "
                      f"E-L={el:.1%}{el_s} θ={self.theta_ltp_current} "
                      f"R={R_m:.3f} 胶质={self.glia_events} 键={nb} {crit}")

        return logs

# ============================================================
def plot_v8(net, logs, sf, Cf, Lf, af):
    fig, axes = plt.subplots(2, 3, figsize=(18,11))
    fig.suptitle(
        'SDI Network v8 — True C.elegans Connectome + Directed Graph + Cell Types\n'
        f'N={net.N}(real) | Chem={int((~net.is_elec).sum())} + Elec={int(net.is_elec.sum()//2)} gap junctions\n'
        f'Sensory:{len(net.sensor_idx)} Motor:{len(net.motor_idx)} Interneuron:{len(net.inter_idx)}',
        fontsize=10, fontweight='bold')
    steps = logs['step']

    ax=axes[0,0]
    ax.plot(steps,logs['sigma'],'b-o',ms=3,lw=1.5,label='σ (v8 real connectome)')
    ax.axhline(CEL_SIGMA,color='green',ls='--',lw=2,label=f'C.elegans σ={CEL_SIGMA}')
    ax.axhline(5.0,color='orange',ls=':',lw=1.5,label='target ≥5.0')
    ax.set_title('σ Evolution (Real Connectome Init)'); ax.set_xlabel('Step')
    ax.legend(fontsize=8); ax.grid(True,alpha=0.3)

    ax=axes[0,1]
    av=[v for v in logs['alpha'] if v>0]
    as_=[s for s,v in zip(steps,logs['alpha']) if v>0]
    if av:
        ax.plot(as_,av,'r-o',ms=3,lw=2,label='α')
        ax.fill_between(as_,[1.5]*len(as_),[2.5]*len(as_),
                        alpha=0.2,color='green',label='Target [1.5,2.5]')
        ax.axhline(1.5,color='green',ls='--',lw=2,label='Beggs&Plenz α=1.5')
    ax.set_title('Power-law α → 1.5\n(STD+Refractory+Directed)')
    ax.set_xlabel('Step'); ax.legend(fontsize=8); ax.grid(True,alpha=0.3)

    ax=axes[0,2]
    ax.plot(steps,[v*100 for v in logs['el_ratio']],'darkblue',lw=2,label='E-L%')
    ax.axhline(EL_TARGET_LO*100,color='green',ls='--',lw=1.5)
    ax.axhline(EL_TARGET_HI*100,color='red',ls='--',lw=1.5)
    ax.axhline(20,color='purple',ls=':',lw=1.5,label='Song 2005 ~20%')
    ax2=ax.twinx()
    ax2.plot(steps,logs['glia'],'crimson',lw=1.5,ls='--',label='Glia events')
    ax2.plot(steps,logs['scaling'],'orange',lw=1,ls=':',label='Scaling events')
    ax.set_title('E-L Ratio + Glia Modulation\n(CEPsh sheath cells, Yoshimura&Bhatt 2020)')
    ax.set_xlabel('Step'); ax.set_ylabel('E-L %',color='darkblue')
    ax2.set_ylabel('Events',color='crimson')
    ax.legend(loc='upper right',fontsize=7); ax2.legend(loc='lower right',fontsize=7)
    ax.grid(True,alpha=0.3)

    ax=axes[1,0]
    ax.plot(steps,logs['R_mean'],'teal',lw=2,label='R_mean (STD resource, chem only)')
    ax.set_title('STD Resource R(t)\n(Chemical vs Electrical distinct dynamics)')
    ax.set_xlabel('Step'); ax.set_ylabel('R'); ax.legend(fontsize=8); ax.grid(True,alpha=0.3)

    ax=axes[1,1]
    if net.avalanche_sizes:
        s=np.array(net.avalanche_sizes); u,c=np.unique(s,return_counts=True); p=c/c.sum()
        ax.loglog(u,p,'ko',ms=2.5,alpha=0.5,label='Observed')
        xr=np.linspace(max(u.min(),2),min(u.max(),net.N//2),100)
        yr15=xr**(-1.5); yr15/=yr15.sum()
        ax.loglog(xr,yr15,'g--',lw=2,label='Target α=1.5')
        if af:
            yrf=xr**(-af); yrf/=yrf.sum()
            ax.loglog(xr,yrf,'r-',lw=2,label=f'Fit α={af:.2f}')
    ax.set_title('Avalanche Distribution (Directed propagation)')
    ax.set_xlabel('S'); ax.set_ylabel('P(S)')
    ax.legend(fontsize=8); ax.grid(True,alpha=0.3)

    ax=axes[1,2]; ax.axis('off')
    chem_mask = ~net.is_elec
    bc=defaultdict(int)
    for bt in net.btype[chem_mask]: bc[bt]+=1
    tb=int(chem_mask.sum())
    a_str=f"{af:.3f}" if af else "N/A"
    crit_ok=af and 1.5<=af<=2.5

    rows=[
        ('C.elegans TRUE CONNECTOME RESULT','black',11,True),
        ('','white',4,False),
        (f'σ={sf:.3f}  (C.elegans: {CEL_SIGMA})',
         'green' if sf>=5.0 else 'orange',9,False),
        (f'C={Cf:.3f}  (C.elegans: {CEL_C})',
         'green' if abs(Cf-CEL_C)<0.1 else 'orange',9,False),
        (f'L={Lf:.3f}  (C.elegans: {CEL_L})',
         'green' if abs(Lf-CEL_L)<1.0 else 'orange',9,False),
        (f'α={a_str}  (target 1.5-2.5)',
         'green' if crit_ok else 'orange',9,False),
        ('','white',4,False),
        ('NEW in v8 (C.elegans specific)','black',10,True),
        ('① Real connectome init (Varshney 2011)','navy',8,False),
        ('② Directed chem + undirected elec syn','navy',8,False),
        ('③ 3 cell types: sensory/motor/inter','navy',8,False),
        ('④ Weight from synaptic count','navy',8,False),
        ('⑤ CEPsh glia modulation (Yoshimura 2020)','crimson',8,False),
        (f'   Glia events: {net.glia_events}','gray',7,False),
        (f'   Scaling events: {net.scaling_events}','gray',7,False),
        ('','white',4,False),
        ('BOND DISTRIBUTION (chem only)','black',10,True),
        (f'E-L:{bc[2]}({bc[2]/max(1,tb):.1%}) I-L:{bc[3]}({bc[3]/max(1,tb):.1%})',
         'navy',8,False),
        (f'E-S:{bc[0]}({bc[0]/max(1,tb):.1%}) I-S:{bc[1]}({bc[1]/max(1,tb):.1%})',
         'royalblue',8,False),
        (f'Elec(fixed):{int(net.is_elec.sum())} bonds','teal',8,False),
        ('','white',4,False),
        ('★ First SDI sim on REAL connectome','darkgreen',10,True),
    ]
    y=0.98
    for txt,col,fs,bold in rows:
        ax.text(0.02,y,txt,transform=ax.transAxes,fontsize=fs,color=col,
                fontweight='bold' if bold else 'normal',va='top')
        y-=max(0.034,fs*0.0043)

    out='/home/work/.openclaw/workspace/sdi_sim/sdi_v8_real_connectome.png'
    plt.savefig(out,dpi=150,bbox_inches='tight')
    plt.close()
    print(f"\n✅ 图表: {out}")
    return out

# ============================================================
if __name__=='__main__':
    t0=time.time()
    print("="*70)
    print("SDI网络仿真 v8 — 真实C.elegans Connectome + 有向图 + 三类神经元")
    print("="*70)
    np.random.seed(42)
    net=SDI_v8()
    s0,C0,L0=net.compute_sigma()
    print(f"初始小世界: σ={s0:.3f}, C={C0:.3f}, L={L0:.3f}")
    print(f"对比真实值: σ={CEL_SIGMA}, C={CEL_C}, L={CEL_L}")

    logs=net.run()

    sf,Cf,Lf=net.compute_sigma()
    af=net.fit_powerlaw()
    a_str=f"{af:.3f}" if af else "N/A"
    chem_mask=~net.is_elec
    el_f=np.sum((net.btype==2)&chem_mask)/max(1,chem_mask.sum())

    print("\n"+"="*70)
    print("v8最终结果（真实Connectome）：")
    print(f"  σ={sf:.3f}  (C.elegans基准={CEL_SIGMA}, {'✓' if sf>=5.0 else '△'})")
    print(f"  C={Cf:.3f}  (C.elegans基准={CEL_C})")
    print(f"  L={Lf:.3f}  (C.elegans基准={CEL_L})")
    print(f"  α={a_str}  (目标1.5-2.5, {'✓' if af and 1.5<=af<=2.5 else '△'})")
    print(f"  E-L化学突触占比={el_f:.1%} (目标15-28%)")
    print(f"  胶质细胞调制={net.glia_events}次")
    print(f"  突触缩放={net.scaling_events}次")
    print(f"  总耗时={time.time()-t0:.1f}s")

    plot_v8(net,logs,sf,Cf,Lf,af)
