# -*- coding: utf-8 -*-
"""hierarchie de K-polyedres : chaque noeud EST le polyedre, recolle a partir de ses deux enfants."""
import math

K, FLAT, KY = 0.72, 0.70, 2.40
PITCH = 1.80

BND = [(10,1.42),(40,1.28),(78,1.34),(115,1.02),(150,1.40),(178,1.12),
       (215,1.35),(255,1.44),(285,1.06),(310,1.24),(335,1.38),(355,1.18)]
B = {i+1: (K*r*math.cos(math.radians(a)), K*FLAT*r*math.sin(math.radians(a)))
     for i,(a,r) in enumerate(BND)}
pt = lambda i: (0.0,0.0) if i == 0 else B[i]

PIECE = {1:[0,1,2], 2:[0,2,3,4], 3:[0,4,5,6,7], 4:[0,7,8], 5:[0,8,9,10], 6:[0,10,11,12,1]}
SHADE = {1:12, 2:58, 3:30, 4:78, 5:42, 6:95}

LEAF  = {'p%d'%i: i for i in range(1,7)}
RLEAF = {'p1':0.22,'p2':0.38,'p3':0.13,'p4':0.31,'p5':0.44,'p6':0.26}
def _bx(p):
    xs = [pt(i)[0] for i in PIECE[p]]
    return sum(xs) / len(xs)
# ordre des feuilles impose par la geometrie : a chaque fusion, l'enfant place a
# gauche est celui dont les pieces occupent la partie gauche du parent.
_PAIRS = {'A': ('p1', 'p2'), 'B': ('p3', 'p4'), 'C': ('p5', 'p6'),
          'D': ('A', 'B'), 'R': ('D', 'C')}
def _leaves(n):
    if n.startswith('p'):
        return [n]
    a, b = _PAIRS[n]
    la, lb = _leaves(a), _leaves(b)
    ma = sum(_bx(LEAF[x]) for x in la) / len(la)
    mb = sum(_bx(LEAF[x]) for x in lb) / len(lb)
    return la + lb if ma <= mb else lb + la
_ORDRE_FEUILLES = _leaves('R')
XLEAF = {n: 0.50 + k * PITCH for k, n in enumerate(_ORDRE_FEUILLES)}
INT   = {'A':(['p1','p2'],0,[2]), 'B':(['p3','p4'],0,[7]), 'C':(['p5','p6'],0,[10]),
         'D':(['A','B'],0,[4]),   'R':(['D','C'],0,[8,1])}
ORDER = ['p1','p2','p3','p4','p5','p6','A','B','C','D','R']

def pieces_of(n): return [LEAF[n]] if n in LEAF else [p for c in INT[n][0] for p in pieces_of(c)]
def contour(pcs):
    """contour exterieur d'un groupe de pieces contigues (O + chaine frontiere)"""
    arc=[]
    for p in pcs:
        a=PIECE[p][1:]
        arc += a[1:] if (arc and arc[-1]==a[0]) else a
    if len(pcs)==6: return arc          # polygone entier : pas de sommet O
    return [0]+arc
def spokes_in(pcs):
    """rayons internes au groupe (jonctions entre pieces consecutives)"""
    return [PIECE[p][1] for p in pcs[1:]]
def seams_of(n):
    if n in LEAF: return []
    out=[]
    for c in INT[n][0]:
        out += seams_of(c)
        if c in INT: out += INT[c][2]
    return out

yy = lambda r: KY*r

def bbox(pcs):
    xs=[pt(i)[0] for p in pcs for i in PIECE[p]]; ys=[pt(i)[1] for p in pcs for i in PIECE[p]]
    return min(xs),max(xs),min(ys),max(ys)
def hauteur(n):
    x0,x1,y0,y1 = bbox(pieces_of(n)); return y1-y0

GAP = 0.30
BONUS = {'A':0.00, 'B':0.13, 'C':0.26, 'D':0.06, 'R':0.12}   # etale les rayons de fusion
RV, XT = dict(RLEAF), dict(XLEAF)
for k in ('A','B','C','D','R'):
    ch = INT[k][0]
    RV[k] = max(RV[c] + ((hauteur(k)+hauteur(c))/2.0 + GAP)/KY for c in ch) + BONUS[k]
    RV[k] = math.ceil(RV[k]*20)/20.0
    XT[k] = sum(XT[c] for c in ch)/len(ch)

info={}
for n in ORDER:
    pcs=pieces_of(n); x0,x1,y0,y1=bbox(pcs)
    ox=XT[n]-(x0+x1)/2.0; oy=yy(RV[n])-(y0+y1)/2.0
    info[n]=(pcs,ox,oy,x0+ox,x1+ox,y0+oy,y1+oy)

bad=[]
for i,n in enumerate(ORDER):
    for m in ORDER[i+1:]:
        a,b,c,d=info[n][3:7]; e,f,g,h=info[m][3:7]
        if a-0.18<f and e<b+0.18 and c-0.18<h and g<d+0.18: bad.append((n,m))
for n in ORDER:
    print("%-3s x[%6.2f,%6.2f] y[%6.2f,%6.2f]  noeud(%5.2f,%5.2f)"%((n,)+tuple(info[n][3:7])+(XT[n],yy(RV[n]))))
