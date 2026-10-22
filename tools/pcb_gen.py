import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import pcbnew
from pcbnew import VECTOR2I, FromMM
import design
from design import C, W, H, SLOTS, KEEPOUT, PREROUTE
import placement
for k,v in placement.POS.items(): C[k]['pcb']=v

OX, OY = 100.0, 80.0
out = sys.argv[1]
FPDIR = "/usr/share/kicad/footprints"
PROJ_LIB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hardware", "rain-sensor.pretty")
REFHIDE = ("J", "SW", "TP", "H", "NT")

def P(x, y): return VECTOR2I(FromMM(OX + x), FromMM(OY + y))

b = pcbnew.CreateEmptyBoard()
nets = {}
def net(name):
    if name is None: return None
    if name not in nets:
        n = pcbnew.NETINFO_ITEM(b, name); b.Add(n); nets[name] = n
    return nets[name]
for c in C.values():
    for n in c["pins"].values(): net(n)

for ref, c in C.items():
    if c["fp"] is None or c["pcb"] is None: continue
    lib, name = c["fp"]
    path = PROJ_LIB if lib == "rain-sensor" else f"{FPDIR}/{lib}.pretty"
    fp = pcbnew.FootprintLoad(path, name)
    if fp is None: raise SystemExit(f"missing footprint {lib}:{name}")
    x, y, rot = c["pcb"]
    fp.SetFPID(pcbnew.LIB_ID(lib, name))
    fp.SetReference(ref); fp.SetValue(c["value"])
    fp.SetPosition(P(x, y)); fp.SetOrientationDegrees(rot)
    for pad in fp.Pads():
        num = pad.GetNumber()
        try: k = int(num)
        except: continue
        if k in c["pins"] and c["pins"][k]:
            pad.SetNet(nets[c["pins"][k]])
    if ref == "U1":
        for pad in fp.Pads():
            if pad.GetNetname() == "GND": pad.SetZoneConnection(pcbnew.ZONE_CONNECTION_FULL)
    fp.Reference().SetTextSize(pcbnew.VECTOR2I(FromMM(0.8), FromMM(0.8))); fp.Reference().SetTextThickness(FromMM(0.12))
    fp.Value().SetVisible(False)
    if ref.startswith(REFHIDE): fp.Reference().SetVisible(False)
    if ref == "R8": fp.Reference().SetPosition(P(x + 1.3, y)); fp.Reference().SetTextAngleDegrees(90)
    if ref == "Q1": fp.Reference().SetPosition(P(x - 6.6, y + 1.8)); fp.Reference().SetTextAngleDegrees(90)
    b.Add(fp)
    # LCSC field
    if c["lcsc"]:
        f = pcbnew.PCB_FIELD(fp, fp.GetFieldCount(), "LCSC") if hasattr(pcbnew, "PCB_FIELD") else None
        if f:
            f.SetText(c["lcsc"]); f.SetVisible(False); fp.AddField(f)



# ---- pre-placed GND vias for pads that are hard to reach for the autorouter
PRE_GND = [("C9", "2", 0, -1.6), ("SJ2", "2", -1.8, 0), ("U4", "3", -2.0, 0), ("U4", "5", -2.0, 0), ("U4", "7", -2.0, 0),
           ("U4", "9", 2.0, 0), ("U4", "11", 2.0, 0), ("U4", "13", 2.0, 0)]
for ref, num, dx, dy in PRE_GND:
    fp = b.FindFootprintByReference(ref)
    pad = [p for p in fp.Pads() if p.GetNumber() == num][0]
    c = pad.GetPosition(); p = VECTOR2I(c.x + FromMM(dx), c.y + FromMM(dy))
    v = pcbnew.PCB_VIA(b); v.SetPosition(p); v.SetWidth(FromMM(0.6)); v.SetDrill(FromMM(0.3))
    v.SetViaType(pcbnew.VIATYPE_THROUGH); v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu); v.SetNet(nets["GND"]); b.Add(v)
    t = pcbnew.PCB_TRACK(b); t.SetStart(c); t.SetEnd(p); t.SetWidth(FromMM(0.3)); t.SetLayer(pcbnew.F_Cu); t.SetNet(nets["GND"]); b.Add(t)

