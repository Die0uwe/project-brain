# Template — Bug & Workaround Bijdrage

> Gebruik dit template voor bekende bugs, crashes, taint issues, en workarounds
> Doelbestand: `docs/knowledge/known-bugs.md`

---

## Tabel formaat

Kopieer de rij die past en plak in de juiste sectie van `known-bugs.md`:

```markdown
| [Korte bug beschrijving] | [Symptoom] | [Workaround / Fix] | [Versie] |
```

---

## Secties in known-bugs.md

Kies de juiste sectie:

| Sectie | Gebruik voor |
|---|---|
| **Kritieke Crashes** | Addon laadt niet, game crasht, stille fouten |
| **API Deprecated Calls** | Functies die niet meer werken |
| **Taint Issues** | Secure frame interferentie, combat lockdown |
| **Frame / UI Bugs** | Visuele glitches, frame positionering |
| **CurseBot (Python)** | Discord bot, Python errors |
| **WordPress (Slayer Alliance)** | Plugin errors, PHP bugs |

---

## Voorbeeld invoer

```markdown
### Kritieke Crashes

| `SomeOldTemplate` | Stille crash bij laden | Vervang door `NewTemplate` | 12.0.x |
```

---

## Uitgebreid formaat (voor complexe bugs)

Als een tabelrij te weinig ruimte biedt:

```markdown
#### [Bug naam] — [Versie]

**Symptoom**: [Wat ziet de gebruiker / wat gaat er mis]

**Oorzaak**: [Waarom gebeurt dit — optioneel als onbekend]

**Reproductie**:
1. [Stap 1]
2. [Stap 2]
3. [Bug treedt op]

**Fix / Workaround**:
```lua
-- Oud (kapot):
oud_patroon()

-- Nieuw (werkt):
nieuw_patroon()
```

**Status**: VERIFIED / PROBABLE / UNVERIFIED
**Bron**: [jouw naam of Discord handle, datum]
```

---

## Checklist voor je PR

- [ ] Bug zelf gereproduceerd (of duidelijk als `UNVERIFIED` gemarkeerd)
- [ ] WoW versie vermeld (bijv. `12.0.5` of `12.0.x`)
- [ ] Workaround aanwezig of `[No fix known]`
- [ ] Juiste sectie gekozen
- [ ] Branch naam: `fix/bug-[korte beschrijving]`

---

## Wat we NIET willen

- Speculaties zonder reproductie (markeer als `UNVERIFIED` als je twijfelt)
- Bugs uit oude expansions zonder versie-annotatie
- Duplicaten — check eerst of de bug al staat
