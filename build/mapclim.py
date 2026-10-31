import json, math, collections, statistics as st
import os
R=os.environ.get('CLIMATE_MAP_INAT', os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','bogman-climate-map','inat'))+'/'
d=json.load(open(R+'drosera.json')); cc=json.load(open(R+'climate-cache.json')); el=json.load(open(R+'elev-cache.json'))
sd=json.load(open(R+'species-data.json'))['species']
taxa=d['taxa']; obs=d['obs']
def lapse(tC,rh,elev):
    g,cpd,Hv,Rsd,eps=9.81,1004.6,2.501e6,287.05,0.622
    T=tC+273.15; P=1013.25*math.pow(1-2.25577e-5*(elev or 0),5.25588)
    es=6.112*math.exp(17.67*tC/(tC+243.5)); rs=eps*es/max(P-es,1e-3)
    gm=g*(1+Hv*rs/(Rsd*T))/(cpd+Hv*Hv*rs*eps/(Rsd*T*T))*1000; gd=g/cpd*1000
    rh=55 if rh is None else max(0,min(100,rh))
    return max(4.0,min(9.8,gd-(gd-gm)*(rh/100)))
r1=lambda x: round(x*10)/10 if x is not None else None   # JS Math.round-ish
def corr(c,elev):
    if elev is None or c.get('modelElev') is None: return c
    dz=(elev-c['modelElev'])/1000; out=dict(c)
    for f in ('tempMax','tempMin','tempMaxHi','tempMinLo'):
        arr=c.get(f)
        if not isinstance(arr,list): continue
        o=[]
        for m,v in enumerate(arr):
            if v is None: o.append(None); continue
            mt=(c['tempMax'][m]+c['tempMin'][m])/2 if c['tempMax'][m] is not None and c['tempMin'][m] is not None else v
            o.append(r1(v-lapse(mt,(c.get('rhMean') or [None]*12)[m],c['modelElev'])*dz))
        out[f]=o
    return out
def key(lat,lng): return f"{math.floor(lat/0.5)}:{math.floor(lng/0.5)}"
def stats(cells):
    cl=[corr(cc[k],el.get(k)) for k in cells if k in cc]
    if not cl: return None
    hot=[max(v for v in c['tempMaxHi'] if v is not None) for c in cl]
    avgH=[max(v for v in c['tempMax'] if v is not None) for c in cl]
    # hottest month by mean of p90 across cells
    mo=[st.mean([c['tempMaxHi'][m] for c in cl if c['tempMaxHi'][m] is not None]) for m in range(12)]
    return dict(n=len(cl),hotTypical=r1(st.mean(hot)),avgHigh=r1(st.mean(avgH)),hotMonth=mo.index(max(mo)),
                monthlyHi=[r1(st.mean([c['tempMax'][m] for c in cl])) for m in range(12)],
                monthlyLo=[r1(st.mean([c['tempMin'][m] for c in cl])) for m in range(12)],
                monthlyP90=[r1(x) for x in mo],
                precip=[round(st.mean([c['precipMm'][m] or 0 for c in cl])) for m in range(12)])
def inWA(lat,lng): return -36.2<lat<-26.5 and 112<lng<124.5
