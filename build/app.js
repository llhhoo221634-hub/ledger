
const CATS=[
  ['吃饭','<path d="M4.6 11a7.4 7.4 0 0 0 14.8 0M3.4 11h17.2M8.6 4.6c0 1.2.9 1.6.9 2.8M12.4 3.4c0 1.4 1 1.8 1 3.2M16.2 4.6c0 1.2.9 1.6.9 2.8"/>','#FF8A4C'],['饮料零食','<path d="M5.6 8.2h12.8l-1.3 11.6a2 2 0 0 1-2 1.7H8.9a2 2 0 0 1-2-1.7zM3.8 8.2h16.4M9.4 4.6h5.2"/>','#FFB74D'],['烟','<path d="M2.8 13.4h13.6a1.2 1.2 0 0 1 1.2 1.2v3.2a1.2 1.2 0 0 1-1.2 1.2H2.8zM8.8 13.4v5.6M20.6 13.4v5.6"/>','#A78BFA'],
  ['话费','<path d="M7.2 2.6h9.6a2 2 0 0 1 2 2v14.8a2 2 0 0 1-2 2H7.2a2 2 0 0 1-2-2V4.6a2 2 0 0 1 2-2zM10.6 5.6h2.8M11 18.6h2"/>','#5AA2FF'],['日用','<path d="M9.6 2.6h4.8v3.2l1.7 2.2V20a1.6 1.6 0 0 1-1.6 1.6H9.5A1.6 1.6 0 0 1 7.9 20V8l1.7-2.2zM8 12.4h8"/>','#22D3EE'],['交通','<rect x="3.4" y="3.6" width="17.2" height="11.4" rx="2"/><path d="M3.4 9.4h17.2"/><circle cx="8" cy="18" r="1.7"/><circle cx="16" cy="18" r="1.7"/>','#34D399'],
  ['娱乐','<rect x="2.6" y="6.4" width="18.8" height="11.2" rx="5.6"/><path d="M8 10.2v4M6 12.2h4"/><circle cx="16" cy="11.4" r="1"/><circle cx="18" cy="13.4" r="1"/>','#F472B6'],['其他','<path d="M3.6 7.6 12 3.1l8.4 4.5v8.8L12 20.9l-8.4-4.5z"/><path d="M3.6 7.6 12 12.1l8.4-4.5M12 12.1v8.8"/>','#94A3B8']
];
const INCOME=['收入','<path d="M12 3.4v11.2M7.6 10.4 12 14.8l4.4-4.4M4.2 19.6h15.6"/>','#34D97B'];
/* 线性图标：fill:none + stroke:currentColor，颜色由外层 color 决定 */
const svgIcon=(inner,style)=>'<svg viewBox="0 0 24 24"'+(style?' style="'+style+'"':'')+'>'+inner+'</svg>';
const ICON_EMPTY='<path d="M5 3.6h11.2a2 2 0 0 1 2 2V21l-3.4-2.4H5a2 2 0 0 1-2-2V5.6a2 2 0 0 1 2-2z"/><path d="M7.6 8.4h8M7.6 12h5.2"/>';
const GOALS=[
  {n:'应急金',t:5000,c:'#FF7A45',h:'一次生病 / 一次被辞 / 一次回家路费'},
  {n:'考证基金',t:2000,c:'#4C9AFF',h:'消防设施操作员证，投资不是消费'},
  {n:'设备基金',t:4000,c:'#2BD97C',h:'二手 3060 主机，跑 Three.js'}
];
const K='ledger_v2';
const DEFAULT={cfg:{pay:805,save:0,fix:50,mdays:31},tx:[],cat:'吃饭',goals:[0,0,0],tab:'list',dayOff:0};
const $=id=>document.getElementById(id);
const p2=n=>n<10?'0'+n:''+n;
const dstr=d=>d.getFullYear()+'-'+p2(d.getMonth()+1)+'-'+p2(d.getDate());
let TODAY=dstr(new Date());

/* ---------- 转义：任何用户数据进 DOM 前必过 ---------- */
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const numOr=(v,def)=>{const n=Number(v);return Number.isFinite(n)?n:def;};

