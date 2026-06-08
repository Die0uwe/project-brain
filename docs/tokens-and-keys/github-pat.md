# GitHub Personal Access Token (PAT) — Hoe te verkrijgen
> Beheerder: wow-brain-manager · Nooit echte tokens opslaan in dit bestand

---

## Waarvoor heb je een GitHub PAT nodig?

- Code pushen naar `Die0uwe/*` repos via wow-git-manager
- GitHub Actions triggeren via API
- Repo inhoud ophalen of aanpassen via REST API

---

## Stap-voor-stap aanmaken

```
1. Ga naar github.com → log in als Die0uwe
2. Klik rechtsboven op je profielfoto
3. Settings → (links onderaan) Developer settings
4. Personal access tokens → Tokens (classic)
5. Generate new token → Generate new token (classic)
6. Naam: bijv. "delvetracker-push" of "cursebot-push"
7. Expiration: kies 90 days of No expiration (jouw keuze)
8. Vink aan: ✅ repo  (geeft volledige repo toegang)
9. Generate token
10. KOPIEER DE TOKEN (ghp_... of github_pat_...)
    ⚠️ Slechts ÉÉN keer zichtbaar — kopieer nu!
```

---

## Gebruik in sessie (nooit opslaan in bestanden)

```bash
# Exporteer als omgevingsvariabele in de huidige bash sessie
export GH_TOKEN="ghp_jouw_token_hier"

# Gebruik in git commands
git remote set-url origin https://$GH_TOKEN@github.com/Die0uwe/DelveTracker.git
git push origin main

# Of direct via API
curl -H "Authorization: Bearer $GH_TOKEN" https://api.github.com/repos/Die0uwe/DelveTracker/contents
```

---

## GitHub Actions Secrets (voor pipelines)

PAT tokens voor geautomatiseerde pipelines sla je op als GitHub Secret:

```
Repo → Settings → Secrets and variables → Actions
→ New repository secret
Naam: GH_TOKEN (of CURSEFORGE_KEY, etc.)
Waarde: [plak token]
```

In de workflow yml dan: `${{ secrets.GH_TOKEN }}`

---

## Veiligheidsregels

- ❌ Nooit een token in een .lua, .py, .php, of .md bestand zetten
- ❌ Nooit committen met een token in de code
- ❌ Nooit een token in de chat typen tenzij in een afgesloten privé sessie
- ✅ Altijd via omgevingsvariabele (`export GH_TOKEN=...`)
- ✅ Token verlopen? Nieuwe aanmaken via bovenstaande stappen
- ✅ Compromised? Onmiddellijk intrekken via github.com/settings/tokens
