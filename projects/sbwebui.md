---
id: sbwebui
type: repo
bijgewerkt: 2026-10-18
bron_repo: Die0uwe/SBwebui
---
# SBWebUI

## Doel
Eigen Nederlands CMS met geïntegreerde AI-chat en code-modus: de AI-chat is het centrum, met blokken links en rechts, volledig aanpasbaar en sneller dan Open WebUI. Bron: README.md, docs/besluiten.md en CHANGELOG.md in de repo.

## Twee sporen
- **Hoofdlijn (Next.js, TypeScript strict, Drizzle, Postgres + pgvector, SSE):** ontwerp en besluiten (ADR-001 t/m ADR-023 in `docs/besluiten.md`), nog geen productie. De meeste ADR's zijn *voorstel*; alleen wat als *besloten door Ouwe* staat telt als besluit.
- **Strato-beta (`beta-strato/`, PHP + MySQL):** werkende site op https://sbwebui.scriptspace.nl/, bedoeld om het ontwerp in de praktijk te proberen. Ollama draait op Ouwe's eigen pc.

## Stand 2026-10-18
- **Beta 0.9.23** live op sbwebui.scriptspace.nl. Sinds 0.9.8: kennisbank met AI-indeling, dicteren, DeepSeek-reserve, webzoeken via eigen SearXNG en de **Beeldmaker**.
- **Beeldmaker (ADR-029, gebouwd):** SBWebUI → img.scriptspace.nl (Cloudflare-tunnel, sleutel) → beeldserver op de pc → Fooocus 2.5.5 (SDXL) op een RTX 4060 (8 GB).
  Ollama-model `owlai` maakt van een Nederlands idee een Engelse beeldopdracht; vaste profielen foto/algemeen/anime/kunst; beeldkaart in de chat met voortgang,
  Groter en Variatie; Mijn beelden (privé / via link / openbaar), galerij voor leden, deelpagina met Open Graph-kaart en deelknoppen; rechten per rol of per lid,
  daglimiet en tegoed; 18+ alleen voor volwassenen en altijd privé (minderjarigen en jong klinkende woorden altijd geweigerd); moderatie-logboek op de pc.
- **CoreBot (Discord-bot):** live 0.5.7; testbot 0.7.0 met 8 plugins, waaronder **Tekenen** (`/teken`, knop "Maak een beeld", via dezelfde beeldserver, nooit 18+).
- **Muziekmaker (ADR-030, voorstel):** ACE-Step 1.5 (MIT) op de pc via een muziekserver en muziek.scriptspace.nl; asynchroon, gedeelde GPU-wachtrij met de beeldserver,
  geen Docker-GPU, externe cloud later en standaard uit. Fase 0 (proef: geheugen, snelheid, Nederlands zingen) akkoord op 2026-10-18.
- Lessen: Fooocus crasht bij een modelwissel als het wisselbestand te klein is (nu 32–64 GB); Docker Desktop kan na een herstart vastlopen op een oud socketbestand.

## Versie en status (2026-10-11)
- Beta v0.8.3-beta, databaseschema 10. Nieuw in 0.8.3: RAG v1 op de Bibliotheek (categorieën en subcategorieën, één samengevoegd document per gepubliceerde pagina, MySQL FULLTEXT, bronnen onder het antwoord; ADR-024 blijft voorstel, embeddings later) en een vloeiendere login-tunnel. Eerder in 0.8.2: Open Graph/Twitter Card-tags per platform (Beheer → Delen), mobiele chat gefixt (toetsenbord, vraag bovenaan), versie en klok bovenin, zoeken boven inklapbare gesprekkenlijst.
- Eerder in 0.8.1: Nieuw in 0.8.0: Beheer, Discord-bot, kanaalkeuze, alarmen in een privékanaal, eigen `!commando's`. Nieuw in 0.8.1: avatar-schuiven 12 tot 180 px, login-tunnel met perspectief en trager tempo, handleidingen als HTML.
- Discord-bot v0.3.0 en tray-starter v0.1.0 in `tools/discord-bot/` (ADR-023: bot beheerd vanuit het paneel; gebouwd in de beta, voorstel voor de hoofdlijn).
- Hosting: Strato voor de beta, Docker voor de hoofdlijn (besluit van Ouwe, ADR-010).

## Bot en tray in het kort
- Bot meldt zich elke 30 s bij `bot_ping.php` (HMAC-SHA256 over de body, tijdvenster 300 s, 30 verzoeken per minuut per IP). Instellingen en testopdrachten komen terug in het antwoord.
- Tray-starter meldt zich apart (`role: tray`, elke 15 s) en voert alleen `start`, `stop` en `restart` uit.
- Lokale poorten voor enkelvoudige instantie: 47831 (bot) en 47832 (tray).

## Besluiten van Ouwe
- Hosting met Docker; thema's Helder en Hoog contrast blijven naast het donkere thema (donker standaard); skills met voorvoegsel `sbwebui-`; uitvoering stap voor stap.
- ~~Geen AI-beeldgeneratie (ADR-009)~~ **herzien 2026-10-18:** beeldgeneratie mag lokaal met Fooocus voor wie de beheerder het toestaat (ADR-029). Muziek: voorstel (ADR-030). Sandbox publiek voor iedereen (2026-10-10).

## Bekende valkuilen
- Windows-batchbestanden: `errorlevel` blijft staan na overgeslagen regels; gebruik vlagvariabelen. `.bat` en `.vbs` hebben CRLF nodig. `^&^&` in een bat breekt `python -m venv`.
- `set_setting()` moet de instellingencache per verzoek bijwerken, anders blijft een verlopen opdracht zichtbaar.
- Ouwe's `.env` nooit overschrijven; zips bevatten alleen `.env.example`.

## Niet getest (stand 2026-10-11)
- `start-tray.bat` op Windows, echt Discord en privékanaalgedrag, Strato met de nieuwste release, tray op Windows, tunnel-tempo op Ouwe's scherm.
- Er is nog geen baseline-meting van Open WebUI; "sneller" is dus een doel, geen meting.

## Voorgesteld, niet gebouwd
- ADR-024: RAG voor chats (bijlagen, kennisverzamelingen per assistent, Bibliotheek, eigen gesprekken, later de brain); embeddings `bge-m3` via Ollama, rechten vóór zoeken. Scope wacht op Ouwe.
- Stappenplan voor 2026-10-12 in `docs/stappenplan-2026-10-12.md` (repo SBwebui). Beeldgeneratie met Fooocus botst met ADR-009 (geen AI-beeldgeneratie): besluit van Ouwe nodig.

## Openstaande vragen
- Welke rollen mogen code uitvoeren en op welke host; Windows-pc of Linux-VPS; gastgebruik; sociale login-providers; vision-model. Zie de lijst in `docs/besluiten.md`.