/* ---------- 数据规范化：localStorage 与导入备份全部过这里 ---------- */
function normalize(raw){
  const o=(raw&&typeof raw==='object')?raw:{};
  const cfg=Object.assign({},DEFAULT.cfg);
  if(o.cfg&&typeof o.cfg==='object'){
    ['pay','save','fix','mdays'].forEach(k=>{
      const v=Number(o.cfg[k]);
      if(Number.isFinite(v)&&v>=0&&v<1e7)cfg[k]=v;
    });
  }
  const okCat=c=>CATS.concat([INCOME]).some(x=>x[0]===c);
  const tx=(Array.isArray(o.tx)?o.tx:[])
    .filter(t=>t&&Number.isFinite(Number(t.amt))&&Number(t.amt)>0)
    .map(t=>({
      id:String(t.id||(Date.now()+Math.random().toString(36).slice(2,6))).slice(0,40),
      d:/^\d{4}-\d{2}-\d{2}$/.test(t.d)?t.d:TODAY,
      ts:numOr(t.ts,0),
      amt:Math.min(1e7,Math.round(Number(t.amt)*100)/100),
      cat:okCat(t.cat)?t.cat:'其他',
      note:String(t.note==null?'':t.note).slice(0,60)
    }));
  const goals=GOALS.map((g,i)=>{const v=numOr(o.goals&&o.goals[i],0);return v>0?v:0;});
  const tab=['list','stat','goal','cfg'].indexOf(o.tab)>=0?o.tab:'list';
  return {cfg:cfg,tx:tx.slice(0,5000),goals:goals,cat:okCat(o.cat)?o.cat:'吃饭',tab:tab,dayOff:0};
}
let S=normalize(null);
try{const raw=JSON.parse(localStorage.getItem(K));if(raw)S=normalize(raw);}catch(e){}
const dayStr=off=>{const d=new Date();d.setDate(d.getDate()-off);return dstr(d);};
const r2=n=>Math.round(n*100)/100;
const money=n=>{const v=r2(Math.abs(n));return (n<0?'-':'')+'¥'+v.toLocaleString('zh-CN',{minimumFractionDigits:v%1?2:0,maximumFractionDigits:2});};
const save=()=>{try{localStorage.setItem(K,JSON.stringify(S));}catch(e){}};
const catOf=c=>[...CATS,INCOME].find(x=>x[0]===c)||CATS[7];
const isExp=t=>t.cat!=='收入';
const thisMonth=d=>d.slice(0,7)===TODAY.slice(0,7);

function toast(t){const e=$('toast');e.textContent=t;e.classList.add('on');clearTimeout(e._t);e._t=setTimeout(()=>e.classList.remove('on'),1900);}

/* ================= 预算模型 ================= */
function budget(){
  const d=new Date();
  const realDim=new Date(d.getFullYear(),d.getMonth()+1,0).getDate();
  const cfgDays=Math.round(numOr(S.cfg.mdays,realDim));
  const dim=(cfgDays>=28&&cfgDays<=31)?cfgDays:realDim;   /* 设置页的天数真正参与计算 */
  const dom=Math.min(d.getDate(),dim);
  const quota=Math.max(0,S.cfg.pay-S.cfg.save-S.cfg.fix);
  let spent=0;
  S.tx.forEach(t=>{if(isExp(t)&&thisMonth(t.d))spent+=t.amt;});
  const left=quota-spent, leftDays=Math.max(1,dim-dom+1);
  return {quota,spent,left,leftDays,perDay:left/leftDays,dim,dom};
}
function renderList(){
  const b=budget();
  $('hToday').innerHTML='<i>¥</i>'+money(b.perDay).replace('¥','');
  $('hToday').style.opacity=b.perDay<0?.75:1;
  $('hBar').style.width=(b.quota>0?Math.min(100,b.spent/b.quota*100):100)+'%';
  $('hQuota').textContent=money(b.quota).replace('¥','');
  $('hSpent').textContent=money(b.spent).replace('¥','');
  $('hDays').textContent=b.leftDays;
  $('mLeft').textContent=money(b.left);
  $('mLeft').className='v '+(b.left<0?'r':'b');
  $('mSave').textContent=money(S.cfg.save);

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
  let out='',cur='';
  mine.slice(0,120).forEach(t=>{
    if(t.d!==cur){
      if(cur)out+='</div>';
      cur=t.d;
      const sum=byDay[cur]||0;
      out+='<div class="dayhd"><span>'+(cur===TODAY?'今天':(cur.slice(5,7)*1)+'月'+(cur.slice(8)*1)+'日')+'</span><span>'+(sum?'支出 '+money(sum).replace('¥','¥'):'')+'</span></div><div class="icard">';
    }
    const c=catOf(t.cat);
    out+='<div class="tx" data-id="'+esc(t.id)+'">'+
      '<div class="ic" style="background:'+c[2]+'1E;border:1px solid '+c[2]+'3A;color:'+c[2]+'">'+svgIcon(c[1])+'</div>'+
      '<div class="mid"><div class="t1">'+esc(t.cat)+'</div>'+
      (t.note?'<div class="t2">'+esc(t.note)+'</div>':'')+'</div>'+
      '<div class="amt'+(t.cat==='收入'?' i':'')+'">'+(t.cat==='收入'?'+':'-')+money(t.amt).replace('¥','¥')+'</div></div>';
  });
  out+='</div>';
  box.innerHTML=out;
}
function askDel(id){
  const t=S.tx.find(x=>x.id===id);if(!t)return;
  if(confirm('删除这笔 '+t.cat+' '+money(t.amt)+' ？')){
    S.tx=S.tx.filter(x=>x.id!==id);save();renderAll();toast('已删除');
  }
}
/* 长按删除（单击不再触发删除，避免误触） */
let lpTimer=null,lpX=0,lpY=0;
$('list').addEventListener('pointerdown',e=>{
  const row=e.target&&e.target.closest?e.target.closest('.tx[data-id]'):null;
  if(!row)return;
  lpX=e.clientX;lpY=e.clientY;clearTimeout(lpTimer);
  lpTimer=setTimeout(()=>{
    lpTimer=null;
    if(navigator.vibrate){try{navigator.vibrate(18);}catch(_){}}
    askDel(row.dataset.id);
  },650);
});
$('list').addEventListener('pointermove',e=>{
  if(lpTimer&&(Math.abs(e.clientX-lpX)>10||Math.abs(e.clientY-lpY)>10)){clearTimeout(lpTimer);lpTimer=null;}
});
['pointerup','pointercancel','pointerleave'].forEach(ev=>$('list').addEventListener(ev,()=>{clearTimeout(lpTimer);lpTimer=null;}));

