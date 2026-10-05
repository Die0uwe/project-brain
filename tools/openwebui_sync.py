#!/usr/bin/env python3
"""Synchroniseert project-brain naar een Open WebUI Knowledge-collectie (alleen standaardbibliotheek).

Wat het doet:
  1. git pull in de brain-repo (tenzij --no-pull)
  2. verzamelt de kennisbestanden (projects/, docs/, manifest, CONTEXT.md, index/llms.txt)
  3. vergelijkt met de vorige run (tools/.openwebui_state.json, sha256 per bestand)
  4. uploadt nieuwe en gewijzigde bestanden, wacht tot Open WebUI ze heeft verwerkt,
     voegt ze toe aan de collectie en haalt oude versies en verwijderde bestanden weg

Instellingen komen uit omgevingsvariabelen of uit een .env-bestand (bij voorkeur ~/.openwebui-brain.env,
buiten de repo; nooit als argument,
want een argument is zichtbaar in de proceslijst):
  OPENWEBUI_URL        bijvoorbeeld https://ai.scriptspace.nl
  OPENWEBUI_API_KEY    Open WebUI, Instellingen, Account, API-sleutels
  OPENWEBUI_KNOWLEDGE  naam van de collectie (standaard: DieOuwe Brain)

Gebruik:
  python tools/openwebui_sync.py              synchroniseren
  python tools/openwebui_sync.py --dry-run    alleen laten zien wat er zou gebeuren
  python tools/openwebui_sync.py --status     toon collectie en lokale staat
  python tools/openwebui_sync.py --reset      haal alle bestanden van deze sync uit de collectie

Exitcode 0 = goed, 1 = fout(en) tijdens de sync, 2 = instellingen ontbreken of onjuist.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = Path(__file__).resolve().parent / ".openwebui_state.json"
ENV_FILES = [Path.home() / ".openwebui-brain.env", Path(__file__).resolve().parent / ".openwebui.env", ROOT / ".openwebui.env"]
DEFAULT_KNOWLEDGE = "DieOuwe Brain"
POLL_SECONDS = 1.0  # tussen twee statusvragen
TRANSIENT = (0, 502, 503, 504, 524)  # tijdelijke fouten (tunnel/time-out): eerst controleren, niet blind opruimen
DESCRIPTION = "Kennisbank van Ouwe: projecten, WoW-data, API-referenties en skills (gesynchroniseerd uit project-brain)."

# Wat naar de collectie gaat: bewust niet de vertalingen (i18n), de website of templates.
INCLUDE_GLOBS = ["projects/*.md", "docs/**/*.md", "manifest/projects.yml", "CONTEXT.md", "index/llms.txt"]


class ApiError(RuntimeError):
    def __init__(self, status: int, detail: str):
        super().__init__(f"HTTP {status}: {detail}")
        self.status = status
        self.detail = detail


# ----------------------------------------------------------------------------- instellingen

def load_env_files() -> None:
    """Leest KEY=waarde uit de .env-bestanden en vult alleen aan wat nog niet in de omgeving staat."""
    for path in ENV_FILES:
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            print(f"! {path} is geen UTF-8 (opgeslagen met PowerShell '>'?): sla het op als UTF-8, overgeslagen.")
            continue
        for raw in text.splitlines():
            line = raw.strip()
            if line.startswith("export "):
                line = line[7:].lstrip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key.strip(), value)


def check_url(url: str) -> str:
    url = url.strip().rstrip("/")
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("OPENWEBUI_URL moet met http:// of https:// beginnen")
    local = parsed.hostname in ("localhost", "127.0.0.1", "::1")
    if parsed.scheme == "http" and not local:
        raise ValueError("Een sleutel over http naar een niet-lokaal adres is onveilig: gebruik https")
    return url


# ----------------------------------------------------------------------------- Open WebUI client

class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Volgt nooit een redirect: anders reist de Authorization-header mee naar een andere host."""

    def redirect_request(self, *args, **kwargs):
        return None


