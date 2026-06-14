# CurseForge API Key — Aanmaak Instructies
> HOE je de key aanmaakt · NOOIT echte keys hier opslaan

---

## Stappenplan

1. Ga naar `curseforge.com` → log in
2. Klik op je profielnaam rechtsboven → **API Keys**
3. Klik **Generate API Key**
4. Geef een naam (bijv. `CurseBot-SlayerAlliance`)
5. Kopieer de key

---

## CurseBot Config (NIET de echte key)

```python
# In CurseBot — key wordt opgeslagen via key_manager.py
# Nooit hardcoden, altijd via keyring of encrypted config

KEYRING_SERVICE = "CurseBot-SlayerAlliance"
KEYRING_USERNAME = "curseforge_api_key"

# key_manager.py haalt de key op:
import keyring
key = keyring.get_password(KEYRING_SERVICE, KEYRING_USERNAME)
```

## Bekende Config Data (GEEN geheimen)

| Waarde | Data |
|---|---|
| Author ID | `1417946` |
| Slug | `dieouwe` |
| Keyring service | `CurseBot-SlayerAlliance` |

---

## Veiligheidsregels

- Sla de echte key **ALLEEN** op via `keyring` of Fernet-encrypted config
- Nooit in `.env` bestanden committen
- Nooit in code hardcoden

---

*Beheerd door cursebot-security + wow-brain-manager*
