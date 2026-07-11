"""
全局中文字体修复模块
在任何需要中文图表的脚本顶部 import 此模块
用法：import fix_chinese_font  # noqa
"""
import matplotlib as mpl
import matplotlib.font_manager as fm
import os

_TTF = '/home/work/.local/lib/python3.12/site-packages/matplotlib/mpl-data/fonts/ttf/NotoSansCJKsc-Regular.ttf'

def _setup():
    if not os.path.exists(_TTF):
        # 尝试提取
        try:
            from fontTools.ttLib import TTCollection
            ttc = TTCollection('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
            ttc[2].save(_TTF)
        except Exception as e:
            print(f"[fix_chinese_font] 字体提取失败: {e}")
            return

    fm.fontManager.addfont(_TTF)
    mpl.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'Noto Sans CJK JP', 'DejaVu Sans']
    mpl.rcParams['axes.unicode_minus'] = False
    mpl.rcParams['font.family'] = 'sans-serif'

_setup()
