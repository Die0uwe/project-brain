---
project: project-brain
bijgewerkt: 2026-10-06
---
# De brain als kennisbron voor je lokale AI (Open WebUI)

> Stappenplan voor een werkdag, met controlepunten, testen en terugvallen. Uitgangspunt: Windows 11, Docker met Open WebUI, Ollama, qwen3:4b op een RTX 4060 met 4 GB VRAM, bereikbaar via Cloudflare Tunnel. Scripts: `tools/openwebui_sync.py`, `tools/openwebui_eval.py`, `tools/brain_sync.bat`.

## Wat je krijgt

- De brain (42 bestanden, circa 122 KB tekst, ruim 30.000 tokens) staat als collectie "DieOuwe Brain" in Open WebUI.
- Dat past niet in het contextvenster van een 4B-model. De AI haalt per vraag de 3 tot 5 relevante stukken op (RAG) en antwoordt daaruit.
- De sync uploadt alleen wat veranderd is, wacht tot Open WebUI het heeft verwerkt en ruimt oude versies op.
- Er gaan alleen `projects/`, `docs/`, `manifest/projects.yml`, `CONTEXT.md` en `index/llms.txt` mee. Niet: vertalingen (`i18n/`), de website, templates.

## Rolverdeling (BigBoss-routing)

| Rol (skill) | Taak in dit plan | Status |
|---|---|---|
| general-researcher | Open WebUI API en RAG-instellingen gecontroleerd tegen de upstream-broncode (`routers/knowledge.py`, `routers/files.py`) en de RAG-handleiding | klaar |
| code-architect | Ontwerp sync: staat per bestand (sha256), eerst toevoegen dan oude versie weghalen, hervatten na fout | klaar |
| cursebot-security | Sleutel alleen uit omgeving of `.env`, nooit als argument; geen http naar andere hosts; geen redirects met sleutel; `.gitignore` | klaar |
| wp-test-deployer (testaanpak) | Nep-Open WebUI met 33 tests: eerste run, geen wijziging, wijziging, verwijderen, handmatig weggehaald, mislukte verwerking, dubbele inhoud, verwijderde collectie, CRLF, 524, redirect | klaar |
| data-grinder | Welke bestanden mee mogen; geen dubbele inhoud in de set (gecontroleerd) | klaar |
| floor-manager | Dit stappenplan en de controlepunten | klaar |
| wow-brain-manager | Doc en scripts in de brain, index opnieuw gebouwd | klaar |
| Ouwe | Uitvoeren op de pc (blok 0 tot en met 6), eval-uitslag beoordelen | morgen |

Opmerking: dit zijn rollen die ik hier heb toegepast, geen 30 losse sessies. Een onafhankelijke review-agent heeft de scripts gelezen tegen de upstream-broncode; zijn bevindingen zijn verwerkt en met tests vastgelegd.

## Stappenplan (ongeveer 2 uur)

### Blok 0, voorcheck en back-up (15 min)

1. `python --version` geeft 3.9 of hoger, en `git --version` werkt. Zo niet: installeer Python van python.org (vink "Add to PATH" aan).
2. Open WebUI is bereikbaar op je tunneladres en lokaal. Noteer het lokale adres waarop je Open WebUI opent (bijvoorbeeld `http://localhost:3000`, controleer `docker ps` voor de poort).
3. Back-up van het Open WebUI-volume (controleer eerst de naam met `docker volume ls`, vaak `open-webui`):
   `docker run --rm -v open-webui:/data -v %cd%:/backup alpine tar czf /backup/openwebui-backup.tgz /data`
4. Controlepunt: back-up bestaat en is groter dan 0 bytes.

### Blok 1, embedding-model kiezen (20 min)

De brain is Nederlands. `nomic-embed-text` is vooral op Engels getraind; een meertalig model zoekt Nederlandse vragen beter.

