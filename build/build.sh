#!/usr/bin/env bash
# Rebuild public/pygmy-data.json from sources.
# Needs a read-only clone of bogman-climate-map next to this repo (or set CLIMATE_MAP_INAT to its inat/ folder).
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p ../work
python3 build_clim.py      # climate-map hot extremes (research-grade, in-range records)
python3 build_bom.py       # BOM station rainfall, temps, dry months
python3 widget_data.py     # species/hybrid text, moisture scores, climate merge
python3 widget_patch.py    # Fierce Flora, D. micra label, dormancy flags, sources
cp ../work/pygmy-data.json ../public/pygmy-data.json
python3 make_widget.py     # public/widget.js + embed/squarespace-code-block.html
echo "Built public/pygmy-data.json"
