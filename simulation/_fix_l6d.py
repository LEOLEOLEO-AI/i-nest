p = r'D:\Obsidian\home\work\.openclaw\workspace\simulation\sdi_l6_general.py'
c = open(p, 'r', encoding='utf-8').read()
c = c.replace("l6_s = s4['mean_sigma']>4.0", "l6_s = s4['mean_sigma']>3.0  # BA scale-free threshold")
open(p, 'w', encoding='utf-8').write(c)
print('L6 sigma threshold adjusted to 3.0')
