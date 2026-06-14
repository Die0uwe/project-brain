# Sessie History — DieOuwe Ecosysteem
> Beslissingen, lessen en project state per sessie · Laatste update: 2026-06-14

---

## Ecosysteem State — 2026-06-14 (BigBoss Full Analyse)

### DelveTracker Suite — WoW Retail 12.0.5 Midnight

**Target build**: `12.0.5.67314` · Interface: `120005`

| Addon/Plugin | Versie | Status | Notities |
|---|---|---|---|
| DelveTracker Core | v2.x | ✅ Actief | Hoofd addon, plugin registry |
| DT_preytracker | v3.x | 🔧 In ontwikkeling | Compass HUD, hoekberekening |
| AdvancedAutoReply | v2.2 | ✅ Actief | |
| WarbankBuddy ME | v2.0 | ✅ Actief | Warband bank tracking |
| Alle DT_ plugins | v2.x | ✅ Actief | Cloth, Currency, Lockout etc. |

**Kritieke data:**
- Prey quest ID range: `91095 – 91400`
- Dawncrest currency IDs: `3383, 3341, 3343, 3345, 3347`
- Extra currencies: `3377, 2803, 3378`
- Warband bag IDs: `12-16` | Player bags: `0-4`

---

### CurseBot — Python Discord Bot

**Stack**: Python 3.11+ · discord.py / py-cord · SQLite/PostgreSQL

| File | Versie | Status |
|---|---|---|
| dashboard.py | v2.1.0 | ✅ Actief |
| bot/main.py | v2.2.0 | ✅ Actief |
| bot/services/stats.py | v2.1.0 | ✅ Actief |
| bot/services/key_manager.py | v1.0.0 | ✅ Nieuw |
| bot/services/curseforge_api.py | v2.1.0 | ✅ Actief |
| bot/cogs/curseforge.py | v2.1.0 | ✅ Actief |
| ui/app.py | v1.2.0 | ✅ Actief |
| ui/setup_wizard.py | v1.0.0 | ✅ Nieuw |

**CurseForge config:**
- Author ID: `1417946`
- Slug: `dieouwe`
- Keyring: `CurseBot-SlayerAlliance`

**Volgende sprint:**
- CF Browser tab in CurseBot UI
- CurseBot .exe build + setup wizard test
- GitHub push v2.2.0

---

### Slayer Alliance — WordPress Plugin

**URL**: `slayeralliance.com`
**Stack**: PHP 8.x · WordPress · Blizzard EU API

**Actieve modules:**
- `sa_armory` — Character armory
- `guild_roster` — Gilde roster
- `sa_collections` — Mount/pet collecties
- `sa_addon_list` — Addon overzicht
- `sa_realm_status` — Realm monitor
- `guild_recruitment` — Recruitment module
- `sa_decor_browser` — Housing decoraties
- `discord module` — Discord integratie

**Functies:**
- `sa_get_valid_token()` — Blizzard OAuth token
- `sa_get_core_settings()` — Core plugin instellingen
- `sa_get_blizzard_data()` — API data ophalen
- `sync_manager` — Data sync
- `backup_manager` — DB backup

---

### Project Brain — Kennisbank

**Repo**: `Die0uwe/project-brain`
**URL**: `https://die0uwe.github.io/project-brain/`

**Status:**
- Dark-themed HTML viewer ✅
- Sidebar navigatie ✅
- Multilingual support ✅ (NL/EN/DE/FR stubs)
- Fork/PR templates ✅
- GitHub Issue forms ✅
- validate.yml workflow ✅

---

## Historische Lessen

### 2026-06 — Skill Naming Kritiek
**Les**: Lokale folder naam moet exact matchen met `name` field in YAML frontmatter.
Mismatch → Claude behandelt upload als nieuwe skill i.p.v. update.

### 2026-06 — GitHub Pages Path
**Les**: Alleen `/` of `/docs` zijn geldige source paths voor GitHub Pages.
Willekeurige subdirectories werken niet.

### 2026-06 — PAT Scope
**Les**: Full pipeline vereist `repo` + `workflow` scopes.
Missing `workflow` scope → stille failure bij push naar `.github/workflows/`.
Oplossing: workflows handmatig aanmaken via GitHub UI.

### 2026-06 — Skill Update Verificatie
**Les**: Vóór herpackaging altijd programmatisch verifiëren dat geen originele content verloren ging.

### Permanente WoW API Lessen

| Probleem | Oorzaak | Oplossing |
|---|---|---|
| Stille crash bij slider | `OptionsSliderTemplate` verwijderd | Custom slider frame |
| Font laadt niet | `FRIZQT__.TTF` bestaat niet | `Fonts\2002.ttf` |
| Dropdown crash | `UIDropDownMenu_*` deprecated | `MenuUtil.CreateContextMenu()` |
| getglobal nil | Deprecated | `_G["naam"]` |
| Tooltip hook werkt niet | `OnTooltipSetItem` deprecated | `TooltipDataProcessor.AddTooltipPostCall` |
| Currency nil | `GetCurrencyInfo(id)` deprecated | `C_CurrencyInfo.GetCurrencyInfo(id)` |
| Spell nil | `GetSpellInfo(id)` deprecated | `C_Spell.GetSpellInfo(id)` |
| OnUpdate performance | Polling | `C_Timer.NewTicker(interval, fn)` |

---

*Beheerd door data-grinder + wow-brain-manager*
