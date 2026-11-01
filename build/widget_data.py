"""Build pygmy-widget data. Sources:
 soil  = Nunn & Lambers 2017, CPN 46(1) Table 1 (verbatim class)
 text  = paraphrased from ICPS Guide to the Pygmy Drosera (after Lowrie et al. 2017), verified verbatim Oct 30 2026
 heat  = Bogman Climate Map method (NASA POWER, p90 daily high of hottest month, lapse-corrected),
         recomputed on research-grade, in-range records only
"""
import json
import os, sys
HERE=os.path.dirname(os.path.abspath(__file__)); WORK=os.path.join(HERE,'..','work'); sys.path.insert(0,HERE)
M=json.load(open(os.path.join(WORK,'mapclim_out.json')))
BOM=json.load(open(os.path.join(WORK,'bom_out.json')))
MON=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
# name: (score, soil N&L, distribution (paraphrase), habitat (paraphrase), note)
S={
'albonotata':(2.5,None,"Western Wheatbelt: Wandoo National Park and the Northam, York and Quairading shires.","Sandy clay-loam on gravelly slopes, ridges and low rises in Wandoo woodland.","Described 2018, after Nunn & Lambers' soil table."),
'allantostigma':(4,"pale sand","A few roadside sites near Hill River, north of Perth.","Loam, silica sand or peaty sand on the edges of winter-wet depressions.",None),
'androsacea':(2.5,"pale sand","South of Perth: Corrigin, Dragon Rocks, Katanning, Stirling Range, Varley and Williams.","Stony white sandy loam, or brown loam with laterite gravel, in low open heath. These soils bake hard in summer.",None),
'australis':(2.5,"pale sand, laterite or peat","A narrow strip along the south coast from Augusta to east of Esperance.","Sandy soil over laterite, on the drier ground beside wet depressions.",None),
'barbigera':(1.5,"laterite, yellow sand over laterite","Two areas: Eneabba to York, and around Dumbleyung and Lake Grace.","Only on laterite hilltops, in white silica sand mixed with laterite gravel.",None),
'bindoon':(2,"laterite","A 40 km stretch between Muchea and Wannamal.","Heavy laterite soils.",None),
'callistos':(2,"laterite, pale sand over laterite","Around Gidgegannup and the state forest along the Brookton Highway.","Heavy laterite-covered sand, and pockets of pure sand surrounded by laterite.",None),
'citrina':(1,"yellow sand","Regans Ford (Moore River) and Boonanarring, north of Perth.","Well-drained deep yellow sand in open heath or under Banksia woodland.","Includes D. coalara, merged into this species in 2020."),
'closterostigma':(4,"pale sand","Gingin to Cataby, east toward Mogumber.","Deep white sand grayed by humus, often in winter-wet depressions and swampy heath.",None),
'coomallo':(1.5,"laterite","Badgingarra, Cataby and Coomallo.","Laterite pebbles with a little sand over laterite sheet rock, on hill slopes.",None),
'depauperata':(5,"peat","Only its type site: Lake Pleasant View near Manypeaks.","Lake edges and wet depressions in sandy soil under paperbarks.",None),
'dichrosepala':(2,"laterite","Near Woodanilling and between Katanning and Nyabing.","Shallow sand over laterite with washed-in laterite pebbles, in low heath.",None),
'echinoblastus':(4,"pale sand","Hill River, Coomallo and Mount Lesueur, extending north and south.","Deep white sand or beige clayey sand beside winter-wet streams, depressions and seeps.",None),
'eneabba':(1,"pale sand","Eneabba, Badgingarra, Coomallo and Mount Lesueur.","White silica sand in low open heath.",None),
'enodes':(4.5,"peat","The far south-west corner: Scott River and Windy Harbour.","Black peaty sand on swamp edges.",None),
'gibsonii':(2.5,"laterite","Near the base of Bluff Knoll in the Stirling Range.","Clayey sand on watershed slopes strewn with flat sandstone, in low heath.",None),
'grievei':(2.5,"yellow sand over laterite","Lake Grace east to Baanga Hill, and around Lake King and Newdegate.","Beige sandy clay with a little laterite, in low open heath.",None),
'helodes':(4,"pale sand","Bullsbrook, Byford, Muchea and Gingin.","Gray sand in winter-wet depressions, and black humic sand on seasonal swamp edges.",None),
'hyperostigma':(2,"laterite","Darling Range: Bannister, Gidgegannup, Lesmurdie, Parkerville and The Lakes.","Laterite mixed with silica sand in light open forest.",None),
'lasiantha':(2,"laterite","Porongurup Range and Mount Lindesay, near Albany and Denmark.","Loamy laterite on high scree slopes in low jarrah forest.",None),
'leioblastus':(2,"pale sand","The Cataby region.","Silica sand with leaf-litter humus and laterite pebbles, under low heath.",None),
'leucoblasta':(3,"pale sand","York, Brookton, Cranbrook, Arthur River and Esperance.","Clayey sand and laterite between low shrubs in heath; soils often carry organic matter and peat.",None),
'leucostigma':(4,"pale sand","Cataby region, south-east to Mogumber.","Sandy soils on the edges of winter-wet depressions.",None),
'mannii':(3.5,"peat","Gleneagle, Boulder Rock and toward Jarrahdale.","Loam in jarrah forest, peaty sand on winter-wet seeps, and granite-outcrop aprons.",None),
'micra':(4.5,"peat","City of Swan, Perth (Swan Coastal Plain). Priority One flora.","Peat with sand mixed through. One parent of the swamp hybrid D. × badgerupii.","Few records; no climate-map data."),
'micrantha':(3,"pale sand","Common from Perth to Albany.","White silica sand on the higher edges of swamps, and deep sand pockets in the Darling Range.",None),
'microscapa':(4.5,"peat","Denmark, Hortons, Manypeaks and Frenchman Bay.","Black silty sand in seepage areas of swampy heath.",None),
'miniata':(2.5,"laterite","Gidgegannup, Toodyay and York.","Laterite and clay, or loam washed onto granite-outcrop aprons.",None),
'minutiflora':(1,"pale sand","Cataby, Mogumber, Wanneroo, Gnangarra and The Lakes.","Deep white silica sand between low shrubs in heath.",None),
'nitidula':(4,"yellow sand","East of Perth, south to Augusta and east to Cape Le Grand.","Clayey sand in and around winter-wet depressions and swamps.",None),
'nivea':(1,"yellow sand","Only around Coorow.","Deep pale yellow to beige sand on sandplain heath.",None),
'occidentalis':(4.5,"peat","Gingin, Bullsbrook, Perth, Pinjarra and Carbarup.","Peaty sand around swamp edges, winter-wet depressions and seeps.",None),
'omissa':(4,"pale sand","Widespread: Kalbarri to Ravensthorpe.","Deep white sand around winter-wet depressions; occasionally laterite.",None),
'oreopodion':(2.5,"pale sand over laterite","The foot of the Darling Range.","Sandy clay mixed with laterite pebbles in low heath.","No climate-map data."),
'paleacea':(5,"peat","Albany area: Lake Sepping, Princess Royal Harbour, Frenchman Bay, Little Grove.","Black sand among reeds and paperbarks on flats that flood in winter.",None),
'patens':(4,"pale sand","Four sites across Perth's northern suburbs, plus Manaring Lake.","Sandy edges of swamps, lakes and winter-wet depressions.",None),
'pedicellaris':(1,"pale sand","South-west of Three Springs, with sites near Badgingarra and Nambung.","Deep beige to white sand between low shrubs in heath.",None),
'platystigma':(2.5,"laterite over sand","Albany, Bannister, Busselton, Pinjarra, Stirling Range, Ravensthorpe.","Clayey sand, laterite or loam in open heath and jarrah-forest clearings.",None),
'pulchella':(4.5,"peat","Perth, Augusta, Albany and Esperance.","Sand, peaty sand, peat, laterite or loam on the edges of lakes, swamps and streams.",None),
'pycnoblasta':(1.5,"pale sand","Pingelly, Tammin, Goomalling and the Lake King area.","Clayey white sand over laterite gravel, white sand or yellow sand, in low open heath.",None),
'pygmaea':(4.5,"peat","South-eastern Australia and New Zealand; in WA only near Albany and Karridale.","A wide range of poor soils, from lake edges flooded for weeks to dry heath.","Climate covers the whole range, not just WA."),
'rechingeri':(1,"pale sand","Kalbarri, Ajana, Binnu, Mingenew and Dongara.","Deep white or yellow sand in open heath.",None),
'roseana':(4.5,"peat","South coast from Albany to Augusta.","Peaty sand on swamp edges.",None),
'sargentii':(1,"pale sand","Esperance to Cape Le Grand and Cape Arid.","Deep white silica sand in low heath and on consolidated coastal dunes.",None),
'scorpioides':(1.5,"laterite over pale sand","Albany, Manypeaks, Bowelling and Gidgegannup.","Rocky laterite outcrops with a little silica sand, in open woodland or heath.",None),
'sewelliae':(2,"laterite","Chittering Valley, Muchea and Toodyay.","Laterite with silica sand in open forest, and laterite over sheet rock.",None),
'silvicola':(1.5,"laterite","Avon Valley, North Bannister and Boddington.","Laterite on the summits of high hills in open jarrah forest.",None),
'spilos':(2.5,"laterite","Widespread: Walkaway south to Bannister, inland to Wyalkatchem.","Loam strewn with laterite pebbles, or clayey sand, often near granite outcrops.",None),
'stelliflora':(2,"laterite","Jarrah forest between Busselton and Margaret River.","Laterite soils, sometimes with a little silica sand.",None),
'trichocaulis':(1.5,"pale sand","Stirling Range east along the coast to Cape Arid.","Deep white sand, or laterite and sand, under low heath and open woodland.",None),
'verrucata':(2.5,"pale sand","Common from Albany to Manypeaks.","Clayey sand between low shrubs in heath and scrub.",None),
'walyunga':(4,"laterite over pale sand","Walyunga National Park and nearby.","Sandy white clay with a thin laterite gravel layer, around winter-wet springs and seeps.",None),
}
H={  # hybrids: (score, parents, distribution, habitat, note)
'× badgerupii':(4.5,"D. micra × D. patens","Western Australia. Now extinct in the wild.","Peaty sand or pure peat on swamp and lake edges.","Known only in cultivation; no climate shown."),
'× badgingarra':(4,"D. allantostigma × D. omissa","Only its type site at Badgingarra.","Clay-rich sand on the edges of wet depressions.","No climate-map data."),
'× carbarup':(4,"D. occidentalis × D. platystigma","Only its type site at Carbarup, near Mount Barker.","Laterite and sand in winter-wet depressions with dwarf paperbarks.","Sterile. One grower source gives D. nitidula × D. occidentalis instead."),
'× legrandii':(4.5,"D. nitidula × D. australis","Only its type site at Cape Le Grand.","Black silty sand in swampy heath.","Sterile. No climate-map data."),
'× pingellyensis':(4,"D. nitidula × D. omissa","Only its type site near Pingelly.","White sand on the edges of wet depressions.","No climate-map data."),
'× sidjamesii':(4,"D. patens × D. pulchella","Three sites, two of them in the Perth metropolitan area.","Sandy edges of swamps, lakes and winter-wet depressions.",None),
}
band=lambda s:'Dry' if s<=1.5 else 'Drained' if s<=2.5 else 'Moist' if s<=4 else 'Wet'
out=[]
def clim(key):
    v=M.get(key)
    if not v or not v['filt'] or key=='× badgerupii': return None,None
    f=v['filt']
    b=BOM.get(key)
    c={'p90':f['hotTypical'],'hotMonth':MON[f['hotMonth']],'avgHigh':max(b['hi']) if b else f['avgHigh'],
       'hi':b['hi'] if b else f['monthlyHi'],'lo':b['lo'] if b else f['monthlyLo'],'p90m':f['monthlyP90'],
       'pr':b['pr'] if b else f['precip'],'rainSrc':'bom' if b else 'power',
       'records':v['nKeep'],'cells':f['n'],'obscured':v['obsc'],'dryMo':(b or f)['dryMo'],'deficit':(b or f)['deficit']}
    return c, v['taxon_id']
for k,(s,soil,dist,hab,note) in S.items():
    c,tid=clim(k)
    out.append({'id':k,'name':'Drosera '+k,'hyb':False,'band':band(s),'score':s,'soil':soil,'dist':dist,'hab':hab,
                'note':note,'clim':c,'taxon':tid,'alias':['coalara'] if k=='citrina' else []})
for k,(s,par,dist,hab,note) in H.items():
    c,tid=clim(k)
    out.append({'id':k.replace('× ','x-'),'name':'Drosera '+k,'hyb':True,'parents':par,'band':band(s),'score':s,'soil':None,
                'dist':dist,'hab':hab,'note':note,'clim':c,'taxon':tid,'alias':[]})
json.dump({'v':1,'built':'2026-10-30','taxa':out},open(os.path.join(WORK,'pygmy-data.json'),'w'),separators=(',',':'))
import collections
print(len(out), collections.Counter(t['band'] for t in out), 'no climate:',[t['id'] for t in out if not t['clim']])
