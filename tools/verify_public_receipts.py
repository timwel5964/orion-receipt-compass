#!/usr/bin/env python3
import json,pathlib,re,sys
bad=[]; rx=re.compile(r'(seed|private|token|cookie|password|secret|signed_url|wallet)',re.I)
for p in pathlib.Path('receipts/public').glob('*.json'):
 d=json.loads(p.read_text()); t=json.dumps(d,sort_keys=True)
 if rx.search(t) or '/say-signed/' in t or '/set-signed/' in t: bad.append(str(p))
print(json.dumps({'ok':not bad,'problems':bad},indent=2)); sys.exit(1 if bad else 0)
