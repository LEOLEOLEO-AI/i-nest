#!/usr/bin/env python3
"""
知识库自动进化引擎 v2.1
目标Vault: /home/work/obsidian-vault (Gitee: iBrainNest/i-nest, main分支)

流程:
  1. Get笔记新增 → Hermes处理 → 写入Obsidian Vault → Gitee push
  2. 印象笔记最近更新 → Hermes处理 → 写入Obsidian Vault → Gitee push
"""

import os, json, time, re, struct, subprocess, urllib.request, urllib.parse, urllib.error
from datetime import datetime
from pathlib import Path

# ─────────── 配置 ───────────
GETNOTE_API_KEY   = "gk_live_ba76d18881436f1a.a8e43043ab464418dcc9bb5dba5ba779bfd6aa1fd41ba0b7"
GETNOTE_CLIENT_ID = "cli_3802f9db08b811f197679c63c078bacc"
VAULT_DIR  = Path("/home/work/obsidian-vault")
STATE_FILE = VAULT_DIR / ".kb_sync_state.json"
GITEE_URL  = "https://iBrainNest:Liusansan%406363@gitee.com/iBrainNest/i-nest.git"

# 印象笔记配置
EVERNOTE_TOKEN     = "S=s27:U=1bb10ab:E=19df93b0456:C=19dd52e7d58:P=1cd:A=en-devtoken:V=2:H=3cb06202c5a2add381d30d90472a7a88"
EVERNOTE_NOTESTORE = "https://app.yinxiang.com/shard/s27/notestore"

# Get笔记 → Vault目录映射（基于Hermes分类）
CATEGORY_MAP = {
    "AI研究":   "00_KnowledgeBase_知识库/03_Inbox_文献与碎片",
    "学术论文":  "00_KnowledgeBase_知识库/03_Inbox_文献与碎片",
    "科技资讯":  "Clippings",
    "个人成长":  "01_Ideas_想法",
    "工作方法":  "01_Ideas_想法",
    "项目管理":  "05_Projects_项目",
    "日记":     "01_Ideas_想法",
    "会议记录":  "05_Projects_项目",
    "技术实践":  "04_Code_代码",
    "default":  "Clippings",
}

HEADERS = {
    "Authorization": GETNOTE_API_KEY,
    "X-Client-ID":   GETNOTE_CLIENT_ID,
    "Content-Type":  "application/json",
}
API_BASE = "https://openapi.biji.com/open/api/v1/resource"

# ─────────── API工具 ───────────
def api_get(path, params=None):
    import urllib.request, urllib.parse
    url = f"{API_BASE}/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def api_post(path, body):
    import urllib.request
    url = f"{API_BASE}/{path}"
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

# ─────────── 状态 ───────────
def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"last_cursor": "", "processed_ids": []}

def save_state(s):
    STATE_FILE.write_text(json.dumps(s, ensure_ascii=False, indent=2))

# ─────────── Hermes处理（轻量版，基于规则+关键词，不消耗LLM配额）───────────
def hermes_classify(note: dict) -> dict:
    """
    基于标题/内容关键词进行快速分类。
    如需LLM深度处理，设置环境变量 HERMES_DEEP=1
    """
    title   = note.get("title", "")
    content = note.get("content", "") or ""
    tags    = [t.get("name","") if isinstance(t,dict) else str(t) for t in note.get("tags", [])]
    note_type = note.get("note_type", "plain_text")
    text_sample = (title + " " + content[:300]).lower()

    # 规则分类
    category = "default"
    if any(k in text_sample for k in ["日记","diary","今天","昨天"]):
        category = "日记"
    elif any(k in text_sample for k in ["会议","meeting","讨论","纪要"]):
        category = "会议记录"
    elif any(k in text_sample for k in ["arxiv","paper","论文","doi","nature","science","ieee","neurips","icml"]):
        category = "学术论文"
    elif any(k in text_sample for k in ["cst","ncc","sdi","inest","类脑","memristor","忆阻"]):
        category = "AI研究"
    elif any(k in text_sample for k in ["ai","gpt","llm","transformer","神经网络","deep learning","大模型"]):
        category = "AI研究"
    elif any(k in text_sample for k in ["项目","申报","专项","经费","预算","立项"]):
        category = "项目管理"
    elif any(k in text_sample for k in ["代码","python","git","algorithm","github","function","def ","class "]):
        category = "技术实践"
    elif note_type == "link":
        category = "科技资讯"

    importance = "high" if any(k in text_sample for k in ["重要","urgent","关键","★","⭐","todo"]) else "medium"

    # 摘要：取前150字
    summary = content.strip()[:150].replace("\n", " ") if content.strip() else title

    return {
        "category":   category,
        "target_dir": CATEGORY_MAP.get(category, CATEGORY_MAP["default"]),
        "importance": importance,
        "summary":    summary,
        "tags":       tags,
        "source_type": note_type,
    }

