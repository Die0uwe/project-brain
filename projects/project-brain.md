---
id: project-brain
type: repo
bijgewerkt: 2026-10-06
bron_repo: Die0uwe/project-brain
---
# project-brain

## Doel
Centrale AI-kennisbank en RAG-bron: geverifieerde WoW-data, API-referenties, bekende bugs, sessie-lessen, instructies voor tokens (nooit waarden) en, sinds deze structuur, een manifest en projectkaarten voor alle projecten.

## Stack
Markdown + statische HTML-viewer (`index.html`, `web/`, GitHub Pages: https://die0uwe.github.io/project-brain/), Python-standaardbibliotheek voor de index (`tools/`). Publieke repo, licentie CC BY-SA 4.0 (zie CONTRIBUTING.md).

## Structuur
`CONTEXT.md` (instructies voor AI-sessies), `docs/` (knowledge, api, tokens-and-keys, skills), `manifest/projects.yml`, `projects/`, `index/` (gegenereerd), `tools/`, `i18n/`, `contributing/`, `.github/`.

## Build, test, deploy
- `python3 tools/build_index.py` bouwt `index/brain.jsonl` en `index/llms.txt`; `--check` controleert of de index actueel is. Test: `python3 tools/test_build_index.py`.
- CI: `.github/workflows/brain-index.yml` (valideren, geen auto-commit).
- Zie [RAG-architectuur](../docs/RAG-ARCHITECTURE.md).
- Lokale AI: `tools/openwebui_sync.py` zet de kennisbestanden in een Open WebUI-collectie (alleen veranderde bestanden, hervat na fouten), `tools/openwebui_eval.py` test met 8 vaste vragen, `tools/brain_sync.bat` voor de Windows-taakplanner. Tests: `python3 tools/test_openwebui_sync.py` (nep-server, 33 tests). Handleiding en stappenplan: [OPENWEBUI-KENNISBANK](../docs/OPENWEBUI-KENNISBANK.md). Instellingen en staat staan in `.gitignore`.

## Beheer
Skill: wow-brain-manager (met data-grinder en wow-git-manager).

## Openstaande punten
- `github/workflows/validate.yml` staat in `github/` zonder punt en wordt door GitHub dus niet uitgevoerd; verplaatsen naar `.github/workflows/` is een bewuste keuze voor de eigenaar (de bestaande sessie-les over de `workflow`-PAT-scope speelt hier).
- Vertalingen in `i18n/` zijn stubs (alleen README plus enkele docs).
