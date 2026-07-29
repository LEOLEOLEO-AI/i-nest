import os, json, sys, time
sys.stdout.reconfigure(encoding='utf-8')
import openai

vault = r'D:\Obsidian\vault'

with open(os.path.join(vault, '90_System/scripts/classify_ambiguous.json'), 'r', encoding='utf-8') as f:
    ambiguous = json.load(f)

client = openai.OpenAI(
    api_key='REDACTED_LEAKED_DEEPSEEK',
    base_url='https://api.deepseek.com/v1'
)

# Target options
targets = [
    '30_TCC/31_Theory', '30_TCC/32_Tech', '30_TCC/33_Dev',
    '30_TCC/34_Projects', '30_TCC/35_Simulation',
    '40_iNEST/41_Theory', '40_iNEST/42_Tech', '40_iNEST/43_Engineering',
    '40_iNEST/44_Projects', '40_iNEST/45_Simulation',
    'SKIP'  # not relevant to TCC/iNEST
]

batch_size = 25
results = {}

for i in range(0, len(ambiguous), batch_size):
    batch = ambiguous[i:i+batch_size]
    
    file_list = '\n'.join([
        '%d. [%dB] %s\n   %s' % (j, size, rel, preview[:200].replace('\n',' '))
        for j, (rel, size, preview) in enumerate(batch)
    ])
    
    prompt = """Classify each file into exactly ONE of these directories:

TCC (Topology-Centric Computing): 30_TCC/31_Theory, 30_TCC/32_Tech, 30_TCC/33_Dev, 30_TCC/34_Projects, 30_TCC/35_Simulation
iNEST (Neuromorphic Engineering): 40_iNEST/41_Theory, 40_iNEST/42_Tech, 40_iNEST/43_Engineering, 40_iNEST/44_Projects, 40_iNEST/45_Simulation
SKIP: not relevant to TCC or iNEST research

Guidelines:
- Chip, wafer, semiconductor, memristor, NoC, interconnect, VLSI, chiplet, packaging, fabrication → TCC
- Brain, neuron, neural, neuroscience, cognition, SNN, spiking, avalanche, criticality, dynamics, complex networks, emergence → iNEST
- Free energy, active inference, reservoir computing → iNEST
- AI/ML papers without specific chip/brain focus → SKIP
- General articles, news, non-research → SKIP
- _dup files are duplicates from 得到APP, classify based on content topic

Respond with ONLY a JSON object mapping file index numbers to target directories. Example: {"0": "40_iNEST/41_Theory", "1": "30_TCC/32_Tech", "2": "SKIP"}

Files:
""" + file_list

    print('Batch %d/%d (%d files)...' % (i//batch_size + 1, (len(ambiguous)+batch_size-1)//batch_size, len(batch)))
    
    try:
        resp = client.chat.completions.create(
            model='deepseek-chat',
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.1,
            max_tokens=2000
        )
        text = resp.choices[0].message.content.strip()
        # Extract JSON
        if '`' in text:
            text = text.split('`')[1]
            if text.startswith('json'):
                text = text[4:]
        parsed = json.loads(text)
        for k, v in parsed.items():
            idx = int(k)
            if idx < len(batch):
                rel = batch[idx][0]
                results[rel] = v
        print('  Got %d classifications' % len(parsed))
    except Exception as e:
        print('  ERROR: %s' % str(e)[:100])
        # Fallback: SKIP
        for j, (rel, size, _) in enumerate(batch):
            if rel not in results:
                results[rel] = 'SKIP'
    
    if i + batch_size < len(ambiguous):
        time.sleep(1)  # Rate limit

# Save results
with open(os.path.join(vault, '90_System/scripts/classify_llm.json'), 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# Stats
tcc = sum(1 for v in results.values() if v.startswith('30_TCC'))
inest = sum(1 for v in results.values() if v.startswith('40_iNEST'))
skip = sum(1 for v in results.values() if v == 'SKIP')
print('')
print('Done! TCC: %d, iNEST: %d, SKIP: %d, Total: %d' % (tcc, inest, skip, len(results)))
