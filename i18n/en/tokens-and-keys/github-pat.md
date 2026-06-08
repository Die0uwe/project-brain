> 🌐 Translation of [`docs/tokens-and-keys/github-pat.md`](../../../docs/tokens-and-keys/github-pat.md)
> Language: English · Translated by: DieOuwe team · Date: 2026-06-08

# GitHub Personal Access Token (PAT) — How to get one
> Never store real tokens in this file

---

## What is a GitHub PAT used for?

- Pushing code to `Die0uwe/*` repos via wow-git-manager
- Triggering GitHub Actions via API
- Reading or modifying repo contents via REST API

---

## Step-by-step: create a token

```
1. Go to github.com → log in
2. Click your profile picture (top right)
3. Settings → (bottom left) Developer settings
4. Personal access tokens → Tokens (classic)
5. Generate new token → Generate new token (classic)
6. Name: e.g. "delvetracker-push" or "cursebot-push"
7. Expiration: choose 90 days or No expiration
8. Check: ✅ repo  (full repository access)
9. Generate token
10. COPY THE TOKEN (ghp_... or github_pat_...)
    ⚠️ Only shown ONCE — copy it now!
```

---

## Using the token in a session (never save in files)

```bash
# Export as environment variable for the current bash session only
export GH_TOKEN="ghp_your_token_here"

# Use in git commands
git remote set-url origin https://$GH_TOKEN@github.com/Die0uwe/DelveTracker.git
git push origin main

# Or directly via API
curl -H "Authorization: Bearer $GH_TOKEN" https://api.github.com/repos/Die0uwe/DelveTracker/contents
```

---

## GitHub Actions Secrets (for pipelines)

Store PAT tokens for automated pipelines as GitHub Secrets:

```
Repo → Settings → Secrets and variables → Actions
→ New repository secret
Name: GH_TOKEN (or CURSEFORGE_KEY, etc.)
Value: [paste token]
```

In the workflow yml: `${{ secrets.GH_TOKEN }}`

---

## Security rules

- ❌ Never put a token in a .lua, .py, .php, or .md file
- ❌ Never commit code that contains a token
- ❌ Never type a token in chat unless in a private session
- ✅ Always use environment variables (`export GH_TOKEN=...`)
- ✅ Token expired? Create a new one using the steps above
- ✅ Compromised? Immediately revoke at github.com/settings/tokens
