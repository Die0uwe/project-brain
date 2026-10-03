---
id: panicroom
type: repo
bijgewerkt: 2026-10-03
bron_repo: Die0uwe/panicroom
---
# PanicRoom CMS

## Doel
Hardware-check voor Windows-pc's: een lokale scan-tool schrijft een JSON-bestand, een dashboard toont overzicht, prestaties-momentopname en updatecontrole met advies. Er wordt nooit automatisch iets gedownload of geïnstalleerd. Repo is **privé**.

## Stack
- Scan-tool: Python 3.9+ (alleen standaardbibliotheek), PowerShell/CIM, optioneel winget; geen adminrechten, geen serienummers, MAC-adressen, gebruikersnamen, computernaam of IP-adressen in de uitvoer.
- Dashboard: statische `web/index.html` (Tailwind via CDN), alles lokaal in de browser.
- Gepland (Fase 2 en 3): Vercel Hobby, Supabase Free, AI-uitleg via Gemini of Groq. Alleen gratis diensten.

## Versie en status
- Scanner v0.2.0 (CHANGELOG 2026-10-03), nog niet getagd; wacht op test op een echte Windows-pc (Fase 1C). PowerShell-deel is tot nu toe alleen getest met nagebootste uitvoer.
- JSON-schema 1.1 (1.0 blijft geldig). Merge van PR #1 (`fase1b-scanner-v0.2`) op main.

## Structuur
`tool/panicroom_scan.py`, `schema/scan_schema.json`, `tests/test_scan.py` (13 tests), `web/index.html`, `docs/` (FASE1_ARCHITECTUUR, WERKBESPREKING, PLAN_VAN_AANPAK), `CHANGELOG.md`.

## Build, test, deploy
- Scan: `python tool/panicroom_scan.py --print` (en `--updates` voor wachtende Windows- en app-updates).
- Tests: `pip install jsonschema` en `python -m unittest discover -s tests -v`.
- Deploy: nog niet ingericht (Fase 2).

## Belangrijke beslissingen
- Gebruiker uploadt scanresultaten zelf; er is geen automatische verzending.
- Fabriekslinks alleen via `https` en alleen van een lijst met officiële domeinen.
- API-sleutels (Gemini/Groq) alleen in environment variables, nooit in de repo.

## Openstaande punten
- Test op echte hardware, daarna tag v0.2.0.
- Open besluiten uit de werkbespreking: frontend-framework (statisch of Next.js), anoniem scannen zonder opslag tegenover opslag met account, en de eerste lijst met fabrikantdomeinen.
- De nieuwste BIOS- of driverversie is niet uit de pc te halen; dat hoort bij de kennisbank in Fase 2 en 3.
