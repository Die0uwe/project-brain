#!/usr/bin/env python3
"""Synchroniseert project-brain naar de Bibliotheek van SBWebUI (kennis_sync.php), alleen standaardbibliotheek.

Wat het doet:
  1. git pull in de brain-repo (tenzij --no-pull)
  2. neemt CONTEXT.md, projects/*.md en docs/knowledge/session-history.md
  3. splitst lange bestanden op koppen (##) in delen van hoogstens 7500 tekens
  4. vraagt SBWebUI welke Brain-pagina's er al zijn, stuurt alleen nieuwe of gewijzigde delen en haalt verdwenen delen weg

In SBWebUI komen de pagina's in de categorie "DieOuwe Brain", gepubliceerd en geïndexeerd: de chat (RAG) en de Discord-bot gebruiken ze.

Instellingen (één van beide):
  - ~/.sbwebui-brain.env met SBWEBUI_URL (bijv. https://sbwebui.scriptspace.nl) en SBWEBUI_BOT_SECRET
  - anders: de .env van de live CoreBot (SBWEBUI_PING_URL en SBWEBUI_BOT_SECRET), die staat al goed
Het geheim komt nooit in de repo, in een argument of in de uitvoer.

Gebruik:
  python tools/brain_sync_sbwebui.py              synchroniseren
  python tools/brain_sync_sbwebui.py --dry-run    alleen laten zien wat er zou gebeuren (vraagt wel de lijst op)
  python tools/brain_sync_sbwebui.py --offline    alleen de delen maken en tonen, niets versturen
Exitcode 0 = goed, 1 = fout(en), 2 = instellingen ontbreken.
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PREFIX = 'https://github.com/Die0uwe/project-brain/blob/main/'
MAX_PART = 7500
BOT_ENV = Path(r'C:\SERVERS\DIEOUWE-AI\SBWEBUI\##sbwebui-discord-bot##\discord-bot\.env')
OWN_ENV = Path(os.environ.get('BRAIN_SYNC_ENV') or (Path.home() / '.sbwebui-brain.env'))   # BRAIN_SYNC_ENV: ander bestand (tests)
UA = 'DieOuwe-brain-sync/1.0'


def read_env(p: Path) -> dict:
    out = {}
    try:
        for line in p.read_text(encoding='utf-8').splitlines():
            if '=' in line and not line.lstrip().startswith('#'):
                k, v = line.split('=', 1)
                out[k.strip()] = v.strip().strip('"').strip("'")
    except OSError:
        pass
    return out


def settings() -> tuple[str, str, str]:
    own = read_env(OWN_ENV)
    url, secret, where = own.get('SBWEBUI_URL', ''), own.get('SBWEBUI_BOT_SECRET', ''), str(OWN_ENV)
    if not (url and secret):
        bot = read_env(BOT_ENV)
        ping = bot.get('SBWEBUI_PING_URL', '')
        url = url or re.sub(r'/[^/]*$', '', ping)
        secret = secret or bot.get('SBWEBUI_BOT_SECRET', '')
        where = 'de .env van de live CoreBot'
    return url.rstrip('/'), secret, where


def files() -> list[Path]:
    out = [ROOT / 'CONTEXT.md'] + sorted((ROOT / 'projects').glob('*.md'))
    sh = ROOT / 'docs' / 'knowledge' / 'session-history.md'
    if sh.exists():
        out.append(sh)
    return [p for p in out if p.exists()]


def strip_front(md: str) -> tuple[str, dict]:
    meta = {}
    m = re.match(r'^---\n(.*?)\n---\n', md, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ':' in line:
                k, v = line.split(':', 1)
                meta[k.strip()] = v.strip().strip('"')
        md = md[m.end():]
    return md.strip(), meta


def title_of(md: str, path: Path) -> str:
    m = re.search(r'^#\s+(.+)$', md, re.M)
    t = m.group(1).strip() if m else path.stem.replace('-', ' ')
    return re.sub(r'[*_`]', '', t)


def split(md: str, size: int = MAX_PART) -> list[str]:
    """Op ##-koppen in blokken; te grote blokken op alinea's. Elk deel hoogstens size tekens."""
    if len(md) <= size:
        return [md]
    blocks = re.split(r'(?m)^(?=## )', md)
    parts, cur = [], ''
    for b in blocks:
        while len(b) > size:
            cut = b.rfind('\n\n', 0, size)
            cut = cut if cut > size // 3 else size
            if cur:
                parts.append(cur.strip())
                cur = ''
            parts.append(b[:cut].strip())
            b = b[cut:]
        if len(cur) + len(b) > size and cur:
            parts.append(cur.strip())
            cur = ''
        cur += b
    if cur.strip():
        parts.append(cur.strip())
    return [p for p in parts if p]


