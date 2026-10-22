import sys, math
import pcbnew
from pcbnew import VECTOR2I, FromMM, ToMM
src, dst = sys.argv[1], sys.argv[2]
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from design import W, H
b = pcbnew.LoadBoard(src)
gnd = b.FindNet("GND")
VIA_D, VIA_DR, CLR = 0.6, 0.3, 0.2

def items_other():
    out = []
    for fp in b.GetFootprints():
        for p in fp.Pads():
            if p.GetNetCode() != gnd.GetNetCode(): out.append(p)
    for t in b.GetTracks():
        if t.GetNetCode() != gnd.GetNetCode(): out.append(t)
    return out

def clear(shape_list, others, pos_shapes):
    for o in others:
        os_ = o.GetEffectiveShape()
        for s in pos_shapes:
            if os_.Collide(s, FromMM(CLR)): return False
    return True

from pcbnew import SHAPE_SEGMENT, SHAPE_CIRCLE
def seg(a, c, w):
    return SHAPE_SEGMENT(a, c, FromMM(w))
def circ(p, d):
    return SHAPE_CIRCLE(p, FromMM(d / 2))

import re, tempfile, os
def unconnected():
    pcbnew.ZONE_FILLER(b).Fill(b.Zones())
    tmp = tempfile.mktemp(suffix='.rpt')
    pcbnew.WriteDRCReport(b, tmp, pcbnew.EDA_UNITS_MILLIMETRES, True)
    txt = open(tmp).read(); os.remove(tmp)
    out = set()
    for blk in txt.split('\n[')[0:]:
        if 'unconnected_items' in blk[:30]:
            for m in re.finditer(r'Pad (\S+) \[GND\] of (\S+)', blk): out.add((m.group(2), m.group(1)))
    return out
todo = unconnected()
print('unconnected GND pads:', sorted(todo))
placed = []
n_new = 0
def pad_via(fp, pad):
        global n_new, placed
        c = pad.GetPosition()
        # skip if already has a via/track from GND (none routed) -> always add
        done = False
        for r in [1.1, 1.3, 1.5, 1.8, 2.2, 2.6, 3.0, 3.5, 4.0]:
            for ang in range(0, 360, 15):
                p = VECTOR2I(c.x + FromMM(r * math.cos(math.radians(ang))), c.y + FromMM(r * math.sin(math.radians(ang))))
                shapes = [circ(p, VIA_D + 0.0), seg(c, p, 0.3)]
                if not clear(None, items_other() + placed, shapes): continue
                # keep off board edge
                bb = b.GetBoardEdgesBoundingBox()
                if not bb.Contains(VECTOR2I(p.x, p.y)) or p.y - bb.GetTop() < FromMM(1.0) and False: continue
                v = pcbnew.PCB_VIA(b); v.SetPosition(p); v.SetWidth(FromMM(VIA_D)); v.SetDrill(FromMM(VIA_DR))
                v.SetViaType(pcbnew.VIATYPE_THROUGH); v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu); v.SetNet(gnd)
                t = pcbnew.PCB_TRACK(b); t.SetStart(c); t.SetEnd(p); t.SetWidth(FromMM(0.3)); t.SetLayer(pcbnew.F_Cu if pad.IsOnLayer(pcbnew.F_Cu) else pcbnew.B_Cu); t.SetNet(gnd)
                b.Add(v); b.Add(t); placed += [v, t]; n_new += 1; done = True; break
            if done: break
        if not done: print("NO GND VIA for", fp.GetReference(), pad.GetNumber())
        return done
for fp in b.GetFootprints():
    for pad in fp.Pads():
        if pad.GetNetCode() != gnd.GetNetCode(): continue
        if (fp.GetReference(), pad.GetNumber()) not in todo: continue
        if pad.GetAttribute() == pcbnew.PAD_ATTRIB_PTH or pad.GetAttribute() == pcbnew.PAD_ATTRIB_NPTH: continue
        if fp.GetReference().startswith("U1") and pad.GetNumber() == "39": continue  # thermal pad: many vias below
        pad_via(fp, pad)
print("gnd vias", n_new)

# ---- stitch every F.Cu pour fragment to the B.Cu plane
def stitch():
    added = 0
    for layer in (pcbnew.F_Cu, pcbnew.B_Cu):
        added += stitch_layer(layer)
    return added

