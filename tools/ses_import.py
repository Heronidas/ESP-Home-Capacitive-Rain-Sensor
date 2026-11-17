import re, sys
import pcbnew
from pcbnew import VECTOR2I, FromMM

def tokenize(t):
    return re.findall(r'\(|\)|"[^"]*"|[^\s()]+', t)

def parse(toks):
    st=[[]]
    for k in toks:
        if k=='(':
            st.append([])
        elif k==')':
            x=st.pop(); st[-1].append(x)
        else:
            st[-1].append(k.strip('"'))
    return st[0][0]

def find(node, name):
    return [c for c in node if isinstance(c, list) and c and c[0]==name]

def import_ses(b, path):
    tree = parse(tokenize(open(path).read()))
    routes = find(tree, 'routes')[0]
    netout = find(routes, 'network_out')[0]
    layers = {'F.Cu': pcbnew.F_Cu, 'B.Cu': pcbnew.B_Cu}
    nets = {n.GetNetname(): n for n in b.GetNetsByName().values()} if hasattr(b.GetNetsByName(),'values') else {}
    if not nets:
        nn = b.GetNetsByName()
        nets = {str(k): nn[k] for k in nn.keys()}
    P = lambda x, y: VECTOR2I(int(round(float(x) / 10.0 * 1000)), int(round(-float(y) / 10.0 * 1000)))
    nt = nv = 0
    for net in find(netout, 'net'):
        name = net[1]
        if name == 'GND': continue
        ni = nets[name]
        for w in find(net, 'wire'):
            for p in find(w, 'path'):
                layer = layers[p[1]]; width = int(round(float(p[2]) / 10.0 * 1000))
                pts = [(p[i], p[i+1]) for i in range(3, len(p) - 1, 2)]
                for a, c in zip(pts, pts[1:]):
                    t = pcbnew.PCB_TRACK(b); t.SetStart(P(*a)); t.SetEnd(P(*c)); t.SetWidth(width)
                    t.SetLayer(layer); t.SetNet(ni); b.Add(t); nt += 1
        for v in find(net, 'via'):
            m = re.search(r'_(\d+):(\d+)_um', v[1])
            via = pcbnew.PCB_VIA(b); via.SetPosition(P(v[2], v[3]))
            via.SetWidth(int(m.group(1)) * 1000); via.SetDrill(int(m.group(2)) * 1000)
            via.SetViaType(pcbnew.VIATYPE_THROUGH); via.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
            via.SetNet(ni); b.Add(via); nv += 1
    return nt, nv
