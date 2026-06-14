# Maps & Zones — Geverifieerde Data
> WoW Retail 12.0.5 Midnight · Laatste update: 2026-06-14

---

## Midnight Zones

> **Status**: Gedeeltelijk geverifieerd — uitbreiden per sessie

| Zone | MapID | Notities |
|---|---|---|
| Dawncrest (hoofd) | TBD | Midnight hoofdzone |
| Dawncrest Hub | TBD | Centrale hub/portal zone |

*MapIDs toevoegen zodra geverifieerd via in-game `C_Map.GetBestMapForUnit("player")`*

---

## API Gebruik

```lua
-- Huidige map van speler
local mapID = C_Map.GetBestMapForUnit("player")

-- Map info
local info = C_Map.GetMapInfo(mapID)
-- info.name         → zone naam
-- info.mapType      → Enum.UIMapType (World/Continent/Zone/Dungeon/etc)
-- info.parentMapID  → parent zone

-- World coordinates
local wx, wy = C_Map.GetWorldPosFromMapPos(mapID, {x=0.5, y=0.5})
```

## Zone Entry Detectie

```lua
-- Event voor zone wisseling
frame:RegisterEvent("ZONE_CHANGED_NEW_AREA")
frame:RegisterEvent("ZONE_CHANGED")
frame:RegisterEvent("ZONE_CHANGED_INDOORS")

frame:SetScript("OnEvent", function(self, event)
    local mapID = C_Map.GetBestMapForUnit("player")
    -- logica voor nieuwe zone
end)
```

---

## Portalen & Routing

> Uitbreiden zodra Midnight portaal-coördinaten geverifieerd zijn via in-game testing.

---

*Beheerd door data-grinder · Gedeeltelijk VERIFIED — uitbreiden*
