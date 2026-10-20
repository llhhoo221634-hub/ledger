#!/usr/bin/env python3
"""v2 改版：极光背景 / 环形预算 / 7 日折线 / 环形占比 / 悬浮 Dock。"""
import pathlib

P = pathlib.Path('/var/minis/workspace/ledger/账本.html')
h = P.read_text(encoding='utf-8')
CSS = pathlib.Path('/tmp/style_v2.css').read_text(encoding='utf-8')

def cut(s, a, b, rep):
    i = s.index(a); j = s.index(b, i)
    return s[:i] + rep + s[j:]

# ---------- 1) 整块样式 ----------
i = h.index('<style>'); j = h.index('</style>') + len('</style>')
h = h[:i] + '<style>\n' + CSS.strip() + '\n</style>' + h[j:]

# ---------- 2) Hero + mini + 月度进度 ----------
HERO = '''<div class="hero" id="hero">
    <div class="orb"></div>
    <div class="htop">
      <div class="k">今天还能花</div>
      <div class="chip" id="hChip">—</div>
    </div>
    <div class="hrow">
      <div class="hval">
        <div class="big" id="hToday"><i>¥</i>0</div>
        <div class="sub" id="hSub">—</div>
      </div>
      <div class="ringwrap">
        <svg class="ring" viewBox="0 0 100 100" aria-hidden="true">
          <defs>
            <linearGradient id="ringGrad" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0" stop-color="#FFB56B"/><stop offset="1" stop-color="#E63A6B"/>
            </linearGradient>
          </defs>
          <circle class="rt" cx="50" cy="50" r="42"/>
          <circle class="rp" id="hRing" cx="50" cy="50" r="42"/>
        </svg>
        <div class="rlab"><b id="hPct">0</b><span>%</span><em>剩余</em></div>
      </div>
    </div>
    <svg class="spark" id="hSpark" viewBox="0 0 320 64" preserveAspectRatio="none" aria-hidden="true">
      <defs>
        <linearGradient id="sparkGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="rgba(255,150,90,.42)"/>
          <stop offset="1" stop-color="rgba(255,150,90,0)"/>
        </linearGradient>
      </defs>
      <path id="sparkArea" fill="url(#sparkGrad)"/>
      <path id="sparkLine" fill="none" stroke="#FFC59B" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round"/>
      <circle id="sparkDot" r="2.8" fill="#fff"/>
    </svg>
    <div class="sparklab"><span>近 7 天</span><span id="hWeek">—</span></div>
    <div class="meta">
      <span>额度 <b id="hQuota">–</b></span>
      <span>已花 <b id="hSpent">–</b></span>
      <span>剩 <b id="hDays">–</b> 天</span>
    </div>
    <div class="plus"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#fff"
      stroke-width="2.4" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg></div>
  </div>

  <div class="mini">
    <div><div class="k">本月还能花</div><div class="v b" id="mLeft">–</div></div>
    <div><div class="k">按计划能存下</div><div class="v g" id="mSave">–</div></div>
  </div>

  <div class="progc">
    <div class="ph"><span>本月额度已用</span><b id="pUse">0%</b></div>
    <div class="ptrack"><i id="pFill"></i></div>
  </div>

  '''
h = cut(h, '<div class="hero" id="hero">', '<div class="secttl"><span>最近记录', HERO)

# ---------- 3) 底部 Dock ----------
NAV = '''<nav class="tabbar">
  <div class="dock">
    <div class="tab" data-p="list">
      <svg viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h10"/></svg>明细
    </div>
    <div class="tab" data-p="stat">
      <svg viewBox="0 0 24 24"><path d="M5 19V9M12 19V5M19 19v-6"/></svg>统计
    </div>
    <div class="fab" id="fab"><svg viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg></div>
    <div class="tab" data-p="goal">
      <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3.2"/></svg>目标
    </div>
    <div class="tab" data-p="cfg">
      <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M12 2.6v2.2M12 19.2v2.2M4.4 4.4l1.6 1.6M18 18l1.6 1.6M2.6 12h2.2M19.2 12h2.2M4.4 19.6 6 18M18 6l1.6-1.6"/></svg>设置
    </div>
  </div>
</nav>'''
h = cut(h, '<nav class="tabbar">', '</nav>', NAV)

