<!-- ============================================================
     Project Brain — DieOuwe Ecosysteem Kennisbank
     © 2026 DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     Licentie: CC BY-SA 4.0 — Vrij te delen met bronvermelding
     ============================================================ -->

# Kompas Wiskunde — De Heilige Formule
> Status: VERIFIED · Versie: V3.6 geverifieerd · Beheerder: data-grinder

---

## ⚠️ HEILIG — Nooit wijzigen zonder BigBoss goedkeuring

```lua
-- Methode A (standaard)
local angle = math.atan2(dx, -dy)           -- dx = tx-px, dy = ty-py
local relative = angle - GetPlayerFacing()
relative = relative % (math.pi * 2)
needle:SetRotation(-relative + needleOffset)
```

```lua
-- Methode B (CalcAngle — geverifieerd V3.6)
local function NormAngle(a)
    return a % (math.pi * 2)
end

local targetCW  = NormAngle(math_atan2(-dx, dy))
local facingCCW = GetPlayerFacing()               -- WoW geeft CCW terug
local facingCW  = NormAngle(TWO_PI - facingCCW)
return NormAngle(targetCW - facingCW + (offset or 0))
```

---

## Variabelen

| Variabele | Betekenis |
|---|---|
| `dx` | `targetX - playerX` |
| `dy` | `targetY - playerY` |
| `GetPlayerFacing()` | Geeft CCW radialen terug (WoW intern) |
| `needleOffset` | Compensatie voor TGA rotatie-startpunt |
| `TWO_PI` | `math.pi * 2` (= 6.2831...) |

---

## TGA Vereiste

```
Compass_Arrow.tga punt moet OMHOOG staan (North = 0 graden)
Elke andere oriëntatie breekt de naaldrichting.
```

---

## C_Timer voor 50fps animatie

```lua
local ticker = C_Timer.NewTicker(0.02, function()
    -- compass update logic hier
    local facing = GetPlayerFacing()
    needle:SetRotation(CalcAngle(targetX, targetY) )
end)
```

---

## Coördinaten ophalen (cross-zone)

```lua
-- Cross-zone coördinaten
local worldX, worldY = C_Map.GetWorldPosFromMapPos(mapID, {x = mapX, y = mapY})

-- Speler positie
local playerMapPos = C_Map.GetPlayerMapPosition(C_Map.GetBestMapForUnit("player"), "player")
```

---

## Bekende valkuilen

| Probleem | Oorzaak | Fix |
|---|---|---|
| Naald altijd naar Noord | `GetPlayerFacing()` niet afgetrokken | Voeg `-GetPlayerFacing()` toe |
| Naald 90° gedraaid | TGA staat niet North-up | Roteer TGA bestand zelf |
| Naald springt | `%` modulo ontbreekt | Altijd `% (math.pi * 2)` na berekening |
| Nil errors | `C_Map` call zonder pcall | Wikkel in `pcall()` |

<!-- ============================================================
     File    : docs/knowledge/compass-math.md
     Version : 1.0.0  Created: 2026-06-08  Updated: 2026-06-08
     Status  : New
     DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     ============================================================ -->
