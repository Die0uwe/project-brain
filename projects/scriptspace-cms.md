---
id: scriptspace-cms
type: repo
bijgewerkt: 2026-10-13
bron_repo: Die0uwe/scriptspace-cms
---
# ScriptSpace CMS

## Doel
PHP-platform achter scriptspace.nl: accounts met rollen (RBAC), een AI-playground met live preview, tijdelijke sandboxes (72 uur), beheerpaneel, back-up/herstel en een veilige updater. Bron: README.md en docs/MASTERPLAN.md in de repo.

## Stack
- PHP 8.x (getest met 8.4, CI draait 8.3), MySQL/MariaDB via PDO (getest met MariaDB 10.11).
- Hosting: STRATO shared hosting (geen cron nodig, pseudo-cron elke 6 uur).
- Frontend: Ace-editor, marked, DOMPurify, highlight.js (gebundeld in `assets/vendor/`), PWA (`manifest.php`, `sw.js`).
- AI-aanbieders: DeepSeek, Gemini en een eigen model ("DIEOUWE AI") via Open WebUI/Ollama of elke OpenAI-compatibele server.

## Versie en status
- Versie 0.26.1 op `main` (2026-10-13). Live op scriptspace.nl: 0.25.0 (VERIFIED via `<meta name="ss-version">`, 2026-10-13). 0.26.0 = DeepSeek als reserve onder het eigen model; 0.26.1 = footer in ScriptSpace-stijl.
- Sinds 0.23.0 (zelfde dag): 0.24.0 afbeeldingen plakken met Ctrl+V en galerij plus versie-badge, 0.24.1 de startpagina als eerste scherm en een knop Afbeeldingen, 0.25.0 de knop Download project (hele project als ZIP). 0.25.0: `ai_builtin => false` zet DeepSeek en Gemini uit, alleen het eigen model.
- Laatste gepubliceerde release in `scriptspace-releases`: V0.22.0, zie [scriptspace-releases](scriptspace-releases.md); 0.23.0 en 0.24.x zijn nog niet uitgebracht.
- Repository is **privé** (GitHub); deze kaart bevat daarom alleen functionele feiten, geen config.

## Structuur
- `api/` JSON/SSE/ZIP-endpoints (sandbox, files, ai_chat, ai_stream, pdf_save, php_run, ...).
- `includes/` kern: bootstrap, auth, rbac, crypto, ai, oauth, migrate, updater.
- `admin/` en `user/` beheer- en accountpagina's; `sql/schema.sql` + `sql/migrations/NNNN_naam.sql` (laatst 0006_profielen_0_22).
- `templates/starter/` starterproject voor nieuwe projecten; `leden.php` ledenparade; `profile.php` openbaar profiel.
- `docs/`: MASTERPLAN, AUTH, ROADMAP, DEPLOY, SECURITY-AUDIT, HANDLEIDING, EIGEN-MODEL.

## Build, test, deploy
- Geen build-stap. Lokaal: `cp config/config.example.php config/config.php` en `php -S 127.0.0.1:8000`.
- Tests (CI `.github/workflows/ci.yml`, MySQL 8 service): `tests/flow_test.py` (end-to-end), `ui_test.py` (Playwright), `auto_cleanup_test.php`, `ai_provider_test.php` (met `fake_ai_server.php`), `update_migrate_test.php`, `updater_install_test.php`, `pdf_sandbox_test.php`, `pdf_tools_test.js`.
- Deploy: bestanden via (S)FTP naar STRATO, `install.php` eenmalig draaien en daarna verwijderen; zie docs/DEPLOY.md.
- Releases: `tools/release.py` bouwt zip + manifest met Ed25519-handtekening, lokaal op de eigen pc. Releases-repo: `Die0uwe/scriptspace-releases` (bestaat, laatste GitHub Release V0.22.0).

## Footer (0.26.1, 2026-10-13)
- `includes/footer.php` met `site_footer($root)`: eigen `<style>` (klasse `.ssfoot`), logo, kolommen ScriptSpace (playground, leden, wiki), Meer van ons (cms, CoreBot, SBWebUI, Discord) en Over (privacy, DieOuwe, Slayer Alliance), onderregel met `ss_version()`.
- Gebruikt door `page_footer()` in `includes/layout.php` (alle gewone pagina's) en door `index.php` (gast- en ingelogde weergave).
- Startpagina: body mag nu scrollen; het eerste scherm blijft gevuld (`min-height: calc(100dvh / 1.2)`). De inlogsectie wordt met `zoom: 1.2` vergroot in plaats van `transform: scale(1.2)`; transform telt niet mee in de opmaak en liet de kaart over de footer vallen en buiten beeld lopen. Op schermen tot 600px geen vergroting.
- Geen GitHub-link in de footer: de repo is privé (bezoekers kregen 404). Commit 2f5807b.
- FTP-update (lokaal, alleen index.php, includes/layout.php, includes/footer.php; past op live 0.25.0): `scriptspace-0.26.1-footer-update.zip` onder `C:\SERVERS\DIEOUWE-AI`.

## Belangrijke beslissingen
- Open registratie met e-mailverificatie, rate-limit en optioneel Turnstile.
- PHP uitvoeren in de playground: alleen `super_admin`, standaard uit (`php_exec`); gewone gebruikers krijgen HTML/CSS/JS in een afgeschermde iframe.
- Rechtenmodel (RBAC met priority) is overgenomen van Blueprint CMS, zie docs/AUTH.md.
- AI-sleutels per gebruiker AES-256-GCM-versleuteld met `app_key`; de browser praat nooit rechtstreeks met een model.
- Updates alleen via ondertekende releases met back-up vooraf en automatisch terugzetten.

## Links
- Site: https://scriptspace.nl
- Relaties: zie [scriptspace-nl](scriptspace-nl.md), [blueprint-cms](blueprint-cms.md), [dieouwe-ai](dieouwe-ai.md).

## Openstaande punten
- Nog open volgens README: lokale map koppelen, PHP-WASM voor gebruikers, GrapesJS-ontwerptab.
- Beheer-skill: onbekend (geen skill uit het skill-register is aantoonbaar voor dit project).
- Een PR/branch voor deze repo is niet gecontroleerd (alleen main aanwezig in de lokale clone).
