<!-- ============================================================
     Project Brain — DieOuwe Ecosysteem Kennisbank
     © 2026 DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     Licentie: CC BY-SA 4.0 — Vrij te delen met bronvermelding
     ============================================================ -->

# Maps & Zones — Geverifieerde MapIDs
> Build: 12.0.5.67314 (Midnight) · Beheerder: data-grinder · Updated: 2026-06-08

---

## Midnight Zones (12.0.x)

| Zone naam | mapID | uiMapID | Type | Status | Bron |
|---|---|---|---|---|---|
| Dawncrest | 2420 | 2420 | Zone | PROBABLE | wow-oudedoos |
| Midnight Hub (TBD) | ? | ? | City | UNVERIFIED | datamine |

---

## Portalen & Entry Points

| Van | Naar | Type | Coördinaten (van) | Status |
|---|---|---|---|---|
| Oribos | Dawncrest | Portal | TBD | UNVERIFIED |

---

## WoW Bag / Bank mapIDs

| Type | ID Range | Gebruik |
|---|---|---|
| Player bags | 0 – 4 | C_Container iteratie |
| Warband Bank | 12 – 16 | WarbankBuddy ME |

---

## API: Positie ophalen

```lua
-- Speler positie op huidige map
local mapID = C_Map.GetBestMapForUnit("player")
local pos = C_Map.GetPlayerMapPosition(mapID, "player")
if pos then
    local x, y = pos:GetXY()
end

-- Cross-zone wereldcoördinaten
local worldX, worldY = C_Map.GetWorldPosFromMapPos(mapID, {x = mapX, y = mapY})

-- MapID van een zone op naam (via uiMapID)
local mapInfo = C_Map.GetMapInfo(uiMapID)
```

---

## Betrouwbaarheidslegenda
- **VERIFIED** — Meerdere bronnen, zelf getest
- **PROBABLE** — Één betrouwbare bron
- **UNVERIFIED** — Community aanvulling gewenst

<!-- ============================================================
     File    : docs/knowledge/maps-and-zones.md
     Version : 1.0.0  Created: 2026-06-08  Updated: 2026-06-08
     Status  : New
     DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     ============================================================ -->
