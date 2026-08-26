import os, re, json, sys, time
sys.stdout.reconfigure(encoding='utf-8')

vault = r'D:\Obsidian\vault'
source_dirs = ['03_Topics', '10_Library', '10_Knowledge', '20_Ideas', 'papers']

# Target mapping
TCC_DIRS = {
    'theory': '30_TCC/31_Theory',
    'tech': '30_TCC/32_Technology',
    'dev': '30_TCC/33_Engineering',
    'project': '30_TCC/34_Projects',
    'sim': '30_TCC/35_Simulation',
}
INEST_DIRS = {
    'theory': '40_iNEST/41_Theory',
    'tech': '40_iNEST/42_Technology',
    'dev': '40_iNEST/43_Engineering',
    'project': '40_iNEST/44_Projects',
    'sim': '40_iNEST/45_Simulation',
}

# Keyword rules
TCC_KEYWORDS = [
    '晶上', '芯片', 'wafer', 'chiplet', 'NoC', 'SDI', '互连', '计算架构',
    '封装', '硅基', '集成电路', '半导体', 'die-to-die', 'chiplet',
    'TCC', '拓扑中心', 'topology centric', 'dark silicon',
    'memristor', '忆阻', 'ferroelectric', 'crossbar', 'VLSI',
    'signal integrity', 'DFT', 'physical design', 'placement',
    'manycore', 'multicore', 'noc', 'network-on-chip',
    '晶圆', '异构集成', 'chiplet互联', '先进封装',
    '软件定义', 'SDSoW', '互连架构', 'Chiplet',
    'CST', '计算存储传输', '计算范式',
    'FPGA', '晶上系统', '晶上大脑'
]

INEST_KEYWORDS = [
    '神经', '脑', '类脑', 'neuron', 'brain', 'SNN', '脉冲',
    '雪崩', '临界', 'avalanche', 'criticality',
    'neuroscience', 'neuromorphic', 'spiking',
    '认知', 'cognition', 'synaptic', '突触',
    'dendrit', 'axon', 'cortical', '皮层',
    'hippocampus', '海马', 'prefrontal', '前额叶',
    '自由能', 'free energy', 'active inference',
    'consciousness', '意识', 'whole brain',
    'visual cortex', '视觉皮层', 'place cell', 'grid cell',
    '小世界', 'small world', 'scale-free', '无标度',
    '复杂网络', 'complex network', 'network science',
    '自组织', 'self-organized', '涌现', 'emergence',
    '具身', 'embodied', '感知', 'perception',
    '动力学', 'dynamics', 'oscillation', '振荡',
    '同步', 'synchronization', 'reservoir',
    '储备池', 'echo state', 'liquid state',
    '形态计算', '形态', 'morphological',
]

# Classification function
def classify_file(filepath, content_preview):
    filename = os.path.basename(filepath).lower()
    text = (filename + ' ' + content_preview[:1000]).lower()
    
    tcc_score = sum(1 for kw in TCC_KEYWORDS if kw.lower() in text)
    inest_score = sum(1 for kw in INEST_KEYWORDS if kw.lower() in text)
    
    if tcc_score > inest_score:
        # Determine subcategory
        if any(k in text for k in ['simulation', '仿真', 'simulator', 'simulate']):
            return 'TCC', 'sim'
        elif any(k in text for k in ['project', '项目', 'proposal', '申报', 'roadmap', '路线']):
            return 'TCC', 'project'
        elif any(k in text for k in ['implementation', 'implementation', 'code', '开发', '工程', 'fabrication', '制造']):
            return 'TCC', 'dev'
        elif any(k in text for k in ['technology', '技术', 'architecture', '架构', 'design', '设计']):
            return 'TCC', 'tech'
        else:
            return 'TCC', 'theory'
    elif inest_score > tcc_score:
        if any(k in text for k in ['simulation', '仿真', 'simulator']):
            return 'iNEST', 'sim'
        elif any(k in text for k in ['project', '项目', 'proposal', '申报']):
            return 'iNEST', 'project'
        elif any(k in text for k in ['implementation', 'code', '开发', '工程']):
            return 'iNEST', 'dev'
        elif any(k in text for k in ['technology', '技术', 'architecture', '架构']):
            return 'iNEST', 'tech'
        else:
            return 'iNEST', 'theory'
    else:
        # Ambiguous - need LLM
        return 'AMBIGUOUS', None

# Scan files
to_classify = []
ambiguous = []
for sdir in source_dirs:
    spath = os.path.join(vault, sdir)
    if not os.path.exists(spath):
        continue
    for root, dirs, files in os.walk(spath):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in files:
            if not f.endswith('.md'):
                continue
            full = os.path.join(root, f)
            size = os.path.getsize(full)
            if size < 600:
                continue
            rel = os.path.relpath(full, vault)
            try:
                with open(full, 'r', encoding='utf-8') as fh:
                    content = fh.read(2000)
            except:
                content = ''
            category, subcat = classify_file(rel, content)
            if category == 'AMBIGUOUS':
                ambiguous.append((rel, size, content[:500]))
            else:
                if category == 'TCC':
                    target = TCC_DIRS[subcat]
                else:
                    target = INEST_DIRS[subcat]
                to_classify.append((rel, target))

print('Clear keyword matches: %d' % len(to_classify))
print('Ambiguous (need LLM): %d' % len(ambiguous))
print('')
print('Sample clear matches:')
for rel, target in to_classify[:10]:
    print('  %s -> %s' % (rel, target))
print('')
print('Sample ambiguous:')
for rel, size, _ in ambiguous[:10]:
    print('  [%dB] %s' % (size, rel))

# Save for next step
with open(os.path.join(vault, '90_System/scripts/classify_clear.json'), 'w', encoding='utf-8') as f:
    json.dump(to_classify, f, ensure_ascii=False, indent=2)
with open(os.path.join(vault, '90_System/scripts/classify_ambiguous.json'), 'w', encoding='utf-8') as f:
    json.dump(ambiguous, f, ensure_ascii=False, indent=2)
print('')
print('Saved to 90_System/scripts/classify_*.json')
