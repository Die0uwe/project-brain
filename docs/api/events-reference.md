<!-- ============================================================
     Project Brain — DieOuwe Ecosysteem Kennisbank
     © 2026 DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     Licentie: CC BY-SA 4.0 — Vrij te delen met bronvermelding
     ============================================================ -->

# Events Reference — WoW Events die we gebruiken
> Build: 12.0.5.67314 (Midnight) · Beheerder: data-grinder · Updated: 2026-06-08

---

## Addon Lifecycle

| Event | Wanneer | Gebruik |
|---|---|---|
| `ADDON_LOADED` | Addon geladen | SavedVariables initialiseren |
| `PLAYER_LOGIN` | Speler ingelogd | UI bouwen, data ophalen |
| `PLAYER_ENTERING_WORLD` | Laadscherm voorbij | Map/positie data beschikbaar |
| `PLAYER_LOGOUT` | Uitloggen | Cleanup, final save |

```lua
local f = CreateFrame("Frame")
f:RegisterEvent("ADDON_LOADED")
f:SetScript("OnEvent", function(self, event, addonName)
    if event == "ADDON_LOADED" and addonName == "DelveTracker" then
        -- initialiseer DB
        self:UnregisterEvent("ADDON_LOADED")
    end
end)
```

---

## Combat Events

| Event | Wanneer | Gebruik |
|---|---|---|
| `PLAYER_REGEN_DISABLED` | Combat start | InCombatLockdown guard |
| `PLAYER_REGEN_ENABLED` | Combat einde | UI herstellen |
| `COMBAT_LOG_EVENT_UNFILTERED` | Elke combat actie | Spell tracking |

---

## Quest Events

| Event | Wanneer | Payload |
|---|---|---|
| `QUEST_ACCEPTED` | Quest aangenomen | `questID` |
| `QUEST_REMOVED` | Quest verlaten/voltooid | `questID` |
| `QUEST_WATCH_UPDATE` | Tracker update | — |
| `QUEST_TURNED_IN` | Quest ingeleverd | `questID, xpReward, moneyReward` |

---

## Currency & Money Events

| Event | Wanneer | Gebruik |
|---|---|---|
| `PLAYER_MONEY` | Gold wijziging | GetMoney() aanroepen |
| `CURRENCY_DISPLAY_UPDATE` | Currency update | C_CurrencyInfo.GetCurrencyInfo() |
| `BAG_UPDATE` | Bag inhoud wijziging | Container iteratie |

---

## Map & Positie Events

| Event | Wanneer | Gebruik |
|---|---|---|
| `ZONE_CHANGED` | Zone gewisseld | mapID opnieuw ophalen |
| `ZONE_CHANGED_NEW_AREA` | Nieuw subgebied | Compass reset |
| `MINIMAP_ZONE_CHANGED` | Minimap zone update | — |

---

## UI Events

| Event | Wanneer | Gebruik |
|---|---|---|
| `PLAYER_ALIVE` | Na dood | UI herstellen |
| `DISPLAY_SIZE_CHANGED` | Resolutie wijziging | Frame posities resetten |
| `UI_SCALE_CHANGED` | UI schaal wijziging | SetClampedToScreen hercheck |

---

## Frame registratie patroon

```lua
local f = CreateFrame("Frame", "DTEventFrame", UIParent)
f:RegisterEvent("PLAYER_LOGIN")
f:RegisterEvent("ZONE_CHANGED")
f:RegisterEvent("QUEST_ACCEPTED")
f:SetScript("OnEvent", function(self, event, ...)
    if event == "PLAYER_LOGIN" then
        -- init
    elseif event == "ZONE_CHANGED" then
        -- zone update
    elseif event == "QUEST_ACCEPTED" then
        local questID = ...
        -- quest check
    end
end)
```

<!-- ============================================================
     File    : docs/api/events-reference.md
     Version : 1.0.0  Created: 2026-06-08  Updated: 2026-06-08
     Status  : New
     DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     ============================================================ -->
