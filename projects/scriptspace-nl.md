---
id: scriptspace-nl
type: site
bijgewerkt: 2026-10-13
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
- Live versie 2026-10-13: **0.25.0** (VERIFIED, `<meta name="ss-version">` in de HTML). Repo staat op 0.26.1.
- De root toont de linktree/inlogpagina van scriptspace-cms (eerder werd gemeld dat de root de CoreBot-site toonde; dat is niet meer zo).
- Nieuwe footer (0.26.1) staat klaar als FTP-update; uploaden doet Ouwe zelf.
