<!-- ============================================================
     Project Brain — DieOuwe Ecosysteem Kennisbank
     © 2026 DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     Licentie: CC BY-SA 4.0 — Vrij te delen met bronvermelding
     ============================================================ -->

# Blizzard OAuth2 — Hoe te gebruiken
> Beheerder: wow-brain-manager · Nooit echte credentials opslaan

---

## Waarvoor

- Armory data ophalen (guild roster, character info)
- Realm status controleren
- WoW game data API (items, spells, achievements)
- Slayer Alliance WordPress plugin (`sa_get_valid_token`)

---

## Client Credentials aanmaken

```
1. Ga naar develop.battle.net
2. Log in met je Battle.net account
3. Klik "Create Client"
4. Vul in:
   - Client Name: bijv. "SlayerAlliance-Plugin"
   - Redirect URI: https://slayeralliance.com/callback (of localhost voor test)
   - Service URL: https://slayeralliance.com
5. Sla op → kopieer Client ID en Client Secret
   ⚠️ Client Secret is maar één keer zichtbaar!
```

---

## Token ophalen (Client Credentials Flow)

```python
import requests

def get_blizzard_token(client_id: str, client_secret: str, region: str = "eu") -> str:
    """Haal een Blizzard OAuth token op. Nooit client_id/secret hardcoden."""
    url = f"https://{region}.battle.net/oauth/token"
    response = requests.post(
        url,
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret)
    )
    response.raise_for_status()
    return response.json()["access_token"]

# Gebruik (keys komen uit key_manager, nooit hardcoded):
token = get_blizzard_token(
    client_id=km.get_key("blizzard_client_id"),
    client_secret=km.get_key("blizzard_client_secret"),
    region="eu"
)
```

---

## WordPress implementatie (Slayer Alliance)

```php
// sa_get_valid_token() in sa-master.php
// Haalt token op uit wp_options, vernieuwt automatisch bij expiry
$token = sa_get_valid_token();
if (!$token) {
    // credentials ontbreken of API onbereikbaar
}
```

---

## Endpoints (EU region)

| Endpoint | Gebruik |
|---|---|
| `https://eu.api.blizzard.com/data/wow/...` | Game data |
| `https://eu.api.blizzard.com/profile/wow/...` | Character/guild data |
| `https://eu.battle.net/oauth/token` | Token ophalen |
| `https://eu.battle.net/oauth/check_token` | Token valideren |

---

## Token expiry & refresh

- Tokens verlopen na **24 uur**
- Implementeer altijd een refresh check vóór API calls
- Sla expiry timestamp op naast het token (nooit het token zelf in plaintext)

---

## Veiligheidsregels

- ❌ Client Secret nooit in PHP/Python broncode
- ❌ Nooit in WordPress `wp-config.php` als hardcoded string
- ✅ Opslaan via `cursebot-security` key_manager (Python)
- ✅ Opslaan via `sa_get_core_settings()` encrypted options (WordPress)
- ✅ Bij twijfel: revoke op develop.battle.net en nieuwe aanmaken

<!-- ============================================================
     File    : docs/tokens-and-keys/blizzard-oauth.md
     Version : 1.0.0  Created: 2026-06-08  Updated: 2026-06-08
     Status  : New
     DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     ============================================================ -->
