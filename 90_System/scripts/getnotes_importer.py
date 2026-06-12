#!/usr/bin/env python3
"""GetNotes Importer v1.3 — iNEST/TCC Knowledge Base
Strategy: Import ALL tech/research content. Only exclude diaries and personal life.
Date filter: 2026-05-20 onwards.
"""

import os, re, json, hashlib, datetime, shutil

CONFIG = {
    "watch_dir": r"D:\Obsidian\GetNotes_Inbox",
    "output_inbox": r"D:\Obsidian\home\work\.openclaw\workspace\00_Inbox",
    "state_file": r"D:\Obsidian\scripts\getnotes_state.json",
    "cutoff_date": "2026-05-20",
}

# ============================================================
# INCLUSION: Broad tech/research keywords (any match = import)
# ============================================================

TECH_KEYWORDS = [
    # AI & Intelligence
    '智能', 'AI', 'ai', 'AGI', '人工智能', '大模型', 'LLM', 'GPT', 'Claude',
    'Transformer', 'transformer', '深度学习', '机器学习', '强化学习',
    '涌现', '推理', 'Agent', 'agent', '多模态',

    # Neural & Brain
    '神经', '脑', '类脑', '突触', '神经元', '皮层', '海马', '前额叶',
    '连接组', '线虫', '果蝇', '斑马鱼', '小鼠', '灵长',
    'SNN', 'snn', '脉冲', 'spike', 'STDP', 'stdp',

    # Computing & Chips
    '芯片', '算力', 'GPU', 'gpu', 'NPU', 'npu', 'TPU', 'tpu',
    'FPGA', 'fpga', 'ASIC', 'asic', '忆阻器', '存算一体',
    '晶圆', '制程', '流片', '硅光', '光计算', '量子',

    # Network & Architecture
    '网络', '互联', '拓扑', '路由', '交换', '协议',
    '分布式', '边缘', '数据中心', '超算', '云计算',
    '软件定义', 'SDN', 'sdn', 'SDI', 'sdi',

    # Computing Paradigm
    '计算', '架构', '范式', '冯诺依曼', '非冯', '近存',
    'CST', 'cst', 'TCC', 'tcc', 'iNEST', 'inest',

    # Energy & Efficiency
    '能耗', '功耗', '能效', '绿色', '节能',

    # Free Energy & Physics
    'FEP', 'fep', '自由能', '最小作用量', '变分', '惊讶度',
    '物理第一性', '自组织', '临界态', 'SOC', '相变',
    '复杂网络', '小世界', '无标度', '幂律',

    # Hardware & Engineering
    '异步电路', 'AER', '事件驱动', '晶圆级', '3D堆叠',
    'RISC-V', 'riscv', 'HBM', 'CXL', 'PCIe',

    # Research & Papers
    'Nature', 'Science', 'Cell', 'arXiv', '论文', '综述',
    '仿真', '实验', '验证', '原型', '基准',

    # Specific Terms
    'KAN', 'kan', 'LNN', 'lnn', 'CfC', 'cfc', 'LiquidAI',
    'Friston', 'Hinton', 'LeCun', 'Ng',
]

# ============================================================
# EXCLUSION: Diary & personal life keywords (skip these)
# ============================================================

DIARY_KEYWORDS = [
    '日记', '日志', '周记', '备忘', 'todo', 'TODO', '购物清单',
    '今天天气', '今天吃了', '今天去了', '今天买',
    '健身', '跑步', '游泳', '瑜伽', '锻炼',
    '做饭', '菜谱', '美食', '餐厅',
    '旅游', '酒店', '机票', '火车票',
    '购物', '淘宝', '京东', '拼多多', '快递',
    '账单', '工资', '理财', '基金', '股票', '保险',
    '孩子', '家长会', '幼儿园', '学校', '作业',
    '医院', '挂号', '体检', '看病',
    '朋友圈', '抖音', '微博', '小红书', '刷手机',
    '心情', '情绪', '焦虑', '失眠', '冥想',
]

def is_diary(text):
    """Return True if content looks like a personal diary."""
    t = text.lower()
    score = 0
    for kw in DIARY_KEYWORDS:
        if kw.lower() in t:
            score += 1
    # Also check: very short content with no tech keywords
    if len(text.strip()) < 50:
        has_tech = any(kw.lower() in t for kw in TECH_KEYWORDS)
        if not has_tech:
            score += 3
    return score >= 1

def extract_date(filepath, text):
    name = os.path.basename(filepath)
    for pat in [r'(\d{4}-\d{2}-\d{2})', r'(\d{4}_\d{2}_\d{2})', r'(\d{4}\d{2}\d{2})']:
        m = re.search(pat, name)
        if m:
            d = m.group(1).replace('_','-')
            if len(d) == 8: d = d[:4]+'-'+d[4:6]+'-'+d[6:8]
            try: return datetime.datetime.strptime(d, '%Y-%m-%d')
            except: pass
    m = re.search(r'date:\s*(\d{4}-\d{2}-\d{2})', text)
    if m:
        try: return datetime.datetime.strptime(m.group(1), '%Y-%m-%d')
        except: pass
    try: return datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
    except: return None

def is_after_cutoff(filepath, text, cutoff):
    d = extract_date(filepath, text)
    return d is None or d >= cutoff

def match_score(text):
    """Count how many tech keywords match."""
    t = text.lower()
    return sum(1 for kw in TECH_KEYWORDS if kw.lower() in t)

