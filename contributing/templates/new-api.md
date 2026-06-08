# Template — API Bevinding Bijdrage

> Gebruik dit template voor Blizzard API gedrag, nieuwe calls, deprecated functies
> Doelbestanden: `docs/api/blizzard-api-reference.md` · `docs/api/deprecated-calls.md`

---

## Nieuwe werkende API call

Voeg toe aan `docs/api/blizzard-api-reference.md`:

```markdown
| `C_Namespace.FunctionName(args)` | [Wat het doet] | [Return type/waarde] | [VERIFIED/PROBABLE] | [Bron] |
```

### Uitgebreid voorbeeld (voor complexe calls):

```markdown
#### `C_QuestLog.GetActivePreyQuest()`

**Beschrijving**: Geeft de actieve prey quest ID terug voor de huidige zone.

**Parameters**: Geen

**Return**: `questID` (number) of `nil` als geen actieve prey quest

**Gebruik**:
```lua
local questID = C_QuestLog.GetActivePreyQuest()
if questID then
    -- prey is actief
end
```

**Events die dit triggeren**: `QUEST_ACCEPTED`, `QUEST_REMOVED`

**Status**: VERIFIED · Build 12.0.5.67314
**Bron**: [bron / eigen test / wowhead]
```

---

## Deprecated call melden

Voeg toe aan `docs/api/deprecated-calls.md`:

```markdown
| `OudeFunctie(args)` | DEPRECATED | `NieuweVervanger(args)` | [Versie deprecated] |
```

Voorbeeld:
```markdown
| `GetAuraData(unit, i)` | DEPRECATED | `C_UnitAuras.GetAuraDataByIndex(unit, i, filter)` | 11.0+ |
```

---

## Event documentatie

Voeg toe aan `docs/api/events-reference.md`:

```markdown
| `EVENT_NAME` | [Wanneer het vuurt] | [Payload argumenten] | [Status] | [Bron] |
```

Voorbeeld:
```markdown
| `PLAYER_PREY_UPDATED` | Wanneer prey target wijzigt | `unitGUID, questID` | PROBABLE | wowdev wiki |
```

---

## Checklist voor je PR

- [ ] Call zelf getest in-game (of `UNVERIFIED` als niet getest)
- [ ] WoW build vermeld (bijv. `12.0.5.67314`)
- [ ] Juist doelbestand gekozen
- [ ] Voor deprecated calls: vervanging vermeld of `[No replacement]`
- [ ] Branch naam: `docs/api-[functienaam]`

---

## Bronnen die we accepteren

| Bron | Betrouwbaarheid |
|---|---|
| Eigen in-game test | VERIFIED |
| wowdev.wiki | VERIFIED |
| wowhead.com | PROBABLE |
| GitHub wowdev community | PROBABLE |
| Reddit r/wowdev | PROBABLE |
| Speculatie | UNVERIFIED — altijd labelen |
