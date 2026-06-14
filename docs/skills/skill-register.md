# Skill Register — DieOuwe Ecosysteem
> Volledig overzicht van alle actieve skills · Laatste update: 2026-06-14

---

## Organisatiestructuur

```
DieOuwe (eigenaar)
    │
    ▼
wow-bigboss-orchestrator  ← commandopost (v2.1.0)
    │
    ├── OPLEIDING
    │       ├── learn
    │       └── skill-creator
    │
    ├── TECHNIEK (via code-architect)
    │       ├── WoW Addon
    │       │   ├── wow-addon-architect       ← total builder
    │       │   ├── wow-db-migrator           ← SavedVariables migraties
    │       │   ├── wow-dt-integrator         ← plugin naar core koppelen
    │       │   ├── wow-test-framework        ← in-game unit tests
    │       │   ├── wow-poi-builder           ← routing en waypoints
    │       │   ├── wow-poi-auditor           ← data conflict detectie
    │       │   ├── poi-architect             ← orchestrator voor POI
    │       │   ├── wow-prey-research         ← prey hunt systemen
    │       │   └── wow-i18n-specialist       ← lokalisatie/talen
    │       │
    │       ├── CurseBot / Discord
    │       │   ├── discord-bot-architect     ← Python Discord bot
    │       │   ├── cursebot-security         ← API key encryptie
    │       │   └── wow-inno-setup            ← Windows installer (.iss)
    │       │
    │       └── WordPress
    │           ├── wp-senior-dev             ← generiek WP dev
    │           └── wp-sa-suite               ← Slayer Alliance plugin
    │
    ├── DESIGN (via design-architect)
    │       ├── wow-ui-polish                 ← TOC, minimap, file cards
    │       ├── wow-theme-artist              ← WTTheme systeem, kleuren
    │       ├── wow-character-avatars         ← avatar sheet processor
    │       └── frontend-design              ← web UI/CSS
    │
    ├── KENNISBANK
    │       ├── general-researcher            ← web research
    │       ├── data-grinder                  ← structureren/opslaan
    │       ├── wow-oudedoos                  ← primaire kennisbank
    │       └── wow-brain-manager             ← GitHub kennisbank beheer
    │
    └── PLATFORM (gedeeld)
            ├── floor-manager                 ← dagelijkse coördinatie
            ├── wow-session-closer            ← sessie afsluiten
            ├── wow-changelog-manager         ← changelog schrijven
            ├── wow-personeelsbeleid          ← HR/org structuur
            └── wow-git-manager              ← GitHub push manager
```

---

## Skill Tabel — Volledig

| Skill | Versie | Afdeling | Status |
|---|---|---|---|
| wow-bigboss-orchestrator | v2.1.0 | Commandopost | ✅ Actief |
| floor-manager | v1.1.0 | Platform | ✅ Actief |
| wow-session-closer | v1.x | Platform | ✅ Actief |
| wow-changelog-manager | v1.x | Platform | ✅ Actief |
| wow-personeelsbeleid | v1.1.0 | Platform | ✅ Actief |
| wow-git-manager | v1.x | Platform/Techniek | ✅ Actief |
| wow-brain-manager | v1.0.0 | Kennisbank | ✅ Actief |
| learn | v1.x | Opleiding | ✅ Actief |
| skill-creator | v1.x | Opleiding | ✅ Actief |
| code-architect | v1.x | Techniek | ✅ Actief |
| wow-addon-architect | v1.x | Techniek/WoW | ✅ Actief |
| wow-db-migrator | v1.x | Techniek/WoW | ✅ Actief |
| wow-dt-integrator | v1.x | Techniek/WoW | ✅ Actief |
| wow-test-framework | v1.x | Techniek/WoW | ✅ Actief |
| wow-poi-builder | v1.x | Techniek/WoW | ✅ Actief |
| wow-poi-auditor | v1.x | Techniek/WoW | ✅ Actief |
| poi-architect | v1.x | Techniek/WoW | ✅ Actief |
| wow-prey-research | v1.x | Techniek/WoW | ✅ Actief |
| wow-i18n-specialist | v1.x | Techniek/WoW | ✅ Actief |
| discord-bot-architect | v1.x | Techniek/CurseBot | ✅ Actief |
| cursebot-security | v1.x | Techniek/CurseBot | ✅ Actief |
| wow-inno-setup | v1.x | Techniek/CurseBot | ✅ Actief |
| wp-senior-dev | v1.x | Techniek/WP | ✅ Actief |
| wp-sa-suite | v1.x | Techniek/WP | ✅ Actief |
| design-architect | v1.x | Design | ✅ Actief |
| wow-ui-polish | v1.x | Design | ✅ Actief |
| wow-theme-artist | v1.x | Design | ✅ Actief |
| wow-character-avatars | v1.x | Design | ✅ Actief |
| frontend-design | v1.x | Design | ✅ Actief |
| general-researcher | v1.x | Kennisbank | ✅ Actief |
| data-grinder | v1.x | Kennisbank | ✅ Actief |
| wow-oudedoos | v1.x | Kennisbank | ✅ Actief |

**Totaal: 32 actieve skills**

---

## Routing Beslisboom

```
Nieuwe taak binnenkomt
    │
    ├── Strategisch/multi-project  → wow-bigboss-orchestrator
    ├── Coördinatie/dagelijks      → floor-manager
    ├── WoW Lua code               → code-architect → wow-addon-architect
    ├── Python/bot                 → code-architect → discord-bot-architect
    ├── WordPress/PHP              → code-architect → wp-sa-suite
    ├── GitHub push                → wow-git-manager
    ├── Kennisbank update GitHub   → wow-brain-manager
    ├── Data/IDs opzoeken          → wow-oudedoos (ALTIJD EERST)
    ├── Visueel/UI                 → design-architect → wow-ui-polish
    ├── Sessie afsluiten           → wow-session-closer
    └── Skill wijzigen             → wow-personeelsbeleid → skill-creator
```

---

*Beheerd door wow-personeelsbeleid + wow-brain-manager*
*Rapporteert aan: wow-bigboss-orchestrator*
