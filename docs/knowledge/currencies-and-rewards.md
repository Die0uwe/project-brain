<!-- ============================================================
     Project Brain — DieOuwe Ecosysteem Kennisbank
     © 2026 DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     Licentie: CC BY-SA 4.0 — Vrij te delen met bronvermelding
     ============================================================ -->

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

<!-- ============================================================
     File    : docs/knowledge/currencies-and-rewards.md
     Version : 1.0.0  Created: 2026-06-08  Updated: 2026-06-08
     Status  : New
     DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     ============================================================ -->

## Midnight 12.x Currencies (volledig, 2026-06-13)
Zie: midnight-currency-ids.md (volledig overzicht)
Korte samenvatting:
- Dawncrest: 3383(Adv)/3341(Vet)/3343(Champ)/3345(Hero)/3347(Myth)
- Valorstones: 3008 · Dawnlight Manaflux: 3378 · Shard of Dundun: 3376
- Coffer Keys: 3028 · Shards: 3310 · Delver's Journey: 3318
- Voidlight Marl: 3316 · Brimming Arcana: 3379 · Luminous Dust: 3385
- Remnant of Anguish: 3392 · Undercoin: 2803 · Unalloyed Abundance: 3377
