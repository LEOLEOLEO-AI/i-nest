#!/usr/bin/env python3
"""
iNEST PaperQA2 PDF 索引构建器
用法：
  python3 paperqa_index.py              # 索引所有 PDF
  python3 paperqa_index.py "你的问题"   # 直接提问
"""
import sys, os, asyncio
from pathlib import Path

PDF_DIR = Path('/home/work/obsidian-vault/02_Papers/pdf')
INDEX_DIR = Path('/home/work/obsidian-vault/02_Papers/paperqa-index')
INDEX_DIR.mkdir(parents=True, exist_ok=True)

# 使用已配置的 Genspark Anthropic 代理
os.environ.setdefault('ANTHROPIC_BASE_URL', 'https://www.genspark.ai/api/anthropic')

async def build_index():
    from paperqa import Settings, Docs
    pdfs = list(PDF_DIR.glob('**/*.pdf'))
    print(f'找到 {len(pdfs)} 个 PDF 文件')
    if not pdfs:
        print(f'请把 PDF 放入: {PDF_DIR}')
        return None

    settings = Settings(
        llm='claude-sonnet-4-6',
        summary_llm='claude-haiku-4-5',
        paper_directory=str(PDF_DIR),
    )

    docs = Docs()
    for i, pdf in enumerate(pdfs, 1):
        print(f'  [{i}/{len(pdfs)}] 索引: {pdf.name}')
        try:
            await docs.aadd(str(pdf), settings=settings)
        except Exception as e:
            print(f'    跳过（错误: {e}）')

    # 保存索引
    index_path = INDEX_DIR / 'docs.pkl'
    import pickle
    with open(index_path, 'wb') as f:
        pickle.dump(docs, f)
    print(f'\n✅ 索引已保存: {index_path}')
    print(f'   共索引 {len(pdfs)} 篇文献')
    return docs

async def query(question: str, docs=None):
    from paperqa import Settings, Docs, ask
    import pickle

    index_path = INDEX_DIR / 'docs.pkl'
    if docs is None:
        if not index_path.exists():
            print('❌ 索引不存在，请先运行: python3 paperqa_index.py')
            return
        with open(index_path, 'rb') as f:
            docs = pickle.load(f)

    settings = Settings(
        llm='claude-sonnet-4-6',
        summary_llm='claude-haiku-4-5',
    )

    print(f'\n🔍 问题: {question}\n')
    answer = await docs.aquery(question, settings=settings)

    print('=' * 60)
    print('📝 答案:\n')
    print(answer.answer)

    if hasattr(answer, 'context') and answer.context:
        print('\n📚 引用来源:')
        seen = set()
        for ctx in answer.context[:5]:
            src = getattr(ctx, 'text', {})
            name = getattr(src, 'name', '') if hasattr(src, 'name') else str(src)[:60]
            if name not in seen:
                seen.add(name)
                print(f'  - {name}')

async def main():
    if len(sys.argv) > 1:
        question = ' '.join(sys.argv[1:])
        await query(question)
    else:
        docs = await build_index()
        if docs:
            # 建完索引后跑一个测试问题
            test_q = 'What is the main contribution of these papers related to neural criticality or TCC?'
            await query(test_q, docs)

if __name__ == '__main__':
    asyncio.run(main())
