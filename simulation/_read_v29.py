import json
d = json.load(open(r'D:\Obsidian\home\work\.openclaw\workspace\simulation\data\v28_results\v29_results.json', 'r', encoding='utf-8'))
print('V29 keys:', list(d.keys()))
for k, v in d.items():
    if isinstance(v, dict):
        sf = v.get('sigma_final', '?')
        ef = v.get('el_final', '?')
        print(f'  {k}: sigma={sf}, el={ef}')
    else:
        print(f'  {k}: {type(v).__name__}')
