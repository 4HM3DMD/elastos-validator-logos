# Elastos Validator Logos

Single source of truth for Elastos BPoS validator (supernode) logos.

## Served at
- `https://rpc.elastos.info/images/<file>` — box-1 syncs this repo on a daily timer
- `https://cdn.jsdelivr.net/gh/4HM3DMD/elastos-validator-logos@main/images/<file>` — free global CDN, hotlinkable

## Add / update a logo
Open a PR adding `images/<ValidatorName>.png` (`.jpg`/`.jpeg`/`.svg` also fine). Square, ideally < 100 KB.
Consumers pick it up automatically — jsDelivr within minutes, `rpc.elastos.info/images` within a day.

## Consumers (point both here — one source, no drift)
- The Elastos explorer (`elastos-explorer-new`) — fetch logos from this repo / jsDelivr.
- `rpc.elastos.info/images` — box-1 pulls this repo via a daily `systemd` timer.

Logos are matched to a validator by **filename**.
