"""Widget climate: Bogman Climate Map method (NASA POWER, lapse-corrected cells), research-grade records only,
WA range only (except D. pygmaea), plus explicit exclusions of records outside the published range."""
import json
import os, sys
HERE=os.path.dirname(os.path.abspath(__file__)); WORK=os.path.join(HERE,'..','work'); sys.path.insert(0,HERE)

from mapclim import *
name={i:t[1] for i,t in enumerate(taxa)}; tid={i:t[0] for i,t in enumerate(taxa)}
EXCLUDE={('Drosera occidentalis',-30.583,115.269):"~150 km north of published range (Gingin–Carbarup); obscured record"}
PYG='albonotata allantostigma androsacea australis barbigera bindoon callistos citrina closterostigma coomallo depauperata dichrosepala echinoblastus eneabba enodes gibsonii grievei helodes hyperostigma lasiantha leioblastus leucoblasta leucostigma mannii micra micrantha microscapa miniata minutiflora nitidula nivea occidentalis omissa oreopodion paleacea patens pedicellaris platystigma pulchella pycnoblasta pygmaea rechingeri roseana sargentii scorpioides sewelliae silvicola spilos stelliflora trichocaulis verrucata walyunga'.split()
HYB=['× badgerupii','× badgingarra','× carbarup','× legrandii','× pingellyensis','× sidjamesii']
def excluded(n,o): return any(n==a and abs(o[1]-b)<0.002 and abs(o[2]-c)<0.002 for (a,b,c) in EXCLUDE)
def drymetrics(s):
    T=[(a+b)/2 for a,b in zip(s['monthlyHi'],s['monthlyLo'])]; P=s['precip']
    dry=[m for m in range(12) if P[m]<2*T[m]]
    return len(dry), round(sum(2*T[m]-P[m] for m in dry))
out={}; dropped=[]
for i,n in name.items():
    p=n.split(' ',1)
    if len(p)<2 or (p[1] not in PYG and p[1] not in HYB): continue
    ep=p[1]; allo=[o for o in obs if o[3]==i]
    keep=[]
    for o in allo:
        if o[5]&1: continue                                   # needs_id
        if not (ep=='pygmaea' or inWA(o[1],o[2])): dropped.append((n,o[1],o[2],'outside WA')); continue
        if excluded(n,o): dropped.append((n,o[1],o[2],'outside published range')); continue
        keep.append(o)
    s=stats({key(o[1],o[2]) for o in keep}) if keep else None
    if s: s['dryMo'],s['deficit']=drymetrics(s)
    out[ep]=dict(taxon_id=tid[i],nAll=len(allo),nKeep=len(keep),obsc=sum(1 for o in keep if o[5]&2),filt=s)
# D. micra: single type-locality cell (not in the map's records)
s=stats({key(-31.8557,115.9124)}); s['dryMo'],s['deficit']=drymetrics(s)
out['micra']=dict(taxon_id=None,nAll=0,nKeep=1,obsc=0,filt=s)
json.dump(out,open(os.path.join(WORK,'mapclim_out.json'),'w'))
print('dropped:',len(dropped)); [print('  ',d) for d in dropped]
o=out['occidentalis']['filt']; print('occidentalis now: p90',o['hotTypical'],'dryMo',o['dryMo'],'cells',o['n'])
