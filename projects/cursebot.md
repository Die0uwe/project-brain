---
id: cursebot
type: tool
bijgewerkt: 2026-10-03
bron_repo: Die0uwe/cursebot
---
# CurseBot (Slayer Alliance Edition)

## Doel
Python Discord-bot en desktoptool voor CurseForge-addonbeheer en release-notificaties voor de Slayer Alliance community.

## Stack
Python 3.11+, discord.py/py-cord, SQLite of PostgreSQL, CustomTkinter-UI; API-keys via keyring (naam `CurseBot-SlayerAlliance`) en een setup-wizard. Windows-installer via Inno Setup.

## Versie en status
- Laatst gedocumenteerd: bot/main.py v2.2.0, dashboard.py v2.1.0 (docs/knowledge/session-history.md, juni 2026). Actuele stand: onbekend/te verifiëren (repo niet toegankelijk in deze sessie; de repo-URL Die0uwe/cursebot komt uit de projectnotities van Ouwe).
- Volgende sprint volgens die notitie: CF Browser-tab, .exe-build met setup-wizard, GitHub-push v2.2.0.

## Structuur (juni 2026)
`bot/main.py`, `bot/services/` (stats, key_manager, curseforge_api), `bot/cogs/curseforge.py`, `ui/app.py`, `ui/setup_wizard.py`, `dashboard.py`.

## Beveiliging
Echte tokens en keys staan nooit in git of in deze brain; zie docs/tokens-and-keys/ voor hoe je ze aanmaakt en cursebot-security voor opslag (Fernet/DPAPI/keyring).

## Links
[CurseForge-key aanmaken](../docs/tokens-and-keys/curseforge-api-key.md), [Discord-bottoken](../docs/tokens-and-keys/discord-bot-token.md). Skills: discord-bot-architect, cursebot-security, wow-inno-setup.

## Openstaande punten
Versie, tests en deploy-pad in de repo verifiëren.
