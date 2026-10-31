"""Map layer for the widget.
  public/map/sw-wa-koppen.png   Köppen–Geiger 1991–2020 base map of south-west WA (Beck et al. 2023, CC BY 4.0)
  work/pygmy-data.json          adds D.map (extent, grid, towns, Köppen legend) and, per taxon:
                                  cells  coarse 0.25° grid cells with research-grade records (no coordinates)
                                  inat   iNaturalist observation ids with photos (photos + attribution load live)
Records follow build_clim.py: research grade, inside WA, minus excluded records. D. micra: type-locality cell only.
"""
import os, sys, json, math
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..'); WORK = os.path.join(ROOT, 'work')
sys.path.insert(0, HERE)
from mapclim import taxa, obs, inWA
from build_clim import PYG, HYB, excluded

KG_TIF = os.environ.get('KOPPEN_TIF', os.path.join(os.path.dirname(os.environ.get('CLIMATE_MAP_INAT', os.path.join(ROOT, '..', 'bogman-climate-map', 'inat'))),
                        'koppen_geiger_tif', '1991_2020', 'koppen_geiger_0p00833333.tif'))
W, E, N, S = 113.5, 123.6, -27.2, -35.2           # map extent (lon/lat)
G = 0.25                                          # grid cell, degrees (≈ iNat's obscuring box)
MAXOBS = 40

# ---- Köppen base image
import tifffile
tf = tifffile.TiffFile(KG_TIF); pg = tf.pages[0]
d = pg.tags['ModelPixelScaleTag'].value[0]; lon0, lat0 = pg.tags['ModelTiepointTag'].value[3:5]
r0, r1 = int(round((lat0 - N) / d)), int(round((lat0 - S) / d)); c0, c1 = int(round((W - lon0) / d)), int(round((E - lon0) / d))
kg = pg.asarray()[r0:r1, c0:c1]
KOPPEN = {  # code: (name, plain-English, colour tuned to WA landscape tones)
    4:  ('BWh', 'Hot desert',                        (108, 50, 36)),
    6:  ('BSh', 'Hot semi-arid',                     (146, 82, 46)),
    7:  ('BSk', 'Cool semi-arid',                    (124, 98, 70)),
    8:  ('Csa', 'Mediterranean, hot summer',         (172, 144, 64)),
    9:  ('Csb', 'Mediterranean, warm summer',        (96, 124, 70)),
    15: ('Cfb', 'Temperate, no dry season',          (48, 90, 64)),
}
# ---- records → cells + iNat ids
name = {i: t[1] for i, t in enumerate(taxa)}
D = json.load(open(os.path.join(WORK, 'pygmy-data.json')))
byid = {t['id']: t for t in D['taxa']}
def wid(ep): return ('x-' + ep[2:]) if ep.startswith('× ') else ep
def cell(lat, lng): return [int(math.floor((lng - W) / G)), int(math.floor((N - lat) / G))]
for i, n in name.items():
    p = n.split(' ', 1)
    if len(p) < 2 or (p[1] not in PYG and p[1] not in HYB): continue
    t = byid.get(wid(p[1]))
    if not t: continue
    keep = [o for o in obs if o[3] == i and not (o[5] & 1) and not excluded(n, o)]
    wa = [o for o in keep if inWA(o[1], o[2]) and W <= o[2] <= E and S <= o[1] <= N]
    cells = sorted({tuple(cell(o[1], o[2])) for o in wa})
    t['cells'] = [list(c) for c in cells]
    ph = sorted([o for o in keep if o[5] & 4], key=lambda o: o[4] or '', reverse=True)
    t['inat'] = [o[0] for o in ph[:MAXOBS]]
    zc = {}
    for o in wa:
        z = int(kg[int((N - o[1]) / d), int((o[2] - W) / d)]) if (S < o[1] < N and W < o[2] < E) else 0
        if z in KOPPEN: zc[z] = zc.get(z, 0) + 1
    tot = sum(zc.values())
    t['kz'] = [[KOPPEN[z][0], round(100 * n / tot)] for z, n in sorted(zc.items(), key=lambda kv: -kv[1]) if 100 * n / tot >= 10] if tot else []
if 'micra' in byid:                               # Priority One: type locality only, one coarse cell
    byid['micra']['cells'] = [cell(-31.8557, 115.9124)]; byid['micra']['inat'] = []; byid['micra']['kz'] = [['Csa', 100]]

# equal-area-ish: scale longitude by cos(mid-lat) so the image isn't stretched
midlat = math.radians((N + S) / 2); PX = 110                       # px per degree latitude
w = int(round((E - W) * math.cos(midlat) * PX)); h = int(round((N - S) * PX))
small = np.array(Image.fromarray(kg).resize((w, h), Image.NEAREST))
rgba = np.zeros((h, w, 4), np.uint8)
for code, (_, _, c) in KOPPEN.items():
    m = small == code; rgba[m, :3] = c; rgba[m, 3] = 255
land = small > 0
os.makedirs(os.path.join(ROOT, 'public', 'map'), exist_ok=True)
Image.fromarray(rgba, 'RGBA').quantize(colors=16, method=Image.FASTOCTREE).save(os.path.join(ROOT, 'public', 'map', 'sw-wa-koppen.png'), optimize=True)
present = {int(k) for k in np.unique(small) if k in KOPPEN}
D['map'] = dict(
    img='map/sw-wa-koppen.png', w=w, h=h, ext=[W, E, N, S], g=G, cos=round(math.cos(midlat), 5),
    koppen=[dict(c=KOPPEN[k][0], n=KOPPEN[k][1], rgb='#%02x%02x%02x' % KOPPEN[k][2]) for k in sorted(present, key=lambda k: [6, 4, 7, 8, 9, 15].index(k))],
    towns=[['Perth', -31.95, 115.86], ['Geraldton', -28.78, 114.61], ['Bunbury', -33.33, 115.64], ['Albany', -35.02, 117.88],
           ['Esperance', -33.86, 121.89], ['Kalgoorlie', -30.75, 121.47], ['Narrogin', -32.93, 117.18]],
)
json.dump(D, open(os.path.join(WORK, 'pygmy-data.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
nc = sum(1 for t in D['taxa'] if t.get('cells')); ni = sum(len(t.get('inat', [])) for t in D['taxa'])
print('map %dx%d, taxa with cells %d/%d, iNat ids %d, koppen %s' % (w, h, nc, len(D['taxa']), ni, [k['c'] for k in D['map']['koppen']]))
print('no cells:', [t['id'] for t in D['taxa'] if not t.get('cells')])
