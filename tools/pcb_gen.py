import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import pcbnew
from pcbnew import VECTOR2I, FromMM
import design
from design import C, W, H, ESP_X, ESP_Y
import placement
for k,v in placement.POS.items(): C[k]['pcb']=v

OX, OY = 100.0, 80.0
out = sys.argv[1]
FPDIR = "/usr/share/kicad/footprints"
PROJ_LIB = "/home/claude/rain-sensor-board/hardware/rain-sensor.pretty"

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
            if pad.GetNumber() == "39":
                pad.SetZoneConnection(pcbnew.ZONE_CONNECTION_FULL)
                if pad.GetAttribute() == pcbnew.PAD_ATTRIB_PTH:
                    pad.SetDrillSize(pcbnew.VECTOR2I(FromMM(0.3), FromMM(0.3))); pad.SetSize(pcbnew.VECTOR2I(FromMM(0.6), FromMM(0.6)))
    fp.Reference().SetTextSize(pcbnew.VECTOR2I(FromMM(0.8), FromMM(0.8))); fp.Reference().SetTextThickness(FromMM(0.12))
    fp.Value().SetVisible(False)
    if ref[:2] in ('J1','J2','J3','J4','J5','J6','J7','J8') or ref.startswith(('SW','TP','J','H')): fp.Reference().SetVisible(False)
    if ref in ('J1','J2','J3','J4','J5','J6','J7','J8','SW1','SW2'): fp.Reference().SetVisible(False)
    b.Add(fp)
    # LCSC field
    if c["lcsc"]:
        f = pcbnew.PCB_FIELD(fp, fp.GetFieldCount(), "LCSC") if hasattr(pcbnew, "PCB_FIELD") else None
        if f:
            f.SetText(c["lcsc"]); f.SetVisible(False); fp.AddField(f)



# ---- pre-placed GND vias for pads that are hard to reach for the autorouter
PRE_GND = [("U3", "2", -2.0, 0), ("U4", "3", -2.0, 0), ("U4", "5", -2.0, 0), ("U4", "7", -2.0, 0),
           ("U4", "9", 2.0, 0), ("U4", "11", 2.0, 0), ("U4", "13", 2.0, 0)]
for ref, num, dx, dy in PRE_GND:
    fp = b.FindFootprintByReference(ref)
    pad = [p for p in fp.Pads() if p.GetNumber() == num][0]
    c = pad.GetPosition(); p = VECTOR2I(c.x + FromMM(dx), c.y + FromMM(dy))
    v = pcbnew.PCB_VIA(b); v.SetPosition(p); v.SetWidth(FromMM(0.6)); v.SetDrill(FromMM(0.3))
    v.SetViaType(pcbnew.VIATYPE_THROUGH); v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu); v.SetNet(nets["GND"]); b.Add(v)
    t = pcbnew.PCB_TRACK(b); t.SetStart(c); t.SetEnd(p); t.SetWidth(FromMM(0.3)); t.SetLayer(pcbnew.F_Cu); t.SetNet(nets["GND"]); b.Add(t)

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
mk("Power", 0.6, ["+5V", "/VIN_RAW", "+12V", "/SW", "/HEAT_RET"])
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
for e in labels.L: label(e[0], e[1], e[2], e[3] if len(e) > 3 else 0.8)

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
ds.SetAuxOrigin(VECTOR2I(FromMM(OX), FromMM(OY + H)))
b.Save(out)
print("saved", out)
