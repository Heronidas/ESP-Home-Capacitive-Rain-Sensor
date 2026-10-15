"""Board dimension drawing (docs/board-dimensions.svg) and CAD outline (mechanical/board-outline.dxf) from the KiCad board."""
import pcbnew
import os
R=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")+"/"
b=pcbnew.LoadBoard(R+"hardware/regensensor.kicad_pcb"); mm=pcbnew.ToMM
bb=b.GetBoardEdgesBoundingBox(); X0,Y0=mm(bb.GetX())+0.05,mm(bb.GetY())+0.05
W,H=round(mm(bb.GetWidth())-0.1,2),round(mm(bb.GetHeight())-0.1,2)
def fab(ref, layer=pcbnew.F_Fab):
    f=b.FindFootprintByReference(ref); xs=[];ys=[]
    for it in f.GraphicalItems():
        if it.GetLayer()==layer and hasattr(it,"GetWidth"):
            r=it.GetBoundingBox(); hw=mm(it.GetWidth())/2
            xs+=[mm(r.GetX())-X0+hw,mm(r.GetRight())-X0-hw]; ys+=[mm(r.GetY())-Y0+hw,mm(r.GetBottom())-Y0-hw]
    if not xs:
        r=f.GetCourtyard(pcbnew.F_CrtYd).BBox(); xs=[mm(r.GetX())-X0,mm(r.GetRight())-X0]; ys=[mm(r.GetY())-Y0,mm(r.GetBottom())-Y0]
    return round(min(xs),1),round(min(ys),1),round(max(xs),1),round(max(ys),1)
holes=[]
for r in ["H1","H2","H3","H4"]:
    f=b.FindFootprintByReference(r); p=f.GetPosition(); d=mm(next(iter(f.Pads())).GetDrillSize().x)
    holes.append((round(mm(p.x)-X0,2),round(mm(p.y)-Y0,2),d))
esp=fab("U1")
parts={"J1":"POWER IN","J6":"I2C","J3":"HEATER","J2":"SENSOR","J4":"I2C socket","J5":"I2C header","J7":"UART","J8":"EXPANSION","SW1":"BOOT","SW2":"RESET"}
boxes={k:fab(k) for k in parts}


# ---------- SVG
S=9; M=70  # px/mm, margin px
top=-esp[1]  # antenna overhang
ox,oy=M+50,M+top*S
VW=int(W*S+2*M+60); VH=int((H+top)*S+2*M+60)
X=lambda x:ox+x*S; Y=lambda y:oy+y*S
o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" width="{VW}" height="{VH}" font-family="DejaVu Sans,Arial,sans-serif">',
   f'<rect width="{VW}" height="{VH}" fill="#ffffff"/>',
   '<defs><marker id="a" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#334155"/></marker>',
   '<pattern id="h" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="#94a3b8" stroke-width="2"/></pattern></defs>',
   f'<rect x="{X(0)}" y="{Y(0)}" width="{W*S}" height="{H*S}" rx="2" fill="#e8f3ec" stroke="#1e293b" stroke-width="2"/>']
ex0,ey0,ex1,ey1=esp
o.append(f'<rect x="{X(ex0)}" y="{Y(ey0)}" width="{(ex1-ex0)*S}" height="{(0-ey0)*S}" fill="url(#h)" stroke="#475569" stroke-width="1.2"/>')
o.append(f'<rect x="{X(ex0)}" y="{Y(0)}" width="{(ex1-ex0)*S}" height="{ey1*S}" fill="#cbd5e1" stroke="#475569" stroke-width="1.2"/>')
o.append(f'<text x="{X((ex0+ex1)/2)}" y="{Y(9)}" font-size="13" text-anchor="middle" fill="#1e293b">ESP32 module</text>')
o.append(f'<text x="{X((ex0+ex1)/2)}" y="{Y(ey0/2)+4}" font-size="11" text-anchor="middle" fill="#1e293b">antenna</text>')
for k,(x0,y0,x1,y1) in boxes.items():
    o.append(f'<rect x="{X(x0)}" y="{Y(y0)}" width="{(x1-x0)*S}" height="{(y1-y0)*S}" fill="#fef3c7" stroke="#b45309" stroke-width="1"/>')
    vert=(y1-y0)>(x1-x0)*1.5
    cx,cy=X((x0+x1)/2),Y((y0+y1)/2)
    lab=f'{k} {parts[k]}' if (max(x1-x0,y1-y0)>9) else parts[k]
    rot=f' transform="rotate(-90 {cx} {cy})"' if vert else ''
    o.append(f'<text x="{cx}" y="{cy+4}" font-size="10" text-anchor="middle" fill="#78350f"{rot}>{lab}</text>')
for (x,y,d) in holes:
    o.append(f'<circle cx="{X(x)}" cy="{Y(y)}" r="{3.4*S}" fill="none" stroke="#64748b" stroke-dasharray="4 3"/>')
    o.append(f'<circle cx="{X(x)}" cy="{Y(y)}" r="{d/2*S}" fill="#ffffff" stroke="#1e293b" stroke-width="1.5"/>')
