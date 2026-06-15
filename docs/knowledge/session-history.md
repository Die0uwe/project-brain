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

## Sessie 2026-06-15 — Theme Engine 2.0 + DT_Abundance refactor

### Uitgevoerd
- WowTracker v3.5.5 opgeleverd
- DT_Theme.lua v2.0 → v1.2.0: 11 themes totaal
  - Nieuw: Titan Bronze, Void Reborn, Emerald Elven
  - B/X/Murloc icon callbacks (DT_RegistryOpenBtn, DelveTrackerFrame.close, DT_MurlocBtn)
  - BlendMode ADD → BLEND fix
- 45 TGA icons gesneden van ChatGPT sheet (1467×1072px, zwarte achtergrond)
  - Correcte crop: x=440-619, 647-816, 848-1023, 1048-1217, 1248-1415
  - v3.5.5 naamgeving: icon_{slot}_{themekey}.tga in Media/Icons/20px/
- WowTracker.lua: knoppen 22px → 32px, Cleanup DB knop admin panel
- DT_Abundance.lua aangemaakt — Abundance tegel uit DT_QuickSet gesplitst
  - Publieke API: DT_BuildAbundanceFrame(), DT_RefreshAbundanceFrame()
  - Data via DT_GetAbundanceData() uit DT_events.lua
- DT_MinimapIcon.lua: nieuw bestand, LibDBIcon integratie
- WowTracker.xml: DT_Abundance + MinimapIcon in load order
- /wt-cleanup command: verwijdert dubbele roster entries

### Kritieke lessen
- Icon sheet MOET zwarte achtergrond hebben voor correcte crop detectie
- v3.5.5 draait DelveTrackerDB, repo had WowTrackerDB (v4.0.3) — baseline = v3.5.5
- SetBlendMode("ADD") op MBtn.tex maakt murloc transparant → fix via DT_Theme.lua callback
- DT_RegistryOpenBtn is globaal → bereikbaar vanuit DT_Theme.lua zonder plugin aan te raken
- Abundance tegel dependency map:
  - UI: DT_QuickSet → DT_BuildAbundanceFrame() in DT_Abundance.lua
  - Data: DT_events.lua → DT_GetAbundanceData() public API
  - Strings: WowTracker.lua i18n (QS_AB_*, QS_LOADING, QS_REMAINING)

### GitHub status
- WowTracker: ✓ gepushed (commit 4880c2e)
- README: ✓ bijgewerkt v3.5.5
- CHANGELOG: ✓ v3.5.5 entry toegevoegd
