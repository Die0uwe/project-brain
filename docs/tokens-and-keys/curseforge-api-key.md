<!-- ============================================================
     Project Brain — DieOuwe Ecosysteem Kennisbank
     © 2026 DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     Licentie: CC BY-SA 4.0 — Vrij te delen met bronvermelding
     ============================================================ -->

# CurseForge API Key — Hoe te verkrijgen
> Beheerder: wow-brain-manager · Nooit echte keys opslaan in dit bestand

---

## CurseBot Config (geen secrets)

| Instelling | Waarde |
|---|---|
| CF Author ID | 1417946 |
| CF Slug | dieouwe |
| Keyring naam | CurseBot-SlayerAlliance |

---

## API Key aanmaken op CurseForge

```
1. Ga naar console.curseforge.com
2. Log in met je CurseForge account
3. Klik op "My API Keys" of "Create API Key"
4. Geef een naam: bijv. "CurseBot-SlayerAlliance"
5. Kopieer de key ($2a$... formaat)
   ⚠️ Sla op in je password manager — niet in code!
```

---

## Gebruik in CurseBot

De key wordt opgeslagen via `cursebot-security` skill met Fernet encryptie.
Nooit plaintext in `config.py`, `.env`, of enig ander bestand in de repo.

```python
# Ophalen via key_manager (cursebot-security pattern)
from bot.services.key_manager import KeyManager
km = KeyManager()
cf_key = km.get_key("curseforge_api_key")
```

---

## Endpoints die we gebruiken

| Endpoint | Gebruik |
|---|---|
| `GET /v1/mods/{authorId}/files` | Addon releases ophalen |
| `GET /v1/mods/{modId}` | Addon info |
| `GET /v1/mods/{modId}/files/{fileId}` | Specifieke release |

**Base URL**: `https://api.curseforge.com`
**Header**: `x-api-key: {jouw_key}`

---

## Rate Limits

- 100 requests per uur per key (gratis tier)
- Bij 429 response: exponential backoff (0.5s, 1s, 2s, 4s)
- Zie `docs/knowledge/known-bugs.md` voor de backoff implementatie

<!-- ============================================================
     File    : docs/tokens-and-keys/curseforge-api-key.md
     Version : 1.0.0  Created: 2026-06-08  Updated: 2026-06-08
     Status  : New
     DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     ============================================================ -->
