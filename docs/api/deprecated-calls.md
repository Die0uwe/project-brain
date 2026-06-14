# Deprecated API Calls — WoW Retail 12.0.5 Midnight
> Alle verwijderde of gewijzigde APIs · Laatste update: 2026-06-14

---

## Directe Vervangingen (VERIFIED)

| Deprecated | Vervanger | Severity |
|---|---|---|
| `GetCurrencyInfo(id)` | `C_CurrencyInfo.GetCurrencyInfo(id)` | CRASH |
| `GetSpellInfo(id)` | `C_Spell.GetSpellInfo(id)` | CRASH |
| `UIDropDownMenu_*` | `MenuUtil.CreateContextMenu()` | CRASH |
| `EasyMenu()` | `MenuUtil.CreateContextMenu()` | CRASH |
| `getglobal("name")` | `_G["name"]` | CRASH |
| `OnTooltipSetItem` | `TooltipDataProcessor.AddTooltipPostCall` | SILENT |
| `OptionsSliderTemplate` | Custom slider frame | CRASH |
| `Fonts\FRIZQT__.TTF` | `Fonts\2002.ttf` | CRASH |

## OnUpdate → Timer

```lua
-- DEPRECATED (performance + polling issues)
frame:SetScript("OnUpdate", function(self, elapsed)
    -- logica
end)

-- CORRECT
C_Timer.NewTicker(interval, function()
    -- logica
end)
```

## Tooltip Hook

```lua
-- DEPRECATED
GameTooltip:SetScript("OnTooltipSetItem", function(tooltip)
    -- logica
end)

-- CORRECT
TooltipDataProcessor.AddTooltipPostCall(Enum.TooltipDataType.Item, function(tooltip, data)
    -- logica
end)
```

## Slider

```lua
-- DEPRECATED (stille crash — blokkeert volledig .lua bestand)
-- <Slider name="$parentSlider" inherits="OptionsSliderTemplate"/>

-- CORRECT — handmatig slider frame
local slider = CreateFrame("Slider", "MySlider", parent, "BackdropTemplate")
slider:SetMinMaxValues(0, 100)
slider:SetValue(50)
slider:SetWidth(200)
slider:SetHeight(16)
-- Voeg handmatig thumb toe
```

## UIDropDownMenu

```lua
-- DEPRECATED (verwijderd in Dragonflight, weg in Midnight)
-- UIDropDownMenu_Initialize, UIDropDownMenu_AddButton, etc.

-- CORRECT
local menu = MenuUtil.CreateContextMenu(parent, function(owner, rootDescription)
    rootDescription:CreateTitle("Mijn Menu")
    rootDescription:CreateButton("Optie 1", function() end)
    rootDescription:CreateDivider()
    rootDescription:CreateButton("Optie 2", function() end)
end)
```

## Font Pad

```lua
-- NIET MEER BESCHIKBAAR
-- "Fonts\\FRIZQT__.TTF"

-- GEBRUIK
local font = CreateFont("MyFont")
font:SetFont("Fonts\\2002.ttf", 12, "OUTLINE")

-- Of direct op frame
myText:SetFont("Fonts\\2002.ttf", 12, "OUTLINE")
```

---

*Bron: Sessie-geverifieerd build 67314 · VERIFIED*
