<!-- ============================================================
     Project Brain — DieOuwe Ecosysteem Kennisbank
     © 2026 DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     Licentie: CC BY-SA 4.0 — Vrij te delen met bronvermelding
     ============================================================ -->

# Sessie Geschiedenis & Lessen
> Beheerder: data-grinder · Elke sessie voegt een entry toe

---

## Format

```
### [DATUM] — [Onderwerp]
**Sessie doel**: [wat wilde je bereiken]
**Wat geleerd**: [nieuwe inzichten, API bevindingen]
**Beslissingen**: [architectuur of structuurkeuzes]
**Nieuwe IDs**: [eventuele nieuwe mapIDs / questIDs / etc.]
**Openstaand**: [wat nog op te lossen]
```

---

### 2026-06-08 — GitHub Project Brain Architectuur

**Sessie doel**: GitHub structuur opzetten voor het volledige DieOuwe ecosysteem, kennisbank op GitHub zetten, nieuwe wow-brain-manager skill aanmaken.

**Beslissingen**:
- Vier repos: `DelveTracker`, `cursebot`, `slayeralliance-wp`, `project-brain`
- `project-brain` is de centrale kennisbank — geen code, alleen docs
- `CONTEXT.md` in root van elke repo voor Claude-sessie instructies
- Branch strategie: `main` (stabiel) → `dev` (dagelijks) → `feature/xxx`
- Tokens/keys nooit opslaan — alleen HOE je ze verkrijgt documenteren
- `wow-brain-manager` skill aangemaakt als nieuwe Kennisbank skill (v1.0.0)
- Afdeling: Kennisbank, rapporteert aan BigBoss

**Nieuwe skills**: wow-brain-manager v1.0.0

**Openstaand**:
- Blizzard OAuth flow documenteren (`docs/tokens-and-keys/blizzard-oauth.md`)
- `maps-and-zones.md` aanvullen met alle Midnight mapIDs
- `prey-database.md` aanmaken met questID range 91095–91400
- GitHub Actions `validate.yml` activeren
- wow-personeelsbeleid updaten met wow-brain-manager entry

---

*Voeg nieuwe sessies toe bovenaan (nieuwste eerst)*

<!-- ============================================================
     File    : docs/knowledge/session-history.md
     Version : 1.0.0  Created: 2026-06-08  Updated: 2026-06-08
     Status  : New
     DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     ============================================================ -->

## Sessie 2026-06-12 (v3.0.9→v3.1.9)
- Regressie hersteld: race-systeem, admin panel, warband stats herbouwd
- Fase 1+2 stappenplan compleet · 22 plugins geregistreerd
- Nieuwe lessen: SavedVariables init-timing, ipairs-nil valkuil,
  GetGuildRosterMOTD protected, frames-zijn-tables Hide-loop
- Midnight security model gedocumenteerd (zie midnight-security-model.md)
- Race icons definitief (zie race-icons-definitief.md)

## Sessie 2026-06-13 (v3.2.0→v3.5.2) — MARATHONSESSIE

### Versies geleverd: 33 releases (v3.2.0 t/m v3.5.2)

### i18n COMPLEET (Fase 3.1)
- WT_LANG 5 talen × 35+ sleutels BOVENAAN Core (zodat WT_T() overal beschikbaar is)
- WT_ApplyLanguage() ververst alle statische labels; dynamische teksten via WT_T() op bouw-moment
- Plugins: QuickSet (37 strings), Charmory (I18N_LABELS registry + Fill refresh), Registry, Lockout, HelpGuide (body herbouwt op OnShow)
- SCOPE LES: frames die op file-load bouwen (vóór taal-restore) → I18N_LABELS registry patroon

### WTTheme uitrol COMPLEET (Fase 3.2)
- Patroon: hardcoded kleuren = startwaarde; WTTheme.Register(callback) werkt alleen kleuren bij
- Gekoppeld: Registry, Charmory, ClothCounter (ApplyWindowStyle), Debugger (border groen bewaard), SkinNRare, ExchangeBot (border subtiel), MailAttach (border goud bewaard), HelpGuide
- Lockout/QuickSet: geen eigen frame → kleurden al mee via PluginArea

### Guild Calendar Scanner (Fase 3.3)
- Blizzard_Calendar is LoD → C_AddOns.LoadAddOn op PLAYER_LOGIN
- C_Timer.After(8) eerste scan (kalender moet initialiseren)
- SetAbsMonth VERPLICHT vóór elke scan
- CALENDAR_UPDATE_EVENT_LIST UNregistered tijdens scan (anders infinite loop)
- API: DT_GetGuildEvents() → {date,time,title,eventType,inviteStatus}, gesorteerd, toekomstig
- Guild tab: WT_UpdateGuildEventsList() global; ticker: [G]-regels

