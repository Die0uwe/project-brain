# Currencies & Rewards — Geverifieerde Data
> WoW Retail 12.0.5 Midnight · Laatste update: 2026-06-14

---

## Dawncrest Valuta (VERIFIED)

| Currency ID | Naam | Notities |
|---|---|---|
| 3383 | Dawncrest (primair) | Hoofd Midnight valuta |
| 3341 | Dawncrest variant | |
| 3343 | Dawncrest variant | |
| 3345 | Dawncrest variant | |
| 3347 | Dawncrest variant | |
| 3377 | Extra Midnight currency | |
| 2803 | Extra currency | |
| 3378 | Extra currency | |

## API Gebruik

```lua
-- CORRECT (Midnight 12.0.5)
local info = C_CurrencyInfo.GetCurrencyInfo(3383)
if info then
    local amount = info.quantity
    local name   = info.name
    local icon   = info.iconFileID
end

-- DEPRECATED (crasht)
-- GetCurrencyInfo(3383)  ← gebruik NIET
```

## Bag IDs

| Type | ID Range |
|---|---|
| Player bags | 0 – 4 |
| Warband bank bags | 12 – 16 |

## Notes

- Altijd `pcall()` gebruiken rondom currency API calls
- Dawncrest ID 3383 is de primaire voor DelveTracker display

---

*Bron: Sessie-geverifieerd · VERIFIED*
