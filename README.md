# Elastos Validator Logos

Single source of truth for Elastos BPoS validator (supernode) logos.

## Served at
- `https://rpc.elastos.info/images/<file>` — box-1 syncs this repo on a daily timer
- `https://cdn.jsdelivr.net/gh/4HM3DMD/elastos-validator-logos@main/images/<file>` — free global CDN, hotlinkable

## Add / update a logo
Open a PR adding `images/<ValidatorName>.png` (`.jpg`/`.jpeg`/`.svg` also fine). Square, ideally < 100 KB.
For a new BPoS validator, also add its owner public key to `overrides.json`, mapped to the image filename.
The explorer and Essentials look logos up by owner key, so without that entry the image is never shown.
Consumers pick it up automatically: jsDelivr within minutes, the explorer within the hour,
`rpc.elastos.info/images` within a day.

## Consumers (point both here — one source, no drift)
- The Elastos explorer (`elastos-explorer-new`): syncs this repo hourly and builds its own `logo.json`
  from a frozen base mapping plus `overrides.json`.
- `rpc.elastos.info/images` — box-1 pulls this repo via a daily `systemd` timer.

Images are matched to a validator through `logo.json`, keyed by owner public key (BPoS) or DID (council).
A filename alone does not link an image to a validator; the mapping does.

## Logo ownership
Each logo is the property of its respective validator / node operator, hosted here only to display their
identity across Elastos services. Operators can request a change or removal via an issue or PR.
