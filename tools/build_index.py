#!/usr/bin/env python3
"""Bouwt de AI-index van project-brain (alleen standaardbibliotheek).

Leest manifest/projects.yml, projects/*.md, docs/**/*.md en CONTEXT.md, valideert ze
en schrijft:
  index/brain.jsonl   een chunk per regel (JSON)
  index/llms.txt      korte kaart voor AI-agents

Gebruik:
  python3 tools/build_index.py            valideer en schrijf de index
  python3 tools/build_index.py --check    valideer en controleer dat index/ actueel is (voor CI)
  python3 tools/build_index.py --validate valideer alleen, schrijf niets

Exitcode 0 = goed, 1 = validatiefouten, 2 = index niet actueel (alleen --check).
Zie docs/RAG-ARCHITECTURE.md.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TYPES = {"repo", "site", "addon", "tool", "ai"}
REQUIRED = ["id", "type", "name", "url", "status", "stack", "description", "version",
            "depends_on", "deploys_to", "documents", "docs", "last_checked", "owner_skill"]
LIST_FIELDS = {"depends_on", "deploys_to", "documents", "docs"}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MAX_CHUNK = 3000  # tekens; langere secties worden op alinea's gesplitst

# Geheimpatronen. Waarden met duidelijke plaatshouders worden genegeerd.
SECRET_PATTERNS = [
    ("OpenAI/Anthropic-achtige sleutel (sk-)", re.compile(r"\bsk-[A-Za-z0-9_-]{16,}")),
    ("GitHub token (ghp_/gho_/ghs_/ghu_/ghr_)", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}")),
    ("GitHub fine-grained token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}")),
    ("AWS access key (AKIA)", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Google API key (AIza)", re.compile(r"\bAIza[0-9A-Za-z_-]{30,}")),
    ("Slack token", re.compile(r"\bxox[abpr]-[A-Za-z0-9-]{10,}")),
    ("Privesleutel-blok", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("Discord bottoken", re.compile(r"\b[MNO][A-Za-z0-9_-]{23,25}\.[A-Za-z0-9_-]{6}\.[A-Za-z0-9_-]{27,}")),
    ("api_key/secret/token/password met waarde",
     re.compile(r"(?i)\b(?:api[_-]?key|secret|token|password|passwd|client_secret)\b\s*[:=]\s*['\"]?([A-Za-z0-9_\-+/=.]{12,})(?![A-Za-z0-9_\-+/=.(])")),
]
PLACEHOLDER_RE = re.compile(
    r"(?i)(x{3,}|\*{3,}|\.{3,}|your|jouw|example|voorbeeld|placeholder|changeme|dummy|test|<.*>|\$\{?[A-Z_]+|"
    r"getenv|environ|env\.|_here|hier|plak|invullen|keyring|os\.)")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


# ---------------------------------------------------------------- manifest

def _scalar(raw: str, where: str):
    raw = raw.strip()
    if raw.startswith('"'):
        if not raw.endswith('"') or len(raw) < 2:
            raise ValueError(f"{where}: ongesloten string")
        return json.loads(raw)
    if raw.startswith("["):
        return _inline_list(raw, where)
    return raw


def _inline_list(raw: str, where: str) -> list:
    raw = raw.strip()
    if not (raw.startswith("[") and raw.endswith("]")):
        raise ValueError(f"{where}: lijst moet [..] zijn")
    try:
        value = json.loads(raw)  # onze subset is geldige JSON voor lijsten van strings
    except json.JSONDecodeError:
        inner = raw[1:-1].strip()
        value = [x.strip() for x in inner.split(",") if x.strip()]
    if not isinstance(value, list):
        raise ValueError(f"{where}: geen lijst")
    return value


def parse_manifest(text: str) -> list[dict]:
    """Parser voor de strikte YAML-subset van manifest/projects.yml."""
    entries: list[dict] = []
    current: dict | None = None
    seen_root = False
    for n, line in enumerate(text.splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        where = f"manifest regel {n}"
        if not seen_root:
            if line.strip() != "projects:":
                raise ValueError(f"{where}: verwacht 'projects:'")
            seen_root = True
            continue
        m = re.match(r"^(\s*)(- )?([a-z_]+):\s*(.*)$", line)
        if not m:
            raise ValueError(f"{where}: onleesbare regel: {line!r}")
        _, dash, key, rest = m.groups()
        if dash:
            current = {}
            entries.append(current)
        if current is None:
            raise ValueError(f"{where}: veld buiten een entry")
        if key in current:
            raise ValueError(f"{where}: dubbel veld {key}")
        current[key] = _scalar(rest, where)
    if not seen_root:
        raise ValueError("manifest is leeg")
    return entries


# ---------------------------------------------------------------- markdown

def split_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    meta = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"')
    return meta, text[end + 5:]


def strip_html_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def slugify(title: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s or "sectie"


def split_sections(body: str, default_title: str) -> list[tuple[str, str]]:
    """Splitst op koppen van niveau 1-2 (buiten codeblokken). Geeft (titel, tekst)."""
    sections: list[tuple[str, list[str]]] = [(default_title, [])]
    in_code = False
    for line in body.splitlines():
        if line.lstrip().startswith("```"):
            in_code = not in_code
        m = None if in_code else re.match(r"^(#{1,2})\s+(.+?)\s*$", line)
        if m:
            sections.append((m.group(2), []))
        else:
            sections[-1][1].append(line)
    out = []
    for title, lines in sections:
        text = "\n".join(lines).strip()
        if text:
            out.append((title, text))
    return out


def split_long(text: str) -> list[str]:
    if len(text) <= MAX_CHUNK:
        return [text]
    parts, cur = [], ""
    for para in re.split(r"\n\s*\n", text):
        if cur and len(cur) + len(para) + 2 > MAX_CHUNK:
            parts.append(cur.strip())
            cur = ""
        if len(para) > MAX_CHUNK:  # laatste redmiddel: op regels splitsen
            for ln in para.splitlines():
                if cur and len(cur) + len(ln) + 1 > MAX_CHUNK:
                    parts.append(cur.strip())
                    cur = ""
                cur += ln + "\n"
        else:
            cur += para + "\n\n"
    if cur.strip():
        parts.append(cur.strip())
    return parts


UPDATED_RES = [
    re.compile(r"(?i)(?:laatste update|bijgewerkt|updated)\s*[:\s]\s*(\d{4}-\d{2}-\d{2})"),
]


def find_updated(meta: dict, text: str) -> str:
    for key in ("bijgewerkt", "updated"):
        if DATE_RE.match(meta.get(key, "")):
            return meta[key]
    for rx in UPDATED_RES:
        m = rx.search(text)
        if m:
            return m.group(1)
    return "onbekend"


LINK_RE = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def check_links(path: Path, text: str, rep: Report) -> None:
    rel = path.relative_to(ROOT)
    in_code = False
    for ln in text.splitlines():
        if ln.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        for target in LINK_RE.findall(ln):
            if re.match(r"^(https?:|mailto:|#|tel:)", target):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            dest = (path.parent / target).resolve()
            try:
                dest.relative_to(ROOT)
            except ValueError:
                rep.error(f"{rel}: link wijst buiten de repo: {target}")
                continue
            if not dest.exists():
                rep.error(f"{rel}: dode link: {target}")


def scan_secrets(rel: str, text: str, rep: Report) -> None:
    for lineno, line in enumerate(text.splitlines(), 1):
        for label, rx in SECRET_PATTERNS:
            for m in rx.finditer(line):
                value = m.group(1) if m.groups() else m.group(0)
                if PLACEHOLDER_RE.search(value):
                    continue
                rep.error(f"{rel}:{lineno}: mogelijk geheim ({label}); haal weg of vervang door een plaatshouder")


# ---------------------------------------------------------------- opbouw

def validate_manifest(entries: list[dict], rep: Report) -> None:
    ids = set()
    for i, e in enumerate(entries, 1):
        label = e.get("id", f"entry {i}")
        for f in REQUIRED:
            if f not in e or e[f] in ("", None):
                rep.error(f"manifest {label}: verplicht veld ontbreekt: {f}")
        extra = set(e) - set(REQUIRED) - {"verified"}
        if extra:
            rep.error(f"manifest {label}: onbekende velden: {sorted(extra)}")
        eid = e.get("id", "")
        if eid and not ID_RE.match(eid):
            rep.error(f"manifest {label}: ongeldig id (alleen a-z, 0-9, '-')")
        if eid in ids:
            rep.error(f"manifest: dubbel id {eid}")
        ids.add(eid)
        if e.get("type") not in TYPES:
            rep.error(f"manifest {label}: type moet een van {sorted(TYPES)} zijn")
        for f in LIST_FIELDS:
            if f in e and not isinstance(e[f], list):
                rep.error(f"manifest {label}: {f} moet een lijst zijn")
        if e.get("last_checked") and not DATE_RE.match(str(e["last_checked"])):
            rep.error(f"manifest {label}: last_checked moet YYYY-MM-DD zijn")
        for d in e.get("docs", []) if isinstance(e.get("docs"), list) else []:
            if not (ROOT / d).is_file():
                rep.error(f"manifest {label}: bronpad bestaat niet: {d}")
        if not (ROOT / "projects" / f"{eid}.md").is_file():
            rep.error(f"manifest {label}: projectkaart projects/{eid}.md ontbreekt")
    for e in entries:
        for f in ("depends_on", "deploys_to", "documents"):
            for ref in e.get(f, []) if isinstance(e.get(f), list) else []:
                if ref.startswith("extern:"):
                    continue
                if ref not in ids:
                    rep.error(f"manifest {e.get('id')}: {f} verwijst naar onbekend id: {ref} (gebruik 'extern:naam' voor buiten het manifest)")
    for card in sorted((ROOT / "projects").glob("*.md")):
        if card.stem not in ids:
            rep.error(f"projects/{card.name}: staat niet in het manifest")


def doc_files() -> list[Path]:
    files = [ROOT / "CONTEXT.md"]
    files += sorted((ROOT / "docs").rglob("*.md"))
    return [f for f in files if f.is_file()]


def build(rep: Report) -> tuple[list[dict], list[dict]]:
    manifest_path = ROOT / "manifest" / "projects.yml"
    if not manifest_path.is_file():
        rep.error("manifest/projects.yml ontbreekt")
        return [], []
    try:
        entries = parse_manifest(manifest_path.read_text(encoding="utf-8"))
    except ValueError as exc:
        rep.error(str(exc))
        return [], []
    scan_secrets("manifest/projects.yml", manifest_path.read_text(encoding="utf-8"), rep)
    validate_manifest(entries, rep)
    by_id = {e.get("id"): e for e in entries}

    chunks: list[dict] = []

    def add(project: str, ptype: str, title: str, text: str, source: str, updated: str,
            slug: str, extra: dict | None = None) -> None:
        for n, part in enumerate(split_long(text), 1):
            cid = f"{project}:{source}#{slug}" + (f"~{n}" if n > 1 else "")
            row = {"id": cid, "project": project, "type": ptype, "title": title,
                   "text": part, "source": source, "updated": updated}
            if extra:
                row.update(extra)
            chunks.append(row)

    # 1. manifest: een samenvattingschunk per entry
    for e in entries:
        g = lambda k: e.get(k, "onbekend")  # noqa: E731  (velden kunnen ontbreken; die fouten zijn al gemeld)
        lines = [f"{g('name')} ({g('type')}): {g('description')}",
                 f"Status: {g('status')}. Stack: {g('stack')}. Versie: {g('version')}. URL: {g('url')}.",
                 f"Beheer-skill: {g('owner_skill')}. Geverifieerd: {g('verified')}. Laatst gecontroleerd: {g('last_checked')}."]
        for f, label in (("depends_on", "Hangt af van"), ("deploys_to", "Deployt naar"), ("documents", "Documenteert")):
            if isinstance(e.get(f), list) and e[f]:
                lines.append(f"{label}: {', '.join(e[f])}.")
        docs = e.get("docs") if isinstance(e.get("docs"), list) else []
        lines.append("Bronnen: " + ", ".join(docs) + ".")
        add(g("id"), g("type"), f"{g('name')} (manifest)", "\n".join(lines),
            "manifest/projects.yml", g("last_checked"), "manifest")

    # 2. projectkaarten
    for card in sorted((ROOT / "projects").glob("*.md")):
        raw = card.read_text(encoding="utf-8")
        rel = card.relative_to(ROOT).as_posix()
        scan_secrets(rel, raw, rep)
        check_links(card, raw, rep)
        meta, body = split_front_matter(raw)
        pid = meta.get("id", card.stem)
        if pid != card.stem:
            rep.error(f"{rel}: front-matter id '{pid}' wijkt af van bestandsnaam")
        entry = by_id.get(pid)
        if entry and meta.get("type") != entry.get("type"):
            rep.error(f"{rel}: front-matter type '{meta.get('type')}' wijkt af van manifest '{entry.get('type')}'")
        if not DATE_RE.match(meta.get("bijgewerkt", "")):
            rep.error(f"{rel}: front-matter 'bijgewerkt' (YYYY-MM-DD) ontbreekt")
        ptype = (entry or {}).get("type", meta.get("type", "onbekend"))
        updated = find_updated(meta, raw)
        for title, text in split_sections(strip_html_comments(body), card.stem):
            add(pid, ptype, title, text, rel, updated, slugify(title), {"kind": "projectkaart"})

    # 3. docs
    for doc in doc_files():
        raw = doc.read_text(encoding="utf-8")
        rel = doc.relative_to(ROOT).as_posix()
        scan_secrets(rel, raw, rep)
        check_links(doc, raw, rep)
        meta, body = split_front_matter(raw)
        project = meta.get("project", "project-brain")
        if "project" in meta and project not in by_id:
            rep.error(f"{rel}: front-matter project '{project}' staat niet in het manifest")
        updated = find_updated(meta, raw)
        category = doc.parent.name if doc.parent != ROOT else "root"
        for title, text in split_sections(strip_html_comments(body), doc.stem):
            add(project, "doc", title, text, rel, updated, slugify(title),
                {"kind": "doc", "category": category})

    ids = [c["id"] for c in chunks]
    dupes = {i for i in ids if ids.count(i) > 1}
    for d in sorted(dupes):
        rep.error(f"dubbel chunk-id: {d}")
    return entries, chunks


def render_llms(entries: list[dict], chunks: list[dict]) -> str:
    newest = max((e.get("last_checked", "") for e in entries), default="") or "onbekend"
    lines = [
        "# DieOuwe project-brain",
        "",
        "> Centrale kennisbank van Ouwe (Die0uwe): repos, sites, WoW-addons (Retail 12.0.5 Midnight), tools en AI's.",
        "> Lees eerst manifest/projects.yml, dan projects/<id>.md, en pas daarna de bron-repo. Geen geheimen in deze repo.",
        f"> Laatste manifestcontrole: {newest}. Regels met 'onbekend' zijn niet geverifieerd.",
        "",
        "## Startpunten",
        "- [CONTEXT.md](CONTEXT.md): sessie-instructies en kritieke constanten",
        "- [manifest/projects.yml](manifest/projects.yml): alle projecten met relaties",
        "- [docs/RAG-ARCHITECTURE.md](docs/RAG-ARCHITECTURE.md): hoe je deze brain als RAG-bron gebruikt",
        "- [index/brain.jsonl](index/brain.jsonl): chunks voor embedding (een JSON-object per regel)",
        "",
        "## Projecten",
    ]
    for e in entries:
        card = f"projects/{e.get('id')}.md"
        lines.append(f"- [{e.get('name')}]({card}) [{e.get('type')}, {e.get('status')}]: {e.get('description')}")
    lines += ["", "## Kennis",
              "- [docs/knowledge/](docs/knowledge/): WoW-IDs, bugs, kompaswiskunde, sessie-lessen",
              "- [docs/api/](docs/api/): Blizzard-API, events, deprecated calls",
              "- [docs/tokens-and-keys/](docs/tokens-and-keys/): HOE je tokens aanmaakt, nooit waarden",
              "- [docs/skills/skill-register.md](docs/skills/skill-register.md): wie beheert wat",
              "", f"Totaal: {len(entries)} projecten, {len(chunks)} chunks.", ""]
    return "\n".join(lines)


def render_jsonl(chunks: list[dict]) -> str:
    return "".join(json.dumps(c, ensure_ascii=False, sort_keys=True) + "\n" for c in chunks)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="valideer en controleer dat index/ actueel is")
    ap.add_argument("--validate", action="store_true", help="alleen valideren")
    args = ap.parse_args(argv)

    rep = Report()
    entries, chunks = build(rep)
    for w in rep.warnings:
        print(f"WAARSCHUWING: {w}", file=sys.stderr)
    if rep.errors:
        for e in rep.errors:
            print(f"FOUT: {e}", file=sys.stderr)
        print(f"{len(rep.errors)} fout(en); index niet geschreven.", file=sys.stderr)
        return 1

    jsonl, llms = render_jsonl(chunks), render_llms(entries, chunks)
    out = ROOT / "index"
    if args.validate:
        print(f"OK: {len(entries)} projecten, {len(chunks)} chunks (niets geschreven).")
        return 0
    if args.check:
        stale = [n for n, content in (("brain.jsonl", jsonl), ("llms.txt", llms))
                 if not (out / n).is_file() or (out / n).read_text(encoding="utf-8") != content]
        if stale:
            print(f"index/ is niet actueel ({', '.join(stale)}); draai: python3 tools/build_index.py", file=sys.stderr)
            return 2
        print(f"OK: index actueel ({len(entries)} projecten, {len(chunks)} chunks).")
        return 0
    out.mkdir(exist_ok=True)
    (out / "brain.jsonl").write_text(jsonl, encoding="utf-8")
    (out / "llms.txt").write_text(llms, encoding="utf-8")
    print(f"OK: {len(entries)} projecten, {len(chunks)} chunks geschreven naar index/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
