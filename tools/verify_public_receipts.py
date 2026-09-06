#!/usr/bin/env python3
import json, pathlib, re, sys
bad=[]
SECRET_KEY=re.compile(r'(seed|private|token|cookie|password|secret|signed_url|wallet)', re.I)
ALLOW_KEYS={'sig','secret_material_recorded'}
for p in pathlib.Path('receipts/public').glob('*.json'):
    try: data=json.loads(p.read_text())
    except Exception as e: bad.append(f'{p}: invalid json {e}'); continue
    def walk(x,path='$'):
        if isinstance(x,dict):
            for k,v in x.items():
                if SECRET_KEY.search(str(k)) and k not in ALLOW_KEYS:
                    bad.append(f'{p}: secret-like key {path}.{k}')
                walk(v, f'{path}.{k}')
        elif isinstance(x,list):
            for i,v in enumerate(x): walk(v, f'{path}[{i}]')
        elif isinstance(x,str):
            if '/say-signed/' in x or '/set-signed/' in x:
                bad.append(f'{p}: signed URL leaked at {path}')
            if re.fullmatch(r'[0-9a-fA-F]{64}', x) and not path.endswith(('text_sha256','.sha256')):
                bad.append(f'{p}: 64-hex secret-like value at {path}')
    walk(data)
print(json.dumps({'ok':not bad,'problems':bad},indent=2)); sys.exit(1 if bad else 0)
