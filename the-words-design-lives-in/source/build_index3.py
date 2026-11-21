import json,re
d=json.load(open('frames/data.json'))
s=open('frames/A1_f00.svg').read()
s=s[s.index('<svg'):]
s=s.replace("font-family=\"AGaramondPro-Bold, 'Adobe Garamond Pro'\"","font-family=\"AGaramondPro-Bold, 'Adobe Garamond Pro', 'EB Garamond', serif\"")
W,H=1683.78,2383.94; K=W/2384; DY=float(re.search(r'<g id="A1-scale" transform="translate\(0 ([\d.]+)\)',s).group(1))
def cut(src,gid):
    i=src.index(f'<g id="{gid}"'); depth=0; j=i
    for m in re.finditer(r'<g\b|</g>',src[i:]):
        depth+= 1 if m.group(0)=='<g' else -1
        if depth==0: j=i+m.end(); break
    return src[i:j], src[:i]+src[j:]
rings,base=cut(s,'rings')
conn,base=cut(base,'connections')
leaders,base=cut(base,'course-leaders')
dots,base=cut(base,'leader-dots')
defs=re.search(r'<defs>.*?</defs>',s,re.S).group(0)
ringsopen=re.match(r'<g id="rings"[^>]*>',rings).group(0)
strat=re.findall(r'<g class="ring strategy".*?</text></g>',rings,re.S)
lit=re.findall(r'<g class="ring literacy".*?</text></g>',rings,re.S)
assert len(strat)+len(lit)==41,(len(strat),len(lit))
paths=dict(re.findall(r'<path id="ring([^"]+)" (d="[^"]+")',defs))
SPEED=json.load(open('speeds.json'))['speed']
hdr=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}">'
A1=f'<g transform="translate(0 {DY}) scale({K:.6f})">'
ringlayers=[]
for i,num in enumerate(d['nums']):
    g=re.search(r'<g class="ring [a-z]+" data-num="'+re.escape(num)+r'".*?</text></g>',rings,re.S).group(0)
    g=re.sub(r' transform="rotate\([^)]*\)"','',g,count=1)
    ringlayers.append(f'<svg class="ringlayer" data-i="{i}" aria-hidden="true" viewBox="0 0 {W} {H}"><defs><path id="ring{num}" {paths[num]} fill="none"/></defs>'+A1+ringsopen+g+'</g></g></svg>')