print("chevauchements de polyedres :", bad)

# ---------------- emission ----------------
IND=" "*20; L=[]
def wi(s=""): L.append(IND+s if s else "")
f=lambda x: ("%.3f"%x).rstrip('0').rstrip('.')
def poly(idx,ox,oy): return " -- ".join("(%s,%s)"%(f(pt(i)[0]+ox),f(pt(i)[1]+oy)) for i in idx)

TOP=max(v[6] for v in info.values()); RIGHT=max(v[4] for v in info.values())
BOT=min(v[5] for v in info.values())
wi(r"% Hierarchie de K-polyedres proposee comme unite de calcul a la place du point.")
wi(r"% Les six pieces des feuilles sont les six secteurs d'un meme polygone maitre")
wi(r"% irregulier (decoupe en eventail autour d'un point interieur O). Elles sont")
wi(r"% dessinees partout a la meme echelle et dans la meme orientation : le polyedre")
wi(r"% d'un noeud interne est donc litteralement le recollement de ceux de ses deux")
wi(r"% enfants, soude le long de la face tracee en rouge epais. L'ordonnee est le")
wi(r"% rayon physique r ; le point rouge d'un noeud est place en O, au coeur du polyedre.")
wi(r"\begin{tikzpicture}[xscale=1.0, yscale=1.0]")
wi(r"\useasboundingbox (-2.15, -0.40) rectangle (%s, %s);"%(f(RIGHT+0.30), f(TOP+0.62)))
wi()
wi(r"\tikzset{arbre/.style={gris_fonce_inria!75, line width=0.9pt}}")
wi(r"\tikzset{bord/.style={draw=inria-2024-bleu-canard, line width=1.05pt, line join=round}}")
wi(r"\tikzset{couture/.style={draw=inria-2024-bleu-canard!70, line width=0.4pt}}")
wi(r"\tikzset{soudure/.style={draw=inria-rouge, line width=1.7pt}}")
wi()
wi(r"% ==== axe des rayons ====")
wi(r"\draw[-{Latex[length=2.4mm]}, gris_fonce_inria, line width=0.8pt] (-1.00,-0.25) -- (-1.00,%s);"%f(TOP+0.35))
wi(r"\node[font=\scriptsize, text=gris_fonce_inria, anchor=south] at (-1.00,%s) {$r$};"%f(TOP+0.42))
for r in [0.25] + [x/2.0 for x in range(1, int(RV['R']*2)+1)]:
    wi(r"\draw[gris_fonce_inria, line width=0.6pt] (-1.00,%s) -- (-0.84,%s);"%(f(yy(r)),f(yy(r))))
    wi(r"\node[font=\scriptsize, text=gris_fonce_inria, anchor=east] at (-1.08,%s) {$%s$};"%(f(yy(r)),(("%.2f"%r).rstrip('0').rstrip('.') if r < 0.5 else "%.1f"%r).replace('.',',')))
wi(r"\node[rotate=90, font=\scriptsize, text=gris_fonce_inria, anchor=south] at (-1.95,%s) {rayon (m)};"%f(yy(1.2)))
wi()
wi(r"% ==== arbre (passe derriere les polyedres) ====")
for n in ('A','B','C','D','R'):
    ch,_r,_=INT[n]; yn=yy(RV[n])
    for c in ch: wi(r"\draw[arbre] (%s,%s) -- (%s,%s);"%(f(XT[c]),f(yy(RV[c])),f(XT[c]),f(yn)))
    wi(r"\draw[arbre] (%s,%s) -- (%s,%s);"%(f(XT[ch[0]]),f(yn),f(XT[ch[-1]]),f(yn)))
wi()
wi(r"% ==== polyedres : un par noeud, a sa hauteur ====")
for n in ORDER:
    pcs,ox,oy=info[n][0],info[n][1],info[n][2]
    wi(r"%% noeud %s"%n)
    for p in pcs: wi(r"\fill[inria-2024-bleu-canard!%d] %s -- cycle;"%(SHADE[p],poly(PIECE[p],ox,oy)))
    neuf = INT[n][2] if n in INT else []
    for i in spokes_in(pcs):
        if i not in neuf: wi(r"\draw[couture] (%s,%s) -- (%s,%s);"%(f(ox),f(oy),f(B[i][0]+ox),f(B[i][1]+oy)))
    wi(r"\draw[bord] %s -- cycle;"%poly(contour(pcs),ox,oy))
    for i in neuf: wi(r"\draw[soudure] (%s,%s) -- (%s,%s);"%(f(ox),f(oy),f(B[i][0]+ox),f(B[i][1]+oy)))
wi()
wi(r"% ==== noeuds : le point de fusion, au centre du polyedre ====")
for n in ORDER:
    rr = 2.0 if n in LEAF else (2.6 if n!='R' else 3.0)
    wi(r"\fill[inria-rouge] (%s,%s) circle (%.1fpt);"%(f(XT[n]),f(yy(RV[n])),rr))
wi()
wi(r"\end{tikzpicture}")
open('figs/hierarchie_surfaces.tex','w').write("\n".join(L)+"\n")
print("ecrit")
