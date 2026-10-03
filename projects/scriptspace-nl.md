---
id: scriptspace-nl
type: site
bijgewerkt: 2026-10-03
---
# scriptspace.nl

## Doel
Persoonlijke website van Ouwe: "Code, AI & sandboxes op één plek". De site is de live uitrol van [scriptspace-cms](scriptspace-cms.md).

## Stack en hosting
- PHP + MySQL op STRATO shared hosting (bron: docs/DEPLOY.md in scriptspace-cms).
- Postvak `system@scriptspace.nl` wordt in de deploy-handleiding genoemd voor SMTP (geen wachtwoorden in de brain).

## Deploy
Zie [scriptspace-cms](scriptspace-cms.md): testen op een subdomein (bijv. test.scriptspace.nl) met aparte testdatabase, daarna de echte map. Terugweg: back-up van de oude webmap en database.

## Openstaande punten
- Welke versie er op dit moment live staat is niet te verifiëren vanuit de repo (onbekend/te verifiëren; repo staat op 0.23.0).
- Of de site de oude of nieuwe versie draait is niet gecontroleerd.