top=hdr+A1+leaders+dots+'</g></svg>'
base=base.replace('<svg ','<svg class="layer" ',1)
base=re.sub(r' width="[\d.]+pt" height="[\d.]+pt"','',base,count=1)
top=top.replace('<svg ','<svg class="layer" aria-hidden="true" ',1)
words=[[w['k'],w['ring'],round(w['th'],6),round(w['rr'],3)] for w in d['words']]
labels=re.findall(r'<g id="lines-([^"]+)"',conn)
colors=re.findall(r'<g id="lines-[^"]+" stroke="(#[0-9A-Fa-f]{6})"',conn)
cx,cy=d['cx'],d['cy']
ox=cx*K/W*100; oy=(cy*K+DY)/H*100
data=dict(cx=cx,cy=cy,nums=d['nums'],speed=[round(SPEED[n],5) for n in d['nums']],labels=labels,colors=colors,words=words,k=K,dy=DY,W=W,H=H)
BASE='the-words-design-lives-in/downloads'
menu=open('menu.html').read() if False else None
ns={}; exec(open('build_index.py').read(),ns)   # reuse css from the first build
EXTRA_CSS='''
#menu .head{color:#fff;margin:0 0 2px;}
#menu .title{font-size:20px;line-height:1.15;margin-bottom:6px;}
#menu .subtitle{color:#7a7a7a;margin-bottom:24px;}
#menu .system{margin-bottom:22px;}
#menu .dlrow{display:flex;gap:14px;}
#menu .dlrow .label{color:#7a7a7a;width:64px;flex:none;}
#menu .dlrow a{margin:0;}
#menu ul{margin-bottom:20px;}
#menu ul a{position:relative;}
#menu a.on{color:#fff;}
#menu a.on::after{content:"";display:inline-block;width:5px;height:5px;margin-left:8px;vertical-align:middle;border-radius:50%;background:#fff;}
#menu .downloads{margin-bottom:20px;}
#menu .system .lw{color:#7a7a7a;}
#menu .credit{color:#7a7a7a;font-size:11px;line-height:1.45;margin-top:26px;}
body:not(.compact) #menu{bottom:24px;display:flex;flex-direction:column;overflow-y:auto;}
body:not(.compact) #menu .credit{margin-top:auto;padding-top:26px;}
'''
css=ns['css']
menu='''
<button id="menuToggle" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
<nav id="menu" aria-label="Poster views and downloads">
  <p class="title">The words<br>design lives in.</p>
  <p class="subtitle">Generative data visualization</p>
  <p class="head">Variable</p>
  <div class="system">
    <p class="lw">Line weight <span id="lwValue">1.00 pt</span></p>
    <div class="slider">
      <input id="lw" type="range" min="0.25" max="2" step="0.05" value="1" aria-label="Line weight in points" aria-describedby="lwNote">
      <span class="mark" aria-hidden="true"></span>
    </div>
    <p class="scale"><span>0.25</span><button type="button" id="lwReset">1 pt authored</button><span>2</span></p>
    <p class="note" id="lwNote">1 pt is the designer’s authored value. Explore the system freely. The posters and downloads always stay at 1 pt.</p>
  </div>
  <p class="head">Motion</p>
  <ul class="views">
    <li><a href="#continuous" data-mode="flow">Continuous</a></li>
    <li><a href="#step" data-mode="tick">Step</a></li>
  </ul>
  <p class="head">Static</p>
  <ul class="views">
    '''+''.join(f'<li><a href="#{i:02d}" data-frame="{i-1}">{i:02d}</a></li>' for i in range(1,11))+'''
  </ul>
  <p class="head">Download</p>
  <div class="downloads">
    <p class="dlrow"><span class="label" id="dlLabel">All 10</span><a id="dlPdf" download>PDF</a><a id="dlSvg" download>SVG</a><a id="dlPng" download>PNG</a></p>
    <p class="dlrow"><span class="label">Motion</span><a href="the-words-design-lives-in/motion/The_words_design_lives_in_1440x2040.mp4" download>MP4</a></p>
  </div>
  <p class="credit">© 2026 INTENT COLLECTIVE™<br>Designed by Henry Hongmin Kim</p>
</nav>'''
css=css.replace('''main{display:flex;justify-content:center;align-items:center;min-height:100vh;}
#poster{display:block;height:100vh;width:auto;max-width:100vw;}
@media (max-aspect-ratio: 1683/2384){#poster{width:100vw;height:auto;}}''',f'''main{{display:grid;place-items:center;min-height:100vh;}}
#poster{{position:relative;width:min(100vw, calc(100vh * {W} / {H}));height:min(100vh, calc(100vw * {H} / {W}));margin:0 auto;background:#fff;}}
#poster .layer,#poster canvas,#poster img{{position:absolute;inset:0;width:100%;height:100%;display:block;}}
#poster svg.ringlayer{{position:absolute;inset:0;width:100%;height:100%;transform-origin:{ox:.4f}% {oy:.4f}%;will-change:transform;}}''')
js='''
(function(){
const D=%s;
const STEP_S=36, STEP_L=-72, FRAMES=10, TURN=0.3, AUTHORED=1;
const BASE="%s";
const stage=document.getElementById('poster');
const cv=document.getElementById('lines'), ctx=cv.getContext('2d');
const layers=[...stage.querySelectorAll('svg.ringlayer')];
const ringStep=D.speed;
const byWord=D.labels.map(()=>[]);
D.words.forEach(w=>byWord[w[0]].push(w));
let weight=AUTHORED, scale=1, dpr=1, curPos=0;
function resize(){
  const r=stage.getBoundingClientRect(); dpr=Math.min(window.devicePixelRatio||1,2);
  cv.width=Math.round(r.width*dpr); cv.height=Math.round(r.height*dpr);
  scale=r.width/D.W*dpr; drawLines(curPos);
}
function drawLines(pos){
  const W=cv.width,H=cv.height; ctx.setTransform(1,0,0,1,0,0); ctx.clearRect(0,0,W,H);
  // A0 coords -> A1 page -> canvas pixels
  ctx.setTransform(scale*D.k,0,0,scale*D.k,0,scale*D.dy);
  ctx.lineWidth=weight/D.k; ctx.lineCap='round'; ctx.globalCompositeOperation='multiply';
  const rad=ringStep.map(s=>s*pos*Math.PI/180);
  byWord.forEach((ws,k)=>{
    const P=ws.map(w=>{const t=w[2]+rad[w[1]];return [D.cx+w[3]*Math.sin(t),D.cy-w[3]*Math.cos(t)];});
    ctx.beginPath();
    for(let a=0;a<P.length;a++)for(let b=a+1;b<P.length;b++){ctx.moveTo(P[a][0],P[a][1]);ctx.lineTo(P[b][0],P[b][1]);}
    ctx.strokeStyle=D.colors[k]; ctx.stroke();
  });
}
function draw(pos){
  curPos=pos;
  layers.forEach(l=>{l.style.transform='rotate('+((ringStep[+l.dataset.i]*pos)%%360).toFixed(3)+'deg)';});
  drawLines(pos);
}
const ease=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
let mode='flow', frame=0, t0=null, lastPos=null, raf=null;
function loop(now){
  if(t0===null) t0=now;
  const t=(now-t0)/1000; let pos;
  if(mode==='flow'){ pos=t; }
  else { const u=t-(1-TURN); if(u<0) pos=0; else { const n=Math.floor(u), ph=u-n; pos=n+(ph<TURN?ease(ph/TURN):1); } }
  if(pos!==lastPos){ draw(pos); lastPos=pos; }
  raf=requestAnimationFrame(loop);
}
const links=[...document.querySelectorAll('#menu a[data-mode],#menu a[data-frame]')];
const dl={pdf:document.getElementById('dlPdf'),svg:document.getElementById('dlSvg'),png:document.getElementById('dlPng')};
const dlLabel=document.getElementById('dlLabel');
function setDownloads(){
  if(mode==='still'){
    const n=String(frame+1).padStart(2,'0');
    dlLabel.textContent='Poster '+n;
    dl.pdf.href=BASE+'/pdf/The_words_design_lives_in_A1_'+n+'.pdf';
    dl.svg.href=BASE+'/svg/The_words_design_lives_in_A1_'+n+'.svg';
    dl.png.href=BASE+'/png/The_words_design_lives_in_'+n+'_1440x2040.png';
  } else {
    dlLabel.textContent='All 10';
    ['pdf','svg','png'].forEach(t=>dl[t].href=BASE+'/zip/The_words_design_lives_in_10_posters_'+t+'.zip');
  }
}
function setState(m,f){
  cancelAnimationFrame(raf); raf=null; t0=null; lastPos=null;
  mode=m; if(m==='still'){frame=f; draw(f);} else { raf=requestAnimationFrame(loop); }
  links.forEach(a=>a.classList.toggle('on', (a.dataset.mode&&a.dataset.mode===mode)||(mode==='still'&&a.dataset.frame==String(frame))));
  setDownloads();
}
function fromHash(){
  const h=location.hash.slice(1);
  if(h==='continuous'||h==='flow') return setState('flow'); if(h==='step'||h==='tick') return setState('tick');
  const n=parseInt(h,10); if(n>=1&&n<=10) return setState('still',n-1);
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches) return setState('still',0);
  setState('flow');
}
const toggle=document.getElementById('menuToggle');
links.forEach(a=>a.addEventListener('click',e=>{e.preventDefault(); history.replaceState(null,'',a.getAttribute('href')); fromHash(); document.body.classList.remove('open'); toggle.setAttribute('aria-expanded','false');}));
window.addEventListener('hashchange',fromHash);
const lw=document.getElementById('lw'), lwValue=document.getElementById('lwValue');
function setWeight(v){ weight=v; lwValue.textContent=Number(v).toFixed(2)+' pt'+(Math.abs(v-AUTHORED)<1e-9?' authored':''); drawLines(curPos); }
lw.addEventListener('input',()=>setWeight(+lw.value));
document.getElementById('lwReset').addEventListener('click',()=>{lw.value=AUTHORED; setWeight(AUTHORED);});
lwValue.textContent='1.00 pt authored';
toggle.addEventListener('click',()=>{const o=document.body.classList.toggle('open'); toggle.setAttribute('aria-expanded',String(o));});
function layout(){ const r=stage.getBoundingClientRect(); document.body.classList.toggle('compact', r.left<232); if(r.left>=232) document.body.classList.remove('open'); resize(); }
window.addEventListener('resize',layout);
Promise.all([document.fonts.ready]).then(()=>{layout(); fromHash();});
layout();
})();
''' % (json.dumps(data,separators=(',',':')), BASE)
stage=f'''<div id="poster" role="img" aria-label="The words design lives in. Forty-one SCAD Graphic Design course descriptions as rings, with lines joining matching design keywords.">
{base}
<canvas id="lines" aria-hidden="true"></canvas>
{''.join(ringlayers)}
{top}
</div>'''
html=f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The words design lives in.</title>
<meta name="description" content="Forty-one SCAD Graphic Design course descriptions as a generative motion poster.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700&family=EB+Garamond:wght@700&display=block" rel="stylesheet">
<style>{css}{EXTRA_CSS}</style>
</head>
<body>
{menu}
<main>
{stage}
</main>
<script>{js}</script>
</body>
</html>
'''
open('/home/claude/data/index.html','w').write(html)
print('html',len(html))