/* ================= 统计 ================= */
function renderStat(){
  const d=new Date(),dim=new Date(d.getFullYear(),d.getMonth()+1,0).getDate();
  const mine=S.tx.filter(t=>thisMonth(t.d)&&isExp(t));
  const total=mine.reduce((a,t)=>a+t.amt,0);
  $('dStat').textContent=(d.getMonth()+1)+'月';
  $('sTotal').textContent=money(total);
  $('sLast').textContent=dim+'日';

  const byDay=new Array(dim).fill(0);
  mine.forEach(t=>{byDay[+t.d.slice(8)-1]+=t.amt;});
  const max=Math.max(...byDay,1);
  $('sBars').innerHTML=byDay.map((v,i)=>{
    const h=Math.max(3,v/max*100);
    const cls=(i+1===d.getDate())?'t':(v>=max*.7?'hi':'');
    return '<div class="'+cls+'" style="height:'+h+'%" title="'+(i+1)+'日 '+money(v)+'"></div>';
  }).join('');

  $('sCnt').textContent=mine.length+' 笔';
  const agg={};
  mine.forEach(t=>agg[t.cat]=(agg[t.cat]||0)+t.amt);
  const arr=Object.entries(agg).sort((a,b)=>b[1]-a[1]);
  $('sCats').innerHTML=arr.length?arr.map(([c,v])=>{
    const k=catOf(c);
    return '<div class="crow2"><span class="dot" style="background:'+k[2]+'"></span>'+
      '<span class="nm">'+svgIcon(k[1],'color:'+k[2])+' '+c+'</span>'+
      '<span class="pb"><i style="width:'+(v/(arr[0][1]||1)*100)+'%;background:'+k[2]+'"></i></span>'+
      '<span class="vl">'+money(v)+'</span>'+
      '<span class="pc">'+Math.round(v/(total||1)*100)+'%</span></div>';
  }).join(''):'<div class="empty" style="padding:28px 0">本月还没有支出</div>';

  const inc=S.tx.filter(t=>thisMonth(t.d)&&!isExp(t)).reduce((a,t)=>a+t.amt,0);
  $('sSum').innerHTML=
    '<div class="crow2"><span class="dot" style="background:#FF6B81"></span><span class="nm">支出</span>'+
    '<span class="pb"></span><span class="vl">'+money(total)+'</span><span class="pc"></span></div>'+
    '<div class="crow2"><span class="dot" style="background:#2BD97C"></span><span class="nm">收入</span>'+
    '<span class="pb"></span><span class="vl">'+money(inc)+'</span><span class="pc"></span></div>'+
    '<div class="crow2"><span class="dot" style="background:#4C9AFF"></span><span class="nm">结余</span>'+
    '<span class="pb"></span><span class="vl" style="color:#fff">'+money(inc-total)+'</span><span class="pc"></span></div>';
}