def dim(x1,y1,x2,y2,txt,off,horiz=True,fs=13):
    if horiz:
        yy=Y(y1)+off
        o.append(f'<line x1="{X(x1)}" y1="{Y(y1)}" x2="{X(x1)}" y2="{yy+(6 if off>0 else -6)}" stroke="#94a3b8"/>')
        o.append(f'<line x1="{X(x2)}" y1="{Y(y2)}" x2="{X(x2)}" y2="{yy+(6 if off>0 else -6)}" stroke="#94a3b8"/>')
        o.append(f'<line x1="{X(x1)}" y1="{yy}" x2="{X(x2)}" y2="{yy}" stroke="#334155" marker-start="url(#a)" marker-end="url(#a)"/>')
        o.append(f'<text x="{(X(x1)+X(x2))/2}" y="{yy-5}" font-size="{fs}" text-anchor="middle" fill="#0f172a" font-weight="bold">{txt}</text>')
    else:
        xx=X(x1)+off
        o.append(f'<line x1="{X(x1)}" y1="{Y(y1)}" x2="{xx+(6 if off>0 else -6)}" y2="{Y(y1)}" stroke="#94a3b8"/>')
        o.append(f'<line x1="{X(x2)}" y1="{Y(y2)}" x2="{xx+(6 if off>0 else -6)}" y2="{Y(y2)}" stroke="#94a3b8"/>')
        o.append(f'<line x1="{xx}" y1="{Y(y1)}" x2="{xx}" y2="{Y(y2)}" stroke="#334155" marker-start="url(#a)" marker-end="url(#a)"/>')
        cy=(Y(y1)+Y(y2))/2
        o.append(f'<text x="{xx-6}" y="{cy}" font-size="{fs}" text-anchor="middle" fill="#0f172a" font-weight="bold" transform="rotate(-90 {xx-6} {cy})">{txt}</text>')
h1,h2,h3,h4=holes
f=lambda v:("%g"%v).replace(".",",") if False else "%g"%v
dim(0,H,W,H,f"{f(W)} mm",66)
dim(h3[0],h3[1],h4[0],h4[1],f"{f(h4[0]-h3[0])} mm (hole centres)",(H-h3[1])*S+30,fs=12)
dim(W,0,W,H,f"{f(H)} mm",56,horiz=False)
dim(h1[0],h1[1],h3[0],h3[1],f"{f(h3[1]-h1[1])} mm (hole centres)",-(h1[0]*S+30),horiz=False,fs=12)
dim(0,h1[1],h1[0],h1[1],f"{f(h1[0])}",0,fs=11) if False else None
dim(ex1,ey0,ex1,0,f"{f(-ey0)} mm",26,horiz=False,fs=11)
dim(0,ey0,ex0,ey0,f"{f(ex0)} mm",-8,fs=11)
dim(ex0,ey0,ex1,ey0,f"{f(ex1-ex0)} mm",-8,fs=11)
o.append(f'<text x="{X(0)}" y="{VH-34}" font-size="12" fill="#334155">Top view, all dimensions in mm. Holes Ø{f(h1[2])} mm (M3), centres {f(h1[0])} mm from each edge.</text>')
o.append(f'<text x="{X(0)}" y="{VH-16}" font-size="12" fill="#334155">Dashed circle Ø6.8 mm: keep-out for screw head or standoff.</text>')
o.append('</svg>')
open(R+"docs/board-dimensions.svg","w").write("\n".join(o))

# ---------- DXF (R12, mm, origin bottom-left, y up)
L=["0","SECTION","2","ENTITIES"]
def line(a,b_,layer):
    L.extend(["0","LINE","8",layer,"10",f"{a[0]:.3f}","20",f"{a[1]:.3f}","11",f"{b_[0]:.3f}","21",f"{b_[1]:.3f}"])
def circ(c,r,layer): L.extend(["0","CIRCLE","8",layer,"10",f"{c[0]:.3f}","20",f"{c[1]:.3f}","40",f"{r:.3f}"])
fy=lambda y:H-y
pts=[(0,0),(W,0),(W,H),(0,H)]
for i in range(4): line(pts[i],pts[(i+1)%4],"OUTLINE")
for (x,y,d) in holes: circ((x,fy(y)),d/2,"HOLES")
a=[(ex0,fy(ey0)),(ex1,fy(ey0)),(ex1,fy(0)),(ex0,fy(0))]
for i in range(4): line(a[i],a[(i+1)%4],"ANTENNA")
for k,(x0,y0,x1,y1) in boxes.items():
    c=[(x0,fy(y0)),(x1,fy(y0)),(x1,fy(y1)),(x0,fy(y1))]
    for i in range(4): line(c[i],c[(i+1)%4],"CONNECTORS")
L+=["0","ENDSEC","0","EOF"]
open(R+"mechanical/board-outline.dxf","w").write("\n".join(L)+"\n")
