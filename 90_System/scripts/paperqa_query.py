#!/usr/bin/env python3
"""
iNEST PaperQA2 接口
对 Obsidian 知识库中的 PDF/论文做精准问答
用法: python3 paperqa_query.py "你的问题"
"""
import sys, os, asyncio
from pathlib import Path

PAPERS_DIR = Path('/home/work/obsidian-vault/02_Papers')
VAULT_DIR = Path('/home/work/obsidian-vault')

# PaperQA2 需要 ANTHROPIC_API_KEY（已在环境变量中）
os.environ.setdefault('ANTHROPIC_API_KEY', os.environ.get('ANTHROPIC_API_KEY', ''))

async def query(question: str):
    try:
        from paperqa import Settings, ask
        from paperqa.settings import AgentSettings
    except ImportError:
        print('❌ paper-qa 未安装: pip3 install paper-qa --break-system-packages')
        return

    print(f'🔍 问题: {question}')
    print(f'📁 知识库: {PAPERS_DIR}')
    print('...\n')

    settings = Settings(
        llm='claude-sonnet-4-6',
        summary_llm='claude-haiku-4-5',
        paper_directory=str(PAPERS_DIR),
        verbosity=1,
    )

    answer = await ask(question, settings=settings)
    print('\n' + '='*60)
    print('📝 答案:\n')
    print(answer.answer)
    if hasattr(answer, 'references') and answer.references:
        print('\n📚 引用来源:')
        for ref in answer.references[:5]:
            print(f'  - {ref}')

if __name__ == '__main__':
    question = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else \
        'What is the relationship between self-organized criticality and neural computation in C. elegans?'
    asyncio.run(query(question))
