---
id: delvetracker
type: addon
bijgewerkt: 2026-10-03
bron_repo: Die0uwe/DelveTracker
---
# DelveTracker Suite (WowTracker)

## Doel
WoW-addonsuite voor Retail 12.0.5 Midnight (build 12.0.5.67314, `## Interface: 120005`): een core-addon met plugin-registry plus losse DT_-plugins (kompas-HUD voor prey hunts, cloth/warband-tracking, lockouts, currencies). Auteur op CurseForge: dieouwe (author ID 1417946).

## Stack
- Lua (WoW Retail), SavedVariables `DelveTrackerDB` (plus `WowTrackerDB`, `WowTrackerDB_Backup`, `ClothWarbandDB`, `DT_CustomAFK_Settings`).
- Themes via `DT_Theme.lua` (11 themes sinds 2026-06-15).

## Versie en status
- De repo `Die0uwe/DelveTracker` (laatste push 2026-06-02) staat op **3.3.1-beta-hotfix** (CHANGELOG-kop) en heeft geen README. De actuele versie **v3.5.5** (sessie 2026-06-15) staat in de repo `Die0uwe/WowTracker`, zie [wowtracker](wowtracker.md) en docs/knowledge/session-history.md.
- Plugins volgens de brain (stand juni 2026): DT_PreyTracker (kompas-HUD, in ontwikkeling), DT_ClothCounter, DT_WarbankBuddy, AdvancedAutoReply, DT_CustomAFK.

## Structuur
Zie docs/knowledge/addon-architecture.md: `DelveTracker.toc`, `DelveTracker.lua` (core, events, DB-init, plugin-registry), `plugins/DT_*.lua`, `Media/` (o.a. `Compass_Arrow.tga` met punt omhoog), `Libs/`.

## Build, test, deploy
- Geen buildstap; release naar CurseForge. Push naar GitHub via wow-git-manager. In-game tests via wow-test-framework.
- Verplichte regels (zie CONTEXT.md): `local addonName, addonTable = ...`, `SetClampedToScreen(true)`, `InCombatLockdown()`-guard, `pcall()` om `C_*`-calls.

## Belangrijke beslissingen
- Midnight-verboden API's en vervangers staan in docs/api/deprecated-calls.md.
- Kompasformule en hoekberekening: docs/knowledge/compass-math.md.
- Databaseschema: docs/knowledge/wowtracker-db-schema.md.

## Links
- Kennis: [known-bugs](../docs/knowledge/known-bugs.md), [maps-and-zones](../docs/knowledge/maps-and-zones.md), [currencies](../docs/knowledge/currencies-and-rewards.md).
- Beheer-skills (volgens skill-register): wow-addon-architect, wow-db-migrator, wow-dt-integrator, wow-poi-builder/-auditor, wow-prey-research, wow-i18n-specialist.

## Openstaande punten
- Besluit Ouwe (2026-10-03): de DelveTracker-repo blijft ongewijzigd (niet archiveren, geen README).
- Releasestatus en plugin-lijst van v3.5.5 op CurseForge verifiëren.
- Satellietrepo's zijn nu bekend: WowTracker, WowTracker-i18n, WowTracker-Themes (zie [wowtracker](wowtracker.md)).
