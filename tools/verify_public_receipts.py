#!/usr/bin/env python3
import json, pathlib, re, sys
bad=[]; rx=re.compile(r'(seed|private|token|cookie|password|secret|signed_url|wallet)',re.I); allow={'sig','secret_material_recorded'}
for p in pathlib.Path('receipts/public').glob('*.json'):
    try: data=json.loads(p.read_text())
    except Exception as e: bad.append(f'{p}: invalid json {e}'); continue
    def w(x,path='$'):
        if isinstance(x,dict):
            for k,v in x.items():
                if rx.search(str(k)) and k not in allow: bad.append(f'{p}: secret-like key {path}.{k}')
                w(v,f'{path}.{k}')
        elif isinstance(x,list):
            for i,v in enumerate(x): w(v,f'{path}[{i}]')
        elif isinstance(x,str) and ('/say-signed/' in x or '/set-signed/' in x): bad.append(f'{p}: signed URL leaked at {path}')
    w(data)
print(json.dumps({'ok':not bad,'problems':bad},indent=2)); sys.exit(1 if bad else 0)
