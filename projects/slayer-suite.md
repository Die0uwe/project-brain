---
id: slayer-suite
type: repo
bijgewerkt: 2026-10-03
---
# Slayer Alliance Master Suite (SA Suite)

## Doel
WordPress-plugin voor slayeralliance.com: Blizzard-EU-API-integratie, gilde- en addonpagina's, Discord-integratie.

## Wat geverifieerd is
Alleen wat in de brain staat (docs/knowledge/session-history.md, juni 2026); de broncode is niet toegankelijk in deze sessie.
- Stack: PHP 8.x, WordPress, Blizzard EU API.
- Modules: `sa_armory`, `guild_roster`, `sa_collections`, `sa_addon_list`, `sa_realm_status`, `guild_recruitment`, `sa_decor_browser`, Discord-module.
- Functies: `sa_get_valid_token()`, `sa_get_core_settings()`, `sa_get_blizzard_data()`, `sync_manager`, `backup_manager`.
- Blizzard-OAuth aanmaken: docs/tokens-and-keys/blizzard-oauth.md (redirect `https://slayeralliance.com/callback`).

## Beheer
Skill: wp-sa-suite (volgens het skill-register: "Slayer Alliance plugin"), algemeen WordPress: wp-senior-dev, testdeploy: wp-test-deployer.

## Relaties
Deployt naar [slayeralliance-com](slayeralliance-com.md).

## Openstaande punten
Repo-naam, huidige versie, changelog en testdekking: onbekend/te verifiëren.
