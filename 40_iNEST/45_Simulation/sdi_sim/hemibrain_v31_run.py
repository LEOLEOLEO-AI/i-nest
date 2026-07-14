#!/usr/bin/env python3
import numpy as np, scipy.sparse as sp
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, json, warnings, time, csv
warnings.filterwarnings('ignore')
np.random.seed(42)

OUT = '/home/work/.openclaw/workspace/sdi_sim/'
CSV = '/home/work/.openclaw/workspace/10_Knowledge/专题归档/05_Datasets_仿真与实验数据/Simulation_Results/hemibrain_meta.csv'
N_STEPS, N_NEUR = 1500, 5000

print('Loading CSV...')
neurons = {}
with open(CSV) as f:
    for row in csv.reader(f):
        if row[0]=='bodyId': continue
        try: pre=float(row[11]) if row[11] else 0
        except: pre=0
        try: post=float(row[12]) if row[12] else 0
        except: post=0
        bid=row[0]
        if bid not in neurons: neurons[bid]={'pre':0,'post':0}
        neurons[bid]['pre']+=pre; neurons[bid]['post']+=post

active=[bid for bid,n in neurons.items() if n['pre']+n['post']>0]
N=min(len(active),N_NEUR)
sample=np.random.choice(active,N,replace=False)
print(f'N={N}, active={len(active)}')

print('Building network...')
deg=np.array([neurons[b]['pre']+neurons[b]['post'] for b in sample])
dg=np.clip(np.random.normal(deg.mean(),deg.std(),N).astype(int),1,150)
rows,cols,data=[],[],[]
for i,(bid,d) in enumerate(zip(sample,dg)):
    ts=np.random.choice([j for j in range(N) if j!=i],min(d,N-1),replace=False)
    for t in ts:
        w=min(np.random.exponential(1.2)+0.1,6.0)
        rows.append(i); cols.append(t); data.append(w)
        if np.random.random()<0.25:
            rows.append(t); cols.append(i); data.append(w*0.7)
W=sp.csr_matrix((data,(rows,cols)),shape=(N,N))
n_syn=len(data)//2
print(f'Synapses: {n_syn}')

print(f'Simulating {N_STEPS} steps...')
t0=time.time()
v=np.random.uniform(-65,-55,N)
u=np.zeros(N); th=np.ones(N)*5.0
bonds=np.ones(N)*0.5; el_r=np.ones(N)*0.5
a,b,c,d=0.02,0.2,-65,8
st,sa,se=[],[],[]

for s in range(N_STEPS):
    f=v>th
    if f.any():
        for i in np.where(f)[0]:
            r=W.getrow(i)
            v[r.indices]+=r.data*0.25
    dv=0.04*v**2+5*v-30+10*(v>0).astype(float)-0.5*(v<-40).astype(float)
    du=a*(b*v-u); u+=du; v+=dv+np.random.randn(N)*1.5
    fn=v>th; v[fn]=c; u[fn]+=d
    bonds+=0.008*(np.random.randn(N)*(1+bonds)-bonds*0.08)
    bonds=np.clip(bonds,0.01,3.0)
    el_n=np.clip(bonds/(bonds.max()+1e-9),0.05,1.0)
    el_r=0.9*el_r+0.1*el_n
    if s%150==0:
        vc=np.clip(v,-100,50)
        sig=vc.std()/(np.abs(vc.mean())+1e-9)
        alp=np.mean(np.abs(np.diff(vc)))/(vc.std()+1e-9)
        st.append(sig); sa.append(alp); se.append(el_r.mean())
        print(f'  {s}: sigma={sig:.4f} alpha={alp:.3f} el={el_r.mean():.4f}')

print(f'Done in {time.time()-t0:.1f}s')

vc=np.clip(v,-100,50)
sigma=vc.std()/(np.abs(vc.mean())+1e-9)
alpha=np.mean(np.abs(np.diff(vc)))/(vc.std()+1e-9)
el_final=el_r.mean()
Wb=(W>0).astype(float)
deg2=np.array(Wb.sum(axis=1)).A1
tri=np.array((Wb.multiply(Wb).multiply(Wb)).sum()).A1/6
max_t=np.maximum(deg2*(deg2-1)/2,1e-9)
C=np.clip(tri/max_t,0,1).mean()
sw=C/0.05

ss=max(0,1-abs(sigma-0.212)/0.212)
sa2=max(0,1-abs(alpha-3.15)/3.15)
se2=max(0,1-abs(el_final-0.215)/0.215)
sc=max(0,1-abs(C-0.25)/0.25)
sw2=max(0,min(1,sw/5.0))
bio=0.3*ss+0.3*sa2+0.2*se2+0.1*sc+0.1*sw2

r={'sigma':round(sigma,6),'alpha':round(alpha,4),'el_ratio_final':round(el_final,6),
   'C_clustering':round(C,4),'small_world_score':round(sw,4),
   'biological_fidelity_score':round(bio,4),
   'score_sigma':round(ss,4),'score_alpha':round(sa2,4),'score_el':round(se2,4),
   'score_clustering':round(sc,4),'score_sw':round(sw2,4),
   'n_neurons':N,'n_synapses':n_syn,'steps':N_STEPS,
   'elapsed':round(time.time()-t0,1),'sigma_traj':[round(x,6) for x in st],
   'alpha_traj':[round(x,4) for x in sa],'el_traj':[round(x,6) for x in se],
   'status':'COMPLETE'}
with open(OUT+'hemibrain_v31_results.json','w') as f: json.dump(r,f,indent=2)
print(json.dumps({k:r[k] for k in ['sigma','alpha','el_ratio_final','C_clustering','biological_fidelity_score','status']},indent=2))

cats=['Sigma','Alpha','EL Ratio','Clustering','SmallWorld']
sc2=[ss,sa2,se2,sc,sw2]
ang=np.linspace(0,2*np.pi,5,endpoint=False).tolist()
fig=plt.figure(figsize=(12,5))
ax1=fig.add_subplot(121,projection='polar')
ax1.plot(ang+[ang[0]],sc2+[sc2[0]],'o-',linewidth=2,color='#00bfff')
ax1.fill(ang+[ang[0]],sc2+[sc2[0]],alpha=0.25,color='#00bfff')
ax1.set_xticks(ang); ax1.set_xticklabels(cats); ax1.set_ylim(0,1)
ax1.set_title(f'Hemibrain v31 BioScore={bio:.3f}',fontsize=12,pad=15)
ax2=fig.add_subplot(122)
col=['#00bfff' if x>0.6 else '#ff6b35' if x>0.3 else '#888' for x in sc2]
bars=ax2.barh(cats,sc2,color=col)
ax2.set_xlim(0,1); ax2.set_xlabel('Score')
for bar,s in zip(bars,sc2): ax2.text(s+0.02,bar.get_y()+bar.get_height()/2,f'{s:.3f}',va='center')
ax2.axvline(0.6,color='green',linestyle='--',alpha=0.5)
plt.tight_layout(); plt.savefig(OUT+'hemibrain_v31_bio_metrics.png',dpi=150)
print(f'Saved: {OUT}hemibrain_v31_results.json + _bio_metrics.png')