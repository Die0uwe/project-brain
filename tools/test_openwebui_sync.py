#!/usr/bin/env python3
"""Tests voor tools/openwebui_sync.py tegen een nep-Open WebUI (alleen standaardbibliotheek).

Gebruik: python3 tools/test_openwebui_sync.py
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import sys
import tempfile
import threading
import unittest
from email.parser import BytesParser
from email.policy import HTTP
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import openwebui_eval as ev  # noqa: E402
import openwebui_sync as sync  # noqa: E402

KEY = "sk-test-geheim"


class FakeOpenWebUI:
    """Minimale nabootsing van de Open WebUI-endpoints die de sync gebruikt."""

    def __init__(self):
        self.files: dict[str, dict] = {}          # file_id -> {name, data}
        self.knowledge: dict[str, dict] = {}      # id -> {name, files: [file_id]}
        self.pending_polls = 1                    # hoe vaak 'pending' voor 'completed'
        self.fail_names: set[str] = set()         # bestandsnamen die 'failed' worden
        self.polls: dict[str, int] = {}
        self.page_size = 2
        self.requests: list[tuple[str, str]] = []
        self.counter = 0
        self.legacy_no_status = False
        self.chat_answer = "1.34.0 cf_password_resets 60 minuten 3341 Custom slider atan2 0.25.0 onbekend"
        self.chat_bodies: list[dict] = []
        self.deny_remove = False        # remove geeft 400 en DELETE 403 (geen toegang)
        self.add_status: int | None = None   # add geeft deze fout terug, maar voegt het bestand wel toe
        self.knowledge_page_size = 100
        self.redirect_listing = False


def make_handler(state: FakeOpenWebUI):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _send(self, code, payload=None):
            body = json.dumps(payload if payload is not None else {}).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _auth(self):
            if self.headers.get("Authorization") != f"Bearer {KEY}":
                self._send(401, {"detail": "Not authenticated"})
                return False
            return True

        def _body(self):
            return self.rfile.read(int(self.headers.get("Content-Length") or 0))

        def do_GET(self):
            state.requests.append(("GET", self.path))
            if not self._auth():
                return
            path = self.path.split("?")[0]
            if path == "/api/v1/knowledge/":
                if state.redirect_listing:
                    self.send_response(302)
                    self.send_header("Location", "http://127.0.0.1:1/elders")
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
                query = dict(p.split("=") for p in self.path.split("?")[1].split("&")) if "?" in self.path else {}
                page = int(query.get("page", 1))
                rows = [{"id": k, "name": v["name"]} for k, v in state.knowledge.items()]
                chunk = rows[(page - 1) * state.knowledge_page_size: page * state.knowledge_page_size]
                return self._send(200, {"items": chunk, "total": len(rows)})
            if path.startswith("/api/v1/files/") and path.endswith("/process/status"):
                if state.legacy_no_status:
                    return self._send(404, {"detail": "Not Found"})
                fid = path.split("/")[4]
                if fid not in state.files:
                    return self._send(404, {"detail": "Not found"})
                state.polls[fid] = state.polls.get(fid, 0) + 1
                if state.files[fid]["name"] in state.fail_names:
                    return self._send(200, {"status": "failed"})
                return self._send(200, {"status": "pending" if state.polls[fid] <= state.pending_polls else "completed"})
            if path.startswith("/api/v1/knowledge/") and path.endswith("/files"):
                kid = path.split("/")[4]
                query = dict(p.split("=") for p in self.path.split("?")[1].split("&")) if "?" in self.path else {}
                page = int(query.get("page", 1))
                ids = state.knowledge[kid]["files"]
                chunk = ids[(page - 1) * state.page_size: page * state.page_size]
                return self._send(200, {"items": [{"id": i} for i in chunk], "total": len(ids)})
            self._send(404, {"detail": "Not Found"})

        def do_POST(self):
            state.requests.append(("POST", self.path))
            if not self._auth():
                return
            path = self.path.split("?")[0]
            raw = self._body()
            if path == "/api/v1/knowledge/create":
                data = json.loads(raw)
                state.counter += 1
                kid = f"k{state.counter}"
                state.knowledge[kid] = {"name": data["name"], "files": []}
                return self._send(200, {"id": kid, "name": data["name"]})
            if path == "/api/v1/files/":
                msg = BytesParser(policy=HTTP).parsebytes(
                    b"Content-Type: " + self.headers["Content-Type"].encode() + b"\r\n\r\n" + raw)
                part = next(msg.iter_parts())
                filename, payload = part.get_filename(), part.get_payload(decode=True)
                state.counter += 1
                fid = f"f{state.counter}"
                state.files[fid] = {"name": filename, "data": payload}
                return self._send(200, {"id": fid, "filename": filename})
            if path.endswith("/file/add"):
                kid = path.split("/")[4]
                fid = json.loads(raw)["file_id"]
                data = state.files[fid]["data"]
                for other in state.knowledge[kid]["files"]:
                    if state.files.get(other, {}).get("data") == data:
                        return self._send(400, {"detail": "Duplicate content detected. Please provide unique content to proceed."})
                state.knowledge[kid]["files"].append(fid)
                if state.add_status:
                    return self._send(state.add_status, {"detail": "time-out"})
                return self._send(200, {"id": kid})
            if path == "/api/chat/completions":
                state.chat_bodies.append(json.loads(raw))
                return self._send(200, {"choices": [{"message": {"content": "<think>hm</think>" + state.chat_answer}}]})
            if path.endswith("/file/remove"):
                kid = path.split("/")[4]
                fid = json.loads(raw)["file_id"]
                if state.deny_remove:
                    return self._send(400, {"detail": "You do not have the necessary access"})
                if fid in state.knowledge[kid]["files"]:
                    state.knowledge[kid]["files"].remove(fid)
                if "delete_file=true" in self.path:
                    state.files.pop(fid, None)
                return self._send(200, {"id": kid})
            self._send(404, {"detail": "Not Found"})

        def do_DELETE(self):
            state.requests.append(("DELETE", self.path))
            if not self._auth():
                return
            fid = self.path.split("/")[4]
            if state.deny_remove:
                return self._send(403, {"detail": "Forbidden"})
            if state.files.pop(fid, None) is None:
                return self._send(404, {"detail": "Not Found"})
            self._send(200, {"deleted": True})

    return Handler


class Base(unittest.TestCase):
    def setUp(self):
        self.fake = FakeOpenWebUI()
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.fake))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}"

        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "brain"
        for rel, text in {
            "manifest/projects.yml": "projects: []\n",
            "projects/a.md": "# A\nalpha\n",
            "docs/knowledge/b.md": "# B\nbeta\n",
            "CONTEXT.md": "# Context\n",
            "index/llms.txt": "kaart\n",
            "i18n/nl/x.md": "# vertaling, hoort er niet in\n",
            "web/index.md": "# site, hoort er niet in\n",
        }.items():
            path = self.repo / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")

        self.old = (sync.STATE_FILE, sync.ENV_FILES, sync.POLL_SECONDS)
        sync.POLL_SECONDS = 0.01
        sync.STATE_FILE = Path(self.tmp.name) / "state.json"
        sync.ENV_FILES = []
        os.environ["OPENWEBUI_URL"] = self.url
        os.environ["OPENWEBUI_API_KEY"] = KEY
        os.environ.pop("OPENWEBUI_KNOWLEDGE", None)

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        sync.STATE_FILE, sync.ENV_FILES, sync.POLL_SECONDS = self.old
        self.tmp.cleanup()

    def run_sync(self, *extra):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = sync.main(["--repo", str(self.repo), "--no-pull", "--process-timeout", "10", *extra])
        return code, out.getvalue()

    def kb_names(self):
        kid = next(iter(self.fake.knowledge))
        return sorted(self.fake.files[f]["name"] for f in self.fake.knowledge[kid]["files"])


class SyncTest(Base):
    # --- gedrag

    def test_first_run_uploads_only_the_knowledge_files(self):
        code, out = self.run_sync()
        self.assertEqual(code, 0, out)
        self.assertEqual(self.kb_names(), ["CONTEXT.md", "docs__knowledge__b.md", "index__llms.txt.txt",
                                           "manifest__projects.yml.txt", "projects__a.md"])
        self.assertNotIn(KEY, out)

    def test_second_run_changes_nothing(self):
        self.run_sync()
        self.fake.requests.clear()
        code, out = self.run_sync()
        self.assertEqual(code, 0)
        self.assertIn("alles is actueel", out)
        self.assertFalse([r for r in self.fake.requests if r[0] == "POST"])

    def test_changed_file_replaces_the_old_version(self):
        self.run_sync()
        (self.repo / "projects/a.md").write_text("# A\nalpha nieuw\n", encoding="utf-8")
        code, out = self.run_sync()
        self.assertEqual(code, 0, out)
        self.assertEqual(self.kb_names().count("projects__a.md"), 1)
        kid = next(iter(self.fake.knowledge))
        datas = [self.fake.files[f]["data"] for f in self.fake.knowledge[kid]["files"]]
        self.assertIn(b"# A\nalpha nieuw\n", datas)
        self.assertNotIn(b"# A\nalpha\n", datas)
        self.assertEqual(len(self.fake.files), 5, "oude versie moet echt weg zijn")

    def test_deleted_file_is_removed(self):
        self.run_sync()
        (self.repo / "docs/knowledge/b.md").unlink()
        code, _ = self.run_sync()
        self.assertEqual(code, 0)
        self.assertNotIn("docs__knowledge__b.md", self.kb_names())

    def test_file_removed_by_hand_is_uploaded_again(self):
        self.run_sync()
        kid = next(iter(self.fake.knowledge))
        victim = self.fake.knowledge[kid]["files"][0]
        self.fake.knowledge[kid]["files"].remove(victim)
        code, out = self.run_sync()
        self.assertEqual(code, 0, out)
        self.assertIn("1 missing", out)
        self.assertEqual(len(self.fake.knowledge[kid]["files"]), 5)

    def test_listing_is_paginated(self):
        self.fake.page_size = 2
        self.run_sync()
        kid = next(iter(self.fake.knowledge))
        ids = sync.OpenWebUI(self.url, KEY).knowledge_file_ids(kid)
        self.assertEqual(len(ids), 5)

    def test_wrong_key_gives_a_clear_error_without_leaking_it(self):
        os.environ["OPENWEBUI_API_KEY"] = "verkeerd"
        code, out = self.run_sync()
        self.assertEqual(code, 1)
        self.assertIn("API-sleutel", out)
        self.assertNotIn("verkeerd", out)

    def test_missing_settings_exit_2(self):
        os.environ.pop("OPENWEBUI_API_KEY")
        code, out = self.run_sync()
        self.assertEqual(code, 2)
        self.assertIn("OPENWEBUI_API_KEY", out)

    def test_plain_http_to_a_remote_host_is_refused(self):
        os.environ["OPENWEBUI_URL"] = "http://ai.example.com"
        code, out = self.run_sync()
        self.assertEqual(code, 2)
        self.assertIn("https", out)

    def test_failed_processing_leaves_nothing_behind_and_other_files_continue(self):
        self.fake.fail_names = {"projects__a.md"}
        code, out = self.run_sync()
        self.assertEqual(code, 1)
        self.assertIn("projects/a.md", out)
        self.assertNotIn("projects__a.md", self.kb_names())
        self.assertNotIn("projects__a.md", [f["name"] for f in self.fake.files.values()])
        self.assertEqual(len(self.kb_names()), 4)
        # volgende run probeert alleen het mislukte bestand opnieuw
        self.fake.fail_names = set()
        code, out = self.run_sync()
        self.assertEqual(code, 0, out)
        self.assertEqual(len(self.kb_names()), 5)

    def test_duplicate_content_is_skipped_not_fatal(self):
        (self.repo / "docs/knowledge/b.md").write_text("# A\nalpha\n", encoding="utf-8")  # zelfde inhoud als a.md
        code, out = self.run_sync()
        self.assertEqual(code, 0, out)
        self.assertIn("dubbele inhoud", out)

    def test_server_without_status_endpoint_still_works(self):
        self.fake.legacy_no_status = True
        code, out = self.run_sync()
        self.assertEqual(code, 0, out)
        self.assertEqual(len(self.kb_names()), 5)

    def test_dry_run_writes_nothing(self):
        code, out = self.run_sync("--dry-run")
        self.assertEqual(code, 0)
        self.assertIn("5 new", out)
        self.assertEqual(self.fake.files, {})
        self.assertFalse(sync.STATE_FILE.exists())

    def test_reset_empties_the_collection(self):
        self.run_sync()
        code, _ = self.run_sync("--reset")
        self.assertEqual(code, 0)
        kid = next(iter(self.fake.knowledge))
        self.assertEqual(self.fake.knowledge[kid]["files"], [])
        self.assertEqual(self.fake.files, {})

    def test_existing_collection_is_reused(self):
        self.run_sync()
        sync.STATE_FILE.unlink()  # staat kwijt, collectie bestaat nog
        code, out = self.run_sync()
        self.assertEqual(len(self.fake.knowledge), 1, "geen tweede collectie aanmaken")
        self.assertEqual(code, 0, out)


    def test_deleted_collection_is_recreated_and_refilled(self):
        self.run_sync()
        self.fake.knowledge.clear()
        code, out = self.run_sync()
        self.assertEqual(code, 0, out)
        self.assertIn("begin schoon", out)
        self.assertEqual(len(self.kb_names()), 5)

    def test_renamed_collection_gets_filled(self):
        self.run_sync()
        os.environ["OPENWEBUI_KNOWLEDGE"] = "Andere naam"
        code, out = self.run_sync()
        self.assertEqual(code, 0, out)
        self.assertEqual(len(self.fake.knowledge), 2)
        names = {v["name"]: len(v["files"]) for v in self.fake.knowledge.values()}
        self.assertEqual(names["Andere naam"], 5)

    def test_failed_removal_of_an_old_version_is_counted_and_retried(self):
        self.run_sync()
        (self.repo / "projects/a.md").write_text("# A\nalpha v2\n", encoding="utf-8")
        self.fake.deny_remove = True
        code, out = self.run_sync()
        self.assertEqual(code, 1, out)
        self.assertEqual(len(json.loads(sync.STATE_FILE.read_text())["stale"]), 1)
        self.fake.deny_remove = False
        code, out = self.run_sync()
        self.assertEqual(code, 0, out)
        self.assertEqual(json.loads(sync.STATE_FILE.read_text())["stale"], [])
        self.assertEqual(len(self.fake.files), 5, "geen oude versie meer op de server")

    def test_removed_file_stays_tracked_while_removal_fails(self):
        self.run_sync()
        (self.repo / "docs/knowledge/b.md").unlink()
        self.fake.deny_remove = True
        code, _ = self.run_sync()
        self.assertEqual(code, 1)
        self.assertIn("docs/knowledge/b.md", json.loads(sync.STATE_FILE.read_text())["files"])
        self.fake.deny_remove = False
        code, _ = self.run_sync()
        self.assertEqual(code, 0)
        self.assertNotIn("docs/knowledge/b.md", json.loads(sync.STATE_FILE.read_text())["files"])

    def test_duplicate_is_remembered_and_not_uploaded_every_run(self):
        (self.repo / "docs/knowledge/b.md").write_text("# A\nalpha\n", encoding="utf-8")
        self.run_sync()
        self.fake.requests.clear()
        code, out = self.run_sync()
        self.assertEqual(code, 0, out)
        self.assertFalse([r for r in self.fake.requests if r[0] == "POST"])

    def test_crlf_checkout_does_not_look_like_a_change(self):
        self.run_sync()
        (self.repo / "projects/a.md").write_bytes(b"# A\r\nalpha\r\n")
        code, out = self.run_sync()
        self.assertEqual(code, 0)
        self.assertIn("alles is actueel", out)

    def test_upload_never_contains_crlf(self):
        (self.repo / "projects/a.md").write_bytes(b"# A\r\nalpha\r\n")
        self.run_sync()
        self.assertTrue(all(b"\r" not in f["data"] for f in self.fake.files.values()))

    def test_timeout_on_add_is_adopted_when_the_server_did_add_it(self):
        self.fake.add_status = 524
        code, out = self.run_sync()
        self.assertEqual(code, 0, out)
        self.assertEqual(len(self.kb_names()), 5)

    def test_redirect_is_not_followed(self):
        self.fake.redirect_listing = True
        code, out = self.run_sync()
        self.assertEqual(code, 1)
        self.assertIn("redirect", out)

    def test_existing_collection_is_found_on_a_later_page(self):
        self.run_sync()
        sync.STATE_FILE.unlink()
        for n in range(3):
            self.fake.knowledge[f"x{n}"] = {"name": f"Andere {n}", "files": []}
        self.fake.knowledge_page_size = 1
        code, out = self.run_sync()
        self.assertEqual(code, 0, out)
        self.assertEqual(len(self.fake.knowledge), 4, "geen tweede 'DieOuwe Brain' aanmaken")

    def test_upload_names_keep_the_source_path(self):
        self.assertEqual(sync.upload_name("projects/blueprint-cms.md"), "projects__blueprint-cms.md")
        self.assertEqual(sync.upload_name("manifest/projects.yml"), "manifest__projects.yml.txt")


class EvalTest(Base):
    def run_eval(self, *extra):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = ev.main(["--model", "qwen3:4b", *extra])
        return code, out.getvalue()

    def test_eval_passes_when_the_answers_contain_the_facts(self):
        self.run_sync()
        code, out = self.run_eval()
        self.assertEqual(code, 0, out)
        self.assertIn("8/8 goed", out)
        body = self.fake.chat_bodies[0]
        self.assertEqual(body["files"], [{"type": "collection", "id": next(iter(self.fake.knowledge))}])
        self.assertFalse(body["stream"])

    def test_eval_fails_when_the_model_ignores_the_collection(self):
        self.run_sync()
        self.fake.chat_answer = "Dat weet ik niet."
        code, out = self.run_eval()
        self.assertEqual(code, 1)
        self.assertIn("mist: 1.34.0", out)

    def test_eval_without_collection_explains_what_to_do(self):
        code, out = self.run_eval()
        self.assertEqual(code, 1)
        self.assertIn("openwebui_sync.py", out)

    def test_eval_needs_a_model(self):
        os.environ.pop("OPENWEBUI_MODEL", None)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(ev.main([]), 2)


class EnvFileTest(unittest.TestCase):
    def test_bom_and_export_prefix_are_handled(self):
        with tempfile.TemporaryDirectory() as d:
            env = Path(d) / "e.env"
            env.write_bytes(b'\xef\xbb\xbfOPENWEBUI_URL=https://bom.example\nexport OPENWEBUI_API_KEY=k\n')
            old = sync.ENV_FILES
            sync.ENV_FILES = [env]
            for k in ("OPENWEBUI_URL", "OPENWEBUI_API_KEY"):
                os.environ.pop(k, None)
            try:
                sync.load_env_files()
                self.assertEqual(os.environ["OPENWEBUI_URL"], "https://bom.example")
                self.assertEqual(os.environ["OPENWEBUI_API_KEY"], "k")
            finally:
                sync.ENV_FILES = old
                for k in ("OPENWEBUI_URL", "OPENWEBUI_API_KEY"):
                    os.environ.pop(k, None)

    def test_utf16_env_file_is_skipped_with_a_message(self):
        with tempfile.TemporaryDirectory() as d:
            env = Path(d) / "e.env"
            env.write_bytes("OPENWEBUI_URL=https://x\n".encode("utf-16"))
            old = sync.ENV_FILES
            sync.ENV_FILES = [env]
            out = io.StringIO()
            try:
                with contextlib.redirect_stdout(out):
                    sync.load_env_files()
                self.assertIn("UTF-8", out.getvalue())
            finally:
                sync.ENV_FILES = old

    def test_env_file_fills_only_missing_values(self):
        with tempfile.TemporaryDirectory() as d:
            env = Path(d) / ".openwebui.env"
            env.write_text('# commentaar\nOPENWEBUI_URL="https://x.example"\nOPENWEBUI_API_KEY=abc\n', encoding="utf-8")
            old = sync.ENV_FILES
            sync.ENV_FILES = [env]
            os.environ.pop("OPENWEBUI_URL", None)
            os.environ["OPENWEBUI_API_KEY"] = "uit-omgeving"
            try:
                sync.load_env_files()
                self.assertEqual(os.environ["OPENWEBUI_URL"], "https://x.example")
                self.assertEqual(os.environ["OPENWEBUI_API_KEY"], "uit-omgeving")
            finally:
                sync.ENV_FILES = old
                os.environ.pop("OPENWEBUI_URL", None)


if __name__ == "__main__":
    unittest.main(verbosity=2)
