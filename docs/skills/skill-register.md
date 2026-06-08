# Skill Register — DieOuwe Ecosysteem
> Versie: 1.0.0 · Datum: 2026-06-08 · Beheerder: wow-personeelsbeleid

---

## Hiërarchie

```
DieOuwe (eigenaar)
    │
    ▼
wow-bigboss-orchestrator  (commandopost v2.0.0)
    │
    ├── OPLEIDING
    │       ├── learn
    │       └── skill-creator
    │
    ├── TECHNIEK  (via code-architect)
    │       ├── wow-addon-architect
    │       ├── wow-db-migrator
    │       ├── wow-dt-integrator
    │       ├── wow-test-framework
    │       ├── wow-poi-builder
    │       ├── wow-poi-auditor
    │       ├── poi-architect
    │       ├── wow-prey-research
    │       ├── discord-bot-architect
    │       ├── cursebot-security
    │       ├── wow-git-manager
    │       ├── wp-senior-dev
    │       └── wp-sa-suite
    │
    ├── DESIGN  (via design-architect)
    │       ├── wow-ui-polish
    │       └── frontend-design
    │
    ├── KENNISBANK
    │       ├── general-researcher
    │       ├── data-grinder
    │       ├── wow-oudedoos
    │       └── wow-brain-manager  ← NIEUW (v1.0.0)
    │
    └── PLATFORM
            ├── floor-manager
            ├── wow-session-closer
            ├── wow-changelog-manager
            └── wow-personeelsbeleid
```

---

## Volledig Skill Register

### Commandopost
| Skill | Versie | Status |
|---|---|---|
| wow-bigboss-orchestrator | v2.0.0 | ✅ Actief |

### Opleiding
| Skill | Versie | Status |
|---|---|---|
| learn | publiek | ✅ Actief |
| skill-creator | publiek | ✅ Actief |

### Techniek
| Skill | Versie | Status | Taak |
|---|---|---|---|
| code-architect | v1.0.0 | ✅ Actief | Technisch departementshoofd |
| wow-addon-architect | v1.x | ✅ Actief | WoW Lua bouwen |
| wow-db-migrator | v1.x | ✅ Actief | DB schema wijzigingen |
| wow-dt-integrator | v1.x | ✅ Actief | Plugin koppeling aan core |
| wow-test-framework | v1.x | ✅ Actief | In-game unit tests |
| wow-poi-builder | v1.x | ✅ Actief | Routing/waypoint code |
| wow-poi-auditor | v1.x | ✅ Actief | Locatie conflict detectie |
| poi-architect | v1.x | ✅ Actief | POI orchestrator |
| wow-prey-research | v1.x | ✅ Actief | Prey tracker research |
| discord-bot-architect | v1.x | ✅ Actief | CurseBot Python |
| cursebot-security | v1.0.0 | ✅ Actief | API key encryptie |
| wow-git-manager | v1.x | ✅ Actief | GitHub push |
| wp-senior-dev | v1.x | ✅ Actief | WordPress generiek |
| wp-sa-suite | v1.x | ✅ Actief | Slayer Alliance WP plugin |
| wow-inno-setup | v1.x | ✅ Actief | Windows .exe installer |

### Design
| Skill | Versie | Status | Taak |
|---|---|---|---|
| design-architect | v1.0.0 | ✅ Actief | Design departementshoofd |
| wow-ui-polish | v1.x | ✅ Actief | TOC/UI audit en polish |
| frontend-design | publiek | ✅ Actief | Web UI / HTML CSS |

### Kennisbank
| Skill | Versie | Status | Taak |
|---|---|---|---|
| general-researcher | v1.0.0 | ✅ Actief | Extern onderzoek |
| data-grinder | v1.0.0 | ✅ Actief | Data structureren en opslaan |
| wow-oudedoos | v1.x | ✅ Actief | Primaire WoW kennisbank |
| **wow-brain-manager** | **v1.0.0** | **✅ Actief** | **GitHub kennisbank beheer** |

### Platform
| Skill | Versie | Status | Taak |
|---|---|---|---|
| floor-manager | v1.0.0 | ✅ Actief | Sessie coördinatie |
| wow-session-closer | v1.x | ✅ Actief | Sessie afsluiten |
| wow-changelog-manager | v1.x | ✅ Actief | Changelog schrijven |
| wow-personeelsbeleid | v1.0.0 | ✅ Actief | Organisatiestructuur |

---

## Routing Matrix — Snel Naslagwerk

| Zeg je... | Skill die triggert |
|---|---|
| "push naar github" | wow-git-manager |
| "update kennisbank" | wow-brain-manager |
| "push docs naar github" | wow-brain-manager |
| "sla dit op in de kennisbank" | data-grinder → wow-brain-manager |
| "wat staat er in de oudedoos" | wow-oudedoos |
| "maak een nieuwe skill" | skill-creator (via BigBoss) |
| "sessie afsluiten" | wow-session-closer |
| "welke skills zijn er" | wow-personeelsbeleid |

---

## Wijzigingslog

| Datum | Wijziging |
|---|---|
| 2026-06-08 | Initieel register aangemaakt |
| 2026-06-08 | wow-brain-manager toegevoegd als nieuwe skill |
