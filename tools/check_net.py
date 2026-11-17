import sys, xml.etree.ElementTree as ET
import design as D
t=ET.parse(sys.argv[1]); r=t.getroot()
nets={}
for n in r.find('nets'):
    name=n.get('name'); nodes=sorted((x.get('ref'),x.get('pin')) for x in n)
    nets[name]=nodes
# expected from design
exp={}
for ref,c in D.C.items():
    if ref.startswith(('FLG','H')): continue
    for p,net in c['pins'].items():
        if net is None: continue
        exp.setdefault(net,[]).append((ref,str(p)))
# compare (drop nets with a single node? keep)
bad=0
for net,nodes in exp.items():
    nodes=sorted(nodes)
    got=nets.get(net)
    if got is None:
        print('MISSING NET',net,nodes); bad+=1; continue
    if sorted(got)!=nodes:
        print('DIFF',net,'\n   exp',nodes,'\n   got',sorted(got)); bad+=1
for net in nets:
    if net not in exp and not net.startswith('unconnected'):
        print('EXTRA NET',net,nets[net]); bad+=1
print('nets exp',len(exp),'got',len(nets),'problems',bad)