# ─────────── Obsidian Markdown生成（Clipper格式）───────────
def build_obsidian_note(note: dict, hermes: dict) -> tuple:
    """返回 (文件名, markdown内容)"""
    title     = note.get("title") or "无标题"
    note_type = note.get("note_type", "plain_text")
    created   = note.get("created_at", "")[:10]
    note_id   = str(note.get("note_id",""))
    tags      = hermes.get("tags", [])
    summary   = hermes.get("summary","")
    importance= hermes.get("importance","medium")

    # 来源URL
    source_url = ""
    if note_type == "link":
        web = note.get("web_page") or {}
        source_url = web.get("url","")
        body_content = web.get("content") or note.get("content","")
        ai_excerpt   = web.get("excerpt","")
    elif note_type == "audio":
        audio = note.get("audio") or {}
        body_content = audio.get("original","")
        source_url   = audio.get("play_url","")
        ai_excerpt   = ""
    else:
        body_content = note.get("content","") or ""
        ai_excerpt   = ""

    # 标签列表（YAML格式）
    tag_items = tags[:]
    tag_items.append("get-笔记")
    tag_items.append(hermes.get("category","未分类").replace(" ","-"))
    if importance == "high":
        tag_items.append("重要")

    tags_yaml = "\n".join([f'  - "{t}"' for t in tag_items[:8]])

    # frontmatter
    lines = ["---",
             f'title: "{title}"']
    if source_url:
        lines.append(f'source: "{source_url}"')
    lines += [f'created: {created}',
              f'note_id: "{note_id}"',
              "tags:",
              tags_yaml,
              "---", ""]

    # 正文
    lines.append(f"# {title}")
    lines.append("")

    if ai_excerpt:
        lines += [f"> {ai_excerpt}", ""]

    if summary and summary != body_content[:150]:
        lines += ["## 摘要", "", summary, ""]

    if body_content.strip():
        lines += ["## 正文", "", body_content.strip(), ""]

    # 元数据
    lines += ["---",
              f"*来源：Get笔记 | 类型：{note_type} | 入库：{datetime.now():%Y-%m-%d %H:%M}*"]

    # 生成安全文件名（去掉非法字符）
    safe = re.sub(r'[\\/:*?"<>|]', '', title)
    safe = safe.strip()[:60] or note_id[:12]
    filename = f"{safe}.md"

    return filename, "\n".join(lines)

# ─────────── Gitee同步 ───────────
def gitee_push(msg: str) -> bool:
    try:
        subprocess.run(["git","add","-A"],   cwd=VAULT_DIR, capture_output=True, timeout=15)
        r = subprocess.run(["git","commit","-m", msg],
                           cwd=VAULT_DIR, capture_output=True, text=True, timeout=15)
        if "nothing to commit" in r.stdout:
            return False
        subprocess.run(
            ["git","push","origin","main","--force-with-lease"],
            cwd=VAULT_DIR, capture_output=True, timeout=30
        )
        return True
    except Exception as e:
        print(f"  ⚠️ Gitee push: {e}")
        return False

# ─────────── 印象笔记同步 ───────────
def evernote_thrift_call(method, extra_fields=b''):
    """调用印象笔记 NoteStore Thrift API"""
    import struct
    def ws(s):
        b = s.encode('utf-8')
        return struct.pack('>i', len(b)) + b
    msg  = struct.pack('>HH', 0x8001, 0x0001)
    msg += ws(method)
    msg += struct.pack('>i', 1)
    msg += struct.pack('>bh', 11, 1) + ws(EVERNOTE_TOKEN)
    msg += extra_fields
    msg += struct.pack('>b', 0)
    req = urllib.request.Request(EVERNOTE_NOTESTORE, data=msg, method='POST')
    req.add_header('Content-Type', 'application/x-thrift')
    req.add_header('Accept', 'application/x-thrift')
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read()

