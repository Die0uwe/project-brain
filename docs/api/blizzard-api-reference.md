<!-- ============================================================
     Project Brain — DieOuwe Ecosysteem Kennisbank
     © 2026 DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     Licentie: CC BY-SA 4.0 — Vrij te delen met bronvermelding
     ============================================================ -->

# Blizzard API Reference — Actieve Calls
> Build: 12.0.5.67314 (Midnight) · Interface: 120005 · Beheerder: data-grinder

---

## C_CurrencyInfo

| Functie | Return | Status |
|---|---|---|
| `C_CurrencyInfo.GetCurrencyInfo(id)` | `{name, quantity, iconFileID, ...}` | VERIFIED |
| `C_CurrencyInfo.GetCurrencyListSize()` | `number` | VERIFIED |
| `C_CurrencyInfo.GetCurrencyListInfo(index)` | currency info tabel | VERIFIED |

```lua
local info = C_CurrencyInfo.GetCurrencyInfo(3383)
if info then
    print(info.name, info.quantity, info.iconFileID)
end
```

---

## C_Map

| Functie | Return | Status |
|---|---|---|
| `C_Map.GetBestMapForUnit("player")` | `mapID` | VERIFIED |
| `C_Map.GetPlayerMapPosition(mapID, "player")` | `Vector2DMixin` of `nil` | VERIFIED |
| `C_Map.GetMapInfo(uiMapID)` | `{name, mapType, parentMapID, ...}` | VERIFIED |
| `C_Map.GetWorldPosFromMapPos(mapID, pos)` | `continentID, worldX, worldY` | VERIFIED |

---

## C_QuestLog

| Functie | Return | Status |
|---|---|---|
| `C_QuestLog.GetActivePreyQuest()` | `questID` of `nil` | VERIFIED |
| `C_QuestLog.IsOnQuest(questID)` | `bool` | VERIFIED |
| `C_QuestLog.GetNextWaypointForMap(questID, mapID)` | `Vector2DMixin` of `nil` | VERIFIED |
| `C_QuestLog.GetQuestObjectives(questID)` | tabel van objectives | VERIFIED |

---

## C_Spell

| Functie | Return | Status |
|---|---|---|
| `C_Spell.GetSpellInfo(spellID)` | `{name, iconID, castTime, ...}` | VERIFIED |
| `C_Spell.IsSpellDataCached(spellID)` | `bool` | VERIFIED |

---

## C_UnitAuras

| Functie | Return | Status |
|---|---|---|
| `C_UnitAuras.GetAuraDataByIndex(unit, i, filter)` | aura data tabel | VERIFIED |
| `C_UnitAuras.GetPlayerAuraBySpellID(spellID)` | aura data of `nil` | VERIFIED |

---

## C_Timer

| Functie | Gebruik | Status |
|---|---|---|
| `C_Timer.NewTicker(interval, fn, iterations)` | Herhalende timer | VERIFIED |
| `C_Timer.NewTimer(delay, fn)` | Eenmalige timer | VERIFIED |
| `C_Timer.After(delay, fn)` | Shorthand eenmalige | VERIFIED |

```lua
-- 50fps compass update
local ticker = C_Timer.NewTicker(0.02, function()
    -- update logic
end)

-- Stop de ticker
ticker:Cancel()
```

---

## C_Container (Bags)

| Functie | Return | Status |
|---|---|---|
| `C_Container.GetContainerNumSlots(bagID)` | `number` | VERIFIED |
| `C_Container.GetContainerItemInfo(bagID, slot)` | item info tabel | VERIFIED |
| `C_Container.GetContainerNumFreeSlots(bagID)` | `numFreeSlots, bagType` | VERIFIED |

```lua
-- Alle bags itereren
for bag = 0, 4 do  -- player bags
    local slots = C_Container.GetContainerNumSlots(bag)
    for slot = 1, slots do
        local info = C_Container.GetContainerItemInfo(bag, slot)
        if info then print(info.itemID) end
    end
end
```

---

## MenuUtil (context menus)

```lua
-- GEBRUIK DIT (vervangt UIDropDownMenu):
MenuUtil.CreateContextMenu(owner, function(ownerRegion, rootDescription)
    rootDescription:CreateTitle("Mijn Menu")
    rootDescription:CreateButton("Optie 1", function() print("klik") end)
    rootDescription:CreateDivider()
    rootDescription:CreateButton("Sluiten", function() end)
end)
```

---

## GetMoney / PLAYER_MONEY

```lua
-- Huidige gold ophalen
local copper = GetMoney()
local gold   = math.floor(copper / 10000)

-- Luisteren naar wijzigingen
frame:RegisterEvent("PLAYER_MONEY")
frame:SetScript("OnEvent", function(self, event)
    local newGold = math.floor(GetMoney() / 10000)
    print("Gold gewijzigd:", newGold)
end)
```

<!-- ============================================================
     File    : docs/api/blizzard-api-reference.md
     Version : 1.0.0  Created: 2026-06-08  Updated: 2026-06-08
     Status  : New
     DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     ============================================================ -->
