# Template — Vertaling toevoegen

> Gebruik dit als je een bestaand document wilt vertalen naar een andere taal.

---

## Stap 1 — Bestaande vertalingen controleren

Check welke vertalingen al bestaan:

```
i18n/
├── nl/    ← Nederlands (basis — altijd aanwezig)
├── en/    ← English
├── de/    ← Deutsch
├── fr/    ← Français
└── [jouw taalcode]/
```

Bekijk `i18n/[taalcode]/` — staat het document er al? Dan is aanvullen beter dan opnieuw aanmaken.

---

## Stap 2 — Bestand aanmaken

Spiegel de structuur van `docs/` maar dan in `i18n/[taalcode]/`:

```
docs/knowledge/known-bugs.md
→ i18n/en/knowledge/known-bugs.md

docs/api/deprecated-calls.md  
→ i18n/en/api/deprecated-calls.md
```

---

## Stap 3 — Vertaalregels

**Wat je vertaalt:**
- Alle uitleg, beschrijvingen, en toelichting
- Kolom headers in tabellen
- Sectienames en koppen

**Wat je NIET vertaalt:**
- WoW API functienamen: `C_CurrencyInfo.GetCurrencyInfo()` blijft zo
- Lua code: code blijft ongewijzigd
- WoW-specifieke termen: "mapID", "questID", "taint", "InCombatLockdown" blijven zo
- Namen van addons: "DelveTracker", "CurseBot" blijven zo
- GitHub usernames en Discord handles

---

## Stap 4 — Koptekst toevoegen

Elke vertaling begint met:

```markdown
> 🌐 Vertaling van [`docs/[pad/naar/origineel.md`](../../docs/[pad/naar/origineel.md])
> Taal: [Taal naam] · Vertaald door: [jouw naam/handle] · Datum: [YYYY-MM-DD]
> ⚠️ Bij twijfel: raadpleeg altijd het [originele document](../../docs/[pad]).
```

---

## Stap 5 — i18n README bijwerken

Voeg je vertaling toe aan `i18n/[taalcode]/README.md`.
Als die niet bestaat, kopieer dan `i18n/en/README.md` als basis.

---

## Checklist voor je PR

- [ ] Koptekst aanwezig met link naar origineel
- [ ] API calls en code NIET vertaald
- [ ] WoW termen NIET vertaald
- [ ] `i18n/[taalcode]/README.md` bijgewerkt
- [ ] Branch naam: `i18n/[taalcode]-[documentnaam]`

---

## Nieuwe taal toevoegen?

Zie [contributing/templates/new-language.md](new-language.md)