### Weekly Reset (Fase 3.4)
- Oude implementatie: epoch-weken (do 00:00 UTC) = FOUT voor EU
- Fix: GetCVar("portal") → EU=wo(3) 6:00, US=di(2), CN/KR/TW=do(4)
- next-reset als "YYYY-MM-DD" in DelveTrackerDB.WeeklyReset{day,hour,nextReset}
- Schrikkeljaar + maand/jaar-overflow afgedekt; lastResetWeek=nil opgeruimd

### CreateFramePool COMPLEET (Fase 4.1)
- 5 pools: rosterCardPool / currNameRowPool / currTilePool / currScrollPool / currArrowPool
- Aparte InitRosterPools + InitCurrPools (KRITIEK: één pool per parent-frame!)
- backdrop_set flag: SetBackdrop 1x per frame, nooit herhalen
- hScroll:Show() + hContent:Show() VERPLICHT na Acquire (pool doet Hide op release)
- FontStrings/Textures: if not card.ico then ... end guard (geen stapeling)

### Secret-audit COMPLEET (Fase 4.2)
- CHAT_MSG_LOOT: ContentManager + ClothCounter hebben issecretvalue guard
- UNIT_AURA: SkinNRare + PreyTracker hebben defensieve guard (unitID normaal niet secret)
- COMBAT_LOG_EVENT_UNFILTERED: WowTracker gebruikt het NIET → veilig
- STANDAARD GUARD: if issecretvalue and (issecretvalue(msg) or issecretvalue(sender)) then return end + type check

### Security Debugger Tab (Fase 4.3)
- 6 secties: C_RestrictedActions, Secret Value API, Taint Status, Combat Lockdown, Secure Templates, Midnight API Check
- C_RestrictedActions methods bestaan NIET als publieke API in Midnight 12.x → "(niet publiek in 12.x)"
- SecureActionButtonTemplate/SecureHandlerStateTemplate: niet in _G, wel via CreateFrame inherits

### Versie-constante (Fase 4.5)
- WT_VERSION bovenaan Core; header/contextmenu/admin lezen één bron
- Procedure: ALLEEN WT_VERSION + ## Version: in TOC bijwerken

### WT_MakeSAScrollbar (v3.4.0)
- Centrale helper: baan (donker paars 0.18,0.06,0.30) + thumb (neon paars 0.48,0.00,0.80)
- parent = parent or sf:GetParent() fallback (KRITIEK: nil-parent crasht)
- UIPanelScrollFrameTemplate verwijderd uit ALLE frames → sf.ScrollBar:Hide() in helper
- Mousewheel 30px/tik + thumb drag + UpdateThumb via HookScript
- Uitgerold: Core (5 frames) + 10+ plugins

### Roster verbeteringen
- Sortering op CLASS_ORDER (Warrior→Evoker, dan naam)
- Grid gecentreerd: _xOff = (_frameW - _gridW) / 2
- Orphan filter: if not (data.class or data.level or data.race or money) then skip
- visIdx teller (niet i) voor positie — goto bestaat niet in WoW Lua 5.1!
- /wt cleanup + /wt-cleanup: verwijdert orphans + spatie-vs-nospatie duplicaten
- DB duplicaten: "Defias Brotherhood" (spatie) vs "DefiasBrotherhood" (geen spatie)
- rows[i]=card crash: voor _,key = i is nil → rows[visIdx]

### Currency tab
- Volledige Midnight set: Dawncrest 5-tiers (3383/3341/3343/3345/3347)
- Volgorde: Coffer Keys → Dundun → Manaflux → Dawncrest → Valorstones → rest Midnight → vorige expansies
- Pool triple-fix: hScroll:Show() + nameRow reuse + tile reuse

### MOTD race-condition (v3.2.9)
- Tab-open herpogingen 1s (retry) + 3s (NO_MOTD fallback)
- GUILD_ROSTER_UPDATE vult cache ook met tab dicht
- WT_GetMOTD: pcall om C_GuildInfo.GetGuildRosterMOTD

### DB Backup/Restore (v3.5.0-3.5.2)
- WT_DBBackup(): deep-copy DelveTrackerDB → WowTrackerDB_Backup + metadata
- WT_DBRestore(): 2-staps bevestiging, schrijft naar BEIDE DelveTrackerDB + WowTrackerDB
- TOC: WowTrackerDB + WowTrackerDB_Backup SavedVariables (v4.0 bridge)
- Admin panel: 💾 Backup + ↩ Restore knoppen + tooltips
- /wt-dbbackup + /wt-dbrestore slash commands

### Bugs gevangen
- Debugger literal LF in string (Python schrijft echte LF → WoW crasht) → binary fix
- goto in WoW Lua 5.1: bestaat NIET → altijd if/else gebruiken
- Pool parent bug: InitPools met verkeerde parent → aparte Roster/Currency pools
- Kelsey 66×66 rechtsonder online-lijst
- charInfo: stond altijd op "Laden..." → WT_UpdateCharInfo() met naam/lvl/spec/ilvl
- Vault knop footer: Blizzard_WeeklyRewards LoD + InCombatLockdown guard
