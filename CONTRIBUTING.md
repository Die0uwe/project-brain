<!-- ============================================================
     Project Brain — DieOuwe Ecosysteem Kennisbank
     © 2026 DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     Licentie: CC BY-SA 4.0 — Vrij te delen met bronvermelding
     ============================================================ -->

# Contributing to Project Brain

> DieOuwe Ecosysteem · WoW Retail 12.0.5 Midnight · github.com/Die0uwe/project-brain

Welkom! Dit is de kennisbank van het DieOuwe ecosysteem. Iedereen kan bijdragen —
van geverifieerde WoW IDs tot bugfixes, van API-documentatie tot vertalingen.

**Talen / Languages:** [🇳🇱 Nederlands](i18n/nl/CONTRIBUTING.md) · [🇬🇧 English](i18n/en/CONTRIBUTING.md) · [🇩🇪 Deutsch](i18n/de/CONTRIBUTING.md) · [🇫🇷 Français](i18n/fr/CONTRIBUTING.md)

---

## Hoe bijdragen?

### Optie A — Fork & Pull Request (aanbevolen)

```
1. Fork dit repo (knop rechtsboven op GitHub)
2. Maak een branch: git checkout -b add/mijn-bijdrage
3. Voeg je data toe via een van de templates hieronder
4. Commit: git commit -m "docs: add [wat je toevoegt]"
5. Open een Pull Request naar main
```

### Optie B — GitHub Issue

Weet je de data maar wil je niet zelf een PR maken?
Maak een [Issue aan](../../issues/new/choose) met het juiste template.

### Optie C — Discord

Deel je bevinding in de Slayer Alliance Discord: [discord.gg/y8Pu5qsEbQ](https://discord.gg/y8Pu5qsEbQ)
Een van de maintainers verwerkt het dan.

---

## Wat kun je bijdragen?

| Type | Bestand | Template |
|---|---|---|
| WoW Map/Zone IDs | `docs/knowledge/maps-and-zones.md` | [template](contributing/templates/new-id.md) |
| Quest IDs / NPC data | `docs/knowledge/prey-database.md` | [template](contributing/templates/new-id.md) |
| Currency IDs | `docs/knowledge/currencies-and-rewards.md` | [template](contributing/templates/new-id.md) |
| Spell IDs / Aura's | `docs/knowledge/spells-and-auras.md` | [template](contributing/templates/new-id.md) |
| Bug + workaround | `docs/knowledge/known-bugs.md` | [template](contributing/templates/new-bug.md) |
| API bevinding | `docs/api/blizzard-api-reference.md` | [template](contributing/templates/new-api.md) |
| Vertaling | `i18n/[taalcode]/` | [template](contributing/templates/new-translation.md) |
| Nieuwe taal | Maak `i18n/[taalcode]/` aan | [template](contributing/templates/new-language.md) |

---

## Regels

**✅ Wél bijdragen:**
- Geverifieerde IDs met bronvermelding
- Bugs die je zelf hebt gereproduceerd
- Vertalingen van bestaande documenten
- Correcties op bestaande data

**❌ Nooit bijdragen:**
- API keys, tokens, of wachtwoorden
- Datamined data die Blizzard's ToS schendt
- Speculatieve data zonder bron (gebruik dan `UNVERIFIED`)
- Code (code hoort in de addon repos, niet hier)

---

## Betrouwbaarheidslabels

Elke entry krijgt een label. Wees eerlijk:

| Label | Betekenis |
|---|---|
| `VERIFIED` | Meerdere bronnen, zelf getest of officieel gedocumenteerd |
| `PROBABLE` | Één betrouwbare bron, logisch consistent |
| `UNVERIFIED` | Niet getest — community check gewenst |
| `DEPRECATED` | Was correct, nu verouderd |

---

## Review proces

Pull Requests worden gereviewd door de maintainers (DieOuwe team).
Gemiddelde reactietijd: 1–3 dagen.

Bij vragen: open een Issue of kom langs op [Discord](https://discord.gg/y8Pu5qsEbQ).

<!-- ============================================================
     File    : CONTRIBUTING.md
     Version : 1.0.0  Created: 2026-06-08  Updated: 2026-06-08
     Status  : New
     DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     ============================================================ -->
