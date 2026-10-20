#!/usr/bin/env python3
"""把新设计系统套用到账本源码上：换 CSS + emoji 图标换 SVG。"""
import pathlib
import re

SRC = pathlib.Path('/var/minis/workspace/账本App/src/index.html')
CSS = pathlib.Path('/tmp/new_style.css')

html = SRC.read_text(encoding='utf-8')
css = CSS.read_text(encoding='utf-8')

# SVG 图标的 stroke 跟随 currentColor
css = css.replace('.ic svg{width:21px;height:21px;fill:none;stroke-width:1.9;',
                  '.ic svg{width:21px;height:21px;fill:none;stroke:currentColor;stroke-width:1.9;')
css = css.replace('.cbtn .b svg{width:25px;height:25px;fill:none;stroke-width:1.9;',
                  '.cbtn .b svg{width:25px;height:25px;fill:none;stroke:currentColor;stroke-width:1.9;')
css = css.replace('.crow2 .nm svg{width:15px;height:15px;fill:none;stroke-width:2;',
                  '.crow2 .nm svg{width:15px;height:15px;fill:none;stroke:currentColor;stroke-width:2;')

# ---------- 1) 整块替换 <style> ----------
old_css = re.search(r'<style>.*?</style>', html, re.S).group(0)
html = html.replace(old_css, '<style>\n' + css.strip() + '\n</style>')

# ---------- 2) 分类表：emoji → SVG 路径 ----------
ICONS = {
    '吃饭': '<path d="M4.6 11a7.4 7.4 0 0 0 14.8 0M3.4 11h17.2M8.6 4.6c0 1.2.9 1.6.9 2.8M12.4 3.4c0 1.4 1 1.8 1 3.2M16.2 4.6c0 1.2.9 1.6.9 2.8"/>',
    '饮料零食': '<path d="M5.6 8.2h12.8l-1.3 11.6a2 2 0 0 1-2 1.7H8.9a2 2 0 0 1-2-1.7zM3.8 8.2h16.4M9.4 4.6h5.2"/>',
    '烟': '<path d="M2.8 13.4h13.6a1.2 1.2 0 0 1 1.2 1.2v3.2a1.2 1.2 0 0 1-1.2 1.2H2.8zM8.8 13.4v5.6M20.6 13.4v5.6"/>',
    '话费': '<path d="M7.2 2.6h9.6a2 2 0 0 1 2 2v14.8a2 2 0 0 1-2 2H7.2a2 2 0 0 1-2-2V4.6a2 2 0 0 1 2-2zM10.6 5.6h2.8M11 18.6h2"/>',
    '日用': '<path d="M9.6 2.6h4.8v3.2l1.7 2.2V20a1.6 1.6 0 0 1-1.6 1.6H9.5A1.6 1.6 0 0 1 7.9 20V8l1.7-2.2zM8 12.4h8"/>',
    '交通': '<rect x="3.4" y="3.6" width="17.2" height="11.4" rx="2"/><path d="M3.4 9.4h17.2"/><circle cx="8" cy="18" r="1.7"/><circle cx="16" cy="18" r="1.7"/>',
    '娱乐': '<rect x="2.6" y="6.4" width="18.8" height="11.2" rx="5.6"/><path d="M8 10.2v4M6 12.2h4"/><circle cx="16" cy="11.4" r="1"/><circle cx="18" cy="13.4" r="1"/>',
    '其他': '<path d="M3.6 7.6 12 3.1l8.4 4.5v8.8L12 20.9l-8.4-4.5z"/><path d="M3.6 7.6 12 12.1l8.4-4.5M12 12.1v8.8"/>',
    '收入': '<path d="M12 3.4v11.2M7.6 10.4 12 14.8l4.4-4.4M4.2 19.6h15.6"/>',
}
COLORS = {
    '吃饭': '#FF8A4C', '饮料零食': '#FFB74D', '烟': '#A78BFA', '话费': '#5AA2FF',
    '日用': '#22D3EE', '交通': '#34D399', '娱乐': '#F472B6', '其他': '#94A3B8', '收入': '#34D97B',
}
order = ['吃饭', '饮料零食', '烟', '话费', '日用', '交通', '娱乐', '其他']
cat_lines = []
for i in range(0, len(order), 3):
    chunk = order[i:i + 3]
    cat_lines.append('  ' + ','.join("['%s','%s','%s']" % (n, ICONS[n], COLORS[n]) for n in chunk))