/* ================= 目标 ================= */
function renderGoals(){
  const done=GOALS.reduce((a,g,i)=>a+Math.min(numOr(S.goals[i],0),g.t),0);
  const all=GOALS.reduce((a,g)=>a+g.t,0);
  $('gProg').textContent='总进度 '+money(done)+' / '+money(all)+' （'+Math.round(done/all*100)+'%）';
  $('goals').innerHTML=GOALS.map((g,i)=>{
    const v=numOr(S.goals[i],0),pct=Math.min(100,v/g.t*100),ok=v>=g.t;
    return '<div class="goal"><div class="top"><span class="nm">'+(ok?'✅ ':'')+g.n+
      '<em>目标 '+money(g.t).replace('¥','¥')+'</em></span>'+
      '<span class="vl">'+money(v)+' / '+money(g.t)+'</span></div>'+
      '<div class="pb"><i style="width:'+pct+'%;background:'+g.c+'"></i></div>'+
      '<div class="foot"><span class="hint">'+g.h+'</span>'+
      '<span class="stepper" data-i="'+i+'"><button data-d="-100">−100</button><button data-d="100">+100</button></span></div></div>';
  }).join('');
}
function step(i,d){
  if(!Number.isFinite(i)||i<0||i>=GOALS.length)return;
  S.goals[i]=Math.max(0,numOr(S.goals[i],0)+d);save();renderGoals();
}
$('goals').addEventListener('click',e=>{
  const b=e.target&&e.target.closest?e.target.closest('.stepper button'):null;
  if(!b)return;
  step(+b.parentNode.dataset.i,+b.dataset.d);
});

/* ================= 设置 ================= */
function renderCfg(){
  [['cPay','pay'],['cSave','save'],['cFix','fix'],['cDays','mdays']].forEach(([id,k])=>{
    if(document.activeElement!==$(id))$(id).value=S.cfg[k];   /* 不打断正在输入的框 */
  });
  const q=Math.max(0,S.cfg.pay-S.cfg.save-S.cfg.fix);
  const days=Math.round(numOr(S.cfg.mdays,31));
  $('cfgTip').textContent='额度 = '+money(S.cfg.pay)+' − '+money(S.cfg.save)+' − '+money(S.cfg.fix)+' = '+money(q)+'。按 '+days+' 天算，日均 '+(q/(days||31)).toFixed(1)+' 元。';
}
let cfgTimer=null;
[['cPay','pay'],['cSave','save'],['cFix','fix'],['cDays','mdays']].forEach(([id,k])=>{
  $(id).addEventListener('input',()=>{
    S.cfg[k]=+$(id).value||0;save();
    clearTimeout(cfgTimer);cfgTimer=setTimeout(renderAll,160);   /* 防抖，不再每按一键全量重绘 */
  });
});
$('wipe').onclick=()=>{if(confirm('清空全部记录和目标？不可恢复。')){S=normalize(null);save();renderAll();go('cfg');toast('已清空');}};
$('exp').onclick=()=>{
  const blob=new Blob([JSON.stringify(S,null,1)],{type:'application/json'});
  const url=URL.createObjectURL(blob);
  const a=document.createElement('a');a.href=url;
  a.download='账本备份_'+TODAY+'.json';document.body.appendChild(a);a.click();a.remove();
  setTimeout(()=>URL.revokeObjectURL(url),1000);
  toast('已导出');
};
$('imp').onclick=()=>{
  const f=document.createElement('input');f.type='file';f.accept='.json,application/json';
  f.onchange=()=>{const r=new FileReader();r.onload=()=>{
    let parsed=null;
    try{parsed=JSON.parse(r.result);}catch(e){alert('文件读不出来，不是有效的 JSON。');return;}
    if(!parsed||typeof parsed!=='object'){alert('文件内容不对。');return;}
    const clean=normalize(parsed);            /* 先规范化，再落地 */
    if(!confirm('导入 '+clean.tx.length+' 笔记录？现有数据会被覆盖。'))return;
    S=clean;save();renderAll();go(S.tab);toast('导入成功，共 '+clean.tx.length+' 笔');
  };r.readAsText(f.files[0]);};
  f.click();
};

