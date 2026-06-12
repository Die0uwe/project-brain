<!-- ============================================================
     Project Brain — DieOuwe Ecosysteem Kennisbank
     © 2026 DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     Licentie: CC BY-SA 4.0 — Vrij te delen met bronvermelding
     ============================================================ -->

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

<!-- ============================================================
     File    : docs/knowledge/session-history.md
     Version : 1.0.0  Created: 2026-06-08  Updated: 2026-06-08
     Status  : New
     DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     ============================================================ -->

## Sessie 2026-06-12 (v3.0.9→v3.1.9)
- Regressie hersteld: race-systeem, admin panel, warband stats herbouwd
- Fase 1+2 stappenplan compleet · 22 plugins geregistreerd
- Nieuwe lessen: SavedVariables init-timing, ipairs-nil valkuil,
  GetGuildRosterMOTD protected, frames-zijn-tables Hide-loop
- Midnight security model gedocumenteerd (zie midnight-security-model.md)
- Race icons definitief (zie race-icons-definitief.md)
