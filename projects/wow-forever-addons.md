---
id: wow-forever-addons
type: addon
bijgewerkt: 2026-11-15
bron_repo: lokaal (eigen git, nog niet op GitHub)
---
# WoW Forever-addons: DieOuweUI en NodeHound

## Wat is WoW Forever
De Forever-client van Blizzard: de Retail-client (1.60.1, interface 16001, product `wowf`) met **vanilla-inhoud** en nieuwe zones
(o.a. Zephras Isle 2521, Mount Hyjal 2482, Darkspear Islands 2524, Riverglades 2548, Shen'dralas 2652) en het neutrale ras **Skyborne**.
Alleen vanilla-inhoud: Retail-zaken als Mythic+, keystones en Great Vault horen niet in deze addons. Client-API ≠ spelinhoud.

## Addons op CurseForge (auteur DieOuwe)
| Addon | Spel | CurseForge | Stand 15-11-2026 |
|---|---|---|---|
| DieOuweUI | WoW Forever | `dieouweui` (project 1792573) | 2.23.0 op CurseForge; 2.24.1 klaar |
| NodeHound | WoW Forever | `nodehound` | 0.7.0 live (15-11-2026) |
| The 3D Avatar & Bar (SlayerBar) | Retail 12.0.1 | `slayer-bar-avatar` (project 1445157) | 12.0.1 (januari 2026) |

## DieOuweUI
Complete eigen interface: alles verplaatsen op een raster (F7), Index (F5), instellingen (F6), thema's met ornamenten (DieOuwe Dark,
Forged Iron, Dark Iron, Slayer Neon, Klassekleur), alts en opslag, beroepen, reizen en reizenteller, mail naar alt, vlieg- en AFK-scherm,
macrobouwer, social en PvP, groepsframes (beta), gemak (o.a. glinsters bij kruiden en erts).
- Talen: nl, en, de, ro (1323 teksten per taal). Roemeens: de spellettertypen hebben geen ă/ș/ț, die worden a/s/t; â en î blijven.
- Site en handleiding (4 talen, ook PDF): dieouwe.nl/dieouweui, galerij voor indelingen en looks.
- 2.24.0: Roemeens; omweg voor Blizzards fout `Blizzard_ProfessionsRecipeList.lua:359` (recepknop meldt zich in OnHide opnieuw aan
  voor `RefreshCraftableCount`; DieOuweUI meldt hem na OnHide af, zonder Blizzard-tabellen te wijzigen).
- 2.24.1: glinsters bij kruiden en erts: vaste cursor-FDID's (GatherHerbs 131018, Mine 131025, QuestInteract 1006596 …), herkenning op naam,
  zonder naambordje boven het midden van het scherm.

## NodeHound
Leert erts, kruiden, kisten en visplekken uit eigen verzamelen; pins op wereldkaart en minimap, respawn-timers, levelmodus, zoeken (`/nh find`),
volgende-knop, minimapknop, export/import (NH2, alleen samenvoegen). Talen en, ro. Community-kaart op dieouwe.nl/nodehound met alle
57 kaarten uit de client (UiMap, flight maps overgeslagen), filters, zoeken, insturen met goedkeuring (drempel aantal spelers instelbaar in Beheer).

## Hulpmiddelen (lokaal)
- Eigen CASC-lezer en WDC5-lezer (alleen lezen) voor de spelbestanden: kaarten (UiMap 1957206, UiMapXMapArt 1957217, UiMapArtTile 1957210)
  en itemnamen (ItemSparse 1572924: in Forever een sparse tabel; 15 van 16 secties versleuteld; per record 5 teksten, de 5e is de naam;
  18.003 items zonder testitems).
- Controles: API-check, Lua-syntax, indelingssimulatie, NodeHound-tests, vertaalcontrole; release-scripts per addon.

## Koppelingen met CoreBot (0.7.3)
- Plugin **wowitem**: `/item` en "Items in dit bericht" met de itemnamen uit de client; tooltip van Wowhead Classic
  (`nether.wowhead.com/classic/tooltip/item/<id>`), Forever-eigen items (ID ≥ 240000, ±4.900) krijgen een eigen kaartje.
- Plugin **twitchbrug**: in de Twitch-chat van DieOuwe `!dieouweui`, `!nodehound` (CurseForge-links), `!release`, `!drop`, `!item`.
  Twitch heeft geen openbare API voor lopende drops (alleen entitlements voor de uitgever): de drop wordt met de hand ingesteld.
