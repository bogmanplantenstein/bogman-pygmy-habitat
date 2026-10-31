"""Process photos/ → public/photos/ for the widget.

Naming: photos/<species-id>.jpg, or <species-id>-2.jpg, -3.jpg for extras.
  species-id = the species epithet (roseana, pulchella) or x-<name> for hybrids (x-sidjamesii).
Optional credit: put a line "<filename>: Photographer Name" in photos/credits.txt.

Each output image is re-encoded with NO metadata (EXIF/GPS removed), resized to max 1200 px on
the long edge, saved as JPEG quality 82. A manifest maps species-id → list of images.
"""
import os, re, json, sys
from PIL import Image, ImageOps
try:                                   # iPhone HEIC support, if installed
    from pillow_heif import register_heif_opener; register_heif_opener()
except ImportError:
    pass

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
SRC = os.path.join(ROOT, 'photos'); OUT = os.path.join(ROOT, 'public', 'photos')
DATA = json.load(open(os.path.join(ROOT, 'public', 'pygmy-data.json')))
IDS = {t['id'] for t in DATA['taxa']}
MAX = 1200
os.makedirs(OUT, exist_ok=True)

credits = {}
cpath = os.path.join(SRC, 'credits.txt')
if os.path.exists(cpath):
    for line in open(cpath):
        if ':' in line:
            k, v = line.split(':', 1); credits[k.strip()] = v.strip()

manifest, problems = {}, []
for fn in sorted(os.listdir(SRC)):
    stem, ext = os.path.splitext(fn)
    if ext.lower() not in ('.jpg', '.jpeg', '.png', '.webp', '.heic'):
        continue
    m = re.match(r'^(x-[a-z]+|[a-z]+)(?:-(\d+))?$', stem.lower())
    sid = m.group(1) if m else None
    if sid not in IDS:
        problems.append(f'{fn}: name does not match a species id'); continue
    try:
        im = Image.open(os.path.join(SRC, fn))
        im = ImageOps.exif_transpose(im)          # apply camera rotation before stripping metadata
        im = im.convert('RGB')
        im.thumbnail((MAX, MAX))
        clean = Image.new('RGB', im.size); clean.paste(im)   # fresh image: no EXIF, GPS or ICC carried over
        name = stem.lower() + '.jpg'
        clean.save(os.path.join(OUT, name), 'JPEG', quality=82, optimize=True, progressive=True)
        manifest.setdefault(sid, []).append({'f': name, 'w': clean.width, 'h': clean.height,
                                             **({'credit': credits[fn]} if fn in credits else {})})
    except Exception as e:
        problems.append(f'{fn}: {e}')

# remove outputs whose source was deleted
keep = {i['f'] for v in manifest.values() for i in v}
for fn in os.listdir(OUT):
    if fn.endswith('.jpg') and fn not in keep:
        os.remove(os.path.join(OUT, fn))
for v in manifest.values():
    v.sort(key=lambda i: (len(i['f']), i['f']))
json.dump(manifest, open(os.path.join(OUT, 'manifest.json'), 'w'), indent=1, sort_keys=True)
print(f'{sum(len(v) for v in manifest.values())} photos for {len(manifest)} species')
for p in problems:
    print('WARNING', p)
if problems and '--strict' in sys.argv:
    sys.exit(1)
