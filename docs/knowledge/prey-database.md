# Prey Database — Geverifieerde Data
> WoW Retail 12.0.5 Midnight · Laatste update: 2026-06-14

---

## Prey Quest ID Range (VERIFIED)

**Primaire range**: `91095 – 91400`

Elke actieve quest waarvan het ID in deze range valt is een Prey Hunt quest.
Detectie via range check — niet via string matching op "prey".

```lua
-- CORRECT detectie
local function IsPreyQuest(questID)
    return questID >= 91095 and questID <= 91400
end

-- FOUT (gebruik dit NIET)
-- string.find(questName, "prey")  ← unreliable
```

## API Calls — Prey Systeem

```lua
-- Actieve prey quest ophalen
local preyQuestID = C_QuestLog.GetActivePreyQuest()

-- Waypoint voor prey
local wp = C_QuestLog.GetNextWaypointForMap(questID, mapID)
if wp then
    local x, y = wp.x, wp.y
end

-- Player positie voor kompas
local mapID = C_Map.GetBestMapForUnit("player")
local pos   = C_Map.GetPlayerMapPosition(mapID, "player")
local px, py = pos.x, pos.y
local facing = GetPlayerFacing()  -- radialen, CCW vanuit North
```

## Kompas Hoekberekening (HEILIG)

```lua
-- dx = target.x - player.x, dy = target.y - player.y
local angle    = math.atan2(dx, -dy)
local relative = angle - GetPlayerFacing()
relative       = relative % (math.pi * 2)
needle:SetRotation(-relative + needleOffset)
```

**Of via CalcAngle (geverifieerd V3.6):**
```lua
local function NormAngle(a)
    return a % (math.pi * 2)
end
local TWO_PI = math.pi * 2
local targetCW  = NormAngle(math_atan2(-dx, dy))
local facingCW  = NormAngle(TWO_PI - facingCCW)
return NormAngle(targetCW - facingCW + (offset or 0))
```

**Vereiste**: `Compass_Arrow.tga` moet punt OMHOOG (North) hebben.

## Timer voor HUD Refresh

```lua
-- 50 FPS rotatie-update
C_Timer.NewTicker(0.02, function()
    -- update needle rotation hier
end)
```

---

*Bron: Sessie-geverifieerd · VERIFIED*
