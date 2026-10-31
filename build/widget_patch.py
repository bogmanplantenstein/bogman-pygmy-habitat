"""Second pass, Oct 30 2026: Fierce Flora (Boaz Ng), D. micra type label (Kew K001392875 / PERTH 08989001),
and Matt's growing experience. Applied on top of widget_data.py output."""
import json
import os, sys
HERE=os.path.dirname(os.path.abspath(__file__)); WORK=os.path.join(HERE,'..','work'); sys.path.insert(0,HERE)
D=json.load(open(os.path.join(WORK,'pygmy-data.json'))); T={t['id']:t for t in D['taxa']}
band=lambda s:'Dry' if s<=1.5 else 'Drained' if s<=2.5 else 'Moist' if s<=4 else 'Wet'
FF='https://www.fierceflora.com/'
ffurl={'grievei':'drosera-grievei-species-profile/','eneabba':'drosera-enneaba-species-profile/','australis':'drosera-australis-species-profile/',
 'silvicola':'drosera-silvicola/','citrina':'drosera-citrina/','miniata':'drosera-miniata/','bindoon':'drosera-bindoon/','platystigma':'drosera-platystigma/',
 'hyperostigma':'drosera-hyperostigma-species-profile/','leucoblasta':'drosera-leucoblasta/','callistos':'drosera-callistos/','sewelliae':'drosera-sewelliae/',
 'x-sidjamesii':'drosera-x-sidjamesii/','pycnoblasta':'drosera-pycnoblasta/','sargentii':'drosera-sargentii/','trichocaulis':'drosera-trichocaulis/',
 'verrucata':'drosera-verrucata/','pygmaea':'drosera-pygmaea/','androsacea':'drosera-androsacea/','pulchella':'drosera-pulchella/','gibsonii':'drosera-gibsonii/',
 'barbigera':'drosera-barbigera/','coomallo':'drosera-coomallo/','lasiantha':'drosera-lasiantha/','scorpioides':'drosera-scorpioides/','dichrosepala':'drosera-dichrosepala/'}
# habitat text: ICPS + Fierce Flora, paraphrased
hab={
 'australis':"Wet spots in coastal heath, such as the edges of seasonally flooded swampy hollows; also sandy soil over laterite nearby.",
 'gibsonii':"Granite and laterite scree on the lower slopes of the Stirling Range, laterite on the plains between peaks, and clayey sand on watershed slopes.",
 'bindoon':"Heavy, rough laterite gravel on hillsides and hilltops.",
 'eneabba':"Deep, well-drained white silica sand in low open heath, often under sparse shrubs.",
 'silvicola':"Laterite rubble among leaf litter on the slopes and summits of high hills in jarrah forest.",
 'lasiantha':"Loamy laterite scree on high slopes in low jarrah forest, and skeletal soil on granite.",
 'miniata':"Laterite, clay and silty clay on slopes, often exposed and near granite outcrops; also loam washed onto granite aprons.",
 'androsacea':"Exposed, poor, often compacted or clayey soils in Wheatbelt mallee and low heath: stony white sandy loam or loam with laterite gravel. These soils bake hard in summer.",
 'pulchella':"Sand, peaty sand, peat, laterite or loam on the edges of lakes, swamps, streams and seeps; sometimes grows submerged.",
 'sargentii':"Deep, fine white silica sand in low coastal heath and on consolidated dunes.",
 'pycnoblasta':"Deep white sand, clayey white sand over laterite gravel, or yellow sand, in low heath and mallee.",
 'leucoblasta':"Clayey sand, clay and laterite between low shrubs in heath; soils often carry organic matter and peat.",
 'scorpioides':"Pebbly laterite outcrops with a little silica sand, among heath and open woodland.",
 'coomallo':"Laterite pebbles over laterite sheet rock on the upper slopes of hills.",
 'barbigera':"White silica sand and laterite gravel on the slopes and tops of laterite hills. Moist only while winter rain lasts; dries out in summer.",
 'hyperostigma':"Well-drained laterite mixed with silica sand in open, light forest.",
 'dichrosepala':"Well-drained shallow sand over laterite with laterite pebbles, among low scrub.",
 'verrucata':"Clayey sand between low shrubs in heath and scrub; also roadside gravel.",
 'pygmaea':"A wide range of poor soils, usually near winter water: seeps, trailside ditches, peaty swamp edges, and shallow sand or clay in exposed heath.",
 'x-sidjamesii':"Silica sand stabilised by sedges on lake shores; sometimes underwater in wet winters.",
 'micra':"Black sandy soil in winter-wet swampland.",
}
dist={'micra':"Known from Malaga, in Perth's northern suburbs (its type locality). Listed Priority One flora in WA.",
      'x-sidjamesii':"Shores of a few lakes north of Perth.",
      'grievei':"Hilly country inland of Ravensthorpe: Lake Grace east to Baanga Hill, and around Lake King and Newdegate."}
