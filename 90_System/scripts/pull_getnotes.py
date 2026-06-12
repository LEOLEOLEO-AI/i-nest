import json, os, subprocess
from datetime import datetime
from pathlib import Path

GETNOTE_BIN = os.path.expandvars(r'%LOCALAPPDATA%\getnote\getnote.exe')
INBOX_DIR = Path(r'D:\Obsidian\GetNotes_Inbox')
STATE_FILE = Path(r'D:\Obsidian\scripts\getnote_pull_state.json')
IMPORT_LOG = Path(r'D:\Obsidian\scripts\getnote_pull_log.txt')

INCLUDE_KW = [
    'iNEST','inest','NEST','TCC','SDI','CST',
    'topology','network center',
    'chiplet','Chiplet','FPGA','fpga','RISC-V','riscv','SDSoW','CoWoS','CoPoS',
    'HBM','CXL','WellChip','Coyote','Speck',
    'SNN','neuromorphic','connectome','BCI',
    'emergence','Codex','Claude','LLM','GPT','Agent','MCP',
    'Nature','Science','Cell','arXiv','IEEE',
    'DARPA',
    '拓扑', '拓扑中心计算', 'sdsow', 'metatopology', 'sdi-cc',
    '神经形态', '类脑', '脉冲神经网络', 'snn', 'stdp',
    '自由能', 'fep', '变分', 'bayesian', '主动推理',
    '忆阻器', 'memristor', '异步电路', 'aer',
    '自组织', '临界', '小世界', '连接组',
    '复杂网络', '涌现', '标度律', '幂律',
    '神经计算', '脑启发', 'brain-inspired',
    '晶圆级', '存算一体', '3d堆叠',
    'c.elegans', '线虫', 'drosophila', '斑马鱼',
    '路由算法', '片上网络', 'noc', 'network-on-chip',
    'spike', 'event-driven', '事件驱动',
    '神经', '脑', '海马', '皮层', '突触',
    '论文', '科研', '深度学习', 'transformer', '大模型', 'gpt',
    '学习规则', '可塑性', 'plasticity',
    '连接', '环路', 'circuit',
]

EXCLUDE_KW = [
    'diary','fitness','sleep','weight',
    '日记', '日志', '周记', '备忘', 'todo', '购物清单',
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

INCLUDE_KBS = {
    'QJm6p7nj': 'iNEST',
    'lJ6AQpG0': 'WellChip',
    'qY2v51zY': 'INEST-papers',
    'ongZ3NjJ': 'computing-network',
    'rYMK3jgJ': 'SDSoW',
    '40DMpE1J': 'DARPA-research',
    'jnZmdmqJ': 'paper-ideas',
    'vnr2118n': 'patent',
    'EJXOrao0': 'project-guide',
    'nrddzZ80': 'Codex-tips',
    'Q0Q7QAbn': 'iNEST-dev',
}

def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{ts} | {msg}')
    with open(IMPORT_LOG, 'a', encoding='utf-8') as f:
        f.write(f'{ts} | {msg}\n')

def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, encoding='utf-8') as f:
            return json.load(f)
    return {'last_id': 0, 'imported_ids': [], 'kb_state': {}, 'total_imported': 0}

def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def fetch_notes():
    result = subprocess.run(
        [GETNOTE_BIN, 'notes', '--output', 'json'],
        capture_output=True, text=True, timeout=30, encoding='utf-8', errors='replace'
    )
    if result.returncode != 0:
        log(f'CLI failed: {result.stderr[:100]}')
        return []
    data = json.loads(result.stdout)
    return data.get('data', {}).get('notes', []) or []

def fetch_kb_notes(topic_id):
    result = subprocess.run(
        [GETNOTE_BIN, 'kb', topic_id, '--all', '--output', 'json'],
        capture_output=True, text=True, timeout=60, encoding='utf-8', errors='replace'
    )
    if result.returncode != 0:
        log(f'KB {topic_id} failed: {result.stderr[:100]}')
        return []
    try:
        data = json.loads(result.stdout)
        return data.get('data', {}).get('notes', []) or []
    except:
        return []

def should_include(note):
    title = note.get('title', '')
    content = note.get('content', '')
    text = f'{title} {content}'

    for kw in EXCLUDE_KW:
        if kw.lower() in text.lower():
            return False, f'exclude: {kw}'

    for kw in INCLUDE_KW:
        if kw.lower() in text.lower():
            return True, kw
    return False, ''

def save_note(note, kb_name=None):
    nid = note.get('note_id', note.get('id', 0))
    title = note.get('title', f'note_{nid}')
    content = note.get('content', '')
    note_type = note.get('note_type', 'plain_text')
    created = note.get('created_at', '')

    safe = ''.join(c if c.isalnum() or c in '._- ' else '_' for c in title)[:60]
    prefix = f'kb_{kb_name}_' if kb_name else ''
    filename = f'{prefix}getnote_{nid}_{safe}.md'

    md = '---\n'
    md += f'note_id: {nid}\n'
    md += f'title: "{title}"\n'
    md += f'type: {note_type}\n'
    md += f'created: {created}\n'
    md += 'source: getnote\n'
    md += f'kb: {kb_name or ""}\n'
    md += '---\n\n'
    md += f'# {title}\n\n'
    md += f'{content}\n\n'
    md += '---\n'
    md += f'*getnote | {datetime.now().strftime("%Y-%m-%d %H:%M")}*\n'

    filepath = INBOX_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md)
    return str(filepath)

def pull():
    log('========== GETNOTE PULL v2 ==========')
    state = load_state()
    last_id = state.get('last_id', 0)
    imported = set(state.get('imported_ids', []))
    kb_state = state.get('kb_state', {})
    total_new = 0

    log('Phase 1/2: Recent notes...')
    notes = fetch_notes()
    log(f'  Got {len(notes)} notes')
    included = 0
    for note in notes:
        nid = note['id']
        if nid in imported:
            continue
        if nid <= last_id:
            break
        ok, reason = should_include(note)
        if not ok:
            continue
        save_note(note)
        imported.add(nid)
        included += 1
        log(f'  + [{nid}] {note["title"][:50]} <- {reason}')
    if notes:
        state['last_id'] = max(state['last_id'], notes[0]['id'])
    log(f'  Included {included}')
    total_new += included

    log('Phase 2/2: Knowledge bases...')
    for tid, kb_name in INCLUDE_KBS.items():
        kb_imported = set(kb_state.get(tid, []))
        kb_notes = fetch_kb_notes(tid)
        if not kb_notes:
            log(f'  [{kb_name}] empty or error, skip')
            continue
        kb_new = 0
        for note in kb_notes:
            nid = note.get('note_id', 0)
            if not nid:
                continue
            if nid in kb_imported:
                continue
            ok, reason = should_include(note)
            if not ok:
                continue
            save_note(note, kb_name)
            kb_imported.add(nid)
            kb_new += 1
        kb_state[tid] = list(kb_imported)
        if kb_new:
            log(f'  [{kb_name}] {kb_new}/{len(kb_notes)} new')
        total_new += kb_new

    state['imported_ids'] = list(imported)[-1000:]
    state['kb_state'] = kb_state
    state['total_imported'] = state.get('total_imported', 0) + total_new
    state['last_pull'] = datetime.now().isoformat()
    save_state(state)

    log(f'Total new: {total_new} (cumulative: {state["total_imported"]})')
    log('========== DONE ==========')
    return total_new

if __name__ == '__main__':
    c = pull()
    print(f'\nNew: {c}')