def evernote_get_note_content(guid):
    """获取单条笔记内容（ENML格式）"""
    import struct
    def ws(s):
        b = s.encode('utf-8')
        return struct.pack('>i', len(b)) + b
    # getNoteContent(authToken, guid)
    extra = struct.pack('>bh', 11, 2) + ws(guid)
    resp = evernote_thrift_call("getNoteContent", extra)
    # 提取字符串内容
    i, result = 0, ""
    while i < len(resp) - 6:
        if resp[i] == 11:
            slen = struct.unpack('>i', resp[i+3:i+7])[0]
            if 100 < slen < 100000:
                try:
                    s = resp[i+7:i+7+slen].decode('utf-8')
                    if '<?xml' in s or '<en-note' in s:
                        result = s; break
                except:
                    pass
        i += 1
    # 剥离ENML标签，提取纯文本
    import re
    text = re.sub(r'<[^>]+>', '', result)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    return text

def evernote_fetch_recent(max_notes=30):
    """获取最近更新的笔记（findNotesMetadata）"""
    import struct, urllib.request
    def ws(s):
        b = s.encode('utf-8')
        return struct.pack('>i', len(b)) + b
    def wi32(v): return struct.pack('>i', v)

    extra  = struct.pack('>bh', 12, 2)          # filter struct
    extra += struct.pack('>bh', 8, 1) + wi32(2) # order=UPDATED
    extra += struct.pack('>bh', 2, 2) + struct.pack('>b', 0)  # ascending=false
    extra += struct.pack('>b', 0)               # end filter
    extra += struct.pack('>bh', 8, 3) + wi32(0) # offset=0
    extra += struct.pack('>bh', 8, 4) + wi32(max_notes)
    extra += struct.pack('>bh', 12, 5)          # resultSpec
    extra += struct.pack('>bh', 2, 1) + struct.pack('>b', 1)   # includeTitle
    extra += struct.pack('>bh', 2, 5) + struct.pack('>b', 1)   # includeCreated
    extra += struct.pack('>bh', 2, 6) + struct.pack('>b', 1)   # includeUpdated
    extra += struct.pack('>bh', 2, 10) + struct.pack('>b', 1)  # includeNotebookGuid
    extra += struct.pack('>b', 0)               # end resultSpec

    resp = evernote_thrift_call("findNotesMetadata", extra)

    # 解析笔记元数据（guid + title）
    notes = []
    i = 0
    guids, titles = [], []
    while i < len(resp) - 6:
        if resp[i] == 11:
            slen = struct.unpack('>i', resp[i+3:i+7])[0]
            if 0 < slen < 500:
                try:
                    s = resp[i+7:i+7+slen].decode('utf-8')
                    # guid格式检测: 8-4-4-4-12
                    import re
                    if re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', s):
                        guids.append(s)
                    elif s.isprintable() and len(s) > 1 and not s.startswith('S='):
                        titles.append(s)
                except:
                    pass
        i += 1

    # 配对guid和title
    for idx, guid in enumerate(guids):
        title = titles[idx] if idx < len(titles) else f"笔记_{guid[:8]}"
        notes.append({"guid": guid, "title": title})
    return notes

def poll_evernote():
    """同步印象笔记最近更新"""
    import urllib.request
    state = load_state()
    processed_en = set(state.get("evernote_processed", []))

    try:
        recent = evernote_fetch_recent(30)
    except Exception as e:
        print(f"  ❌ 印象笔记拉取失败: {e}")
        return 0

    new_notes = [n for n in recent if n["guid"] not in processed_en]
    print(f"  [印象笔记] {len(recent)}条 → {len(new_notes)}条新增")
    if not new_notes:
        return 0

    saved = []
    for note in new_notes:
        guid  = note["guid"]
        title = note["title"]
        try:
            # 获取正文
            content = evernote_get_note_content(guid)

            # 构造虚拟note dict走Hermes分类
            mock = {"title": title, "content": content,
                    "note_type": "evernote", "tags": [],
                    "created_at": datetime.now().strftime("%Y-%m-%d")}
            hermes = hermes_classify(mock)

            # 生成Obsidian页面
            fname, md_content = build_obsidian_note(mock, hermes)
            # 标记来源
            md_content = md_content.replace(
                "*来源：Get笔记",
                f"*来源：印象笔记 (guid: {guid[:8]})"
            )

            target = VAULT_DIR / hermes["target_dir"]
            target.mkdir(parents=True, exist_ok=True)
            fp = target / fname
            if fp.exists():
                fp = target / f"{fp.stem}_{guid[:8]}.md"
            fp.write_text(md_content, encoding="utf-8")

            processed_en.add(guid)
            saved.append(title)
            print(f"  ✓ [EN/{hermes['category']}] {title[:40]} → {hermes['target_dir']}/")

        except Exception as e:
            print(f"  ❌ EN {title[:30]}: {e}")

    state["evernote_processed"] = list(processed_en)[-3000:]
    save_state(state)

    if saved:
        msg = f"evernote: {len(saved)}条笔记自动入库 {datetime.now():%Y-%m-%d %H:%M}"
        pushed = gitee_push(msg)
        print(f"  {'✅ Gitee同步完成' if pushed else '⚠️ nothing to push'}")

    return len(saved)