class OpenWebUI:
    def __init__(self, base: str, key: str, timeout: int = 60, add_timeout: int = 300):
        self.base = base
        self.key = key
        self.timeout = timeout
        self.add_timeout = add_timeout  # embedden gebeurt tijdens file/add en kan op CPU lang duren
        self._opener = urllib.request.build_opener(_NoRedirect)

    def _request(self, method: str, path: str, *, body: bytes | None = None,
                 content_type: str | None = None, timeout: int | None = None):
        req = urllib.request.Request(self.base + path, data=body, method=method)
        req.add_header("Authorization", f"Bearer {self.key}")
        req.add_header("Accept", "application/json")
        req.add_header("User-Agent", "project-brain-sync/1.0")
        if content_type:
            req.add_header("Content-Type", content_type)
        try:
            with self._opener.open(req, timeout=timeout or self.timeout) as resp:
                raw = resp.read()
        except urllib.error.HTTPError as exc:
            if 300 <= exc.code < 400:
                raise ApiError(exc.code, "redirect ontvangen: gebruik de definitieve https-URL "
                                         "(en zet geen Cloudflare Access-login voor /api)") from None
            detail = exc.read().decode("utf-8", "replace")[:300]
            try:
                parsed = json.loads(detail)
                detail = str(parsed.get("detail") or parsed.get("error") or detail)[:300]
            except (ValueError, AttributeError):
                pass
            raise ApiError(exc.code, detail) from None
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise ApiError(0, f"geen verbinding met {self.base}: {getattr(exc, 'reason', exc)}") from None
        if not raw:
            return None
        try:
            return json.loads(raw)
        except ValueError:
            raise ApiError(200, "antwoord is geen JSON (staat de URL naar Open WebUI, niet naar een loginpagina?)") from None

    def json(self, method: str, path: str, payload: dict | None = None, timeout: int | None = None):
        body = json.dumps(payload).encode("utf-8") if payload is not None else None
        return self._request(method, path, body=body, content_type="application/json" if body else None,
                             timeout=timeout)

    def upload(self, filename: str, data: bytes):
        boundary = "----brainsync" + uuid.uuid4().hex
        filename = filename.replace('"', "_").replace("\r", "_").replace("\n", "_")
        head = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; "
                f"filename=\"{filename}\"\r\nContent-Type: text/plain\r\n\r\n").encode("utf-8")
        tail = f"\r\n--{boundary}--\r\n".encode("utf-8")
        result = self._request("POST", "/api/v1/files/", body=head + data + tail,
                               content_type=f"multipart/form-data; boundary={boundary}")
        if not isinstance(result, dict) or not result.get("id"):
            raise ApiError(200, "upload gaf geen bestands-id terug")
        return result["id"]

    def wait_processed(self, file_id: str, timeout: int) -> None:
        deadline = time.monotonic() + timeout
        while True:
            try:
                status = (self.json("GET", f"/api/v1/files/{file_id}/process/status") or {}).get("status")
            except ApiError as exc:
                if exc.status in (404, 405):  # oudere versie zonder statusendpoint
                    time.sleep(POLL_SECONDS)
                    return
                raise
            if status in (None, "completed"):
                return
            if status == "failed":
                raise ApiError(200, "Open WebUI kon het bestand niet verwerken (embedding-model aan het laden of niet beschikbaar?)")
            if time.monotonic() > deadline:
                raise ApiError(0, f"verwerken duurde langer dan {timeout}s")
            time.sleep(POLL_SECONDS)

    def list_knowledge(self) -> list[dict]:
        seen: dict[str, dict] = {}
        for page in range(1, 51):
            data = self.json("GET", f"/api/v1/knowledge/?page={page}")
            items = data.get("items", []) if isinstance(data, dict) else (data or [])
            fresh = [k for k in items if isinstance(k, dict) and k.get("id") not in seen]
            for k in fresh:
                seen[k["id"]] = k
            if not fresh:  # lege pagina, of een server die 'page' negeert
                break
        return list(seen.values())

    def create_knowledge(self, name: str) -> dict:
        data = self.json("POST", "/api/v1/knowledge/create", {"name": name, "description": DESCRIPTION})
        if not isinstance(data, dict) or not data.get("id"):
            raise ApiError(200, "collectie aanmaken gaf geen id terug")
        return data

    def knowledge_file_ids(self, kid: str) -> set[str] | None:
        """Alle bestands-id's in de collectie, of None als de server dat niet (volledig) kan tonen."""
        ids: set[str] = set()
        try:
            page, total = 1, None
            while page < 200:
                data = self.json("GET", f"/api/v1/knowledge/{kid}/files?page={page}&limit=100")
                items = (data or {}).get("items") or []
                total = (data or {}).get("total", total)
                ids.update(i["id"] for i in items if isinstance(i, dict) and i.get("id"))
                if not items or (total is not None and len(ids) >= total):
                    return ids
                page += 1
            return ids
        except ApiError as exc:
            if exc.status not in (404, 405, 422):
                raise
        try:  # oudere versies tonen de bestanden in de collectie zelf
            data = self.json("GET", f"/api/v1/knowledge/{kid}")
            files = (data or {}).get("files")
            if isinstance(files, list):
                return {f["id"] for f in files if isinstance(f, dict) and f.get("id")}
        except ApiError:
            pass
        return None

    def add_file(self, kid: str, file_id: str) -> None:
        self.json("POST", f"/api/v1/knowledge/{kid}/file/add", {"file_id": file_id}, timeout=self.add_timeout)

    def remove_file(self, kid: str, file_id: str) -> None:
        """Haalt het bestand uit de collectie en verwijdert het. Gooit een fout als het er mogelijk nog staat.

        Open WebUI antwoordt op 'bestand niet gevonden' en 'geen toegang' allebei met HTTP 400. Daarom telt
        alleen een geslaagde DELETE of een 404 op het bestand zelf als 'weg'.
        """
        try:
            self.json("POST", f"/api/v1/knowledge/{kid}/file/remove?delete_file=true", {"file_id": file_id})
        except ApiError as exc:
            if exc.status not in (400, 404):
                raise
        try:
            self.json("DELETE", f"/api/v1/files/{file_id}")
        except ApiError as exc:
            if exc.status != 404:
                raise


