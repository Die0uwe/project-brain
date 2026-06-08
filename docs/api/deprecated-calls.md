# Deprecated & Verboden API Calls
> Build target: 12.0.5.67314 (Midnight) · Interface: 120005 · Beheerder: data-grinder

---

## VERBODEN — Veroorzaken crashes of taint

| Verboden call | Waarom | Vervanging |
|---|---|---|
| `OptionsSliderTemplate` | Stille crash, blokkeert bestand | `MinimalSliderWithSteppers` |
| `UIDropDownMenu_*` | Deprecated, taint issues | `MenuUtil.CreateContextMenu()` |
| `EasyMenu()` | Deprecated | `MenuUtil.CreateContextMenu()` |
| `getglobal("naam")` | Deprecated, nil return | `_G["naam"]` |
| `OnTooltipSetItem` | Deprecated hook | `TooltipDataProcessor.AddTooltipPostCall` |
| `Fonts\FRIZQT__.TTF` | Bestand bestaat niet in Midnight | `Fonts\2002.ttf` |

---

## DEPRECATED — Werken niet meer, gebruik vervanging

| Deprecated call | Status | Correcte vervanging |
|---|---|---|
| `GetCurrencyInfo(id)` | DEPRECATED 11.0+ | `C_CurrencyInfo.GetCurrencyInfo(id)` |
| `GetSpellInfo(id)` | DEPRECATED 11.0+ | `C_Spell.GetSpellInfo(id)` |
| `GetItemInfo(id)` | DEPRECATED | `C_Item.GetItemInfo(id)` |
| `UnitAura(unit, i)` | DEPRECATED | `C_UnitAuras.GetAuraDataByIndex(unit, i, filter)` |
| `OnUpdate` (polling) | VERMIJDEN | `C_Timer.NewTicker(interval, fn)` |

---

## VERPLICHTE PATTERNS (altijd gebruiken)

```lua
-- Bovenaan elk Lua bestand
local addonName, addonTable = ...

-- Alle verplaatsbare frames
frame:SetClampedToScreen(true)

-- Drag/move bescherming
if InCombatLockdown() then return end

-- 50fps animaties
local ticker = C_Timer.NewTicker(0.02, fn)

-- Crash-safe API aanroepen
local ok, result = pcall(function()
    return C_SomeNamespace.SomeCall(arg)
end)

-- Cross-zone coördinaten
local worldX, worldY = C_Map.GetWorldPosFromMapPos(mapID, pos)
```

---

## C_Namespaces die actief zijn in 12.0.5

| Namespace | Gebruik |
|---|---|
| `C_CurrencyInfo` | Valuta queries |
| `C_Spell` | Spell data |
| `C_Item` | Item data |
| `C_Map` | Kaart en positie |
| `C_QuestLog` | Quest data, prey quests |
| `C_UnitAuras` | Aura/buff tracking |
| `C_Timer` | Timers en tickers |
| `C_Container` | Bag/item containers |
| `MenuUtil` | Context menus |
