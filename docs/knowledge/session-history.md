# Sessie History — DieOuwe Ecosysteem
> Beslissingen, lessen en project state per sessie · Laatste update: 2026-10-03

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

## Sessie 2026-10-03 — Repo-audit, famfinder, PanicRoom, ScriptSpace

### Uitgevoerd
- famfinder (SpotFam): `assembleDebug` faalde in CI omdat de debug-keystore in `.gitignore` stond. Opgelost met de standaard debug-keystore van de Android Gradle Plugin; release-signing alleen als het secret `STORE_PASSWORD` bestaat. Gemerged naar main (commit beb7209), CI levert artifact `SpotFam-Debug-APK` (ca. 28 MB).
- PanicRoom CMS gestart (multi-agent): architectuur (GitHub, Vercel Hobby, Supabase Free), Windows-scanner v0.1.0 en v0.2.0 (prestaties, schijven, updates), JSON-schema 1.1, dashboard, 13 tests. Gemerged via PR #1; test op een echte pc staat nog open.
- ScriptSpace CMS: 0.23.0 naar 0.25.0 (afbeeldingen plakken en galerij, startpagina als eerste scherm, knop Download project, 0.25.0 schakelaar ai_builtin om DeepSeek en Gemini uit te zetten). Blueprint CMS: module ai-studio via PR #1 gemerged.
- Alle 16 repo's van Die0uwe nagelopen; project-brain, manifest en projectkaarten bijgewerkt.

### Bevindingen
- WowTracker (v3.5.5) is de actuele addon-repo; DelveTracker staat op 3.3.1-beta-hotfix en heeft geen README.
- `scriptspace-releases`: de updater leest de GitHub Releases, niet de bestanden op main. Laatste release is V0.22.0, de CMS is 0.24.2: een nieuwe ondertekende release is nog te bouwen (lokaal, `tools/release.py`). De 0.13.0-bestanden in de hoofdmap zijn oud en ongebruikt.
- Slayer-Suite: plugin-header en CHANGELOG zeiden 25.12.30, het laatste commit 26.1.0. Rechtgezet naar 26.1.0 (commit a4b3df3). De eerste commit bevat nog hardgecodeerde Blizzard-credentials in de git-geschiedenis van de publieke repo: client secret roteren.
- Besluiten van Ouwe: DelveTracker-repo blijft ongewijzigd; SCANNER blijft staan ("wordt vervolgd").
- `SCANNER` bevat alleen een LICENSE; `ai-emoji-generator`, `zeki` (fork) en `BoreD` zijn van 2023 en niet bekeken.
- famfinder mist `google-services.json`: Firebase- en Gemini-functies werken pas na toevoegen.

### Lessen
- Een gitignored bestand dat de build nodig heeft laat CI breken terwijl het lokaal werkt; gebruik de standaard debug-keystore.
- Bouwen van Android-apps kan niet in de Claude-sandbox (Maven/Google geblokkeerd); gebruik GitHub Actions.

## 2026-10-11 — SBWebUI Strato-beta v0.8.0 en v0.8.1, Discord-bot en tray

### Gedaan
- Beta v0.8.0: Beheer → Discord-bot opnieuw gebouwd (status, kanaalkeuze, alarmen in privékanaal, eigen `!commando's`), bot v0.3.0 en tray-starter v0.1.0 (Start/Stop/Herstart ook vanaf de site). Schema 9.
- Beta v0.8.1: avatar-schuiven 12 tot 180 px (oude maximum op 50%), login-tunnel met perspectief en trager tempo, handleidingen en updates ook als HTML (`tools/build-docs-html.py`), `start-tray.bat` herschreven.
- Docs, README en ADR-023 gelijkgetrokken; skills-plan met voorstel `sbwebui-beta-bot`.

### Bevindingen
- `start-tray.bat` meldde "Installeren mislukt" ten onrechte: `errorlevel` bleef 1 na een mislukte import-controle, de venv-stap werd overgeslagen (map bestond al) en `if errorlevel 1` sprong toch naar de foutmelding. Niet getest op Windows.
- Tests: tray 31/31, beta 57/57, v0.5 28/28, nieuwe display-test 12/12. Bekende basisfouten zonder verband: favicon.ico-controle en OAuth-tests (https/http in de testomgeving).
- Audit bot (security): HMAC met `hash_equals`, tijdvenster 300 s, ratelimit, alleen drie vaste tray-opdrachten. Zwakte: replay binnen 5 minuten geeft alleen het antwoord prijs, geen uitvoering.

### Lessen
- Batch: `errorlevel` blijft staan over overgeslagen regels; gebruik vlagvariabelen en blokken met haakjes.
- Playwright: `text=` is een substring-match, `inner_text` past CSS-hoofdletters toe.