1. Test eerst optie A: `ollama pull bge-m3` (meertalig, circa 1,2 GB).
2. Open WebUI, Admin-instellingen, Documenten:
   - Embedding Model Engine: Ollama, dezelfde URL als bij Verbindingen (bij Docker op Windows vaak `http://host.docker.internal:11434`).
   - Embedding Model: `bge-m3`.
   - Tekstsplitter: Token, chunkgrootte 1000, overlap 100 (advies uit de Open WebUI-handleiding voor modellen met 8K context of minder). Zet de Markdown-header-splitter aan als je versie die heeft.
   - Top K: 4. Hybride zoeken: voorlopig uit.
3. Doe dit vóór de eerste upload; een ander embedding-model later betekent opnieuw indexeren.
4. Contextlengte van je model (Werkruimte, Modellen, Geavanceerde parameters): 8192. Controleer na een vraag met `ollama ps` dat de kolom PROCESSOR "100% GPU" zegt. Staat er een CPU-deel bij, zet dan 4096 en Top K op 3.
5. Plan B als `bge-m3` niet past of traag is: het standaard CPU-model van Open WebUI (geen VRAM, zwakker in het Nederlands). Plan C: `nomic-embed-text`.

### Blok 2, API-sleutel en instellingen (15 min)

1. Open WebUI, Instellingen, Account, API-sleutels, nieuwe sleutel. Ontbreekt de sectie: Admin-instellingen, Algemeen, API-sleutels inschakelen.
2. Maak `%USERPROFILE%\.openwebui-brain.env` (Kladblok, opslaan als UTF-8), buiten de repo:
   ```
   OPENWEBUI_URL=http://localhost:3000
   OPENWEBUI_API_KEY=<jouw sleutel>
   OPENWEBUI_MODEL=<modelnaam zoals in Open WebUI>
   ```
   Gebruik voor de sync het lokale adres: dat omzeilt de Cloudflare-limiet van circa 100 seconden per verzoek en alle redirect-problemen. `http` mag alleen voor localhost; voor het tunneladres is `https` verplicht.
3. Maak het bestand niet met PowerShell `>` (dat geeft UTF-16); het script meldt dat en slaat zo'n bestand over.
4. De sleutel geeft toegang tot je hele account: behandel hem als een wachtwoord en verwijder hem in Open WebUI als je hem kwijt bent.

### Blok 3, eerste sync (15 min)

1. `git clone https://github.com/Die0uwe/project-brain C:\AI\project-brain`
2. `cd C:\AI\project-brain`
3. `python tools\openwebui_sync.py --status` (controleert URL en sleutel).
4. `python tools\openwebui_sync.py --dry-run` toont 42 bestanden als "new".
5. `python tools\openwebui_sync.py` doet het echt. Op een CPU-embedding duurt dit enkele minuten.
6. Controlepunt: Open WebUI, Werkruimte, Kennis, "DieOuwe Brain" bevat 42 bestanden; een tweede run meldt "alles is actueel".

### Blok 4, testen (20 min)

1. `python tools\openwebui_eval.py` stelt 8 vaste vragen met de collectie als bron, inclusief een vraag waarop het juiste antwoord "onbekend" is (anti-verzinsel).
2. Doel: 7 van 8 of beter. Let op de tijd per vraag: op 4 GB VRAM is alles boven ongeveer 60 seconden een teken dat het model deels op de CPU draait.
3. Handmatig in de chat: typ `#` en kies de collectie, of gebruik het model uit blok 5. Vraag bijvoorbeeld "Wat is er nieuw in Blueprint CMS 1.34.0?" en controleer of de bronnen onder het antwoord de juiste bestanden noemen.
4. Scoort `bge-m3` onder de 6 van 8: `python tools\openwebui_sync.py --reset`, wissel het embedding-model (plan B of C), draai de sync en de eval opnieuw. Noteer de scores per model.

### Blok 5, eigen model "Ouwe-Brain" (15 min)

1. Werkruimte, Modellen, nieuw model op basis van qwen3:4b (of je eigen Modelfile-model).
2. Kennis: kies "DieOuwe Brain". Een apart model voorkomt dat elke gewone chat langzamer wordt door het opzoeken.
3. Systeemprompt: "Je bent Ouwe's assistent. Beantwoord vragen over zijn projecten en WoW-addons uitsluitend op basis van de bijgevoegde bronnen. Staat iets er niet in of staat er 'onbekend', zeg dat dan. Verzin geen ID's, versies of paden. Antwoord kort in het Nederlands."