# ----------------------------------------------------------------------------- bestanden en staat

def upload_name(rel: str) -> str:
    """projects/blueprint-cms.md wordt projects__blueprint-cms.md: de bronnaam blijft in citaten zichtbaar."""
    name = rel.replace("/", "__")
    return name if name.endswith(".md") else name + ".txt"


def collect(repo: Path) -> dict[str, Path]:
    found: dict[str, Path] = {}
    for pattern in INCLUDE_GLOBS:
        for path in sorted(repo.glob(pattern)):
            if path.is_file():
                found[path.relative_to(repo).as_posix()] = path
    return found


def read_normalised(path: Path) -> bytes:
    """Bytes zoals ze naar de server gaan: CRLF wordt LF, zodat autocrlf op Windows niets 'wijzigt'."""
    return path.read_bytes().replace(b"\r\n", b"\n")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_state() -> dict:
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        if isinstance(data, dict) and isinstance(data.get("files"), dict):
            return data
    except (OSError, ValueError):
        pass
    return {"url": "", "knowledge_id": "", "files": {}}


def save_state(state: dict) -> None:
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=1, sort_keys=True), encoding="utf-8")
    tmp.replace(STATE_FILE)


def git_pull(repo: Path) -> None:
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0")
    try:
        out = subprocess.run(["git", "-C", str(repo), "pull", "--ff-only", "-q"], capture_output=True,
                             encoding="utf-8", errors="replace", timeout=120, env=env, stdin=subprocess.DEVNULL)
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"! git pull overgeslagen: {exc}")
        return
    if out.returncode != 0:
        print(f"! git pull mislukt, ik gebruik de lokale bestanden zoals ze zijn: {out.stderr.strip()[:200]}")


# ----------------------------------------------------------------------------- sync

def plan(files: dict[str, Path], state: dict, present: set[str] | None) -> dict[str, list[str]]:
    known = state["files"]
    new, changed, missing = [], [], []
    for rel, path in files.items():
        entry = known.get(rel)
        if not entry:
            new.append(rel)
        elif entry.get("sha256") != digest(read_normalised(path)):
            changed.append(rel)
        elif present is not None and entry.get("file_id") and entry["file_id"] not in present:
            missing.append(rel)  # handmatig uit de collectie gehaald: opnieuw uploaden
    removed = [rel for rel in known if rel not in files]
    return {"new": new, "changed": changed, "missing": missing, "removed": removed}


