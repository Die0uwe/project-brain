#!/usr/bin/env python3
"""Tests voor tools/build_index.py (alleen standaardbibliotheek): python3 tools/test_build_index.py"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_index as bi  # noqa: E402

GOOD = '''projects:
  - id: "a"
    type: "repo"
    name: "A"
    url: "https://example.org/a"
    status: "actief"
    stack: "PHP"
    description: "Test."
    version: "1.0"
    depends_on: ["b"]
    deploys_to: ["extern:host"]
    documents: []
    docs: ["projects/a.md"]
    last_checked: "2026-10-03"
    owner_skill: "onbekend"

  - id: "b"
    type: "site"
    name: "B"
    url: "https://example.org/b"
    status: "onbekend"
    stack: "onbekend"
    description: "Test b."
    version: "onbekend"
    depends_on: []
    deploys_to: []
    documents: []
    docs: ["projects/b.md"]
    last_checked: "2026-10-03"
    owner_skill: "onbekend"
'''


def card(pid, ptype, body="## Doel\nIets.\n"):
    return f"---\nid: {pid}\ntype: {ptype}\nbijgewerkt: 2026-10-03\n---\n# Titel\n\n{body}"


class TempRepo:
    def __init__(self, manifest=GOOD, extra=None):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "manifest").mkdir()
        (self.root / "projects").mkdir()
        (self.root / "docs").mkdir()
        (self.root / "manifest" / "projects.yml").write_text(manifest, encoding="utf-8")
        (self.root / "projects" / "a.md").write_text(card("a", "repo"), encoding="utf-8")
        (self.root / "projects" / "b.md").write_text(card("b", "site"), encoding="utf-8")
        (self.root / "CONTEXT.md").write_text("# Context\nHallo.\n", encoding="utf-8")
        for rel, text in (extra or {}).items():
            p = self.root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")

    def run(self):
        old = bi.ROOT
        bi.ROOT = self.root
        try:
            rep = bi.Report()
            entries, chunks = bi.build(rep)
            return rep, entries, chunks
        finally:
            bi.ROOT = old
            self.tmp.cleanup()


class ManifestParser(unittest.TestCase):
    def test_parse(self):
        entries = bi.parse_manifest(GOOD)
        self.assertEqual([e["id"] for e in entries], ["a", "b"])
        self.assertEqual(entries[0]["depends_on"], ["b"])
        self.assertEqual(entries[1]["deploys_to"], [])

    def test_bad_line(self):
        with self.assertRaises(ValueError):
            bi.parse_manifest("projects:\n  - id: \"a\"\n  ???\n")

    def test_missing_root(self):
        with self.assertRaises(ValueError):
            bi.parse_manifest("  - id: \"a\"\n")


class Build(unittest.TestCase):
    def test_good_repo_builds(self):
        rep, entries, chunks = TempRepo().run()
        self.assertEqual(rep.errors, [])
        self.assertEqual(len(entries), 2)
        ids = [c["id"] for c in chunks]
        self.assertEqual(len(ids), len(set(ids)))
        for c in chunks:
            for f in ("id", "project", "type", "title", "text", "source", "updated"):
                self.assertIn(f, c)
        self.assertTrue(any(c["id"].startswith("a:manifest") or c["source"] == "manifest/projects.yml" for c in chunks))

    def test_missing_required_field(self):
        rep, _, _ = TempRepo(GOOD.replace('    stack: "PHP"\n', "")).run()
        self.assertTrue(any("verplicht veld ontbreekt: stack" in e for e in rep.errors))

    def test_bad_type(self):
        rep, _, _ = TempRepo(GOOD.replace('type: "repo"', 'type: "robot"')).run()
        self.assertTrue(any("type moet" in e for e in rep.errors))

    def test_unknown_relation(self):
        rep, _, _ = TempRepo(GOOD.replace('["b"]', '["zzz"]')).run()
        self.assertTrue(any("onbekend id: zzz" in e for e in rep.errors))

    def test_missing_card(self):
        t = TempRepo()
        (t.root / "projects" / "b.md").unlink()
        rep, _, _ = t.run()
        self.assertTrue(any("projects/b.md ontbreekt" in e for e in rep.errors))

    def test_card_not_in_manifest(self):
        rep, _, _ = TempRepo(extra={"projects/c.md": card("c", "repo")}).run()
        self.assertTrue(any("staat niet in het manifest" in e for e in rep.errors))

    def test_dead_link(self):
        rep, _, _ = TempRepo(extra={"docs/x.md": "# X\n[weg](nietbestaand.md)\n"}).run()
        self.assertTrue(any("dode link" in e for e in rep.errors))

    def test_good_link_and_code_block_ignored(self):
        rep, _, _ = TempRepo(extra={"docs/x.md": "# X\n[ok](../CONTEXT.md)\n```\n[x](nope.md)\n```\n"}).run()
        self.assertEqual(rep.errors, [])

    def test_long_section_is_split(self):
        text = "# L\n" + "\n\n".join("alinea " + "x" * 500 for _ in range(12))
        rep, _, chunks = TempRepo(extra={"docs/long.md": text}).run()
        self.assertEqual(rep.errors, [])
        parts = [c for c in chunks if c["source"] == "docs/long.md"]
        self.assertGreater(len(parts), 1)
        self.assertTrue(all(len(c["text"]) <= bi.MAX_CHUNK for c in parts))


class Secrets(unittest.TestCase):
    def scan(self, line):
        rep = bi.Report()
        bi.scan_secrets("x.md", line, rep)
        return rep.errors

    def test_detects(self):
        for line in (
            "key = sk-abcdefghijklmnop1234567890",
            "token ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3",
            "AKIA" + "ABCDEFGHIJKLMNOP",
            'api_key = "Zx81hQw93LmN02pQrS"',
            "-----BEGIN RSA PRIVATE KEY-----",
        ):
            self.assertTrue(self.scan(line), line)

    def test_allows_placeholders_and_code(self):
        for line in (
            'export GH_TOKEN="ghp_..."',
            "api_key = <jouw sleutel>",
            "api_key=xxxxxxxxxxxxxxxx",
            "token = get_blizzard_token(",
            "begint met `ghp_` of `sk-`",
            "secret: ${CLIENT_SECRET_VALUE}",
        ):
            self.assertEqual(self.scan(line), [], line)

    def test_secret_in_doc_fails_build(self):
        rep, _, _ = TempRepo(extra={"docs/leak.md": "# Leak\npassword = Hunter2Hunter2Hunter2\n"}).run()
        self.assertTrue(any("mogelijk geheim" in e for e in rep.errors))


class Output(unittest.TestCase):
    def test_deterministic_jsonl_and_llms(self):
        _, entries, chunks = TempRepo().run()
        a, b = bi.render_jsonl(chunks), bi.render_jsonl(chunks)
        self.assertEqual(a, b)
        for line in a.splitlines():
            json.loads(line)
        llms = bi.render_llms(entries, chunks)
        self.assertIn("projects/a.md", llms)
        self.assertTrue(llms.startswith("# "))


class RealRepo(unittest.TestCase):
    def test_real_repo_builds_clean(self):
        rep = bi.Report()
        entries, chunks = bi.build(rep)
        self.assertEqual(rep.errors, [])
        ids = {e["id"] for e in entries}
        for must in ("scriptspace-cms", "blueprint-cms", "slayer-suite", "dieouwe-nl", "slayeralliance-com", "scriptspace-nl"):
            self.assertIn(must, ids)
        self.assertGreater(len(chunks), 50)

    def test_committed_index_is_current(self):
        self.assertEqual(bi.main(["--check"]), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