# ---- fixed heater-current tracks
for name, w, pts in PREROUTE:
    for a, c2 in zip(pts, pts[1:]):
        t = pcbnew.PCB_TRACK(b); t.SetStart(P(*a)); t.SetEnd(P(*c2)); t.SetWidth(FromMM(w))
        t.SetLayer(pcbnew.F_Cu); t.SetNet(nets[name]); t.SetLocked(True); b.Add(t)

# ---- design rules / net classes
ds = b.GetDesignSettings()
ds.m_TrackMinWidth = FromMM(0.2); ds.m_MinClearance = FromMM(0.2)
ds.m_ViasMinSize = FromMM(0.5); ds.m_ViasMinAnnulus = FromMM(0.15); ds.m_MinThroughDrill = FromMM(0.2)
ds.m_CopperEdgeClearance = FromMM(0.3)
dn = ds.m_NetSettings.m_DefaultNetClass
dn.SetTrackWidth(FromMM(0.25)); dn.SetClearance(FromMM(0.2)); dn.SetViaDiameter(FromMM(0.6)); dn.SetViaDrill(FromMM(0.3))
def mk(name, tw, names):
    nc = pcbnew.NETCLASS(name); nc.SetTrackWidth(FromMM(tw)); nc.SetClearance(FromMM(0.2))
    nc.SetViaDiameter(FromMM(0.7)); nc.SetViaDrill(FromMM(0.35))
    ds.m_NetSettings.m_NetClasses[name] = nc

    for n in names:
        if n in nets: nets[n].SetNetClass(nc)
mk("Power", 0.8, ["+5V", "/VIN_HEAT", "GNDPWR", "/HEAT_P", "/HEAT_N", "/HEAT_SW"])
mk("Power33", 0.4, ["+3V3"])

# board outline
pts = [(0, 0), (W, 0), (W, H), (0, H)]
for i in range(4):
    s = pcbnew.PCB_SHAPE(b); s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetLayer(pcbnew.Edge_Cuts)
    s.SetStart(P(*pts[i])); s.SetEnd(P(*pts[(i + 1) % 4])); s.SetWidth(FromMM(0.1)); b.Add(s)


# ---- silkscreen labels
def label(t, x, y, size=1.0, rot=0, layer=pcbnew.F_SilkS):
    tx = pcbnew.PCB_TEXT(b); tx.SetText(t); tx.SetPosition(P(x, y)); tx.SetLayer(layer)
    tx.SetTextSize(pcbnew.VECTOR2I(FromMM(size), FromMM(size))); tx.SetTextThickness(FromMM(0.15)); tx.SetTextAngleDegrees(rot); b.Add(tx)
import labels
for e in labels.L: label(e[0], e[1], e[2], e[3] if len(e) > 3 else 0.8, e[4] if len(e) > 4 else 0)
for t, x, y, sz in labels.BOTTOM:
    tx = pcbnew.PCB_TEXT(b); tx.SetText(t); tx.SetPosition(P(W - x, y)); tx.SetLayer(pcbnew.B_SilkS); tx.SetMirrored(True)
    tx.SetTextSize(pcbnew.VECTOR2I(FromMM(sz), FromMM(sz))); tx.SetTextThickness(FromMM(0.15 if sz < 1.5 else 0.25)); b.Add(tx)
import logo
lx, ly, lsz = labels.LOGO
for ext, holes in logo.polygons(lsz, W - lx, ly, mirror=True):
    ps = pcbnew.SHAPE_POLY_SET(); ps.NewOutline()
    for x, y in ext: ps.Append(FromMM(OX + x), FromMM(OY + y))
    for h in holes:
        hi = ps.NewHole()
        for x, y in h: ps.Append(FromMM(OX + x), FromMM(OY + y), 0, hi)
    ps.Fracture(pcbnew.SHAPE_POLY_SET.PM_FAST)
    s = pcbnew.PCB_SHAPE(b); s.SetShape(pcbnew.SHAPE_T_POLY); s.SetLayer(pcbnew.B_SilkS)
    s.SetPolyShape(ps); s.SetFilled(True); s.SetWidth(0); b.Add(s)