# ---------- 4) 统计页：chips + 环形占比 ----------
STAT = '''<div class="stathero">
    <div class="k">本月支出</div>
    <div class="v" id="sTotal">¥0</div>
    <div class="sc" id="sChips"></div>
    <div class="bars" id="sBars"></div>
    <div class="meta" style="display:flex;justify-content:space-between;font-size:10px;color:var(--dim2);margin-top:7px;border:0;padding-top:0">
      <span>1日</span><span>日支出曲线</span><span id="sLast">31日</span>
    </div>
  </div>
  <div class="secttl"><span>花在哪</span><b id="sCnt"></b></div>
  <div class="donutcard">
    <div class="donut">
      <svg viewBox="0 0 120 120" aria-hidden="true">
        <circle class="dt" cx="60" cy="60" r="48"/>
        <g id="dSegs"></g>
      </svg>
      <div class="dctr"><b id="dTotal">¥0</b><span>支出</span></div>
    </div>
    <div class="dlegend" id="dLeg"></div>
  </div>
  <div class="icard" style="padding:8px 14px;margin-top:10px"><div id="sCats"></div></div>
  '''
h = cut(h, '<div class="stathero">', '<div class="secttl"><span>本月收支', STAT)

# ---------- 5) renderList 重写 ----------
NEWLIST = '''/* ---------- 动效小工具 ---------- */
function countTo(el,to){
  const from=parseFloat(el.dataset.v||'0')||0;
  el.dataset.v=to;
  if(Math.abs(to-from)<0.005){el.innerHTML='<i>'+(to<0?'-':'')+'¥</i>'+money(to).replace(/-?¥/,'');return;}
  const t0=performance.now(),dur=560;
  (function frame(t){
    const k=Math.min(1,(t-t0)/dur),e=1-Math.pow(1-k,3),v=from+(to-from)*e;
    el.innerHTML='<i>'+(v<0?'-':'')+'¥</i>'+money(v).replace(/-?¥/,'');
    if(k<1)requestAnimationFrame(frame);
  })(t0);
}
function last7(){
  const out=[],d=new Date();
  for(let i=6;i>=0;i--){
    const dd=new Date(d.getFullYear(),d.getMonth(),d.getDate()-i),key=dstr(dd);
    out.push({v:S.tx.filter(t=>t.d===key&&isExp(t)).reduce((a,t)=>a+t.amt,0)});
  }
  return out;
}
function drawSpark(){
  const a=last7(),mx=Math.max(...a.map(x=>x.v),1);
  const W=320,H=64,px=8;
  const pts=a.map((x,i)=>[px+i*(W-px*2)/6,H-8-(x.v/mx)*(H-24)]);
  let d='M'+pts[0][0].toFixed(1)+' '+pts[0][1].toFixed(1);
  for(let i=1;i<pts.length;i++){
    const p0=pts[i-1],p1=pts[i],cx=(p0[0]+p1[0])/2;
    d+=' C'+cx.toFixed(1)+' '+p0[1].toFixed(1)+' '+cx.toFixed(1)+' '+p1[1].toFixed(1)+' '+p1[0].toFixed(1)+' '+p1[1].toFixed(1);
  }
  const line=$('sparkLine'),area=$('sparkArea'),dot=$('sparkDot');
  line.setAttribute('d',d);
  area.setAttribute('d',d+' L'+pts[6][0].toFixed(1)+' '+H+' L'+pts[0][0].toFixed(1)+' '+H+' Z');
  dot.setAttribute('cx',pts[6][0]);dot.setAttribute('cy',pts[6][1]);
  $('hWeek').textContent='共 '+money(a.reduce((s,x)=>s+x.v,0)).replace('¥','¥');
  try{
    const len=line.getTotalLength();
    line.style.transition='none';line.style.strokeDasharray=len;line.style.strokeDashoffset=len;
    requestAnimationFrame(()=>{line.style.transition='stroke-dashoffset .95s cubic-bezier(.22,1,.36,1)';line.style.strokeDashoffset=0;});
  }catch(e){}
}

function renderList(){
  const b=budget();
  countTo($('hToday'),b.perDay);
  $('hToday').style.opacity=b.perDay<0?.82:1;
  const pct=b.quota>0?Math.max(0,Math.min(1,b.left/b.quota)):0;
  $('hRing').style.strokeDashoffset=(263.9*(1-pct)).toFixed(1);
  $('hPct').textContent=Math.round(pct*100);
  $('hSub').textContent='额度 '+money(b.quota).replace('¥','¥')+' · 已花 '+money(b.spent).replace('¥','¥');
  $('hChip').textContent='本月 '+b.dom+' / '+b.dim+' 天';
  $('hQuota').textContent=money(b.quota).replace('¥','');
  $('hSpent').textContent=money(b.spent).replace('¥','');
  $('hDays').textContent=b.leftDays;
  $('mLeft').textContent=money(b.left);
  $('mLeft').className='v '+(b.left<0?'r':'b');
  $('mSave').textContent=money(S.cfg.save);
  const used=b.quota>0?Math.min(1,b.spent/b.quota):0;
  $('pFill').style.width=(used*100).toFixed(1)+'%';
  $('pUse').textContent=Math.round(used*100)+'%  ·  '+money(b.spent).replace('¥','¥')+' / '+money(b.quota).replace('¥','¥');
  drawSpark();

  const d=new Date();
  $('dToday').textContent=(d.getMonth()+1)+'月'+d.getDate()+'日 周'+'日一二三四五六'[d.getDay()];

  const mine=S.tx.filter(t=>thisMonth(t.d));
  $('cntLbl').textContent=mine.length?mine.length+' 笔':'';
  const box=$('list');
  if(!mine.length){
    box.innerHTML='<div class="empty">'+svgIcon(ICON_EMPTY)+'还没有记录<br>点下面中间那个 ＋ 记第一笔</div>';
    return;
  }
  const byDay={};
  mine.forEach(t=>{if(isExp(t))byDay[t.d]=(byDay[t.d]||0)+t.amt;});
  let out='',cur='',idx=0;
  mine.slice(0,120).forEach(t=>{
    if(t.d!==cur){
      if(cur)out+='</div>';
      cur=t.d;
      const sum=byDay[cur]||0;
      out+='<div class="dayhd"><span>'+(cur===TODAY?'今天':(cur.slice(5,7)*1)+'月'+(cur.slice(8)*1)+'日')+
        '</span>'+(sum?'<b>支出 '+money(sum).replace('¥','¥')+'</b>':'')+'</div><div class="icard">';
    }
    const c=catOf(t.cat);
    out+='<div class="tx" data-id="'+esc(t.id)+'" style="--i:'+(idx++)+'">'+
      '<div class="ic" style="background:'+c[2]+'24;border:1px solid '+c[2]+'3D;color:'+c[2]+'">'+svgIcon(c[1])+'</div>'+
      '<div class="mid"><div class="t1">'+esc(t.cat)+'</div>'+
      (t.note?'<div class="t2">'+esc(t.note)+'</div>':'')+'</div>'+
      '<div class="amt'+(t.cat==='收入'?' i':'')+'">'+(t.cat==='收入'?'+':'-')+money(t.amt).replace('¥','¥')+'</div></div>';
  });
  out+='</div>';
  box.innerHTML=out;
}
'''
h = cut(h, 'function renderList(){', 'function askDel(', NEWLIST)