def generate_tags(text):
    tags = []
    tag_map = {
        '大模型':['llm','transformer','ai'],
        'LLM':['llm','transformer','ai'],
        '芯片':['chip','hardware','semiconductor'],
        '算力':['computing','infrastructure'],
        '网络':['network','architecture'],
        '类脑':['neuromorphic','brain-inspired'],
        '神经':['neural','neuroscience'],
        'tcc':['tcc','cst'],
        'sdi':['sdi-bond','hardware'],
        'fep':['fep','free-energy'],
        'stdp':['stdp','learning-rule'],
        '涌现':['emergence','criticality'],
        '自组织':['self-organization'],
        '忆阻器':['memristor','hardware'],
        'FPGA':['fpga','hardware'],
        '连接组':['connectome','simulation'],
        '论文':['paper','research'],
        'Nature':['paper','top-journal'],
        'Science':['paper','top-journal'],
        '能耗':['energy','green-ai'],
        '架构':['architecture','design'],
        '物理':['physics','first-principles'],
    }
    t = text.lower()
    for k,v in tag_map.items():
        if k.lower() in t: tags.extend(v)
    return list(set(tags)) if tags else ['inest','research','tech-clip']

def generate_wikilinks(text, tags):
    links = []
    link_map = {
        'sdi-bond':['[[SDI化合物键_四型架构]]'],
        'fep':['[[STDP-FEP梯度下降统一映射]]','[[变分自由能F]]'],
        'stdp':['[[STDP-FEP梯度下降统一映射]]'],
        'tcc':['[[NCL神经计算定律详解]]','[[CST计量仪]]'],
        'cst':['[[NCL神经计算定律详解]]','[[超非线性增益]]'],
        'hardware':['[[SDI化合物键_四型架构]]','[[FPGA原型]]'],
        'emergence':['[[自组织临界态SOC]]'],
        'connectome':['[[v28多尺度仿真结果]]'],
        'llm':['[[paper2_liquid_computing_chemistry]]'],
        'chip':['[[SDI化合物键_四型架构]]'],
        'network':['[[paper1_iNEST_core_architecture]]'],
        'neuromorphic':['[[SDI化合物键_四型架构]]','[[FPGA原型]]'],
        'green-ai':['[[paper2_liquid_computing_chemistry]]'],
        'paper':['[[Papers-MOC]]'],
    }
    for tag in tags:
        if tag in link_map: links.extend(link_map[tag])
    links.extend(['[[iNEST-MOC]]'])
    return list(set(links))


def is_tcc_inest(text):
    """Return True if content is TCC/iNEST related."""
    t = text.lower()
    tcc_inest_keywords = [
        "tcc", "inest", "??", "??????", "cst", "sdi",
        "sdsow", "metatopology", "sdi-cc",
        "????", "??", "??????", "snn", "stdp",
        "???", "fep", "??", "bayesian", "????",
        "???", "memristor", "????", "aer",
        "???", "??", "???", "???", "connectome",
        "????", "??", "???", "??",
        "????", "???", "brain-inspired", "neuromorphic",
        "???", "chiplet", "????", "3d??",
        "c.elegans", "??", "drosophila", "???",
        "risc-v", "fpga", "asic",
        "????", "????", "noc", "network-on-chip",
        "spike", "event-driven", "????",
        "??", "?", "??", "??", "??",
        "nature", "science", "cell", "??", "??",
        "????", "transformer", "???", "gpt",
        "codex", "claude", "agent",
        "????", "???", "plasticity",
        "??", "??", "circuit",

    ]
    return any(kw in t for kw in tcc_inest_keywords)

def process_note(filepath, cutoff):
    with open(filepath, 'r', encoding='utf-8') as fh:
        text = fh.read()
    if not is_after_cutoff(filepath, text, cutoff):
        return None, 'before_cutoff'
    if is_diary(text):
        return None, 'diary'
    if not is_tcc_inest(text):
        return None, 'not_tcc_inest'
    score = match_score(text)
    title = re.sub(r'[\r\n]+',' ',os.path.splitext(os.path.basename(filepath))[0])[:80]
    tags = generate_tags(text)
    links = generate_wikilinks(text, tags)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    yt = '\n'.join('  - '+t for t in tags)
    yl = '\n'.join(links)
    note = f'---\ntitle: {title}\ntags:\n{yt}\ndate: {now}\nsource: GetNotes\nscore: {score}\n---\n\n## Original Note\n\n{text}\n\n---\n\n## Related Notes\n\n{yl}\n'
    return note, 'imported'

def main():
    w = CONFIG['watch_dir']
    a = os.path.join(w, '_processed')
    o = CONFIG['output_inbox']
    s = CONFIG['state_file']
    cutoff = datetime.datetime.strptime(CONFIG['cutoff_date'], '%Y-%m-%d')
    for d in [w,a,o]: os.makedirs(d, exist_ok=True)
    state = json.load(open(s, encoding='utf-8')) if os.path.exists(s) else {}
    files = [f for f in os.listdir(w) if f.endswith(('.md','.txt')) and f != '_processed']
    imported = dup = dskip = diary = notech = 0
    for fn in files:
        fp = os.path.join(w, fn)
        fh = hashlib.md5(open(fp,'rb').read()).hexdigest()
        if fh in state:
            dup += 1; shutil.move(fp, os.path.join(a, fn)); continue
        note, status = process_note(fp, cutoff)
        if status == 'before_cutoff': dskip += 1
        elif status == 'diary': diary += 1
        elif status == 'no_tech': notech += 1
        elif note:
            note_hash = fh
            on = f"GetNote_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{fn}"
            with open(os.path.join(o, on), 'w', encoding='utf-8') as fout:
                fout.write(note)
            state[note_hash] = on; imported += 1
        shutil.move(fp, os.path.join(a, fn))
    json.dump(state, open(s, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    print(f'v1.3 | in={imported} dup={dup} dskip={dskip} diary={diary} notech={notech}')

if __name__ == '__main__':
    main()