def clean_stale(client: OpenWebUI, kid: str, state: dict) -> int:
    """Probeert oude versies te verwijderen die in een eerdere run niet weg wilden. Geeft het aantal fouten."""
    failures = 0
    for file_id in list(state.get("stale", [])):
        try:
            client.remove_file(kid, file_id)
            state["stale"].remove(file_id)
            print(f"- oude versie {file_id[:8]} alsnog verwijderd")
        except ApiError as exc:
            failures += 1
            print(f"! oude versie {file_id[:8]} staat er nog: {exc}")
    return failures


def sync_one(client: OpenWebUI, kid: str, state: dict, rel: str, path: Path, process_timeout: int) -> bool:
    """Uploadt een bestand en zet het in de collectie. Geeft False bij een echte fout."""
    data = read_normalised(path)
    old = state["files"].get(rel)
    file_id = None
    try:
        file_id = client.upload(upload_name(rel), data)
        client.wait_processed(file_id, process_timeout)
        try:
            client.add_file(kid, file_id)
        except ApiError as exc:
            # Tijdelijke fout (tunnel-time-out): de server kan het bestand alsnog hebben toegevoegd.
            if exc.status not in TRANSIENT or file_id not in (client.knowledge_file_ids(kid) or set()):
                raise
    except ApiError as exc:
        duplicate = "duplicate" in exc.detail.lower()
        print(f"! {rel}: {'dubbele inhoud, wordt niet apart opgenomen' if duplicate else exc}")
        if file_id:  # nooit een half bestand achterlaten
            try:
                client.remove_file(kid, file_id)
            except ApiError as cleanup:
                state.setdefault("stale", []).append(file_id)
                print(f"! opruimen van {file_id[:8]} mislukt, probeer ik de volgende run opnieuw: {cleanup}")
        if duplicate:  # onthoud de hash, anders proberen we dit bestand elke run opnieuw
            state["files"][rel] = {"sha256": digest(data), "file_id": None}
            return True
        return False

    state["files"][rel] = {"sha256": digest(data), "file_id": file_id}
    if old and old.get("file_id") and old["file_id"] != file_id:
        try:
            client.remove_file(kid, old["file_id"])
        except ApiError as exc:
            state.setdefault("stale", []).append(old["file_id"])
            print(f"! oude versie van {rel} niet verwijderd (volgende run opnieuw): {exc}")
            print(f"+ {rel}")
            return False
    print(f"+ {rel}")
    return True


