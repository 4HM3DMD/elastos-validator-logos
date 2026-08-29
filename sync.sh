#!/bin/bash
# Pull the validator-logos repo (images) -> publish to /images, build the Essentials logo.json manifest
# (BPoS by ownerpublickey + CR-council by DID), and optimize the served images. Fail-safe.
set -e
REPO_DIR=/opt/elastos-logos
SERVE=/var/lib/widgets-logos/images
git -C "$REPO_DIR" fetch -q --depth 1 origin main
git -C "$REPO_DIR" reset -q --hard origin/main
mkdir -p "$SERVE"
cp -a "$REPO_DIR/images/." "$SERVE/"
# Essentials BPoS + council images need /images/logo.json (see build-logo-manifest.py). Fetch upstream manifest
# -> temp, then merge live CR-council on top -> served logo.json. Keep-last-good on fetch failure.
# The upstream manifest (bocheng0000/BPoS-logo) now returns 404 and is no longer a
# dependency: BPoS nodes are mapped in overrides.json in this repo. The builder bases
# itself on the last-good served logo.json and applies council + overrides on top.
python3 "$REPO_DIR/build-logo-manifest.py" || true
# Optimize served images for mobile (re-derived from pristine repo originals each run -> no generation loss;
# logo.json is never an image extension so it's untouched).
if command -v mogrify >/dev/null 2>&1; then
  shopt -s nullglob nocaseglob
  jpgs=("$SERVE"/*.jpg "$SERVE"/*.jpeg)
  pngs=("$SERVE"/*.png)
  [ ${#jpgs[@]} -gt 0 ] && mogrify -resize '256x256>' -strip -quality 82 -interlace Plane "${jpgs[@]}" || true
  [ ${#pngs[@]} -gt 0 ] && mogrify -resize '256x256>' -strip -define png:compression-level=9 "${pngs[@]}" || true
  # lossy PNG quantization (palette) — typically ~halves logo PNGs; quality floor 70, skip if it would grow the file.
  if command -v pngquant >/dev/null 2>&1 && [ ${#pngs[@]} -gt 0 ]; then
    pngquant --force --skip-if-larger --quality=70-95 --ext .png "${pngs[@]}" 2>/dev/null || true
  fi
  shopt -u nullglob nocaseglob
fi
chown -R widgets:widgets /var/lib/widgets-logos
chmod -R a+rX /var/lib/widgets-logos
