"""Updates from Drosera of the World (Lowrie, Nunn, Robinson, Bourke & Fleischmann 2017, vol. 1).
Facts only, written in our own words. Moisture bands are NOT changed here; disagreements are listed for review.
Adds per taxon: 'rest' (summer rest type) and 'restNote'; edits hab/dist/note where the book adds or corrects detail.
"""
import os, json
WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'work')
P = os.path.join(WORK, 'pygmy-data.json')
D = json.load(open(P))
T = {t['id']: t for t in D['taxa']}

D['sources']['dotw'] = {'t': 'Drosera of the World (Lowrie et al. 2017), vol. 1', 'u': None}

# Summer rest, as described in the book's phenology notes.
#   bud  = dry summer rest as a tight dormant bud
#   slow = rarely fully dormant; keeps growing slowly while some moisture remains deeper in the soil
#   seed = often dies back and returns from seed
REST = {
 'bud': "androsacea bindoon callistos citrina closterostigma coomallo dichrosepala echinoblastus eneabba enodes gibsonii grievei helodes "
        "hyperostigma lasiantha leioblastus leucoblasta mannii micrantha miniata minutiflora nivea occidentalis oreopodion pedicellaris "
        "platystigma pycnoblasta rechingeri roseana sargentii scorpioides sewelliae silvicola spilos stelliflora trichocaulis verrucata walyunga",
 'slow': "australis x-badgerupii x-badgingarra x-carbarup depauperata x-legrandii leucostigma micra microscapa nitidula paleacea patens "
         "x-pingellyensis pulchella x-sidjamesii barbigera",
 'seed': "omissa",
}
REST_NOTE = {
 'barbigera': "Rests dry in summer but seldom forms a bud unless there is a drought.",
 'pulchella': "Rests dry in summer but seldom forms a bud; usually just slows down.",
 'australis': "In a harsh, droughty summer adult plants can die and the colony returns from seed.",
 'occidentalis': "In a harsh, droughty summer the colony may carry over only as seed.",
 'omissa': "Seldom forms a dormant bud; colonies usually return from seed after summer.",
 'paleacea': "Its habitat stays slightly moist; plants slow down rather than going fully dormant.",
 'pygmaea': "Depends on habitat: slows down where moist, forms a bud where summers are dry or winters snowy.",
 'micra': "Can form a dormant bud but usually just slows its growth.",
}
for kind, ids in REST.items():
    for i in ids.split():
        T[i]['rest'] = kind
T['pygmaea']['rest'] = 'varies'
for i, n in REST_NOTE.items():
    T[i]['restNote'] = n

# Habitat / range / notes (paraphrased from the book; suburb- or region-level only).
UPD = {
 'androsacea': dict(dist="Around Perth, with inland records south to Corrigin, Dragon Rocks, Katanning, the Stirling Range, Varley and Williams, and east to Bruce Rock and Merredin."),
 'australis': dict(hab="Sandy soil over laterite near the coast, usually on the slightly drier ground just above winter-wet hollows.",
                   note="Salmon-pink flowered plants are recorded around Warriup."),
 'barbigera': dict(hab="White silica sand and laterite gravel, only on the tops of laterite hills."),
 'coomallo': dict(hab="Laterite pebbles with a little silica sand over sheet laterite, on the slopes of laterite hills."),
 'depauperata': dict(note="Probably of hybrid origin (likely parents grow nearby), but it sets seed and has stabilised as a species."),
 'echinoblastus': dict(hab="Deep white sand or beige clayey sand beside winter-wet streams, depressions and seeps. These stay damp after the rains end but dry out completely in summer.",
                       dist="Centred on Hill River, Coomallo and Mount Lesueur, with a range running about 100 km north and 200 km south."),
 'gibsonii': dict(dist="Stirling Range: near the base of Bluff Knoll and along Stirling Range Drive, about 13 km to the west."),
 'helodes': dict(hab="White sand, sometimes with a little laterite, in winter-wet depressions, and black humic sand on seasonal swamp edges. Often sits in water in midwinter but dries out completely by flowering time."),
 'hyperostigma': dict(dist="Darling Range: Bannister, Bowelling, Gidgegannup, Lesmurdie, Marradong, Parkerville and The Lakes."),
 'leioblastus': dict(dist="Cataby region: the type site and a second site a few kilometres north.",
                     note="Much of the type habitat has been cleared, mined for sand or burnt (2009)."),
 'leucoblasta': dict(hab="Clayey sand and laterite between and under low shrubs in heath.",
                     dist="Widely scattered: the Darling Range east of Perth, York, Brookton and Arthur River, south to Cranbrook and the upper Kalgan River, and along the south coast to about 100 km east of Esperance.",
                     note="Flower centers vary by population: reddish around Esperance, green around Brookton. Cranbrook plants have the largest flowers, about 3.5 cm across."),
 'micra': dict(dist="Perth's northern suburbs (Malaga and Ellenbrook). Listed Priority One flora in WA."),
 'micrantha': dict(dist="Common from Perth to Albany, and north of Perth to Muchea."),
 'minutiflora': dict(note="Quickly colonises disturbed sand, such as old sand pits."),
 'oreopodion': dict(dist="Only its type site near Byford, at the foot of the Darling Range."),
 'patens': dict(note="A former site near Canning Vale was lost to development."),
 'pulchella': dict(hab="Sand, peaty sand, peat, laterite or loam on the edges of lakes, swamps, streams and seeps, wherever the ground stays moist for most of the year; sometimes grows submerged."),
 'pycnoblasta': dict(dist="Pingelly, Tammin, Goomalling, Hatter Hill and the Lake King area."),
 'sargentii': dict(note="Readily colonises disturbed sand such as road verges and firebreaks."),
 'scorpioides': dict(note="A long-stemmed form grows in a permanent seep between Albany and Denmark."),
 'trichocaulis': dict(dist="South coast between Albany and Cape Arid, inland to the Stirling Range, including Ravensthorpe, Hopetoun and Esperance."),
 'x-badgerupii': dict(dist="Perth's northern suburbs: two remaining sites (Malaga and near Ellenbrook). Extinct at its true type site, Lake Jandabup.",
                      note="The name refers to Lake Badgerup by mistake; it was never found there. Remaining sites are threatened by development and falling water tables. No climate-map data."),
 'x-carbarup': dict(note="Sterile. Both parents were found growing near the hybrid in 2001."),
 'x-sidjamesii': dict(dist="Perth's northern suburbs: Lake Gnangarra (type site), Wanneroo, Beechboro and Lake Adams in Mariginiup (found 2014)."),
}
for i, u in UPD.items():
    T[i].update(u)

COVERED = set(REST['bud'].split()) | set(REST['slow'].split()) | {'omissa', 'pygmaea'}
for i in COVERED | set(UPD):
    if 'dotw' not in T[i].get('src', []):
        T[i]['src'] = T[i].get('src', []) + ['dotw']

json.dump(D, open(P, 'w'), ensure_ascii=False, separators=(',', ':'))
print('dotw patch: rest on %d taxa, text updates on %d' % (sum(1 for t in D['taxa'] if t.get('rest')), len(UPD)))
