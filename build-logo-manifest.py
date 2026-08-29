#!/usr/bin/env python3
# Build the served /images/logo.json = upstream BPoS-logo manifest (BPoS nodes by ownerpublickey + many council
# DIDs) PLUS current CR-council members keyed by DID, mapped to a logo we actually serve. Self-maintaining:
# re-derives the live council from listcurrentcrs each run, so newly-elected members with a matching logo are
# auto-covered, and the upstream daily refresh never clobbers them. Members we hold no logo for are left out
# (Essentials falls back to their DID-document/Hive avatar for those — the only image source that exists).
import json, urllib.request, os, re, sys

SERVE = "/var/lib/widgets-logos/images"
up = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else None

def load(p):
    with open(p) as f: return json.load(f)

# base = fetched upstream manifest, else keep the last-good served one
try:
    manifest = load(up) if up else load(f"{SERVE}/logo.json")
except Exception:
    manifest = load(f"{SERVE}/logo.json") if os.path.exists(f"{SERVE}/logo.json") else {}

imgs = [f for f in os.listdir(SERVE) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
norm = lambda s: re.sub(r"[^a-z0-9]", "", (s or "").lower())
by_norm = {}
for f in imgs:
    by_norm.setdefault(norm(os.path.splitext(f)[0]), f)
have = set(imgs)

try:
    req = urllib.request.Request("http://127.0.0.1:8336",
        data=json.dumps({"method": "listcurrentcrs", "params": {"state": "all"}}).encode(),
        headers={"content-type": "application/json"})
    council = json.loads(urllib.request.urlopen(req, timeout=8).read())["result"]["crmembersinfo"]
except Exception as e:
    council = []
    print(f"listcurrentcrs failed ({e}) — upstream-only", file=sys.stderr)

added = 0
for m in council:
    did, nk = m.get("did"), m.get("nickname", "")
    if not did:
        continue
    # already covered by upstream with a logo we serve?
    cur = manifest.get(did)
    if cur and cur.get("logo") in have:
        continue
    g = by_norm.get(norm(nk))
    if g:
        manifest[did] = {"nickname": nk, "logo": g}
        added += 1

# Local overrides, applied last so they beat anything inherited. The upstream BPoS
# manifest (bocheng0000/BPoS-logo) now 404s, so BPoS producers are mapped here by
# owner public key instead of being fetched.
ov = os.path.join(os.path.dirname(os.path.abspath(__file__)), "overrides.json")
try:
    for k, v in load(ov).items():
        if k.startswith("_"):
            continue
        if v.get("logo") in have:
            manifest[k] = v
            added += 1
        else:
            print(f"overrides: {v.get('logo')} not in served images, skipped", file=sys.stderr)
except FileNotFoundError:
    pass
except Exception as e:
    print(f"overrides load failed ({e}) — ignored", file=sys.stderr)

with open(f"{SERVE}/logo.json", "w") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
print(f"logo.json written: {len(manifest)} entries (+{added} live-council additions), council size {len(council)}")
