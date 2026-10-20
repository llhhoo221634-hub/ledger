#!/usr/bin/env python3
"""收尾打磨：修收支空进度条 + 压缩记账面板高度，保证「记一笔」一屏可见。"""
import pathlib

P = pathlib.Path('/var/minis/workspace/ledger/账本.html')
h = P.read_text(encoding='utf-8')

# ---------- 1) 本月收支：三条空条 → 按比例填充 ----------
old = """  const inc=S.tx.filter(t=>thisMonth(t.d)&&!isExp(t)).reduce((a,t)=>a+t.amt,0);
  $('sSum').innerHTML=
    '<div class="crow2"><span class="dot" style="background:#FF6B81"></span><span class="nm">支出</span>'+
    '<span class="pb"></span><span class="vl">'+money(total)+'</span><span class="pc"></span></div>'+
    '<div class="crow2"><span class="dot" style="background:#2BD97C"></span><span class="nm">收入</span>'+
    '<span class="pb"></span><span class="vl">'+money(inc)+'</span><span class="pc"></span></div>'+
    '<div class="crow2"><span class="dot" style="background:#4C9AFF"></span><span class="nm">结余</span>'+
    '<span class="pb"></span><span class="vl" style="color:#fff">'+money(inc-total)+'</span><span class="pc"></span></div>';"""
new = """  const inc=S.tx.filter(t=>thisMonth(t.d)&&!isExp(t)).reduce((a,t)=>a+t.amt,0);
  const mx=Math.max(total,inc,1), net=inc-total;
  const bar=(v,c)=>'<span class="pb"><i style="width:'+Math.round(Math.abs(v)/mx*100)+'%;background:'+c+'"></i></span>';
  $('sSum').innerHTML=
    '<div class="crow2"><span class="dot" style="background:#FF6B81"></span><span class="nm">支出</span>'+
    bar(total,'#FF6B81')+'<span class="vl">'+money(total)+'</span><span class="pc">'+(total?Math.round(total/(total+inc||1)*100)+'%':'')+'</span></div>'+
    '<div class="crow2"><span class="dot" style="background:#2BD97C"></span><span class="nm">收入</span>'+
    bar(inc,'#2BD97C')+'<span class="vl">'+money(inc)+'</span><span class="pc">'+(inc?Math.round(inc/(total+inc||1)*100)+'%':'')+'</span></div>'+
    '<div class="crow2"><span class="dot" style="background:#4C9AFF"></span><span class="nm">结余</span>'+
    bar(net, net<0?'#FF6B81':'#5AA2FF')+'<span class="vl" style="color:'+(net<0?'var(--red)':'var(--green)')+'">'+money(net)+'</span><span class="pc"></span></div>';"""
assert old in h, '收支块没匹配上'
h = h.replace(old, new)

# ---------- 2) 面板压缩：一屏放下 ----------
pairs = [
 ('.sheet{position:fixed;left:0;right:0;bottom:0;z-index:90;margin:0 auto;max-width:640px;\n'
  '  max-height:94vh;overflow-y:auto;padding:0 16px calc(16px + var(--safe));',
  '.sheet{position:fixed;left:0;right:0;bottom:0;z-index:90;margin:0 auto;max-width:640px;\n'
  '  max-height:96vh;overflow-y:auto;padding:0 14px calc(12px + var(--safe));'),
 ('.handle{width:40px;height:4px;border-radius:3px;background:rgba(255,255,255,.2);margin:10px auto 14px}',
  '.handle{width:40px;height:4px;border-radius:3px;background:rgba(255,255,255,.2);margin:8px auto 11px}'),
 ('.crow{display:flex;gap:9px;overflow-x:auto;padding:2px 0 14px;scroll-snap-type:x mandatory}',
  '.crow{display:flex;gap:8px;overflow-x:auto;padding:1px 0 11px;scroll-snap-type:x mandatory}'),
 ('.cbtn{flex:none;width:64px;display:flex;flex-direction:column;align-items:center;gap:6px;',
  '.cbtn{flex:none;width:60px;display:flex;flex-direction:column;align-items:center;gap:5px;'),
 ('.cbtn .b{width:54px;height:54px;border-radius:19px;',
  '.cbtn .b{width:50px;height:50px;border-radius:17px;'),
 ('.daysel{display:flex;gap:8px;padding:0 2px 11px}',
  '.daysel{display:flex;gap:8px;padding:0 2px 9px}'),
 ('.daysel button{flex:1;padding:9px 0;', '.daysel button{flex:1;padding:8px 0;'),
 ('.amtline{text-align:right;font-size:42px;font-weight:800;letter-spacing:-2px;\n'
  '  font-variant-numeric:tabular-nums;padding:2px 4px 14px;min-height:58px;\n'
  '  border-bottom:1px solid var(--hair);margin-bottom:14px}',
  '.amtline{text-align:right;font-size:38px;font-weight:800;letter-spacing:-1.8px;\n'
  '  font-variant-numeric:tabular-nums;padding:0 4px 9px;min-height:50px;\n'
  '  border-bottom:1px solid var(--hair);margin-bottom:10px}'),
 ('.np{display:grid;grid-template-columns:repeat(3,1fr);gap:9px}',
  '.np{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}'),
 ('.np button{padding:16px 0;border-radius:16px;font-size:23px;',
  '.np button{padding:13px 0;border-radius:16px;font-size:22px;'),
 ('.savenote{width:100%;margin:13px 0;padding:13px 15px;',
  '.savenote{width:100%;margin:10px 0;padding:11px 14px;'),
 ('.gobtn{width:100%;padding:16px;border:0;border-radius:17px;font-size:16.5px;',
  '.gobtn{width:100%;padding:14px;border:0;border-radius:16px;font-size:16.5px;'),
]
for a,b in pairs:
    assert a in h, '没匹配上: '+a[:40]
    h = h.replace(a,b)

P.write_text(h, encoding='utf-8')
print('✅ 打磨完成 %d 字节' % len(h.encode()))
