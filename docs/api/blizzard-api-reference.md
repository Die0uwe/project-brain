# Blizzard API Reference — WoW Retail 12.0.5 Midnight
> Geverifieerde API calls voor build 67314 · Laatste update: 2026-06-14

---

## Map & Positie

```lua
-- Beste map voor unit
local mapID = C_Map.GetBestMapForUnit("player")

-- Speler positie op kaart (returnt MapVector2D of nil)
local pos = C_Map.GetPlayerMapPosition(mapID, "player")
if pos then local x, y = pos.x, pos.y end

-- World positie van map positie (cross-zone)
local wx, wy = C_Map.GetWorldPosFromMapPos(mapID, {x=0.5, y=0.5})

-- Map info
local mapInfo = C_Map.GetMapInfo(mapID)
-- mapInfo.name, mapInfo.mapType, mapInfo.parentMapID
```

## Quest System

```lua
-- Actieve prey quest
local questID = C_QuestLog.GetActivePreyQuest()

-- Waypoint voor quest op map
local wp = C_QuestLog.GetNextWaypointForMap(questID, mapID)

-- Quest actief check
local isActive = C_QuestLog.IsOnQuest(questID)

-- Quest info
local info = C_QuestLog.GetQuestInfo(questID)
```

## Currency

```lua
-- Info ophalen (CORRECT)
local info = C_CurrencyInfo.GetCurrencyInfo(currencyID)
if info then
    info.quantity     -- huidige hoeveelheid
    info.name         -- naam van de currency
    info.iconFileID   -- icon texture ID
    info.maxQuantity  -- max (0 = unlimited)
end

-- Currency container (meerdere tegelijk)
local currencies = C_CurrencyInfo.GetCurrencyListInfo()
```

## Spell System

```lua
-- Spell info (CORRECT)
local spellInfo = C_Spell.GetSpellInfo(spellID)
if spellInfo then
    spellInfo.name
    spellInfo.iconID
    spellInfo.castTime
    spellInfo.minRange
    spellInfo.maxRange
end

-- Cooldown
local start, duration, enabled = C_Spell.GetSpellCooldown(spellID)
```

## Player

```lua
-- Facing (radialen, CCW vanuit North/0)
local facing = GetPlayerFacing()

-- Naam en realm
local name, realm = UnitName("player")

-- GUID
local guid = UnitGUID("player")

-- Combat check (ALTIJD vóór UI manipulatie)
if InCombatLockdown() then return end
```

## Frame Systeem

```lua
-- Frame aanmaken (correct pattern)
local frame = CreateFrame("Frame", "MyFrame", UIParent, "BackdropTemplate")
frame:SetSize(200, 100)
frame:SetPoint("CENTER")
frame:SetClampedToScreen(true)        -- ALTIJD voor verplaatsbare frames
frame:SetMovable(true)
frame:EnableMouse(true)

-- Drag met combat guard
frame:SetScript("OnMouseDown", function(self, button)
    if button == "LeftButton" and not InCombatLockdown() then
        self:StartMoving()
    end
end)
frame:SetScript("OnMouseUp", function(self)
    self:StopMovingOrSizing()
end)
```

## Timer

```lua
-- Eenmalig
C_Timer.After(delay, function()
    -- code
end)

-- Herhalend (geeft ticker object terug)
local ticker = C_Timer.NewTicker(interval, function()
    -- code
end, repetitions)  -- repetitions = nil voor oneindig

-- Stoppen
ticker:Cancel()
```

## Tooltip

```lua
-- Item tooltip hook (CORRECT)
TooltipDataProcessor.AddTooltipPostCall(Enum.TooltipDataType.Item, function(tooltip, data)
    local name, link = tooltip:GetItem()
    -- logica
end)

-- Unit tooltip
TooltipDataProcessor.AddTooltipPostCall(Enum.TooltipDataType.Unit, function(tooltip, data)
    local unit = data.guid
    -- logica
end)
```

## Dropdown Menu

```lua
-- Context menu (CORRECT)
MenuUtil.CreateContextMenu(parent, function(owner, rootDescription)
    rootDescription:CreateTitle("Titel")
    rootDescription:CreateButton("Label", function()
        -- actie
    end)
    rootDescription:CreateDivider()
    local submenu = rootDescription:CreateButton("Submenu")
    submenu:CreateButton("Sub-optie", function() end)
end)
```

---

*Bron: Retail 12.0.5 / build 67314 · VERIFIED*
