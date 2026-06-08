# Currency IDs & Reward Systemen
> Status: VERIFIED · Build: 12.0.5.67314 (Midnight) · Beheerder: data-grinder

---

## Midnight (Dawncrest) Currencies

| Naam | ID | Status | Bron |
|---|---|---|---|
| Dawncrest 1 | 3383 | VERIFIED | BigBoss kennisbank |
| Dawncrest 2 | 3341 | VERIFIED | BigBoss kennisbank |
| Dawncrest 3 | 3343 | VERIFIED | BigBoss kennisbank |
| Dawncrest 4 | 3345 | VERIFIED | BigBoss kennisbank |
| Dawncrest 5 | 3347 | VERIFIED | BigBoss kennisbank |
| Extra 1 | 3377 | VERIFIED | BigBoss kennisbank |
| Extra 2 | 2803 | VERIFIED | BigBoss kennisbank |
| Extra 3 | 3378 | VERIFIED | BigBoss kennisbank |

---

## Correcte API Call

```lua
-- GEBRUIK DIT:
local info = C_CurrencyInfo.GetCurrencyInfo(currencyID)
if info then
    local amount = info.quantity
    local name   = info.name
    local icon   = info.iconFileID
end

-- NOOIT DIT (deprecated):
-- GetCurrencyInfo(currencyID)
```

---

## Bag IDs

| Type | ID Range |
|---|---|
| Player bags | 0 – 4 |
| Warband Bank | 12 – 16 |

---

## WarbankBuddy ME — Bekende IDs

Zie ook `docs/knowledge/maps-and-zones.md` voor bank locaties.

| Functie | Implementatie |
|---|---|
| Warband gold ophalen | `GetMoney()` + `PLAYER_MONEY` event |
| Bag iteratie | `for bag = 0, 4 do ... end` (player) |
| Warband bag iteratie | `for bag = 12, 16 do ... end` |

---

## Betrouwbaarheidslegenda
- **VERIFIED** — Meerdere bronnen, zelf getest
- **PROBABLE** — Één betrouwbare bron
- **UNVERIFIED** — Niet getest
