# Template — Nieuwe taal toevoegen

> Wil je een volledig nieuwe taal toevoegen aan de kennisbank?

---

## Stap 1 — Taalcode kiezen

Gebruik de [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) code (2 letters):

| Taal | Code | Map |
|---|---|---|
| Nederlands | `nl` | `i18n/nl/` |
| English | `en` | `i18n/en/` |
| Deutsch | `de` | `i18n/de/` |
| Français | `fr` | `i18n/fr/` |
| Español | `es` | `i18n/es/` |
| Português | `pt` | `i18n/pt/` |
| 中文 | `zh` | `i18n/zh/` |
| 한국어 | `ko` | `i18n/ko/` |
| Русский | `ru` | `i18n/ru/` |

---

## Stap 2 — Mapstructuur aanmaken

```bash
mkdir -p i18n/[code]/knowledge
mkdir -p i18n/[code]/api
mkdir -p i18n/[code]/tokens-and-keys
```

---

## Stap 3 — README aanmaken

Maak `i18n/[code]/README.md` aan. Kopieer de structuur hieronder:

```markdown
# Project Brain — [Taal naam]

> Vertaling van de DieOuwe Ecosysteem kennisbank

## Beschikbare vertalingen

| Document | Status |
|---|---|
| [known-bugs.md](knowledge/known-bugs.md) | ✅ Vertaald |
| [compass-math.md](knowledge/compass-math.md) | 🔄 In progress |
| [deprecated-calls.md](api/deprecated-calls.md) | ❌ Nog te doen |

## Bijdragen aan deze vertaling

Zie [CONTRIBUTING.md](../../CONTRIBUTING.md) voor de spelregels.
Open een PR of Issue als je wilt helpen.

## Vertalers

| Naam / Handle | Documenten |
|---|---|
| [jouw naam] | [welke docs] |
```

---

## Stap 4 — Minimale startset

Begin met tenminste deze 3 documenten:

1. `i18n/[code]/README.md` (verplicht)
2. `i18n/[code]/knowledge/known-bugs.md` (meest gebruikt)
3. `i18n/[code]/api/deprecated-calls.md` (meest gebruikt)

Meer toevoegen kan altijd via latere PRs.

---

## Stap 5 — CONTRIBUTING.md updaten

Voeg je taal toe aan de taalregel bovenin `CONTRIBUTING.md`:

```markdown
**Talen:** [🇳🇱 Nederlands](i18n/nl/CONTRIBUTING.md) · [🇬🇧 English](i18n/en/CONTRIBUTING.md) · [🇩🇪 Deutsch](i18n/de/CONTRIBUTING.md) · [🇫🇷 Français](i18n/fr/CONTRIBUTING.md) · [🏳️ Jouw taal](i18n/[code]/CONTRIBUTING.md)
```

---

## Checklist voor je PR

- [ ] `i18n/[code]/README.md` aanwezig
- [ ] Minimaal 2 vertaalde documenten
- [ ] CONTRIBUTING.md talenrij bijgewerkt
- [ ] Geen API calls of code vertaald
- [ ] Branch naam: `i18n/new-[taalcode]`