score={'australis':4,'gibsonii':1.5,'walyunga':2.5,'bindoon':1.5,'x-sidjamesii':4.5}
for k,v in hab.items(): T[k]['hab']=v
for k,v in dist.items(): T[k]['dist']=v
for k,s in score.items(): T[k]['score']=s; T[k]['band']=band(s)
for t in D['taxa']:
    src=['icps']
    if not t['hyb']: src.insert(0,'nl')
    if t['id'] in ffurl: src.append('ff')
    t['src']=src; t['ff']=FF+ffurl[t['id']] if t['id'] in ffurl else None
    t['basis']=None
T['albonotata']['src']=['robinson2018']
T['micra']['src']=['nl','kew','florabase']
T['citrina']['src'].append('krueger2020')
T['micra']['note']="Can form a dormant bud in summer but usually just slows its growth (Lowrie & Conran 2014). Climate is from its single known site."
T['oreopodion']['note']="No climate-map data."
D['sources']={
 'nl':{'t':"Nunn & Lambers 2017, Carniv. Pl. Newslett. 46(1)",'u':"https://cpn.carnivorousplants.org/articles/CPNv46n1p13_19.pdf"},
 'icps':{'t':"ICPS Guide to the Pygmy Drosera (after Lowrie et al. 2017)",'u':"https://carnivorousplants.org/cp/taxonomy/pygmyDrosera"},
 'ff':{'t':"Fierce Flora (Boaz Ng)",'u':"https://www.fierceflora.com/"},
 'kew':{'t':"Type specimen label, Lowrie & Conran 2014 (Kew K001392875)",'u':None},
 'florabase':{'t':"FloraBase, WA Herbarium",'u':"https://florabase.dbca.wa.gov.au/browse/profile/48763"},
 'robinson2018':{'t':"Robinson et al. 2018, Phytotaxa 346(3)",'u':"https://doi.org/10.11646/phytotaxa.346.3.2"},
 'krueger2020':{'t':"Krueger & Fleischmann 2020, CPN 49(1)",'u':"https://cpn.carnivorousplants.org/articles/CPNv49n1p6_16.pdf"},
}
TF1="https://www.terraforums.com/forums/threads/pygmies-dormant-now.123814"
TF2="https://terraforums.com/forums/threads/pygmies-dormant-now.123814/page-2"
TF3="https://terraforums.com/forums/threads/pygmy-sundews-that-have-a-summer-dormancy.123669/"
TF4="https://terraforums.com/forums/threads/pygmy-summer-survival-tips.90423"
# Direct reports of summer dormancy in cultivation, or grower "summer-sensitive" lists with no contrary report.
DORM={'callistos':TF3,'pycnoblasta':TF3,'leioblastus':TF1,'scorpioides':TF2,'closterostigma':TF1,'eneabba':TF1,
      'miniata':TF2,'androsacea':TF2,'leucoblasta':TF2,'x-badgerupii':TF1,'nivea':TF4,'citrina':TF4,'barbigera':TF4,
      'silvicola':TF4,'walyunga':TF3}
DNOTE={'scorpioides':"One grower reports that plants which go dormant rarely come back, so it is worth keeping this one in active growth.",
       'leioblastus':"Reported under its older name, D. placenta subsp. leioblasta."}
D['sources']['tf']={'t':"Grower reports, Terraforums",'u':TF1}
for t in D['taxa']:
    t['dorm']=t['id'] in DORM
    if t['dorm']:
        t['src']=t['src']+['tf']; t['tf']=DORM[t['id']]; t['dormNote']=DNOTE.get(t['id'])
json.dump(D,open(os.path.join(WORK,'pygmy-data.json'),'w'),separators=(',',':'))
print('dormancy-prone:',sum(t['dorm'] for t in D['taxa']))
import collections
print(collections.Counter(t['band'] for t in D['taxa']), 'FF-sourced:',sum(1 for t in D['taxa'] if t['ff']), 'no clim:',[t['id'] for t in D['taxa'] if not t['clim']])