# ---------- 6) renderStat 重写 ----------
NEWSTAT = '''function renderStat(){
  const d=new Date(),dim=new Date(d.getFullYear(),d.getMonth()+1,0).getDate();
  const mine=S.tx.filter(t=>thisMonth(t.d)&&isExp(t));
  const total=mine.reduce((a,t)=>a+t.amt,0);
  $('dStat').textContent=(d.getMonth()+1)+'月';
  countTo($('sTotal'),total);
  $('sLast').textContent=dim+'日';

  const byDay=new Array(dim).fill(0);
  mine.forEach(t=>{byDay[+t.d.slice(8)-1]+=t.amt;});
  const maxAll=Math.max(...byDay,0);
  const max=Math.max(maxAll,1);
  const topDay=maxAll>0?byDay.indexOf(maxAll):-1;
  $('sBars').innerHTML=byDay.map((v,i)=>{
    const h=Math.max(3,v/max*100);
    const cls=(i+1===d.getDate())?'t':(v>=max*.7&&v>0?'hi':'');
    return '<div class="'+cls+'" style="height:'+h+'%" title="'+(i+1)+'日 '+money(v)+'"></div>';
  }).join('');

  const days=d.getDate();
  $('sChips').innerHTML='<span>日均 <b>'+money(total/days).replace('¥','¥')+'</b></span>'+
    '<span>最高 <b>'+money(maxAll).replace('¥','¥')+'</b>'+(topDay>=0?' · '+(topDay+1)+'日':'')+'</span>'+
    '<span><b>'+mine.length+'</b> 笔</span>';

  $('sCnt').textContent=mine.length+' 笔';
  const agg={};
  mine.forEach(t=>agg[t.cat]=(agg[t.cat]||0)+t.amt);
  const arr=Object.entries(agg).sort((a,b)=>b[1]-a[1]);

  /* 环形占比 */
  const C=2*Math.PI*48;
  let off=0,segs='',leg='';
  const share=v=>v/(total||1);
  arr.slice(0,5).forEach(([c,v])=>{
    const k=catOf(c),len=share(v)*C;
    segs+='<circle class="seg" cx="60" cy="60" r="48" stroke="'+k[2]+'" stroke-dasharray="'+
      Math.max(0,len-1.6).toFixed(2)+' '+(C-Math.max(0,len-1.6)).toFixed(2)+'" stroke-dashoffset="'+(-off).toFixed(2)+'"/>';
    leg+='<div class="dl"><i style="background:'+k[2]+'"></i><span>'+esc(c)+'</span><b>'+Math.round(share(v)*100)+'%</b></div>';
    off+=len;
  });
  if(arr.length>5){
    const rest=arr.slice(5).reduce((a,x)=>a+x[1],0),len=share(rest)*C;
    segs+='<circle class="seg" cx="60" cy="60" r="48" stroke="#4B5568" stroke-dasharray="'+
      Math.max(0,len-1.6).toFixed(2)+' '+(C-Math.max(0,len-1.6)).toFixed(2)+'" stroke-dashoffset="'+(-off).toFixed(2)+'"/>';
    leg+='<div class="dl"><i style="background:#4B5568"></i><span>其他 '+(arr.length-5)+' 类</span><b>'+Math.round(share(rest)*100)+'%</b></div>';
  }
  $('dSegs').innerHTML=segs;
  $('dTotal').textContent=money(total);
  $('dLeg').innerHTML=leg||'<div style="font-size:11.5px;color:var(--dim2)">本月还没有支出</div>';

  $('sCats').innerHTML=arr.length?arr.map(([c,v])=>{
    const k=catOf(c);
    return '<div class="crow2"><span class="dot" style="background:'+k[2]+'"></span>'+
      '<span class="nm">'+svgIcon(k[1],'color:'+k[2])+' '+c+'</span>'+
      '<span class="pb"><i style="width:'+(v/(arr[0][1]||1)*100)+'%;background:'+k[2]+'"></i></span>'+
      '<span class="vl">'+money(v)+'</span>'+
      '<span class="pc">'+Math.round(v/(total||1)*100)+'%</span></div>';
  }).join(''):'<div class="empty" style="padding:26px 0">本月还没有支出</div>';

  const inc=S.tx.filter(t=>thisMonth(t.d)&&!isExp(t)).reduce((a,t)=>a+t.amt,0);
  const mx=Math.max(total,inc,1), net=inc-total;
  const bar=(v,c)=>'<span class="pb"><i style="width:'+Math.round(Math.abs(v)/mx*100)+'%;background:'+c+'"></i></span>';
  $('sSum').innerHTML=
    '<div class="crow2"><span class="dot" style="background:#FF6B81"></span><span class="nm">支出</span>'+
    bar(total,'#FF6B81')+'<span class="vl">'+money(total)+'</span><span class="pc">'+(total?Math.round(total/(total+inc||1)*100)+'%':'')+'</span></div>'+
    '<div class="crow2"><span class="dot" style="background:#35D07F"></span><span class="nm">收入</span>'+
    bar(inc,'#35D07F')+'<span class="vl">'+money(inc)+'</span><span class="pc">'+(inc?Math.round(inc/(total+inc||1)*100)+'%':'')+'</span></div>'+
    '<div class="crow2"><span class="dot" style="background:#28D3E8"></span><span class="nm">结余</span>'+
    bar(net, net<0?'#FF6B81':'#28D3E8')+'<span class="vl" style="color:'+(net<0?'var(--err)':'var(--g)')+'">'+money(net)+'</span><span class="pc"></span></div>';
}

'''
h = cut(h, 'function renderStat(){', '/* ================= 目标', NEWSTAT)

# ---------- 7) 目标卡片：注入主色 ----------
h = h.replace("return '<div class=\"goal\"><div class=\"top\">", "return '<div class=\"goal\" style=\"--gc:\"+g.c+\"\"><div class=\"top\">")
h = h.replace("'<div class=\"pb\"><i style=\"width:'+pct+'%;background:'+g.c+'\"></i></div>'+",
              "'<div class=\"pb\"><i style=\"width:'+pct+'%;background:'+g.c+';color:'+g.c+'\"></i></div>'+")

P.write_text(h, encoding='utf-8')
print('✅ v2 写入 %d 字节' % len(h.encode()))
