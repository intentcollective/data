import re, json, unicodedata
def parse(f, pre):
    t=open(f).read()
    t=t.replace('ﬁ','fi').replace('ﬂ','fl')
    t=re.sub(r'\n?(SCAD Catalog 2026-2027|\d? ?Graphic Dsgn/Visual Experience \(GDVX\) ?\d?|\d? ?Graphic Design \(GRDS\) ?\d?|GRAPHIC DSGN/VISUAL\s*EXPERIENCE \(GDVX\)|GRAPHIC DESIGN \(GRDS\))\n',' \n',t)
    out=[]
    for m in re.finditer(pre+r' (\d{3}F?) (.+?)\((\d) Credits\)(.*?)(?=\n'+pre+r' \d{3}F? [A-Z]|\Z)', t, re.S):
        num,title,_,body=m.groups()
        body=re.split(r'Prerequisite\(s\)|Attributes:',body)[0]
        body=re.sub(r'\s+',' ',body).strip()
        title=re.sub(r'\s+',' ',title).strip()
        out.append(dict(num=num,title=title,desc=body))
    return out
c=parse('/mnt/user-data/uploads/g.txt','GRDS')+parse('/mnt/user-data/uploads/d.txt','GDVX')
def curly(s):
    s=re.sub(r"(\w)'(\w)",r"\1’\2",s); s=re.sub(r"'(\w)",r"‘\1",s); s=s.replace("'","’")
    s=re.sub(r'"(\w)',r'“\1',s); s=s.replace('"','”'); return s
for x in c: x['desc']=curly(x['desc']); x['title']=curly(x['title'])
json.dump(c,open('courses.json','w'),ensure_ascii=False,indent=1)
print(len(c))
for x in c: print(x['num'],'|',x['title'],'|',len(x['desc']),'|',x['desc'][:60],'…',x['desc'][-40:])
