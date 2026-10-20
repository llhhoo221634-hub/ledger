#!/usr/bin/env python3
"""恢复：用 dl.html 作基线 + new_style.css + app.js 重新组装账本单文件版。"""
import pathlib, re

BASE = pathlib.Path('/tmp/dl.html')
CSS   = pathlib.Path('/tmp/new_style.css')
JSM   = pathlib.Path('/tmp/app.js')
OUT   = pathlib.Path('/var/minis/workspace/ledger/账本.html')

html = BASE.read_text(encoding='utf-8')
css  = CSS.read_text(encoding='utf-8')
js   = JSM.read_text(encoding='utf-8')

# SVG 描边跟随 currentColor
css = css.replace('.ic svg{width:21px;height:21px;fill:none;stroke-width:1.9;',
                  '.ic svg{width:21px;height:21px;fill:none;stroke:currentColor;stroke-width:1.9;')
css = css.replace('.cbtn .b svg{width:25px;height:25px;fill:none;stroke-width:1.9;',
                  '.cbtn .b svg{width:25px;height:25px;fill:none;stroke:currentColor;stroke-width:1.9;')
css = css.replace('.crow2 .nm svg{width:15px;height:15px;fill:none;stroke-width:2;',
                  '.crow2 .nm svg{width:15px;height:15px;fill:none;stroke:currentColor;stroke-width:2;')

old_style = re.search(r'<style>.*?</style>', html, re.S).group(0)
html = html.replace(old_style, '<style>\n' + css.strip() + '\n</style>')

# 替换主脚本（最后一个 script 块）
blocks = list(re.finditer(r'<script>(.*?)</script>', html, re.S))
main = blocks[-1]
html = html[:main.start(1)] + js.strip() + html[main.end(1):]

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(html, encoding='utf-8')

print('✅ 输出', OUT)
print('   体积 %d 字节' % len(html.encode()))
print('   残留 emoji:', len(re.findall(r'[🍚🥤🚬📱🧴🚌🎮📦💰🧾]', html)))
print('   svgIcon 调用:', html.count('svgIcon'))