new_cats = ("const CATS=[\n" + ',\n'.join(cat_lines) + "\n];\n"
            "const INCOME=['收入','%s','%s'];\n"
            "/* 线性图标：fill:none + stroke:currentColor，颜色由外层 color 决定 */\n"
            "const svgIcon=(inner,style)=>'<svg viewBox=\"0 0 24 24\"'+(style?' style=\"'+style+'\"':'')+'>'+inner+'</svg>';\n"
            "const ICON_EMPTY='<path d=\"M5 3.6h11.2a2 2 0 0 1 2 2V21l-3.4-2.4H5a2 2 0 0 1-2-2V5.6a2 2 0 0 1 2-2z\"/><path d=\"M7.6 8.4h8M7.6 12h5.2\"/>';"
            % (ICONS['收入'], COLORS['收入']))
old_cats = ("const CATS=[\n"
            "  ['吃饭','🍚','#FF7A45'],['饮料零食','🥤','#FFB020'],['烟','🚬','#A78BFA'],\n"
            "  ['话费','📱','#4C9AFF'],['日用','🧴','#22D3EE'],['交通','🚌','#34D399'],\n"
            "  ['娱乐','🎮','#F472B6'],['其他','📦','#94A3B8']\n"
            "];\n"
            "const INCOME=['收入','💰','#2BD97C'];")
assert old_cats in html, '分类表没匹配上'
html = html.replace(old_cats, new_cats)

# ---------- 3) 面板里的分类按钮 ----------
old = ("    d.innerHTML='<span class=\"b\" style=\"'+st+'\">'+c[1]+'</span>'+c[0];")
new = ("    d.innerHTML='<span class=\"b\" style=\"'+st+';color:'+c[2]+'\">'+svgIcon(c[1])+'</span>'+c[0];")
assert old in html, 'buildCats 没匹配上'
html = html.replace(old, new)

# ---------- 4) 流水行图标 ----------
old = ("      '<div class=\"ic\" style=\"background:'+c[2]+'22;border:1px solid '+c[2]+'33\">'+esc(c[1])+'</div>'+")
new = ("      '<div class=\"ic\" style=\"background:'+c[2]+'1E;border:1px solid '+c[2]+'3A;color:'+c[2]+'\">'+svgIcon(c[1])+'</div>'+")
assert old in html, '流水行图标没匹配上'
html = html.replace(old, new)

# ---------- 5) 统计页分类行 ----------
old = ("      '<span class=\"nm\">'+k[1]+' '+c+'</span>'+")
new = ("      '<span class=\"nm\">'+svgIcon(k[1],'color:'+k[2])+' '+c+'</span>'+")
assert old in html, '统计分类行没匹配上'
html = html.replace(old, new)

# ---------- 6) 空状态 ----------
old = ("    box.innerHTML='<div class=\"empty\"><em>🧾</em>还没有记录<br>点下面中间那个 ＋ 记第一笔</div>';")
new = ("    box.innerHTML='<div class=\"empty\">'+svgIcon(ICON_EMPTY)+'还没有记录<br>点下面中间那个 ＋ 记第一笔</div>';")
assert old in html, '空状态没匹配上'
html = html.replace(old, new)

SRC.write_text(html, encoding='utf-8')
print('✅ 已套用新设计')
print('   文件 %d 字节' % len(html.encode()))
print('   残留 emoji 图标:', len(re.findall(r"'[🍚🥤🚬📱🧴🚌🎮📦💰🧾]'", html)))