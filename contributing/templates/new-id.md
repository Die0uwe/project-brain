# Template — Nieuwe ID Bijdrage

> Gebruik dit template voor: mapIDs, questIDs, currencyIDs, spellIDs, itemIDs, NPC IDs

Kopieer het blok hieronder en plak het in het juiste bestand onder `docs/knowledge/`.

---

## Hoe te gebruiken

1. Kopieer de tabel-rij die past bij jouw bijdrage
2. Vul alle kolommen in — laat niets leeg (gebruik `?` als je iets niet weet)
3. Voeg `UNVERIFIED` toe als je het niet 100% zeker weet
4. Vermeld altijd een bron (wowhead link, eigen test, patch notes, etc.)

---

## Tabel formaten per bestand

### `docs/knowledge/currencies-and-rewards.md`

```markdown
| [Naam van de currency] | [ID nummer] | [VERIFIED/PROBABLE/UNVERIFIED] | [bron: wowhead/eigen test/etc] |
```

Voorbeeld:
```markdown
| Dawncrest Shard | 3391 | UNVERIFIED | wowhead.com/currency=3391 |
```

---

### `docs/knowledge/maps-and-zones.md`

```markdown
| [Zone naam] | [mapID] | [uiMapID] | [Type: Zone/Dungeon/Raid/etc] | [Status] | [Bron] |
```

Voorbeeld:
```markdown
| Dawncrest City | 2420 | 2420 | Zone | VERIFIED | wowhead.com/zone=2420 |
```

---

### `docs/knowledge/prey-database.md`

```markdown
| [NPC naam] | [NPC ID] | [Quest ID] | [Zone] | [mapID] | [Coördinaten X,Y] | [Status] | [Bron] |
```

Voorbeeld:
```markdown
| Shadowmane Alpha | 224819 | 91102 | Dawncrest | 2420 | 48.2, 31.7 | VERIFIED | eigen test 2026-06 |
```

---

### `docs/knowledge/spells-and-auras.md`

```markdown
| [Spell naam] | [Spell ID] | [Type: Buff/Debuff/Active/Passive] | [Bron unit/item] | [Status] | [Bron] |
```

Voorbeeld:
```markdown
| Dawncrest Blessing | 445821 | Buff | Zone aura | PROBABLE | wowhead.com/spell=445821 |
```

---

## Checklist voor je PR

- [ ] Correct bestand gekozen
- [ ] Tabelformat klopt (pipes uitgelijnd is leuk maar niet verplicht)
- [ ] Betrouwbaarheidslabel ingevuld
- [ ] Bron vermeld
- [ ] Geen echte tokens of keys in je bijdrage
- [ ] Branch naam: `add/[type]-[omschrijving]` bijv. `add/currency-dawncrest-shard`

---

## Build target

Deze kennisbank geldt voor: **WoW Retail 12.0.5.67314 (Midnight) · Interface 120005**

Voeg IDs van oudere patches toe met een duidelijke versie-annotatie:
```markdown
| [naam] | [ID] | DEPRECATED | Was actief in 11.x, verwijderd in Midnight |
```
