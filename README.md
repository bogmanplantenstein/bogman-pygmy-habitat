# Bogman Pygmy Sundew Habitat Finder

Searchable widget for **burymeinthebog.com/grow/pygmy-sundews**: 52 pygmy *Drosera* species and 6 natural hybrids, grouped by how wet the soil should stay (Dry / Drained / Moist / Wet). Each species shows its summer heat, dry season, habitat, sources and shop links.

Private repo. Proprietary, all rights reserved (see `LICENSE`). Sources are credited in `ATTRIBUTION.md`.

## How it fits together

```
public/            ← what Cloudflare publishes (Worker: bogman-pygmy-habitat.bogman-plantenstein.workers.dev)
  widget.js          the widget (generated, don't edit by hand)
  pygmy-data.json    the dataset (generated)
  map/               Köppen base map image (generated)
  _headers           only burymeinthebog.com may read the data from a browser
  index.html         test page
src/widget.html    ← widget source (markup, styles, script)
build/             ← scripts that rebuild the data and widget
embed/squarespace-code-block.html  ← paste this into Squarespace
```

## Photos

Photos come from two places, read live in the visitor's browser. Nothing is copied here.

- **Cultivated:** the Bogman Gallery (`gallery.json` on R2, the same file the /species page uses). Publish photos to the gallery as usual and they appear here. Forms show as chips. Cultivated crosses are left out.
- **In the wild:** iNaturalist photos from the research-grade observations the climate map already uses (observation ids are in the dataset; photo URLs and credits load from the iNaturalist API). Only CC0, CC BY and CC BY-SA photos are shown, credited to each photographer. `INAT_LIC` in `src/widget.html` controls this.

## Changing the data or the widget

The text, moisture scores and dormancy flags live in `build/widget_data.py` and `build/widget_patch.py`. The widget lives in `src/widget.html`. To rebuild, with a clone of `bogman-climate-map` next to this repo:

```bash
bash build/build.sh
```

Then commit `public/`. Cloudflare redeploys `main` automatically (settings in `wrangler.jsonc`).

## Embedding

Paste `embed/squarespace-code-block.html` into a Squarespace **Code Block**. It holds only a container, one script tag and a plain-text species list for search engines, so updates never need re-pasting.

## Method notes
- **Map:** Köppen–Geiger 1991–2020 (Beck et al. 2023, 1 km). Species records are shown on a 0.25° (~25 km) grid only.
- **Moisture band:** scored 1–5 from published habitat descriptions. Dry ≤1.5, Drained 2–2.5, Moist 3–4, Wet 4.5–5.
- **Hot extreme:** the climate map's hottest-month 90th-percentile daily high (NASA POWER, ~50 km grid), research-grade records inside the native range only.
- **Dry months:** Bureau of Meteorology station averages; a month is dry when rainfall (mm) is less than twice the mean temperature (°C). 5–6 = dry summer, 7+ = long dry summer.
- **Summer-dormancy flag:** grower reports of dormancy in cultivation.
- **Sensitive locations:** no observation coordinates are published. *D. micra* (Priority One) is described to suburb level only.
