<!-- ============================================================
     Project Brain — DieOuwe Ecosysteem Kennisbank
     © 2026 DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     Licentie: CC BY-SA 4.0 — Vrij te delen met bronvermelding
     ============================================================ -->

# CONTEXT — DieOuwe Project Brain
> Versie: 1.0.0 · Datum: 2026-06-08 · Beheerder: wow-brain-manager

Dit is het centrale AI-instructiebestand voor het DieOuwe ecosysteem.
**Elke Claude-sessie leest dit bestand als eerste stap.**

---

## Wat is dit repo?

`Die0uwe/project-brain` is de **levende kennisbank** van het volledige DieOuwe ecosysteem.
Het bevat geen code — alleen kennis, documentatie, en instructies voor Claude en developers.

---

## Ecosysteem Overzicht

| Repo | Inhoud | Skill-owner |
|---|---|---|
| `Die0uwe/DelveTracker` | WoW Addon Suite (Lua, TOC, XML) | wow-addon-architect |
| `Die0uwe/cursebot` | Python Discord Bot | discord-bot-architect |
| `Die0uwe/slayeralliance-wp` | WordPress Plugin (PHP) | wp-sa-suite |
| `Die0uwe/project-brain` | Kennisbank, docs, skill-instructies | wow-brain-manager |

---

## Build Target (ALTIJD geldig)

```
WoW Retail 12.0.5.67314 — Midnight
Interface: 120005
NOOIT: "The War Within" APIs
NOOIT: deprecated calls (zie docs/api/deprecated-calls.md)
```

---

## Skill Routing — Wie pakt wat op

| Taak | Primaire skill | Ondersteunend |
|---|---|---|
| WoW Lua code schrijven | wow-addon-architect | wow-oudedoos (eerst!) |
| TOC / UI check | wow-ui-polish | design-architect |
| DB schema wijzigen | wow-db-migrator | wow-addon-architect |
| Plugin koppelen aan core | wow-dt-integrator | wow-addon-architect |
| POI / locatie bouwen | poi-architect | wow-poi-auditor → wow-poi-builder |
| Prey / kompas | wow-prey-research | wow-poi-builder |
| Discord bot Python | discord-bot-architect | cursebot-security |
| API keys opslaan | cursebot-security | NOOIT elders |
| WordPress PHP | wp-sa-suite / wp-senior-dev | — |
| GitHub push | wow-git-manager | — |
| Kennisbank opzoeken | wow-oudedoos | — |
| Kennisbank aanvullen | data-grinder | general-researcher |
| Sessie afsluiten | wow-session-closer | wow-changelog-manager |
| Nieuwe skill | skill-creator | BigBoss (opdrachtgever) |
| Organisatiewijziging | wow-personeelsbeleid | BigBoss |
| **GitHub kennisbank** | **wow-brain-manager** | data-grinder |

---

## Navigatie — Wat staat waar

| Zoek je... | Lees dit bestand |
|---|---|
| MapIDs, zone coördinaten, portalen | `docs/knowledge/maps-and-zones.md` |
| Currency IDs, reward tabellen | `docs/knowledge/currencies-and-rewards.md` |
| Quest IDs, NPC database, prey data | `docs/knowledge/prey-database.md` |
| Spell IDs, aura's | `docs/knowledge/spells-and-auras.md` |
| Bekende bugs + workarounds | `docs/knowledge/known-bugs.md` |
| Kompas wiskunde | `docs/knowledge/compass-math.md` |
| Welke Blizzard API calls werken | `docs/api/blizzard-api-reference.md` |
| Deprecated / verboden calls | `docs/api/deprecated-calls.md` |
| WoW events die we gebruiken | `docs/api/events-reference.md` |
| Hoe API keys/tokens te verkrijgen | `docs/tokens-and-keys/` |
| Skill beschrijvingen en routing | `docs/skills/skill-register.md` |
| Sessie-lessen en beslissingen | `docs/knowledge/session-history.md` |

---

## Kritieke Regels (nooit overtreden)

```
VERBODEN in Midnight 12.0.5:
  OptionsSliderTemplate       → stille crash
  Fonts\FRIZQT__.TTF          → gebruik Fonts\2002.ttf
  UIDropDownMenu_* / EasyMenu → MenuUtil.CreateContextMenu()
  getglobal()                 → _G["naam"]
  GetCurrencyInfo(id)         → C_CurrencyInfo.GetCurrencyInfo(id)
  GetSpellInfo(id)            → C_Spell.GetSpellInfo(id)
  OnUpdate polling            → C_Timer.NewTicker(interval, fn)

ALTIJD VERPLICHT:
  local addonName, addonTable = ...   bovenaan elk Lua bestand
  frame:SetClampedToScreen(true)      alle verplaatsbare frames
  InCombatLockdown() guard            alle drag/move functies
  C_Timer.NewTicker(0.02, ...)        50 FPS animaties
  pcall() om alle C_* calls           crash-safe
```

---

## Visuele Identiteit Slayer Alliance

| Element | Waarde |
|---|---|
| Primair neon | `\|cffbf00ff` (Paars) |
| Secundair neon | `\|cff00dfff` (Blauw) |
| Gold accent | `\|cffccaa00` |
| Font | `Fonts\\2002.ttf` + `OUTLINE` |
| Frame strata | `MEDIUM` (HUD) / `HIGH` (Registry) |

---

## Hoe dit repo levend te houden

1. **Na elke sessie**: `data-grinder` schrijft nieuwe bevindingen naar `/docs/knowledge/`
2. **wow-brain-manager pusht** de updates naar GitHub
3. **Volgende sessie**: Claude leest dit bestand → direct up-to-date

> Geen secrets in dit repo. Nooit. Tokens, keys en passwords leven in `.env` (lokaal) of GitHub Secrets.

---
*Created by DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ*