def build() -> list[dict]:
    items = []
    for p in files():
        rel = p.relative_to(ROOT).as_posix()
        md, meta = strip_front(p.read_text(encoding='utf-8'))
        base = title_of(md, p)
        parts = split(md)
        kw = ', '.join(x for x in ['dieouwe brain', meta.get('id', p.stem), meta.get('type', ''), 'project'] if x)
        for i, body in enumerate(parts, 1):
            many = len(parts) > 1
            title = ('Brain: ' + base)[: (66 if many else 80)] + (f' (deel {i})' if many else '')
            key = PREFIX + rel + (f'#deel-{i}' if many else '')
            text = body + f'\n\nBron: Project Brain, {rel}' + (f' (deel {i} van {len(parts)})' if many else '') + ' — github.com/Die0uwe/project-brain'
            items.append({'key': key, 'title': title[:80], 'body': text[:8000], 'keywords': kw[:400]})
    return items


def page_hash(title: str, body: str) -> str:
    # zelfde berekening als kennis_sync.php: md5(titel + "\n" + tekst) na opschonen (bijsnijden, \r\n -> \n)
    clean = lambda s, n: re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', s.replace('\r\n', '\n'))[:n].strip()
    return hashlib.md5((clean(title, 80) + '\n' + clean(body, 8000)).encode('utf-8')).hexdigest()


class Client:
    def __init__(self, url: str, secret: str):
        self.url, self.secret = url + '/kennis_sync.php', secret

    def call(self, payload: dict) -> dict:
        payload = {'ts': int(time.time()), **payload}
        raw = json.dumps(payload, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
        sig = hmac.new(self.secret.encode(), raw, hashlib.sha256).hexdigest()
        req = urllib.request.Request(self.url, data=raw, method='POST', headers={
            'Content-Type': 'application/json', 'X-Bot-Signature': sig, 'User-Agent': UA})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            try:
                return json.loads(e.read().decode('utf-8')) | {'http': e.code}
            except ValueError:
                return {'ok': False, 'error': f'HTTP {e.code}', 'http': e.code}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--offline', action='store_true')
    ap.add_argument('--no-pull', action='store_true')
    a = ap.parse_args()
    if not a.no_pull and not a.offline:
        subprocess.run(['git', '-C', str(ROOT), 'pull', '-q', '--ff-only'], check=False)
    items = build()
    print(f'{len(items)} delen uit {len(files())} bestanden')
    if a.offline:
        for it in items:
            print(f"  {len(it['body']):5d}  {it['title']}")
        return 0
    url, secret, where = settings()
    local = re.match(r'^http://(127\.0\.0\.1|localhost)(:\d+)?(/|$)', url) is not None   # alleen voor een testkopie op deze pc
    if not ((url.startswith('https://') or local) and secret):
        print('Instellingen ontbreken: SBWEBUI_URL en SBWEBUI_BOT_SECRET (in ~/.sbwebui-brain.env of de .env van de live CoreBot).')
        return 2
    print(f'SBWebUI: {url} (geheim uit {where})')
    c = Client(url, secret)
    r = c.call({'act': 'list'})
    if not r.get('ok'):
        print('Lijst opvragen mislukt:', r.get('error') or r)
        if r.get('http') == 404:
            print('kennis_sync.php staat (nog) niet op de site: upload het pakket eerst.')
        return 1
    have = {x['key']: x for x in r.get('items', [])}
    want = {it['key']: it for it in items}
    new = [k for k in want if k not in have]
    changed = [k for k in want if k in have and have[k]['hash'] != page_hash(want[k]['title'], want[k]['body'])]
    gone = [k for k in have if k not in want]
    print(f'nieuw {len(new)} · gewijzigd {len(changed)} · gelijk {len(want) - len(new) - len(changed)} · weg {len(gone)}')
    if a.dry_run:
        for k in new:
            print('  NIEUW   ', want[k]['title'])
        for k in changed:
            print('  ANDERS  ', want[k]['title'])
        for k in gone:
            print('  WEG     ', k[len(PREFIX):])
        return 0
    errors = 0
    for k in new + changed:
        res = c.call({'act': 'upsert', **want[k]})
        if res.get('ok'):
            print(('  nieuw   ' if k in new else '  bijgew. ') + want[k]['title'])
        else:
            errors += 1
            print('  FOUT    ', want[k]['title'], '-', res.get('error'))
    for k in gone:
        res = c.call({'act': 'delete', 'key': k})
        print(('  weg     ' if res.get('ok') else '  FOUT weg ') + k[len(PREFIX):])
        errors += 0 if res.get('ok') else 1
    print('klaar' + (f' met {errors} fout(en)' if errors else ''))
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
