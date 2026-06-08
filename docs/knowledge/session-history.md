# Sessie Geschiedenis & Lessen
> Beheerder: data-grinder · Elke sessie voegt een entry toe

---

## Format

```
### [DATUM] — [Onderwerp]
**Sessie doel**: [wat wilde je bereiken]
**Wat geleerd**: [nieuwe inzichten, API bevindingen]
**Beslissingen**: [architectuur of structuurkeuzes]
**Nieuwe IDs**: [eventuele nieuwe mapIDs / questIDs / etc.]
**Openstaand**: [wat nog op te lossen]
```

---

### 2026-06-08 — GitHub Project Brain Architectuur

**Sessie doel**: GitHub structuur opzetten voor het volledige DieOuwe ecosysteem, kennisbank op GitHub zetten, nieuwe wow-brain-manager skill aanmaken.

**Beslissingen**:
- Vier repos: `DelveTracker`, `cursebot`, `slayeralliance-wp`, `project-brain`
- `project-brain` is de centrale kennisbank — geen code, alleen docs
- `CONTEXT.md` in root van elke repo voor Claude-sessie instructies
- Branch strategie: `main` (stabiel) → `dev` (dagelijks) → `feature/xxx`
- Tokens/keys nooit opslaan — alleen HOE je ze verkrijgt documenteren
- `wow-brain-manager` skill aangemaakt als nieuwe Kennisbank skill (v1.0.0)
- Afdeling: Kennisbank, rapporteert aan BigBoss

**Nieuwe skills**: wow-brain-manager v1.0.0

**Openstaand**:
- Blizzard OAuth flow documenteren (`docs/tokens-and-keys/blizzard-oauth.md`)
- `maps-and-zones.md` aanvullen met alle Midnight mapIDs
- `prey-database.md` aanmaken met questID range 91095–91400
- GitHub Actions `validate.yml` activeren
- wow-personeelsbeleid updaten met wow-brain-manager entry

---

*Voeg nieuwe sessies toe bovenaan (nieuwste eerst)*
