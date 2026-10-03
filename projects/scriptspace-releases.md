---
id: scriptspace-releases
type: repo
bijgewerkt: 2026-10-03
bron_repo: Die0uwe/scriptspace-releases
---
# scriptspace-releases

## Doel
Publieke distributiekanaal voor ondertekende ScriptSpace CMS-releases. De updater in [scriptspace-cms](scriptspace-cms.md) leest hieruit. Repo is **publiek**.

## Inhoud
- De updater (`includes/updater.php`, `UPDATE_DEFAULT_REPO`) leest de **GitHub Releases** (`releases/latest`) met drie assets: `manifest.json`, `manifest.json.sig` (Ed25519) en `scriptspace-<versie>.zip`.
- Releases op 2026-10-03: v0.13.0, v0.13.1 en **V0.22.0** (laatste, met hoofdletter V; de updater accepteert `v` en `V`).
- De bestanden in de hoofdmap (`manifest.json`, `scriptspace-0.13.0.zip`, `RELEASE_NOTES.md`) zijn een oudere upload van 0.13.0 en worden door de updater niet gebruikt.

## Versie en status
- Laatste release: **0.22.0** (2026-10-01). De CMS staat op 0.24.2, dus 0.23.0 en 0.24.x zijn nog niet uitgebracht.
- Een nieuwe release maak je op de eigen pc met `tools/release.py build`; de private sleutel verlaat die computer nooit, daarom kan Claude dit niet doen.

## Openstaande punten
- Nieuwe release bouwen en als GitHub Release publiceren wanneer 0.24.x via de updater uit moet.
- Oude 0.13.0-bestanden in de hoofdmap eventueel opruimen of vervangen.
