import json, uharfbuzz as hb, math
def font(w):
    blob=hb.Blob.from_file_path(f'/home/claude/fonts/Barlow-{w}.ttf'); f=hb.Font(hb.Face(blob)); return f, f.face.upem
F={w:font(w) for w in ['Regular','SemiBold','Medium','Bold']}
def width(text,w='Regular'):
    f,upem=F[w]; b=hb.Buffer(); b.add_str(text); b.guess_segment_properties()
    hb.shape(f,b,{"kern":True,"liga":False})
    return sum(p.x_advance for p in b.glyph_positions)/upem, len(b.glyph_infos)