### Blok 6, automatisch bijwerken (15 min)

1. Open de Windows-taakplanner en maak een taak, dagelijks 09:00, actie: `C:\AI\project-brain\tools\brain_sync.bat`.
   Of in een opdrachtprompt: `schtasks /Create /SC DAILY /ST 09:00 /TN "Brain sync" /TR "C:\AI\project-brain\tools\brain_sync.bat"`.
2. Resultaat staat in `%USERPROFILE%\brain-sync.log`. Controleer na de eerste nacht of er "alles is actueel" of "Klaar." staat.
3. Controlepunt: bij een brain-wijziging op GitHub verschijnt de nieuwe versie de volgende dag in de collectie.

## Terugvallen

- Alles uit de collectie halen: `python tools\openwebui_sync.py --reset`.
- Open WebUI zelf terugzetten: pak de back-up uit blok 0 terug in het volume.
- De sync verandert niets aan je chats of modellen; hij beheert alleen de collectie "DieOuwe Brain".

## Problemen oplossen

| Melding of symptoom | Oorzaak | Oplossing |
|---|---|---|
| "controleer de API-sleutel" (401/403) | Sleutel fout, of API-sleutels staan uit | Blok 2 opnieuw; geen spaties of aanhalingstekens in het `.env`-bestand |
| "geen verbinding" | Container of tunnel staat uit, of verkeerde poort | `docker ps`; gebruik het lokale adres |
| "redirect ontvangen" | `http` naar `https`-omleiding, of Cloudflare Access voor `/api` | Gebruik de definitieve `https`-URL of het lokale adres |
| "antwoord is geen JSON" | URL wijst naar een loginpagina of tunnelfout | Controleer de URL in een browser |
| "kon het bestand niet verwerken" | Embedding-model niet gedownload of niet bereikbaar vanuit de container | `ollama list`; controleer de URL bij Documenten |
| HTTP 524 of time-out | Embedding op CPU duurt lang via de tunnel | Gebruik het lokale adres; de sync hervat waar hij bleef |
| "dubbele inhoud" | Twee bestanden met identieke tekst | Geen probleem, wordt onthouden en overgeslagen |
| Eval: antwoord klopt niet | Verkeerd embedding-model, Top K te laag, collectie niet gekoppeld | Blok 1 en 5; bekijk de bronnen onder het antwoord |
| Traag | Model of embedding valt terug op CPU | `ollama ps`; contextlengte omlaag; kleiner embedding-model |

## Let op

- De brain bevat samenvattingen van je privé-projecten. Gebruik deze collectie alleen voor jezelf. Koppel hem **niet** aan een publiek chat-endpoint (zoals het Blueprint-chatblok of de ScriptSpace-playground voor bezoekers): maak daarvoor een aparte collectie met alleen publieke inhoud.
- De API-eindpunten zijn gecontroleerd tegen de upstream-broncode van Open WebUI (oktober 2026). Draai je een oudere versie, dan werkt de sync nog (het statusendpoint is optioneel), maar draai eerst `--status` en `--dry-run`.
- Nieuwe feiten in de brain? Bouw de index (`python tools/build_index.py`) en push; de sync haalt ze de volgende ronde op.

## Verbeteringen voor daarna

1. ScriptSpace-playground laten antwoorden uit je collectie: de PHP-proxy stuurt `files: [{type: "collection", id: ...}]` mee naar `/api/chat/completions` (past bij je plan om Gemini en DeepSeek te vervangen).
2. Blueprint: een optionele collectie-ID in de Ollama-module, met een aparte publieke collectie (zie "Let op").
3. De eval uitbreiden naar 20 vragen en de scores per embedding-model bijhouden.
4. Hybride zoeken en een reranker, als de scores met alleen vectoren tegenvallen en er VRAM over is.
5. De tests van `tools/test_openwebui_sync.py` in de CI van de brain zetten (`brain-index.yml`); dat vraagt een token met de `workflow`-rechten, dus dat is jouw keuze.
