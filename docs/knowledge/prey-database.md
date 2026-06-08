<!-- ============================================================
     Project Brain — DieOuwe Ecosysteem Kennisbank
     © 2026 DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     Licentie: CC BY-SA 4.0 — Vrij te delen met bronvermelding
     ============================================================ -->

# Prey Database — Quest IDs & NPC Data
> Build: 12.0.5.67314 (Midnight) · Beheerder: data-grinder · Updated: 2026-06-08

---

## Prey Quest ID Range

| Range | Gebruik | Status |
|---|---|---|
| 91095 – 91400 | Midnight prey/hunt quests | VERIFIED |

---

## Prey Detection API

```lua
-- Actieve prey quest ophalen
local questID = C_QuestLog.GetActivePreyQuest()

-- String matching VERMIJDEN — gebruik ID range check
-- NOOIT: if questName:find("prey") then
-- ALTIJD:
local function IsPreyQuest(questID)
    return questID >= 91095 and questID <= 91400
end

-- Quest waypoint voor prey
local wp = C_QuestLog.GetNextWaypointForMap(questID, mapID)
if wp then
    local targetX, targetY = wp:GetXY()
end
```

---

## Events voor Prey Tracking

| Event | Wanneer | Payload |
|---|---|---|
| `QUEST_ACCEPTED` | Prey quest gestart | `questID` |
| `QUEST_REMOVED` | Prey quest afgesloten | `questID` |
| `QUEST_WATCH_UPDATE` | Waypoint update | — |
| `UNIT_SPELLCAST_SUCCEEDED` | NPC ability (zie spells.md) | `unit, _, spellID` |

---

## Bekende Prey NPCs (Midnight)

| NPC Naam | NPC ID | Quest ID | Zone | mapID | Coördinaten | Status |
|---|---|---|---|---|---|---|
| (community aanvulling gewenst) | ? | ? | Dawncrest | 2420 | ?, ? | UNVERIFIED |

> Weet jij een NPC ID? Zie [contributing/templates/new-id.md](../../contributing/templates/new-id.md)

---

## DT_PreyTracker Architectuur Referentie

```lua
-- Prey scan loop (50fps via C_Timer)
local preyTicker = C_Timer.NewTicker(0.02, function()
    local questID = C_QuestLog.GetActivePreyQuest()
    if questID and IsPreyQuest(questID) then
        local wp = C_QuestLog.GetNextWaypointForMap(questID, C_Map.GetBestMapForUnit("player"))
        if wp then
            local tx, ty = wp:GetXY()
            -- kompas update → zie compass-math.md
        end
    end
end)
```

<!-- ============================================================
     File    : docs/knowledge/prey-database.md
     Version : 1.0.0  Created: 2026-06-08  Updated: 2026-06-08
     Status  : New
     DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     ============================================================ -->
