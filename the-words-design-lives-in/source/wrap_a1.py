import re,sys
src,dst=sys.argv[1:3]
s=open(src).read()
W,H=1683.78,2383.94; k=W/2384; dy=(H-3370*k)/2
head=re.search(r'<svg[^>]*>',s).group(0)
body=s[s.index(head)+len(head):s.rindex('</svg>')]
new=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}pt" height="{H}pt" viewBox="0 0 {W} {H}">'
open(dst,'w').write(s[:s.index(head)]+new+f'<rect width="{W}" height="{H}" fill="#FFFFFF"/><g id="A1-scale" transform="translate(0 {dy:.3f}) scale({k:.6f})">'+body+'</g></svg>')
