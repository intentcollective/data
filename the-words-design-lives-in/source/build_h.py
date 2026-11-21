import json,math,re,sys
from metrics import width
exec(open('build_c.py').read().split('# ---------- ring text')[0].split('K=0.75')[1].split('\n',1)[1]
     .replace("def tier","def _tier").replace("PINK=","_PINK="), globals())   # reuse RANK, REG, classify
c=json.load(open('courses.json'))
PW,PH=2384,3370; N=len(c); K=1.0; LW=float(sys.argv[1]); FRAME=float(sys.argv[2]); CS=11.0; PRS=12.74
MAR4=288.0; MAR2=144.0
# ---------- colours: one hue per word, lighter = more frequent ----------
def oklch(L,C,h):
    a=C*math.cos(math.radians(h)); b=C*math.sin(math.radians(h))
    l_=L+0.3963377774*a+0.2158037573*b; m_=L-0.1055613458*a-0.0638541728*b; s_=L-0.0894841775*a-1.2914855480*b
    l,m,s=l_**3,m_**3,s_**3
    r=4.0767416621*l-3.3077115913*m+0.2309699292*s; g=-1.2684380046*l+2.6097574011*m-0.3413193965*s; bb=-0.0041960863*l-0.7034186147*m+1.7076147010*s
    return r,g,bb
def to_hex(L,C,h):
    while True:
        rgb=oklch(L,C,h)
        if all(-1e-4<=v<=1+1e-4 for v in rgb) or C<=0: break
        C-=0.002
    f=lambda v: 12.92*v if v<=0.0031308 else 1.055*v**(1/2.4)-0.055
    return '#%02X%02X%02X'%tuple(round(max(0,min(1,f(v)))*255) for v in rgb)
FREQ={'design':42,'visual':29,'create':21,'communication':18,'graphic':16,'typography':15,'experience':12,'research':10,'media':10,'content':10,'concept':10,'form':9,'solutions':8,'user':7,'designer':6,'digital':6,'systems':6,'message':6,'innovation':6,'prototype':5,'interaction':5,'elements':5,'audience':5,'layout':4,'identity':4,'data':4,'image':4,'narrative':4,'publication':4,'type':3,'poster':3,'logotype':3,'aesthetic':3,'hierarchy':2,'color':2,'brand':2,'portfolio':2}
COL=[]
for k,(rank,lab,_) in enumerate(RANK):
    n=FREQ[lab]; t=(math.log(42)-math.log(n))/(math.log(42)-math.log(2))
    L=0.78-0.34*t
    h=(345+k*137.508)%360          # golden angle: neighbours in the list always differ
    COL.append(to_hex(L,0.21,h))
# ---------- ring geometry: outer ink flush with 4" margins ----------
rings=[]
for x in c:
    wn,nn=width(x['num'],'Bold'); wb,nb=width(' '+x['desc']+' ','Bold')
    rings.append(dict(x,Wu=wn+wb,n=nn+nb,body=' '+x['desc']+' '))
REXT=(PW-2*MAR4)/2
a=max(r['Wu']/(2*math.pi)+(N-1-i)/K for i,r in enumerate(rings))
S=REXT/(a+0.75); D=S/K; R=a*S; r0=R-(N-1)*D
cx=PW/2; cy=MAR4+REXT
# ---------- locate words ----------
STRAT={'229','301','376','380','402','408','440','479','480','503','701','702','749','770','779F','789','791','792'}
SPEED=json.load(open('speeds.json'))['speed']
def rot(num): return SPEED[num]*FRAME
occ=[[] for _ in RANK]; ring_parts=[]; WORDS=[]
for i,r in enumerate(rings):
    rad=r0+i*D; t=(2*math.pi*rad-r['Wu']*S)/r['n']
    parts=[]; pos=width(r['num'],'Bold')[0]*S+len(r['num'])*t
    for m in re.finditer(r"[A-Za-z][A-Za-z\-’']*|[^A-Za-z]+",r['body']):
        s=m.group(0); w,n=width(s,'Bold'); adv=w*S+n*t
        k=None
        if s[0].isalpha():
            k=classify(s.rstrip('’\''));  k=classify(s) if k is None else k
        if k is not None:
            mid=pos+(w*S+(n-1)*t)/2; th0=mid/rad; th=th0+math.radians(rot(r['num'])); rr=rad+0.35*S
            occ[k].append((cx+rr*math.sin(th),cy-rr*math.cos(th))); WORDS.append(dict(k=k,ring=i,th=th0,rr=rr))
        parts.append((s,k)); pos+=adv
    ring_parts.append((rad,t,parts))