/* ================= Tab 切换 ================= */
function go(p){
  S.tab=p;save();
  document.querySelectorAll('.page').forEach(e=>e.classList.toggle('on',e.id==='p-'+p));
  document.querySelectorAll('.tab').forEach(e=>e.classList.toggle('on',e.dataset.p===p));
  window.scrollTo(0,0);
  if(p==='stat')renderStat();if(p==='goal')renderGoals();if(p==='cfg')renderCfg();
}
document.querySelectorAll('.tab').forEach(t=>t.onclick=()=>go(t.dataset.p));

/* ================= 记账面板 ================= */
let buf='';
function buildDaySel(){
  const sel=[['今天',0],['昨天',1],['前天',2]];
  $('daysel').innerHTML=sel.map(([n,o])=>
    '<button data-o="'+o+'" class="'+(S.dayOff===o?'on':'')+'">'+n+'</button>').join('');
  $('daysel').querySelectorAll('button').forEach(b=>b.onclick=()=>{
    S.dayOff=+b.dataset.o;save();buildDaySel();
  });
}
function buildCats(){
  const row=$('crow');
  [...CATS,INCOME].forEach((c,i)=>{
    const d=document.createElement('div');
    d.className='cbtn'+(S.cat===c[0]?' on':'');
    const on = S.cat===c[0];
    const st = 'background:'+c[2]+(on?'40':'1A')+';border-color:'+(on?c[2]:'transparent')+
      (on?';box-shadow:0 6px 16px -6px '+c[2]+'cc':'');
    d.innerHTML='<span class="b" style="'+st+';color:'+c[2]+'">'+svgIcon(c[1])+'</span>'+c[0];
    d.onclick=()=>{S.cat=c[0];save();buildCats();paint();};
    row.appendChild(d);
    if(S.cat===c[0])setTimeout(()=>d.scrollIntoView({inline:'center',block:'nearest'}),0);
  });
}
function paint(){
  const d=$('disp');
  d.className='amtline'+(buf?'':' zero');
  d.innerHTML='<i>¥</i>'+(buf||'0');
  const ok=parseFloat(buf)>0;
  $('gobtn').disabled=!ok;
  $('gobtn').textContent=ok?(S.cat==='收入'?'记收入 '+money(parseFloat(buf)):'记支出 '+money(parseFloat(buf))):'记一笔';
}
function openSheet(){$('mask').classList.add('on');$('sheet').classList.add('on');document.body.classList.add('lock');}
function closeSheet(){$('mask').classList.remove('on');$('sheet').classList.remove('on');document.body.classList.remove('lock');}
$('fab').onclick=openSheet;$('hero').onclick=openSheet;$('mask').onclick=closeSheet;
document.querySelectorAll('.np button').forEach(b=>b.onclick=()=>{
  const k=b.dataset.k;
  if(k==='del')buf=buf.slice(0,-1);
  else if(k==='.'){if(!buf.includes('.'))buf=(buf||'0')+'.';}
  else if(buf.replace('.','').length<8)buf+=k;
  paint();
});
$('gobtn').onclick=()=>{
  const amt=parseFloat(buf);if(!(amt>0))return;
  S.tx.unshift({id:Date.now()+''+Math.random().toString(36).slice(2,6),d:dayStr(S.dayOff||0),ts:Date.now(),
    amt:r2(amt),cat:S.cat,note:$('note').value.trim()});
  buf='';$('note').value='';save();paint();
  closeSheet();renderAll();
  toast((S.dayOff?'已补记到'+['今天','昨天','前天'][S.dayOff]+'：':'已记')+(S.cat==='收入'?'收入 ':'支出 ')+money(amt));
};
$('note').addEventListener('keydown',e=>{if(e.key==='Enter')$('gobtn').click();});

/* ================= 启动 ================= */
function renderAll(){renderList();renderStat();renderGoals();renderCfg();}
buildCats();buildDaySel();paint();renderAll();go(S.tab||'list');

/* ---------- 跨零点自动刷新「今天」 ---------- */
function rollover(){
  const t=dstr(new Date());
  if(t!==TODAY){TODAY=t;save();renderAll();}
}
document.addEventListener('visibilitychange',()=>{if(!document.hidden)rollover();});
setInterval(rollover,60000);

try{
  if(location.protocol.indexOf('http')===0)navigator.serviceWorker.register('sw.js').catch(function(){});
}catch(e){}
