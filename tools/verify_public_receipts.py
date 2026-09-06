#!/usr/bin/env python3
import json, pathlib, re, sys
bad=[]
SECRET_KEYS=re.compile(r'(seed|private|token|cookie|password|secret|signed_url|wallet)', re.I)
for p in pathlib.Path('receipts/public').glob('*.json'):
    try: data=json.loads(p.read_text())
    except Exception as e: bad.append(f'{p}: invalid json {e}'); continue
    text=json.dumps(data, sort_keys=True)
    if SECRET_KEYS.search(text): bad.append(f'{p}: secret-like word present')
    if '/say-signed/' in text or '/set-signed/' in text: bad.append(f'{p}: signed URL leaked')
if bad:
    print(json.dumps({'ok':False,'problems':bad}, indent=2)); sys.exit(1)
print(json.dumps({'ok':True,'problems':[]}, indent=2))