counts=[len(o) for o in occ]
assert counts==[FREQ[l] for _,l,_ in RANK], counts
esc=lambda s:s.replace('&','&amp;').replace('<','&lt;')
INK='#1E1E1E'
STATIC=open('static.svgfrag').read().replace('42 Keywords','37 Keywords')
o=[];A=o.append
A(f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{PW}pt" height="{PH}pt" viewBox="0 0 {PW} {PH}">')
A('<title>The words design lives in.</title>'+f'<rect width="{PW}" height="{PH}" fill="#FFFFFF"/>')
CBOT=MAR4+2*REXT
TB1=CBOT+MAR4+0.514*346.16
STATIC=STATIC.replace('transform="translate(0 2507.832)"',f'transform="translate(0 {TB1:.3f})"')
TITLE=STATIC[STATIC.index('<text id="title"'):STATIC.index('<text id="stats"')]
A(TITLE)
A('<defs>')
for i,r in enumerate(rings):
    rad=r0+i*D
    A(f'<path id="ring{r["num"]}" d="M{cx:.3f},{cy-rad:.3f} A{rad:.3f},{rad:.3f} 0 1 1 {cx:.3f},{cy+rad:.3f} A{rad:.3f},{rad:.3f} 0 1 1 {cx:.3f},{cy-rad:.3f}" fill="none"/>')
A('</defs>')
A(f'<g id="connections" fill="none" stroke-width="{LW}" stroke-linecap="round">')
for k in range(len(RANK)):
    pts=occ[k]
    A(f'<g id="lines-{RANK[k][1]}" stroke="{COL[k]}" style="mix-blend-mode:multiply">')
    for p in range(len(pts)):
        for q in range(p+1,len(pts)):
            A(f'<line x1="{pts[p][0]:.2f}" y1="{pts[p][1]:.2f}" x2="{pts[q][0]:.2f}" y2="{pts[q][1]:.2f}"/>')
    A('</g>')
A('</g>')
A(f'<g id="rings" font-size="{S:.3f}" fill="{INK}" font-family="Barlow-Bold, Barlow" font-weight="700">')
for i,r in enumerate(rings):
    rad,t,parts=ring_parts[i]
    body=''.join(esc(s) if k is None else f'<tspan fill="{COL[k]}">{esc(s)}</tspan>' for s,k in parts)
    A(f'<g class="ring {"strategy" if r["num"] in STRAT else "literacy"}" data-num="{r["num"]}" transform="rotate({rot(r["num"])} {cx} {cy})"><text letter-spacing="{t/S:.5f}em"><textPath xlink:href="#ring{r["num"]}" startOffset="0">{r["num"]}{body}</textPath></text></g>')
A('</g>')
# course list (bottom-left), rows level with each ring's bottom
A(f'<g id="course-list" font-size="{CS}" fill="{INK}">')
leftW=[]
for i,r in enumerate(rings):
    y=cy+r0+i*D
    leftW.append((width(r['num']+' ','SemiBold')[0]+width(r['title'],'Medium')[0])*CS)
    A(f'<text x="{MAR2}" y="{y+0.35*CS:.3f}" font-family="Barlow-Medium, Barlow" font-weight="500"><tspan font-family="Barlow-SemiBold, Barlow" font-weight="600">{r["num"]}</tspan> {esc(r["title"])}</text>')
A('</g>'); A(f'<g id="course-leaders" stroke="{INK}" stroke-width="0.25">')
for i in range(N):
    y=cy+r0+i*D; A(f'<line x1="{MAR2+leftW[i]+8:.2f}" y1="{y:.3f}" x2="{cx:.3f}" y2="{y:.3f}"/>')
A('</g><g id="leader-dots" fill="%s">'%INK+''.join(f'<circle cx="{cx:.3f}" cy="{cy+r0+i*D:.3f}" r="1.2"/>' for i in range(N))+'</g>')
LASTROW=cy+r0+(N-1)*D+0.35*CS
ST=STATIC[STATIC.index('<text id="stats"'):STATIC.index('<text id="paragraph"')]
A(ST.replace('translate(1950.428 1808.5482)',f'translate(1950.428 {LASTROW-172.8:.3f})'))
# word spine: hangline 4" below circles, last baseline on the 2" bottom margin
LS=24.0; hang=cy+REXT+MAR2; first=hang+0.7*LS; last=PH-MAR2; RL=len(RANK)
LEAD=(last-first)/(RL-1); AX=PW/2
A(f'<g id="word-ranking" font-size="{LS}" font-family="Barlow-Medium, Barlow" font-weight="500">')
for k,(rank,lab,_) in enumerate(RANK):
    yb=first+k*LEAD; y=yb-0.35*LS; col=COL[k]
    A(f'<g fill="{col}"><text x="{AX-110:.2f}" y="{yb:.3f}" text-anchor="end">{rank}</text>'
      f'<text x="{AX-41:.2f}" y="{yb:.3f}" text-anchor="end">{counts[k]}</text>'
      f'<line x1="{AX-26:.2f}" y1="{y:.3f}" x2="{AX+26:.2f}" y2="{y:.3f}" stroke="{col}" stroke-width="4.8"/>'
      f'<text x="{AX+41:.2f}" y="{yb:.3f}">{lab}</text></g>')
A('</g>')
# principles: three columns across the paragraph measure, last baseline on 2" margin
PX0,PX1=1400.215,2240.0; PWID=PX1-PX0
PR=[('Strategy','Intellectually sophisticated and critically reasoned.',['Sociocultural intent','Critical inquiry','Human strategy']),
    ('Literacy','Structurally informed and communicatively fluent.',['Linguistic typography','Aesthetic taste','Systemic scalability']),
    ('Synthesis','Critically discerning and integratively resolved.',['Design critique','Design judgment','Design communication'])]
w3=max(width(t,'Regular')[0]*PRS for t in [PR[2][1]]+PR[2][2])
step=(PWID-w3)/2
PB=last-6*PRS
for j,(h,sub,items) in enumerate(PR):
    x=PX0+j*step
    rows=[(0,h,'Bold'),(1.2*PRS,sub,'Regular')]+[(1.2*PRS*(3+q),it,'Regular') for q,it in enumerate(items)]
    A(f'<text id="principle-{h.lower()}" font-size="{PRS}" fill="#000000" transform="translate({x:.3f} {PB:.3f})">'+''.join(
      f'<tspan x="0" y="{yy:.2f}" font-family="Barlow-{wt}, Barlow" font-weight="{700 if wt=="Bold" else 400}">{esc(t)}</tspan>' for yy,t,wt in rows)+'</text>')
# paragraph: same measure, ends two lines above the principles
PARA=open('paragraph.txt').read().strip(); PL=28.8
lines=[]; cur=''
for word in PARA.split():
    test=(cur+' '+word).strip()
    if width(test,'Regular')[0]*24>PWID and cur: lines.append(cur); cur=word
    else: cur=test
lines.append(cur)
PY=PB-2*PL-(len(lines)-1)*PL
A(f'<text id="paragraph" font-family="Barlow-Regular, Barlow" font-size="24" fill="#000000" transform="translate({PX0} {PY:.3f})">'+''.join(f'<tspan x="0" y="{j*PL:.1f}">{esc(l)}</tspan>' for j,l in enumerate(lines))+'</text>')
# logo scaled to 3" wide, anchored bottom-left on the margins
LG=STATIC[STATIC.index('<g id="logo"'):]
L0,LB,LWID=146.25,3222.38,295.0; sc=216/LWID
A(f'<g id="logo-3in" transform="translate({MAR2} {last}) scale({sc:.5f}) translate({-L0} {-LB})">'+LG+'</g>')
A('</svg>')
open(f'frames/A0c_f{int(FRAME):02d}.svg','w').write('\n'.join(o))
print('para lines',len(lines),'PY',round(PY,1),'title b1',round(TB1,1),'b2',round(TB1+295.31,1),'stats last',round(LASTROW,1),'S',round(S,3),'D',round(D,3),'r0',round(r0,1),'R',round(R,1),'cy',cy,'spine leading',round(LEAD,2),'paragraph lines',len(lines),file=sys.stderr)
print('\n'.join(f'{RANK[k][1]} {COL[k]}' for k in range(RL)),file=sys.stderr)

json.dump(dict(cx=cx,cy=cy,words=WORDS,strat=sorted(STRAT),nums=[r['num'] for r in rings],colors=COL,lw=LW,lines=sum(len(o)*(len(o)-1)//2 for o in occ)),open('frames/data.json','w'))
