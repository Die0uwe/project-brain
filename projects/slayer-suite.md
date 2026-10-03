---
id: slayer-suite
type: repo
bijgewerkt: 2026-10-03
---
# Slayer Alliance Master Suite (SA Suite)

## Doel
WordPress-plugin voor slayeralliance.com: Blizzard-EU-API-integratie, gilde- en addonpagina's, Discord-integratie.

## Wat geverifieerd is
Repo: `Die0uwe/Slayer-Suite` (publiek, laatste push 2026-06-04). Plugin-header en CHANGELOG zeggen versie 25.12.30; het laatste commitbericht ("Sprint 1 security hardening v26.1.0") noemt 26.1.0, dat is nog niet in de CHANGELOG verwerkt. Verder wat in de brain staat (docs/knowledge/session-history.md, juni 2026).
- Stack: PHP 8.x, WordPress, Blizzard EU API.
- Modules: `sa_armory`, `guild_roster`, `sa_collections`, `sa_addon_list`, `sa_realm_status`, `guild_recruitment`, `sa_decor_browser`, Discord-module.
- Functies: `sa_get_valid_token()`, `sa_get_core_settings()`, `sa_get_blizzard_data()`, `sync_manager`, `backup_manager`.
- Blizzard-OAuth aanmaken: docs/tokens-and-keys/blizzard-oauth.md (redirect `https://slayeralliance.com/callback`).

## Beheer
Skill: wp-sa-suite (volgens het skill-register: "Slayer Alliance plugin"), algemeen WordPress: wp-senior-dev, testdeploy: wp-test-deployer.

## Relaties
Deployt naar [slayeralliance-com](slayeralliance-com.md).

## Openstaande punten
Versie-afwijking (25.12.30 tegenover 26.1.0) rechtzetten in plugin-header en CHANGELOG; testdekking onbekend.
