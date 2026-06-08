# 🧠 DieOuwe Project Brain

> Centrale kennisbank voor het DieOuwe ecosysteem — WoW Addons, CurseBot, Slayer Alliance WordPress

---

## Wat is dit?

Dit repo bevat **geen code**. Het is de levende kennisbank die alle andere repos voedt.
Claude leest dit als eerste stap van elke sessie. Developers gebruiken het als naslagwerk.

## Structuur

```
project-brain/
├── CONTEXT.md                      ← AI-sessie instructies (lees dit eerst)
├── docs/
│   ├── knowledge/                  ← Geverifieerde WoW data
│   │   ├── maps-and-zones.md       ← MapIDs, zone coördinaten, portalen
│   │   ├── currencies-and-rewards.md
│   │   ├── prey-database.md        ← Quest IDs, NPC data
│   │   ├── spells-and-auras.md
│   │   ├── known-bugs.md
│   │   ├── compass-math.md         ← De heilige kompassformule
│   │   └── session-history.md      ← Sessie-lessen
│   ├── api/
│   │   ├── blizzard-api-reference.md
│   │   ├── deprecated-calls.md     ← Verboden APIs
│   │   └── events-reference.md
│   ├── tokens-and-keys/            ← HOE je tokens verkrijgt (geen echte tokens!)
│   │   ├── github-pat.md
│   │   ├── curseforge-api-key.md
│   │   ├── discord-bot-token.md
│   │   └── blizzard-oauth.md
│   └── skills/
│       └── skill-register.md       ← Alle skills + routing
└── .github/
    └── workflows/
        └── validate.yml            ← Lint check op markdown
```

## Bijdragen

Alleen `data-grinder` en `wow-brain-manager` schrijven naar dit repo.
Handmatige updates altijd via PR op de `dev` branch.

**Nooit in dit repo:**
- API keys, tokens, of passwords
- Ruwe sessie-transcripten
- Persoonlijke of gevoelige data

---

*Build target: WoW Retail 12.0.5.67314 (Midnight) · Interface 120005*
*Created by DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ*