# ---- GND pours (both layers)
def gnd_zone(layer):
    z = pcbnew.ZONE(b); z.SetLayer(layer); z.SetNet(nets["GND"])
    z.SetMinThickness(FromMM(0.2)); z.SetLocalClearance(FromMM(0.25))
    z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL); z.SetThermalReliefGap(FromMM(0.3)); z.SetThermalReliefSpokeWidth(FromMM(0.4))
    ol = z.Outline(); ol.NewOutline()
    for (x, y) in [(0.3, 0.3), (W - 0.3, 0.3), (W - 0.3, H - 0.3), (0.3, H - 0.3)]:
        ol.Append(FromMM(OX + x), FromMM(OY + y))
    z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
    b.Add(z)
gnd_zone(pcbnew.F_Cu); gnd_zone(pcbnew.B_Cu)

# ---- slots around the HTU21D tongue (Edge.Cuts, 1 mm wide, merged into one cut-out)
from shapely.geometry import LineString
from shapely.ops import unary_union
cut = unary_union([LineString([(x1, y1), (x2, y2)]).buffer(0.5, quad_segs=8) for (x1, y1, x2, y2) in SLOTS])
for poly in getattr(cut, "geoms", [cut]):
    ps = pcbnew.SHAPE_POLY_SET(); ps.NewOutline()
    for (x, y) in list(poly.exterior.coords)[:-1]: ps.Append(FromMM(OX + x), FromMM(OY + y))
    sh = pcbnew.PCB_SHAPE(b); sh.SetShape(pcbnew.SHAPE_T_POLY); sh.SetLayer(pcbnew.Edge_Cuts)
    sh.SetPolyShape(ps); sh.SetFilled(False); sh.SetWidth(FromMM(0.05)); b.Add(sh)

def rule_area(poly_pts, tracks=True):
    z = pcbnew.ZONE(b); z.SetIsRuleArea(True); z.SetDoNotAllowCopperPour(False); z.SetDoNotAllowTracks(tracks)
    z.SetDoNotAllowVias(True); z.SetDoNotAllowPads(False); z.SetDoNotAllowFootprints(False)
    ls_ = pcbnew.LSET(); ls_.AddLayer(pcbnew.F_Cu); ls_.AddLayer(pcbnew.B_Cu); z.SetLayerSet(ls_)
    o_ = z.Outline(); o_.NewOutline()
    for (x, y) in poly_pts: o_.Append(FromMM(OX + x), FromMM(OY + y))
    b.Add(z)
# keep the router off the slot edges and out of the narrow bridges at the board edge
for poly in getattr(cut.buffer(0.9, quad_segs=4), "geoms", [cut.buffer(0.9, quad_segs=4)]):
    rule_area(list(poly.exterior.coords)[:-1])
rule_area([(97.0, 38.5), (W, 38.5), (W, 55.5), (97.0, 55.5)])
# copper bridge of the wide net tie NT2 is not a pad: keep the router off it
_nt = C["NT2"]["pcb"]; rule_area([(_nt[0] - 0.9, _nt[1] - 1.0), (_nt[0] + 0.9, _nt[1] - 1.0), (_nt[0] + 0.9, _nt[1] + 1.0), (_nt[0] - 0.9, _nt[1] + 1.0)])

# ---- keep-out below the D1 mini antenna (no copper on either layer)
ko = pcbnew.ZONE(b); ko.SetIsRuleArea(True); ko.SetDoNotAllowCopperPour(True); ko.SetDoNotAllowTracks(True)
ko.SetDoNotAllowVias(True); ko.SetDoNotAllowPads(False); ko.SetDoNotAllowFootprints(False)
ls = pcbnew.LSET(); ls.AddLayer(pcbnew.F_Cu); ls.AddLayer(pcbnew.B_Cu); ko.SetLayerSet(ls)
o = ko.Outline(); o.NewOutline()
kx1, ky1, kx2, ky2 = KEEPOUT
for (x, y) in [(kx1, ky1), (kx2, ky1), (kx2, ky2), (kx1, ky2)]: o.Append(FromMM(OX + x), FromMM(OY + y))
b.Add(ko)

ds.SetAuxOrigin(VECTOR2I(FromMM(OX), FromMM(OY + H)))
b.Save(out)
print("saved", out)
