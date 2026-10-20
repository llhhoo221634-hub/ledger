#!/usr/bin/env python3
"""v2 细节返工：图标、比例条、面板留白、目标百分比。"""
import pathlib

P = pathlib.Path('/var/minis/workspace/ledger/账本.html')
h = P.read_text(encoding='utf-8')

pairs = [
 # 吃饭：碗 + 热气（原来像笑脸）
 ('<path d="M4.6 11a7.4 7.4 0 0 0 14.8 0M3.4 11h17.2M8.6 4.6c0 1.2.9 1.6.9 2.8M12.4 3.4c0 1.4 1 1.8 1 3.2M16.2 4.6c0 1.2.9 1.6.9 2.8"/>',
  '<path d="M3 11.4h18a9 9 0 0 1-18 0z"/><path d="M8 7.6c0-1.1 1-1.4 1-2.5M12.2 6.6c0-1.3 1-1.6 1-2.9M16.4 7.6c0-1.1 1-1.4 1-2.5"/>'),
 # 烟：细长香烟 + 两缕烟
 ('<rect x="2.6" y="13" width="16" height="4.2" rx="2.1"/><path d="M15.6 13v4.2"/><path d="M18.4 10.4c1.3-1.1.2-2.4 1-3.6M15 10.4c1.3-1.1.2-2.4 1-3.6"/>',
  '<rect x="2.4" y="14.4" width="15.2" height="3.4" rx="1.7"/><path d="M20.4 14.4v3.4"/><path d="M17.4 11.6c1.5-1.1.3-2.4 1.2-3.6M13.6 11.6c1.5-1.1.3-2.4 1.2-3.6"/>'),
 # 底部导航「设置」：从太阳改成滑杆
 ('<circle cx="12" cy="12" r="3"/><path d="M12 2.6v2.2M12 19.2v2.2M4.4 4.4l1.6 1.6M18 18l1.6 1.6M2.6 12h2.2M19.2 12h2.2M4.4 19.6 6 18M18 6l1.6-1.6"/>',
  '<path d="M4 7.5h9M17.5 7.5h2.5M4 16.5h4M12.5 16.5h7.5"/><circle cx="15" cy="7.5" r="2.4"/><circle cx="10" cy="16.5" r="2.4"/>'),
 # 统计分类条：改成占总额比例，和右侧百分比对齐
 ("'<span class=\"pb\"><i style=\"width:'+(v/(arr[0][1]||1)*100)+'%;background:'+k[2]+'\"></i></span>'+",
  "'<span class=\"pb\"><i style=\"width:'+Math.max(2,v/(total||1)*100)+'%;background:'+k[2]+'\"></i></span>'+"),
 # 面板底部留白
 ('max-height:96vh;overflow-y:auto;padding:0 14px calc(12px + var(--safe));',
  'max-height:96vh;overflow-y:auto;padding:0 14px calc(18px + var(--safe));'),
 # 金额行加左侧标签
 ('.amtline{text-align:right;font-size:40px;',
  '.amtline{position:relative;text-align:right;font-size:40px;'),
 ('.amtline i{font-style:normal;font-size:20px;color:var(--dim);margin-right:3px}',
  '.amtline i{font-style:normal;font-size:20px;color:var(--dim);margin-right:3px}\n'
  '.amtline::before{content:"金额";position:absolute;left:4px;bottom:14px;font-size:11px;'
  'letter-spacing:.12em;color:var(--dim2);font-weight:600;text-transform:uppercase}'),
 # 底部 Dock 激活态收敛
 ('.tab{position:relative;flex:1;display:flex;flex-direction:column;align-items:center;gap:3px;\n'
  '  color:var(--dim2);font-size:9.5px;letter-spacing:.02em;padding:5px 0 3px;cursor:pointer;\n'
  '  border-radius:18px;transition:color .2s,background .2s}',
  '.tab{position:relative;flex:1;display:flex;flex-direction:column;align-items:center;gap:3px;\n'
  '  color:var(--dim2);font-size:9.5px;letter-spacing:.02em;padding:6px 0 4px;margin:0 3px;cursor:pointer;\n'
  '  border-radius:16px;border:1px solid transparent;transition:color .2s,background .2s,border-color .2s}'),
 ('.tab.on{color:#FF9BAF;background:rgba(255,122,147,.1)}',
  '.tab.on{color:#FF9BAF;background:linear-gradient(180deg,rgba(255,122,147,.16),rgba(255,122,147,.06));\n'
  '  border-color:rgba(255,122,147,.18)}'),
 # 统计柱状图普通柱更可见
 ('.bars div{flex:1;min-height:3px;border-radius:3px 3px 2px 2px;background:rgba(255,255,255,.07);',
  '.bars div{flex:1;min-height:3px;border-radius:3px 3px 2px 2px;background:rgba(255,255,255,.11);'),
]
for a, b in pairs:
    assert a in h, '没匹配上: ' + a[:50]
    h = h.replace(a, b)

# 目标卡：把百分比写进副标题
h = h.replace("'<em>目标 '+money(g.t).replace('¥','¥')+'</em></span>'+",
              "'<em>目标 '+money(g.t).replace('¥','¥')+' · '+Math.round(pct)+'%</em></span>'+")

P.write_text(h, encoding='utf-8')
print('✅ 返工完成 %d 字节' % len(h.encode()))
