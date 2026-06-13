# WowTracker Patterns & Lessen — Kritieke Kennis
*Bijgewerkt 2026-06-13*

## Lua 5.1 Compatibiliteit
- `goto` en `::label::` bestaan NIET in WoW Lua 5.1 → altijd if/else gebruiken
- Literal LF (`\n`) in een string via Python: CRASH in WoW → altijd `\\n` dubbel escapen
- Python schrijft soms echte LF bytes in strings → binary fix nodig
- `table.concat(lines, "\n")` vanuit Python: schrijft echte newline → gebruik binary replace

## Frame Pools (CreateFramePool)
- Aparte pools per parent-frame (roster ≠ currency parent!)
- `pool:ReleaseAll()` doet `Hide()` → altijd `frame:Show()` na Acquire
- ScrollFrame uit pool: `hScroll:Show()` + `hContent:Show()` verplicht
- FontStrings/Textures op gepoold frame: `if not card.ico then ... end` guard
- backdrop_set flag: SetBackdrop slechts 1x per frame-lifetime
- `card:SetParent(hContent)` bij tile acquire voor correcte rendering

## Scrollbars
- `WT_MakeSAScrollbar(sf, parent)`: parent ALTIJD meegeven of `sf:GetParent()` fallback
- UIPanelScrollFrameTemplate verwijderd → sf.ScrollBar:Hide() in helper
- Pool-reset doet Hide() → na Acquire altijd Show()
- Events UI: parent = `EventsUI` (local in file, NIET `evPanel`)

## Roster / For-loop
- `for _,key in ipairs(sorted)`: `_` is nil, niet `i` → gebruik aparte `visIdx` teller
- `rows[i]=card` crashes als i nil → `rows[visIdx]=card`
- `goto continue` bestaat niet → if/else wrapper gebruiken
- Orphan filter: characters zonder class+level+race+gold → overslaan
- DB duplicaten: "Defias Brotherhood" (spatie) vs "DefiasBrotherhood" (geen spatie)

## Admin Panel Load Volgorde (KRITIEK)
Forward declares → tab functies → WT_* definities → Admin panel → Murloc → Events
Admin panel code NOOIT vóór functie-definities!

## Calendar / Events
- Blizzard_Calendar is LoD → C_AddOns.LoadAddOn op PLAYER_LOGIN
- SetAbsMonth VERPLICHT vóór elke scan
- CALENDAR_UPDATE_EVENT_LIST tijdens scan UNregistreren (infinite loop!)
- C_Timer.After(8) eerste scan na login

## Secret Values (Midnight)
- CHAT_MSG_* payloads zijn secret op tainted paths → issecretvalue check verplicht
- UNIT_AURA arg1 (unitID): normaal niet secret maar defensieve guard aanbevolen
- COMBAT_LOG_EVENT_UNFILTERED: WowTracker gebruikt het niet → veilig
- Standaard guard: `if issecretvalue and issecretvalue(v) then return end` + type check

## DB / SavedVariables
- TOC: WowTrackerDB + WowTrackerDB_Backup declareren voor v4.0 bridge
- Backup: WT_DeepCopy() + metadata fields
- Restore: schrijft naar BEIDE DelveTrackerDB + WowTrackerDB
- 2-staps bevestiging voor destructieve acties (30s timeout)
- Weekly reset: GetCVar("portal") → EU=wo(3), US=di(2), CN/KR/TW=do(4)

## Versie procedure
- ALLEEN `local WT_VERSION = "X.Y.Z"` in Core + `## Version:` in TOC
- Nooit versie hardcoden in andere bestanden

## Debugger
- Titel: `"v"..WT_VERSION` (nooit hardcoded)
- C_RestrictedActions methods bestaan NIET publiek in 12.x → label "(niet publiek in 12.x)"
- SecureActionButtonTemplate niet in _G → check altijd via CreateFrame inherits
