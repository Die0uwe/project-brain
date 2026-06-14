# Compass Math — Hoekberekening DelveTracker
> Geverifieerd V3.6 · Laatste update: 2026-06-14

---

## De Heilige Formule

```lua
-- INPUTS:
-- dx = target.x - player.x  (map coords, [0,1] range)
-- dy = target.y - player.y
-- GetPlayerFacing() = CCW radialen vanuit North

local angle    = math.atan2(dx, -dy)    -- richting naar target (CW vanuit North)
local relative = angle - GetPlayerFacing()
relative       = relative % (math.pi * 2)
needle:SetRotation(-relative + needleOffset)
```

**needleOffset** = 0 als de texture al pointing-up is.
Als texture pointing-right is: `needleOffset = -math.pi/2`

---

## Alternatieve Formule (CalcAngle — ook geverifieerd)

```lua
local TWO_PI = math.pi * 2

local function NormAngle(a)
    return a % TWO_PI
end

local function CalcAngle(px, py, tx, ty, facingCCW, offset)
    local dx = tx - px
    local dy = ty - py
    local targetCW  = NormAngle(math.atan2(-dx, dy))
    local facingCW  = NormAngle(TWO_PI - facingCCW)
    return NormAngle(targetCW - facingCW + (offset or 0))
end

-- Gebruik:
local angle = CalcAngle(pos.x, pos.y, target.x, target.y, GetPlayerFacing(), 0)
needle:SetRotation(-angle)
```

---

## Vereisten

1. **Compass_Arrow.tga** moet punt OMHOOG (North) hebben
2. Update frequentie: `C_Timer.NewTicker(0.02, fn)` = 50 FPS
3. Map coords ophalen via `C_Map.GetPlayerMapPosition()` (returnt nil buiten loaded map)
4. Altijd nil-check op pos vóór berekening

---

## Volledige Implementation Template

```lua
local TICK = 0.02  -- 50 FPS

local function UpdateCompass()
    local mapID = C_Map.GetBestMapForUnit("player")
    if not mapID then return end
    
    local pos = C_Map.GetPlayerMapPosition(mapID, "player")
    if not pos then return end
    
    local target = GetCurrentPreyTarget(mapID)  -- eigen functie
    if not target then
        needle:Hide()
        return
    end
    
    local dx = target.x - pos.x
    local dy = target.y - pos.y
    
    -- Afstand check (optioneel, vermijd jitter bij overlap)
    if math.sqrt(dx*dx + dy*dy) < 0.001 then return end
    
    local angle    = math.atan2(dx, -dy)
    local relative = angle - GetPlayerFacing()
    relative       = relative % (math.pi * 2)
    
    needle:SetRotation(-relative)
    needle:Show()
end

local compassTicker = C_Timer.NewTicker(TICK, UpdateCompass)
```

---

## Veelgemaakte Fouten

| Fout | Symptoom | Fix |
|---|---|---|
| `math.atan2(dy, dx)` i.p.v. `(dx, -dy)` | Naald wijst 90° of 180° verkeerd | Swap args |
| Geen `% (math.pi * 2)` | Naald springt bij 0/2π grens | Modulo toevoegen |
| Arrow texture pointing RIGHT | Naald altijd 90° fout | Gebruik texture pointing UP |
| Geen nil-check op `pos` | Crash buiten map | `if not pos then return end` |

---

*Bron: Sessie-geverifieerd V3.6 · VERIFIED*