def stitch_layer(layer):
    added = 0
    fz = [z for z in b.Zones() if not z.GetIsRuleArea() and z.GetFirstLayer() == layer][0]
    ps = fz.GetFilledPolysList(layer)
    vias = [v for v in b.GetTracks() if v.Type() == pcbnew.PCB_VIA_T and v.GetNetCode() == gnd.GetNetCode()]
    for i in range(ps.OutlineCount()):
        o = pcbnew.SHAPE_POLY_SET(); o.AddOutline(ps.Outline(i))
        for h in range(ps.HoleCount(i)): o.AddHole(ps.Hole(i, h))
        bb = o.BBox()
        if sum(1 for v in vias if bb.Contains(v.GetPosition()) and o.Collide(v.GetPosition())) >= 2: continue
        # candidate grid
        best = None
        step = FromMM(0.1)
        x = bb.GetX()
        while x < bb.GetRight() and best is None:
            y = bb.GetY()
            while y < bb.GetBottom():
                pt = VECTOR2I(x, y)
                if pt.x < FromMM(100 + 1.0) or pt.x > FromMM(100 + W - 1.0) or pt.y < FromMM(80 + 1.0) or pt.y > FromMM(80 + H - 1.0):
                    y += step; continue
                ok = all(o.Collide(VECTOR2I(pt.x + int(FromMM(0.3) * math.cos(a)), pt.y + int(FromMM(0.3) * math.sin(a)))) for a in [k * math.pi / 4 for k in range(8)]) and o.Collide(pt)
                holes = [v.GetPosition() for v in vias] + [p.GetPosition() for f in b.GetFootprints() for p in f.Pads() if p.GetAttribute() == pcbnew.PAD_ATTRIB_PTH]
                far = all((pt.x - h.x) ** 2 + (pt.y - h.y) ** 2 > FromMM(1.6) ** 2 for h in holes)
                if ok and far and clear(None, items_other(), [circ(pt, VIA_D)]): best = pt; break
                y += step
            x += step
        if best is None:
            # fragment too narrow for a via: drop one beside a SMD GND pad inside it
            pads = [(fp, p) for fp in b.GetFootprints() for p in fp.Pads() if p.GetNetCode() == gnd.GetNetCode()
                    and p.GetAttribute() == pcbnew.PAD_ATTRIB_SMD and p.IsOnLayer(layer) and o.Collide(p.GetPosition())]
            if pads and pad_via(*pads[0]): added += 1
            continue
        v = pcbnew.PCB_VIA(b); v.SetPosition(best); v.SetWidth(FromMM(VIA_D)); v.SetDrill(FromMM(VIA_DR))
        v.SetViaType(pcbnew.VIATYPE_THROUGH); v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu); v.SetNet(gnd); b.Add(v); added += 1
    return added
for _ in range(3):
    pcbnew.ZONE_FILLER(b).Fill(b.Zones())
    a = stitch(); print('stitch vias', a)
    if a == 0: break

# drop dangling stubs the autorouter leaves behind
tmp = tempfile.mktemp(suffix='.rpt'); pcbnew.WriteDRCReport(b, tmp, pcbnew.EDA_UNITS_MILLIMETRES, True); txt = open(tmp).read(); os.remove(tmp)
for m in re.finditer(r'track_dangling.*?@\(([\d.]+) mm, ([\d.]+) mm\): Track', txt, re.S):
    p0 = VECTOR2I(FromMM(float(m.group(1))), FromMM(float(m.group(2))))
    for t in list(b.GetTracks()):
        if t.Type() == pcbnew.PCB_TRACE_T and not t.IsLocked() and t.GetLength() < FromMM(0.5) and t.HitTest(p0, FromMM(0.05)):
            b.Remove(t); print('removed stub', t.GetNetname())
tmp = tempfile.mktemp(suffix='.rpt'); pcbnew.ZONE_FILLER(b).Fill(b.Zones())
pcbnew.WriteDRCReport(b, tmp, pcbnew.EDA_UNITS_MILLIMETRES, True); txt = open(tmp).read(); os.remove(tmp)
for m in re.finditer(r'starved_thermal.*?[Pp]ad (\S+) \[GND\] of (\S+)', txt, re.S):
    fp = b.FindFootprintByReference(m.group(2))
    for pad in fp.Pads():
        if pad.GetNumber() == m.group(1): pad.SetZoneConnection(pcbnew.ZONE_CONNECTION_FULL); print('full connection', m.group(2), m.group(1))
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
print('remaining', sorted(unconnected()))
b.Save(dst)
