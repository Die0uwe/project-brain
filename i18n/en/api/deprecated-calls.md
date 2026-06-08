> 🌐 Translation of [`docs/api/deprecated-calls.md`](../../../docs/api/deprecated-calls.md)
> Language: English · Translated by: DieOuwe team · Date: 2026-06-08

# Deprecated & Forbidden API Calls
> Build target: 12.0.5.67314 (Midnight) · Interface: 120005

---

## FORBIDDEN — Cause crashes or taint

| Forbidden call | Why | Replacement |
|---|---|---|
| `OptionsSliderTemplate` | Silent crash, blocks file | `MinimalSliderWithSteppers` |
| `UIDropDownMenu_*` | Deprecated, taint issues | `MenuUtil.CreateContextMenu()` |
| `EasyMenu()` | Deprecated | `MenuUtil.CreateContextMenu()` |
| `getglobal("name")` | Deprecated, nil return | `_G["name"]` |
| `OnTooltipSetItem` | Deprecated hook | `TooltipDataProcessor.AddTooltipPostCall` |
| `Fonts\FRIZQT__.TTF` | File doesn't exist in Midnight | `Fonts\2002.ttf` |

---

## DEPRECATED — No longer work, use replacement

| Deprecated call | Status | Correct replacement |
|---|---|---|
| `GetCurrencyInfo(id)` | DEPRECATED 11.0+ | `C_CurrencyInfo.GetCurrencyInfo(id)` |
| `GetSpellInfo(id)` | DEPRECATED 11.0+ | `C_Spell.GetSpellInfo(id)` |
| `GetItemInfo(id)` | DEPRECATED | `C_Item.GetItemInfo(id)` |
| `UnitAura(unit, i)` | DEPRECATED | `C_UnitAuras.GetAuraDataByIndex(unit, i, filter)` |
| `OnUpdate` (polling) | AVOID | `C_Timer.NewTicker(interval, fn)` |

---

## REQUIRED PATTERNS (always use these)

```lua
-- Top of every Lua file
local addonName, addonTable = ...

-- All movable frames
frame:SetClampedToScreen(true)

-- Drag/move protection
if InCombatLockdown() then return end

-- 50fps animations
local ticker = C_Timer.NewTicker(0.02, fn)

-- Crash-safe API calls
local ok, result = pcall(function()
    return C_SomeNamespace.SomeCall(arg)
end)

-- Cross-zone coordinates
local worldX, worldY = C_Map.GetWorldPosFromMapPos(mapID, pos)
```

---

## Active C_Namespaces in 12.0.5

| Namespace | Use |
|---|---|
| `C_CurrencyInfo` | Currency queries |
| `C_Spell` | Spell data |
| `C_Item` | Item data |
| `C_Map` | Map and position |
| `C_QuestLog` | Quest data, prey quests |
| `C_UnitAuras` | Aura/buff tracking |
| `C_Timer` | Timers and tickers |
| `C_Container` | Bag/item containers |
| `MenuUtil` | Context menus |
