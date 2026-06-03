with open(r'D:\Research\research_platform\dashboard\index.html', 'r', encoding='utf-8-sig') as f: lines = f.readlines()  
new_paper = lines[405:413]  
new_insight = lines[416:424]  
print('old_paper:', new_paper[0].strip()[:50])  
print('old_insight:', new_insight[0].strip()[:50])  
print('Total lines:', len(lines))  
