# DieOuwe Project Brain 🧠

> Centrale kennisbank voor het DieOuwe ecosysteem
> **Lees CONTEXT.md als eerste** voor AI-sessie context

---

## Wat is dit?

Project Brain is de levende kennisbank die alle Claude-sessies, developers en
community-bijdragers voedt. Alle geverifieerde data, API-referenties, lessen
uit debugging sessies en design beslissingen staan hier centraal.

---

## Projecten

| Project | Tech | Status |
|---|---|---|
| **WowTracker** (+ i18n, Themes; v3.5.5) | Lua / WoW Retail 12.0.5 Midnight | Actief |
| **DelveTracker** (oudere repo) | Lua / WoW Retail 12.0.5 Midnight | Verouderd |
| **CurseBot** | Python 3.11+ / Discord | Actief |
| **Slayer Alliance Plugin** | PHP / WordPress | Actief |
| **ScriptSpace CMS** | PHP 8.x / MySQL | In ontwikkeling |
| **Blueprint CMS** | PHP 8.3 / MariaDB | Actief |
| **PanicRoom CMS** | Python / PowerShell / HTML | In ontwikkeling |
| **famfinder (SpotFam)** | Android / Kotlin | In ontwikkeling |

Alle projecten (ook sites, CMS'en en AI's) staan in het [manifest](manifest/projects.yml).

---

## Snel Navigeren

- **[CONTEXT.md](CONTEXT.md)** — AI sessie-instructies + navigatietabel
- **[docs/knowledge/](docs/knowledge/)** — WoW data, IDs, bugs, sessie-lessen
- **[docs/api/](docs/api/)** — Blizzard API calls, deprecated functies
- **[docs/tokens-and-keys/](docs/tokens-and-keys/)** — HOE je tokens aanmaakt (NOOIT echte waarden)
- **[docs/skills/](docs/skills/)** — Skill register, organisatiestructuur

---

## Project-brain als AI-kennisbank

Naast de WoW-kennis is deze repo ook de centrale RAG-bron die alle repositories, websites, addons, tools en AI's met elkaar verbindt.

- **[manifest/projects.yml](manifest/projects.yml)**: een entry per project met type, status, stack, versie, relaties en bronpaden
- **[projects/](projects/)**: korte projectkaarten (doel, stack, build/test/deploy, openstaande punten); wat niet geverifieerd is staat als `onbekend`
- **[docs/RAG-ARCHITECTURE.md](docs/RAG-ARCHITECTURE.md)**: chunking, indexformaat, hoe agents het gebruiken, update-flow en veiligheidsregels
- **[index/](index/)**: gegenereerd met `python3 tools/build_index.py` (`brain.jsonl` voor embedding, `llms.txt` als kaart voor agents); tests: `python3 tools/test_build_index.py`

---

## Bijdragen

Zie [CONTRIBUTING.md](CONTRIBUTING.md) voor richtlijnen.

**NOOIT** echte tokens, API keys of wachtwoorden committen.

---

## Live Viewer

Beschikbaar op: **[die0uwe.github.io/project-brain](https://die0uwe.github.io/project-brain/)**

---

*Beheerd door DieOuwe · wow-brain-manager · data-grinder*