def run(args: argparse.Namespace) -> int:
    load_env_files()
    url_raw, key = os.environ.get("OPENWEBUI_URL", ""), os.environ.get("OPENWEBUI_API_KEY", "")
    if not url_raw or not key:
        print("Zet OPENWEBUI_URL en OPENWEBUI_API_KEY (in de omgeving of in ~/.openwebui-brain.env).")
        return 2
    try:
        url = check_url(args.url or url_raw)
    except ValueError as exc:
        print(f"Instelling onjuist: {exc}")
        return 2

    repo = Path(args.repo).resolve()
    if not (repo / "manifest" / "projects.yml").is_file():
        print(f"{repo} lijkt niet op de project-brain repo (manifest/projects.yml ontbreekt).")
        return 2
    if not args.no_pull and not args.dry_run and not args.status and not args.reset:
        git_pull(repo)

    client = OpenWebUI(url, key, args.timeout)
    name = args.knowledge or os.environ.get("OPENWEBUI_KNOWLEDGE") or DEFAULT_KNOWLEDGE
    state = load_state()
    try:
        match = [k for k in client.list_knowledge() if k.get("name") == name]
    except ApiError as exc:
        hint = " (controleer de API-sleutel)" if exc.status in (401, 403) else ""
        print(f"Kan Open WebUI niet bevragen: {exc}{hint}")
        return 1

    current_id = match[0].get("id") if match else ""
    if state["url"] != url or state["knowledge_id"] != current_id:
        if state["files"]:
            print("! De bijgehouden staat hoort bij een andere server of collectie (verwijderd of hernoemd?): "
                  "ik begin schoon. Oude bestanden blijven op de oude plek staan.")
        state = {"url": url, "knowledge_id": current_id, "files": {}}

    if args.status:
        print(f"Server: {url}\nCollectie: {name} ({'bestaat' if match else 'bestaat nog niet'})")
        print(f"Lokaal bijgehouden bestanden: {len(state['files'])}, nog op te ruimen: {len(state.get('stale', []))}")
        return 0

    if args.reset:
        if not match:
            print("Collectie bestaat niet: niets te doen.")
            return 0
        failures = 0
        for rel, entry in sorted(state["files"].items()):
            if not entry.get("file_id"):
                state["files"].pop(rel)
                continue
            try:
                client.remove_file(current_id, entry["file_id"])
                state["files"].pop(rel)
                print(f"- {rel}")
            except ApiError as exc:
                failures += 1
                print(f"! {rel}: {exc}")
        failures += clean_stale(client, current_id, state)
        save_state(state)
        return 1 if failures else 0

    files = collect(repo)
    if not files:
        print("Geen kennisbestanden gevonden: afgebroken.")
        return 1

    present = None
    if match:
        try:
            present = client.knowledge_file_ids(current_id)
        except ApiError as exc:
            print(f"! Kon de bestandslijst van de collectie niet ophalen: {exc}")
    todo = plan(files, state, present)
    summary = ", ".join(f"{len(v)} {k}" for k, v in todo.items() if v) or "alles is actueel"
    print(f"Server {url}, collectie '{name}': {summary} (van {len(files)} bestanden)")
    if args.dry_run:
        for kind, rels in todo.items():
            for rel in rels:
                print(f"  [{kind}] {rel}")
        return 0

    failures = 0
    if match and state.get("stale"):
        failures += clean_stale(client, current_id, state)
        save_state(state)
    if not any(todo.values()):
        return 1 if failures else 0

    try:
        kid = current_id or client.create_knowledge(name)["id"]
    except ApiError as exc:
        print(f"Collectie aanmaken mislukt: {exc}")
        return 1
    state["knowledge_id"] = kid

    for rel in todo["new"] + todo["changed"] + todo["missing"]:
        if not sync_one(client, kid, state, rel, files[rel], args.process_timeout):
            failures += 1
        save_state(state)

    for rel in todo["removed"]:
        entry = state["files"][rel]
        try:
            if entry.get("file_id"):
                client.remove_file(kid, entry["file_id"])
            del state["files"][rel]
            print(f"- {rel}")
        except ApiError as exc:
            failures += 1
            print(f"! {rel}: {exc}")
    save_state(state)
    print("Klaar." if not failures else f"Klaar met {failures} fout(en).")
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):  # Taakplanner/cp1252: een vreemd teken mag de sync niet laten crashen
        with contextlib.suppress(AttributeError, ValueError):
            stream.reconfigure(errors="replace")
    p = argparse.ArgumentParser(description="Synchroniseer project-brain naar Open WebUI Knowledge.")
    p.add_argument("--repo", default=str(ROOT), help="pad naar de project-brain repo (standaard: deze repo)")
    p.add_argument("--url", help="overschrijft OPENWEBUI_URL")
    p.add_argument("--knowledge", help="naam van de collectie")
    p.add_argument("--dry-run", action="store_true", help="laat alleen zien wat er zou gebeuren")
    p.add_argument("--status", action="store_true", help="toon collectie en lokale staat")
    p.add_argument("--reset", action="store_true", help="haal alle bestanden van deze sync uit de collectie")
    p.add_argument("--no-pull", action="store_true", help="geen git pull vooraf")
    p.add_argument("--timeout", type=int, default=60, help="seconden per verzoek")
    p.add_argument("--process-timeout", type=int, default=180, help="seconden wachten op verwerking per bestand")
    return run(p.parse_args(argv))


if __name__ == "__main__":
    sys.exit(main())
