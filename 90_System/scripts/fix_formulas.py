import re
from pathlib import Path
from openai import OpenAI

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
md_path = VAULT / "30_TCC/31_Theory/tcc_paper_background.md"
content = md_path.read_text(encoding="utf-8")

# Find sections with corrupted formula fragments
# Single letters on their own lines, or lines with only Greek/symbol chars
corrupted_lines = []
for i, line in enumerate(content.split("\n")):
    stripped = line.strip()
    if len(stripped) <= 3 and len(stripped) > 0:
        if re.match(r'^[A-Za-zΓΔΣΩαβγδεηθλμνξπρστφχψω∞∂∫∏∑√∇]+$', stripped):
            corrupted_lines.append((i, stripped))

print(f"Found {len(corrupted_lines)} corrupted formula fragments")

# Use DeepSeek to reconstruct formulas
if corrupted_lines:
    # Show context around corrupted lines
    lines = content.split("\n")
    context_samples = []
    for idx, frag in corrupted_lines[:10]:
        ctx_start = max(0, idx-2)
        ctx_end = min(len(lines), idx+3)
        ctx = "\n".join(lines[ctx_start:ctx_end])
        context_samples.append(f"Context (line {idx}, fragment: '{frag}'):\n{ctx}")
    
    print("Sample contexts:")
    for cs in context_samples[:5]:
        print(cs[:200])
        print("---")
else:
    print("No corrupted fragments found - checking other patterns")
    # Also check for common formula corruption patterns
    for i, line in enumerate(content.split("\n")):
        stripped = line.strip()
        # Check for isolated Greek letters
        if re.match(r'^[α-ωΑ-Ω]+$', stripped):
            print(f"  Line {i}: '{stripped}'")
        # Check for lines that are just equation numbers like (1), (2)
        if re.match(r'^\(\d+\)$', stripped):
            print(f"  Line {i}: '{stripped}'")
