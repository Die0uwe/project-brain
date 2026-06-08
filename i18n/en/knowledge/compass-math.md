> 🌐 Translation of [`docs/knowledge/compass-math.md`](../../../docs/knowledge/compass-math.md)
> Language: English · Translated by: DieOuwe team · Date: 2026-06-08

# Compass Math — The Holy Formula
> Status: VERIFIED · Version: V3.6 verified · Maintainer: data-grinder

---

## ⚠️ SACRED — Never change without BigBoss approval

```lua
-- Method A (standard)
local angle = math.atan2(dx, -dy)           -- dx = tx-px, dy = ty-py
local relative = angle - GetPlayerFacing()
relative = relative % (math.pi * 2)
needle:SetRotation(-relative + needleOffset)
```

```lua
-- Method B (CalcAngle — verified V3.6)
local function NormAngle(a)
    return a % (math.pi * 2)
end

local targetCW  = NormAngle(math_atan2(-dx, dy))
local facingCCW = GetPlayerFacing()               -- WoW returns CCW radians
local facingCW  = NormAngle(TWO_PI - facingCCW)
return NormAngle(targetCW - facingCW + (offset or 0))
```

---

## Variables

| Variable | Meaning |
|---|---|
| `dx` | `targetX - playerX` |
| `dy` | `targetY - playerY` |
| `GetPlayerFacing()` | Returns CCW radians (WoW internal) |
| `needleOffset` | Compensation for TGA rotation start point |
| `TWO_PI` | `math.pi * 2` (= 6.2831...) |

---

## TGA Requirement

```
Compass_Arrow.tga arrow tip must point UP (North = 0 degrees)
Any other orientation breaks the needle direction.
```

---

## C_Timer for 50fps animation

```lua
local ticker = C_Timer.NewTicker(0.02, function()
    local facing = GetPlayerFacing()
    needle:SetRotation(CalcAngle(targetX, targetY))
end)
```

---

## Getting coordinates (cross-zone)

```lua
-- Cross-zone coordinates
local worldX, worldY = C_Map.GetWorldPosFromMapPos(mapID, {x = mapX, y = mapY})

-- Player position
local playerMapPos = C_Map.GetPlayerMapPosition(C_Map.GetBestMapForUnit("player"), "player")
```

---

## Known pitfalls

| Problem | Cause | Fix |
|---|---|---|
| Needle always points North | `GetPlayerFacing()` not subtracted | Add `-GetPlayerFacing()` |
| Needle rotated 90° | TGA not North-up | Rotate the TGA file itself |
| Needle jumps | `%` modulo missing | Always add `% (math.pi * 2)` after calculation |
| Nil errors | `C_Map` call without pcall | Wrap in `pcall()` |
