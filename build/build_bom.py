"""Rainfall, monthly highs/lows and dry months from BOM station normals (27 stations), IDW to
research-grade, in-range records (same filter as build_clim.py)."""
import json, statistics as st
import os, sys
HERE=os.path.dirname(os.path.abspath(__file__)); WORK=os.path.join(HERE,'..','work'); sys.path.insert(0,HERE)
from stations import S, interp, metrics
from mapclim import obs, taxa, inWA
EXCL=[('Drosera occidentalis',-30.5829,115.2693)]
name={i:t[1] for i,t in enumerate(taxa)}
out={}
def agg(points):
    mo=[[0]*12,[0]*12,[0]*12]; ms=[]
    for la,lo in points:
        (tx,tn,pr),_=interp(la,lo); ms.append(metrics(tx,tn,pr))
        for j,a in enumerate((tx,tn,pr)):
            for m in range(12): mo[j][m]+=a[m]
    n=len(points); hi=[round(v/n,1) for v in mo[0]]; lo=[round(v/n,1) for v in mo[1]]; pr=[round(v/n) for v in mo[2]]
    T=[(a+b)/2 for a,b in zip(hi,lo)]; dry=[m for m in range(12) if pr[m]<2*T[m]]
    return dict(hi=hi,lo=lo,pr=pr,dryMo=len(dry),dryList=dry,deficit=round(sum(2*T[m]-pr[m] for m in dry)),n=n)
for i,n in name.items():
    p=n.split(' ',1)
    if len(p)<2 or not n.startswith('Drosera'): continue
    pts=[(o[1],o[2]) for o in obs if o[3]==i and not(o[5]&1) and inWA(o[1],o[2])
         and not any(n==a and abs(o[1]-b)<.002 and abs(o[2]-c)<.002 for a,b,c in EXCL)]
    if pts: out[p[1]]=agg(pts)
out['micra']=agg([(-31.8557,115.9124)])
json.dump(out,open(os.path.join(WORK,'bom_out.json'),'w'))
