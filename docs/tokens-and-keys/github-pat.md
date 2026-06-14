# GitHub PAT — Aanmaak Instructies
> Hoe een Personal Access Token aanmaken · NOOIT echte tokens hier opslaan

---

## Stappenplan

1. Ga naar `github.com` → log in
2. Klik rechtsboven op je profielfoto → **Settings**
3. Scroll helemaal naar beneden → **Developer settings** (links onderaan)
4. Klik: **Personal access tokens** → **Tokens (classic)**
5. Klik: **Generate new token** → **Generate new token (classic)**
6. Geef een naam: bijv. `cursebot-push` of `delvetracker-push`
7. Vink aan: **`repo`** (het bovenste vinkje — volledige repo toegang)
8. Vink ook aan: **`workflow`** (voor `.github/workflows/` bestanden)
9. Scroll naar beneden → **Generate token**
10. **Kopieer de token** (begint met `ghp_...` of `github_pat_...`)
    ⚠️ Hij is maar **één keer zichtbaar** — kopieer hem direct!

---

## Scopes Overzicht

| Scope | Waarvoor |
|---|---|
| `repo` | Volledige repo toegang (push/pull/files) |
| `workflow` | Push naar `.github/workflows/` |
| `read:org` | Org info lezen (optioneel) |

**Minimaal vereist**: `repo` + `workflow`

---

## Gebruik in Sessie

```bash
# Zet in huidige shell (verdwijnt na sessie — veilig)
export GH_TOKEN="ghp_..."

# Gebruik in git push
git remote set-url origin https://$GH_TOKEN@github.com/Die0uwe/DelveTracker.git
```

---

## Veiligheidsregels

- **NOOIT** de echte token in dit bestand opslaan
- **NOOIT** token hardcoden in bestanden die worden gepushed
- Alleen gebruiken als omgevingsvariabele in de actieve shell
- Token niet in commit history, .env bestanden, of bestanden

---

*Beheerd door wow-brain-manager · Veiligheidsbeheer: cursebot-security*
