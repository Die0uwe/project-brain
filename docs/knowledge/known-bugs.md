<!-- ============================================================
     Project Brain — DieOuwe Ecosysteem Kennisbank
     © 2026 DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     Licentie: CC BY-SA 4.0 — Vrij te delen met bronvermelding
     ============================================================ -->

# Bekende Bugs & Workarounds
> Beheerder: data-grinder · Laatste update: 2026-06-08 · Bron: wow-oudedoos

---

## Kritieke Crashes (onmiddellijk fixen)

| Bug | Symptoom | Fix | Versie |
|---|---|---|---|
| `OptionsSliderTemplate` | Stille crash, blokkeert hele bestand | Gebruik `MinimalSliderWithSteppers` | 12.0.x |
| `Fonts\FRIZQT__.TTF` | Font bestaat niet → addon laadt niet | Gebruik `Fonts\2002.ttf` | 12.0.x |
| `UIDropDownMenu_*` / `EasyMenu` | Deprecated → taint issues | `MenuUtil.CreateContextMenu()` | 11.0+ |
| `getglobal()` | Deprecated → nil return | `_G["naam"]` | 11.0+ |

---

## API Deprecated Calls

| Oude call | Status | Vervanging |
|---|---|---|
| `GetCurrencyInfo(id)` | DEPRECATED | `C_CurrencyInfo.GetCurrencyInfo(id)` |
| `GetSpellInfo(id)` | DEPRECATED | `C_Spell.GetSpellInfo(id)` |
| `OnUpdate` polling | VERMIJDEN | `C_Timer.NewTicker(interval, fn)` |
| `OnTooltipSetItem` | DEPRECATED | `TooltipDataProcessor.AddTooltipPostCall` |

---

## Taint Issues

| Situatie | Oorzaak | Fix |
|---|---|---|
| Frame drag in combat | `InCombatLockdown()` niet gecheckt | Altijd guard aan begin van drag/move |
| SecureActionButton | Secure frame aangeraakt door addon code | Geen addon code mag secure frames raken |

---

## Frame / UI Bugs

| Bug | Symptoom | Fix |
|---|---|---|
| Frame buiten scherm | Frame verdwijnt bij resolutiewijziging | `frame:SetClampedToScreen(true)` ALTIJD |
| Kompas naald omgekeerd | Punt van arrow.tga staat omlaag | TGA moet punt OMHOOG (North) staan |
| 50fps animatie haperingen | Timer te snel / te langzaam | `C_Timer.NewTicker(0.02, fn)` = exact 50fps |

---

## CurseBot (Python)

| Bug | Symptoom | Fix |
|---|---|---|
| `tasks.loop` stopt bij error | Bot offline zonder melding | `@loop.error` handler toevoegen |
| CF API rate limit | 429 responses, bot crasht | Exponential backoff implementeren |
| Discord token expired | Bot start niet | Token vernieuwen via Discord Developer Portal |

---

## WordPress (Slayer Alliance)

| Bug | Symptoom | Fix |
|---|---|---|
| Nonce verificatie faalt | AJAX calls geblokkeerd | `wp_verify_nonce()` correct implementeren |
| SQL injection risico | Ruwe `$_POST` in queries | Altijd `$wpdb->prepare()` gebruiken |
| Blizzard OAuth expired | API calls falen | Token refresh flow implementeren |

---

## Betrouwbaarheidslegenda
- **VERIFIED** — Meerdere bronnen, zelf getest
- **PROBABLE** — Één betrouwbare bron
- **UNVERIFIED** — Niet getest, gebruik met voorzichtigheid

<!-- ============================================================
     File    : docs/knowledge/known-bugs.md
     Version : 1.0.0  Created: 2026-06-08  Updated: 2026-06-08
     Status  : New
     DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     ============================================================ -->
