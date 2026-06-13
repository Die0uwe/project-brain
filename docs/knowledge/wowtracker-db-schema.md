# WowTracker DB Schema — v3.5.x
*Bijgewerkt 2026-06-13*

## TOC SavedVariables (v3.5.2)
```
DelveTrackerDB        ← actieve DB (v3.x)
WowTrackerDB          ← v4.0 bridge (via Restore gevuld)
WowTrackerDB_Backup   ← backup via admin panel
DT_CustomAFK_Settings ← CustomAFK plugin
ClothWarbandDB        ← ClothCounter warband data
```

## DelveTrackerDB top-level keys
```lua
{
    characters = { ["Naam-Realm"] = {
        class, faction, spec, ilvl, level, money,
        raceTag, sex/gender, delves, totalDone,
        specID, raceID, guild, avgIlvl,
        stats = {stamina,str,agi,int,armor},
        gear = {[slot]={link,ilvl}},
        professions = [{name,icon,rank,maxRank,skillLine}],
        currencies = {[id]=amount},
        lockouts, lastSeen,
    }},
    PluginStates = {["naam"]=bool},
    mainScale, mScale, mainPos, murlocPos,
    tickerShow = {events,guild,prey,time},
    enableCombatAlert,
    language,
    activeTheme,
    WeeklyReset = {day,hour,nextReset},
    theme (legacy),
    preySettings (PreyTracker),
    preyPos,
}
```

## v4.0 Migratie plan
1. Backup drukken (v3.5.x) → Restore drukken → WowTrackerDB gevuld in WTF
2. v4.0: alle 180 code-referenties DelveTrackerDB → WowTrackerDB (geautomatiseerd)
3. TOC: DelveTrackerDB verwijderen uit SavedVariables
4. Garantie: nul data-verlies dankzij de bridge in v3.5.1
