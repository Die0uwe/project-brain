# DieOuwe Ecosysteem — Project Brain CONTEXT
> **AI-sessie instructies** · Altijd als eerste lezen · Laatste update: 2026-06-14

---

## Wat is dit?

`Die0uwe/project-brain` is de centrale kennisbank voor het gehele DieOuwe ecosysteem.
Claude leest dit **vóór elke sessie** om context op te bouwen zonder herhaling.

---

## Projecten — Snel Overzicht

| Project | Taal | Repo | Status |
|---|---|---|---|
| DelveTracker Suite | Lua (WoW Retail 12.0.5) | `Die0uwe/DelveTracker` | Actief |
| CurseBot | Python 3.11+ | `Die0uwe/cursebot` | Actief |
| Slayer Alliance Plugin | PHP (WordPress) | `slayeralliance.com` (wp) | Actief |
| Project Brain | Markdown (Docs) | `Die0uwe/project-brain` | Actief |

---

## Navigatietabel — Wat staat waar

| Ik zoek... | Bestand |
|---|---|
| Map/zone IDs, portalen, routing | `docs/knowledge/maps-and-zones.md` |
| Quest IDs, NPC database, prey data | `docs/knowledge/prey-database.md` |
| Spell IDs, aura's, affix data | `docs/knowledge/spells-and-auras.md` |
| Currency IDs, reward systemen | `docs/knowledge/currencies-and-rewards.md` |
| Kompas wiskunde, hoekberekening | `docs/knowledge/compass-math.md` |
| Bekende bugs en regressions | `docs/knowledge/known-bugs.md` |
| Sessie-beslissingen en lessen | `docs/knowledge/session-history.md` |
| Blizzard API calls en events | `docs/api/blizzard-api-reference.md` |
| Deprecated API calls | `docs/api/deprecated-calls.md` |
| WoW events referentie | `docs/api/events-reference.md` |
| GitHub PAT aanmaken | `docs/tokens-and-keys/github-pat.md` |
| CurseForge API key | `docs/tokens-and-keys/curseforge-api-key.md` |
| Discord bot token | `docs/tokens-and-keys/discord-bot-token.md` |
| Blizzard OAuth | `docs/tokens-and-keys/blizzard-oauth.md` |
| Skill register (wie doet wat) | `docs/skills/skill-register.md` |

---

## Kritieke Constanten (ALTIJD geldig)

```
WoW Target:        Retail 12.0.5.67314 (Midnight)
Interface header:  ## Interface: 120005
Prey Quest Range:  91095 – 91400
Dawncrest IDs:     3383, 3341, 3343, 3345, 3347
Extra Currencies:  3377, 2803, 3378
Warband Bags:      12-16
Player Bags:       0-4
CF Author ID:      1417946
CF Slug:           dieouwe
SA Keyring:        CurseBot-SlayerAlliance
```

---

## Verboden in Midnight 12.0.5

```lua
-- CRASH / VERBROKEN:
OptionsSliderTemplate      -- stille crash
Fonts\FRIZQT__.TTF         -- bestaat niet meer → gebruik Fonts\2002.ttf
UIDropDownMenu_* / EasyMenu -- gebruik MenuUtil.CreateContextMenu()
getglobal()                -- gebruik _G["naam"]
OnTooltipSetItem           -- gebruik TooltipDataProcessor.AddTooltipPostCall
GetCurrencyInfo(id)        -- gebruik C_CurrencyInfo.GetCurrencyInfo(id)
GetSpellInfo(id)           -- gebruik C_Spell.GetSpellInfo(id)
OnUpdate polling           -- gebruik C_Timer.NewTicker(interval, fn)
```

## Altijd Verplicht

```lua
local addonName, addonTable = ...     -- bovenaan elk bestand
frame:SetClampedToScreen(true)        -- alle verplaatsbare frames
InCombatLockdown() guard              -- alle drag/move functies
C_Timer.NewTicker(0.02, ...)          -- 50 FPS animaties
pcall() om alle C_* calls             -- crash-safe
```

---

## Slayer Alliance Visuele Identiteit

| Element | Waarde |
|---|---|
| Primair neon | `\|cffbf00ff` (Paars) |
| Secundair neon | `\|cff00dfff` (Blauw) |
| Gold accent | `\|cffccaa00` |
| Font | `Fonts\\2002.ttf` + `OUTLINE` |
| Media pad | `Interface\\AddOns\\DelveTracker\\Media\\` |
| Frame strata | `MEDIUM` (HUD) / `HIGH` (Registry) |

---

## Kompas Formule (HEILIG)

```lua
local angle = math.atan2(dx, -dy)
local relative = angle - GetPlayerFacing()
relative = relative % (math.pi * 2)
needle:SetRotation(-relative + needleOffset)
```

Compass_Arrow.tga moet punt OMHOOG (North) hebben.

---

## Ecosysteem Skills — Korte Routing

| Taak | Primaire Skill |
|---|---|
| WoW Lua code | wow-addon-architect |
| Python/CurseBot | discord-bot-architect |
| WordPress PHP | wp-sa-suite / wp-senior-dev |
| GitHub push | wow-git-manager |
| Kennisbank push | wow-brain-manager |
| Visueel/thema | wow-theme-artist / design-architect |
| Sessie afsluiten | wow-session-closer |
| Strategische beslissing | wow-bigboss-orchestrator |

Zie `docs/skills/skill-register.md` voor volledig overzicht.

---

*Beheerd door wow-brain-manager · Rapporteert aan wow-bigboss-orchestrator*
