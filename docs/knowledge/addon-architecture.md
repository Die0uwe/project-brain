<!-- ============================================================
     Project Brain — DieOuwe Ecosysteem Kennisbank
     © 2026 DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     Licentie: CC BY-SA 4.0 — Vrij te delen met bronvermelding
     ============================================================ -->

# Addon Architectuur — DelveTracker Suite
> Build: 12.0.5.67314 (Midnight) · Beheerder: wow-addon-architect · Updated: 2026-06-08

---

## Bestandsstructuur DelveTracker

```
DelveTracker/
├── DelveTracker.toc          ← Interface: 120005 — hoofdentry
├── DelveTracker.lua          ← Core: events, DB init, plugin registry
├── DelveTracker.xml          ← Frame definities (optioneel)
├── plugins/
│   ├── DT_ClothCounter.lua   ← Warband cloth tracking
│   ├── DT_PreyTracker.lua    ← Prey hunt kompas HUD
│   ├── DT_WarbankBuddy.lua   ← Gold & bag tracking
│   └── DT_*.lua              ← Elke plugin zelfstandig
├── Media/
│   ├── Compass_Arrow.tga     ← Punt OMHOOG (North-up verplicht)
│   └── icons/
└── Libs/                     ← Embedded libraries
```

---

## Plugin Registry Pattern

```lua
-- In DelveTracker.lua (core)
local DT = DelveTrackerDB  -- global namespace
DT.plugins = DT.plugins or {}

-- Elke plugin registreert zichzelf:
function DT:RegisterPlugin(name, plugin)
    DT.plugins[name] = plugin
    if plugin.OnEnable then plugin:OnEnable() end
end

-- In DT_PreyTracker.lua:
local addon, ns = ...
local PreyTracker = {}
DelveTrackerDB:RegisterPlugin("PreyTracker", PreyTracker)
```

---

## SavedVariables Patroon

```lua
-- TOC:
## SavedVariables: DelveTrackerDB

-- Init in ADDON_LOADED:
DelveTrackerDB = DelveTrackerDB or {}
local DB = DelveTrackerDB

-- DB versie migratie (wow-db-migrator pattern):
local DB_VERSION = 3
if (DB.version or 0) < DB_VERSION then
    -- migreer oude data
    DB.version = DB_VERSION
end
```

---

## Namespace Patroon (elk bestand)

```lua
-- BOVENAAN elk .lua bestand (verplicht):
local addonName, addonTable = ...

-- Gedeelde namespace
addonTable.MyModule = addonTable.MyModule or {}
local M = addonTable.MyModule
```

---

## Frame Hiërarchie

| Strata | Gebruik |
|---|---|
| `BACKGROUND` | Achtergrond decoraties |
| `LOW` | Paneel achtergronden |
| `MEDIUM` | HUD elementen, kompas |
| `HIGH` | Plugin registry frame |
| `DIALOG` | Hoofd configuratie frames |
| `TOOLTIP` | Nooit gebruiken voor eigen frames |

---

## Verplichte Guards

```lua
-- Elke frame drag/move functie:
frame:SetScript("OnMouseDown", function(self, button)
    if InCombatLockdown() then return end
    self:StartMoving()
end)

-- Elke C_* API call:
local ok, result = pcall(C_CurrencyInfo.GetCurrencyInfo, currencyID)
if ok and result then
    -- gebruik result
end
```

<!-- ============================================================
     File    : docs/knowledge/addon-architecture.md
     Role    : DelveTracker addon architectuur referentie
     Version : 1.0.0
     Created : 2026-06-08
     Updated : 2026-06-08  14:30
     Status  : New
     ─────────────────────────────────────────────────────────
     DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     ============================================================ -->
