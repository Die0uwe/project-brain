<!-- ============================================================
     Project Brain — DieOuwe Ecosysteem Kennisbank
     © 2026 DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     Licentie: CC BY-SA 4.0 — Vrij te delen met bronvermelding
     ============================================================ -->

# Discord Bot Token — Hoe te verkrijgen
> Beheerder: wow-brain-manager · Nooit echte tokens opslaan in dit bestand

---

## Token aanmaken / ophalen

```
1. Ga naar discord.com/developers/applications
2. Selecteer je bot applicatie (CurseBot Slayer Alliance)
3. Linker menu → Bot
4. Klik "Reset Token" (of "Copy" als al aangemaakt)
   ⚠️ Kopieer direct — daarna niet meer zichtbaar!
5. Sla op in je password manager
```

---

## Benodigde Bot Permissions (Intents)

In het Developer Portal → Bot → Privileged Gateway Intents:

```
✅ Message Content Intent   (berichten lezen)
✅ Server Members Intent    (guild members ophalen)
✅ Presence Intent          (optioneel, voor status)
```

---

## Benodigde OAuth2 Scopes (invite link)

```
✅ bot
✅ applications.commands    (slash commands)
```

Bot permissions bij invite:
```
✅ Send Messages
✅ Embed Links
✅ Read Message History
✅ Use Slash Commands
✅ Manage Messages (optioneel, voor cleanup)
```

---

## Gebruik in CurseBot

```python
# Nooit hardcoded — altijd via key_manager
from bot.services.key_manager import KeyManager
km = KeyManager()
token = km.get_key("discord_token")
bot.run(token)
```

---

## Token verlopen of compromised?

```
1. discord.com/developers/applications → jouw bot → Bot
2. Reset Token → bevestig
3. Nieuwe token kopiëren
4. Updaten via key_manager / setup_wizard
```

---

## Veiligheidsregels

- ❌ Nooit in requirements.txt, config.py, of enig Python bestand
- ❌ Nooit in Discord zelf sturen (ook niet privé)
- ✅ Opslaan via `cursebot-security` key_manager
- ✅ Bij twijfel: direct resetten en nieuwe token gebruiken

<!-- ============================================================
     File    : docs/tokens-and-keys/discord-bot-token.md
     Version : 1.0.0  Created: 2026-06-08  Updated: 2026-06-08
     Status  : New
     DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     ============================================================ -->
