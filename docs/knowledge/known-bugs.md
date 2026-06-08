<!-- ============================================================
     Project Brain — DieOuwe Ecosysteem Kennisbank
     © 2026 DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     Licentie: CC BY-SA 4.0 — Vrij te delen met bronvermelding
     ============================================================ -->

# Bekende Bugs & Workarounds
> Beheerder: data-grinder · Laatste update: 2026-06-09 · Bron: BugSack live session + Midnight 12.0.5 PDF

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

---

## WowTracker v3.x — Nieuwe Bugs (2026-06-09, BugSack verified)

| Bug | Symptoom | Impact | Fix | Status |
|---|---|---|---|---|
| `RAID_CLASS_COLORS[class]` retourneert function | `attempt to index local 'c' (a function value)` — 23x | Roster + Delves tab crash | `C_ClassColor.GetClassColor(classToken)` | OPEN |
| Forward-declare nil in ShowTab(1) | `attempt to call a nil value` — 12x | Guild tab crash | Guild-laad functie assignment voor ShowTab definitie | OPEN |
| `ts` upvalue nil in MenuUtil callback | `attempt to index upvalue 'ts' (a nil value)` | Murloc menu crash | `local ts_ref = ts` voor closure | OPEN |
| `ClothCharDB` global nil bij zone change | `attempt to index global 'ClothCharDB'` — 27x | ClothCounter crash | `ClothCharDB = ClothCharDB or {}` in ADDON_LOADED | OPEN |

### Detail: C_ClassColor API — VERIFIED fix
```lua
-- FOUT (Midnight 12.x): RAID_CLASS_COLORS[class] kan een functie retourneren!
-- CORRECT:
local classColor = C_ClassColor.GetClassColor(data.class)
local r = classColor and classColor.r or 1
local g = classColor and classColor.g or 1  
local b = classColor and classColor.b or 1
```

### Detail: MenuUtil Closure Scope — VERIFIED
```lua
-- FOUT: upvalue nil in callback context
-- CORRECT: capture voor closure
local ts_ref = ts
root:CreateButton("label", function()
    if ts_ref then ts_ref[key] = not ts_ref[key] end
end)
```

### WowTracker v3.x Tab Structuur (geverifieerd BugSack 2026-06-09)
- Tab1: Guild (guildName, motdText, img, dieouwe, onlineScroll, logoWM, divLine)
- Tab2: Delves
- Tab3: Bounty (DT_BountyArea, quickWrap)
- Tab4: Roster (COLS=3, CARD_W=230, CARD_H=130, GAP=8)
- Tab5: Armory (armoryEmbedded=true)
- Tab6: Currency (searchBox, scroll, hdr)

### SA Kleur constanten in core (geverifieerd BugSack locals):
SA_GOLD="|cffccaa00" SA_GREY="|cff887799" SA_BLUE="|cff00ccff" C_2002="Fonts\2002.ttf"