# ─────────── 主流程 ───────────
def poll_once():
    state = load_state()
    processed = set(state.get("processed_ids", []))
    cursor    = state.get("last_cursor", "")

    # 拉笔记列表
    params = {}
    if cursor:
        params["cursor"] = cursor
    resp = api_get("note/list", params)
    if not resp.get("success"):
        print("  ❌ 笔记列表失败:", resp.get("message",""))
        return 0

    data  = resp.get("data",{})
    notes = data.get("notes", [])
    new_cursor = data.get("cursor", cursor)
    new_notes  = [n for n in notes if str(n.get("note_id","")) not in processed]

    print(f"  [Get笔记] {len(notes)}条 → {len(new_notes)}条新增")
    if not new_notes:
        state["last_cursor"] = new_cursor
        save_state(state)
        return 0

    saved = []
    for note in new_notes:
        nid   = str(note.get("note_id",""))
        title = note.get("title","无标题")
        try:
            # 获取详情
            dr = api_get("note/detail", {"id": nid})
            if dr.get("success"):
                note = dr["data"]["note"]

            hermes = hermes_classify(note)
            fname, content = build_obsidian_note(note, hermes)

            target = VAULT_DIR / hermes["target_dir"]
            target.mkdir(parents=True, exist_ok=True)
            fp = target / fname
            # 去重检查
            if fp.exists():
                base, ext = fp.stem, fp.suffix
                fp = target / f"{base}_{nid[:8]}{ext}"
            fp.write_text(content, encoding="utf-8")

            processed.add(nid)
            saved.append((hermes["target_dir"], fname))
            print(f"  ✓ [{hermes['category']}] {title[:40]} → {hermes['target_dir']}/")

        except Exception as e:
            print(f"  ❌ {title[:30]}: {e}")

    state["last_cursor"]   = new_cursor
    state["processed_ids"] = list(processed)[-3000:]
    save_state(state)

    if saved:
        msg = f"get-note: {len(saved)}条笔记自动入库 {datetime.now():%Y-%m-%d %H:%M}"
        pushed = gitee_push(msg)
        print(f"  {'✅ Gitee同步完成' if pushed else '⚠️ Gitee: nothing to push'}")

    return len(saved)

# ─────────── 入口 ───────────
if __name__ == "__main__":
    import sys
    # 确保vault的git remote指向正确
    subprocess.run(["git","remote","set-url","origin", GITEE_URL],
                   cwd=VAULT_DIR, capture_output=True)
    subprocess.run(["git","config","user.name","iNEST-KB-Bot"],
                   cwd=VAULT_DIR, capture_output=True)
    subprocess.run(["git","config","user.email","qinrangliu@gmail.com"],
                   cwd=VAULT_DIR, capture_output=True)

    once     = "--once"     in sys.argv
    en_only  = "--evernote" in sys.argv
    gn_only  = "--getnote"  in sys.argv
    print(f"🚀 知识库自动进化引擎 v2.1")
    print(f"   Vault: {VAULT_DIR}")
    print(f"   数据源: Get笔记 + 印象笔记 → Gitee iBrainNest/i-nest (main)")
    print()

    def run_all():
        n1 = poll_once()      if not en_only else 0
        n2 = poll_evernote()  if not gn_only else 0
        return n1 + n2

    if once:
        run_all()
    else:
        print("持续轮询模式（每5分钟） — Ctrl+C停止")
        while True:
            try:
                run_all()
            except KeyboardInterrupt:
                print("\n⏹ 已停止"); break
            except Exception as e:
                print(f"  ⚠️ 轮询异常: {e}")
            time.sleep(300)
