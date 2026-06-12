# Race Icons — DEFINITIEVE Referentie (geconsolideerd)
*Bronnen: Constants.lua v3.5.0-3.5.2 (TextureAtlasViewer-geverifieerd) +
gids "Karaktericonen 12.0.5" + "Race Data, Models, DisplayID's" PDF*
*Verwerkt 2026-06-12 · geïmplementeerd in WowTracker Core v3.1.8/v3.1.9*

## De keten (DT_SetRaceIcon)
0. `GetRaceAtlas(raceTag, gender, true)` — officiële dynamische API,
   ALTIJD valideren met `C_Texture.GetAtlasInfo`
1. `raceicon128-{kort}-{gender}` (charactercreateicons atlas, ALLE rassen)
2. `raceicon-{kort}-{gender}` (64px legacy — LET OP: gebruikt soms de
   VOLLE naam: raceicon-highmountaintauren i.p.v. -highmountain!)
2.5 `AlliedRace-Crest-*` (rassen zonder raceicon128, bv. Harronir)
3. `SetTexture(134400)` vraagteken

## Geverifieerde korte namen (✓ = TextureAtlasViewer bevestigd)
darkirondwarf ✓ (MÉT suffix!) · magharorc ✓ (MÉT suffix!) ·
lightforged ✓ (ZONDER suffix) · highmountain ✓ · zandalari ✓ ·
kultiran ✓ · voidelf ✓ · nightborne ✓ · dracthyr ✓ · scourge (Undead)
→ patroon "allied races strippen suffix" is ONBETROUWBAAR — tabel is leidend.

## Midnight
- raceTag = "Harronir" (DUBBELE r), raceID 86 (gameplay) / 37 (gids-lijst)
- `raceicon128-harronir-*` = LEEG in 12.0.5 → probeer "haranir" (single r),
  daarna crest `AlliedRace-Crest-Haranir` (bevestigd via GetRaceInfoByID(86))

## DB-reparatie zonder her-inloggen (v3.1.9)
`C_CreatureInfo.GetRaceInfo(id)` → localized raceName + clientFileString.
Reverse-lookup over raceIDs {1-11,22,24-32,34-37} repareert oude
localized DB-entries ("Undead"→"Scourge") op PLAYER_LOGIN.

## NOOIT
- `C_GameData.GetPlayableRaces/GetPlayableRaceInfo` — BESTAAT NIET publiek
- `texture:SetTexture(displayID)` — DisplayID ≠ texture; alleen voor
  `DressUpModel:SetDisplayInfo(id)` / PlayerModel / ModelScene
- Model paden (Character\...\*.m2) als texture
- WoW Lua heeft GEEN :trim() — crasht

## Class icons
- Modern: `GetClassAtlas("WARRIOR")` → "classicon-warrior" (valideren!)
- Legacy: Icons-Classes + CLASS_ICON_TCOORDS[classFileName]
- Pad-variant: "Interface\\Icons\\ClassIcon_"..Name (ClassIconNames tabel,
  incl. Evoker) — kleurkeys ALTIJD classFileName (11e return roster API)
