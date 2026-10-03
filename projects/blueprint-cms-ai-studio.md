---
id: blueprint-cms-ai-studio
type: tool
bijgewerkt: 2026-10-03
---
# Blueprint CMS module ai-studio

## Status
In review: PR https://github.com/Die0uwe/Blueprint-CMS/pull/1 (branch `feature/ai-studio`), nog niet gemerged.

## Doel
Webomgeving in het Blueprint-admin: links chat met AI-providers op basis van eigen API-keys, rechts een eigen code-editor (HTML/PHP/Twig/JS/CSS). De AI leest de editorinhoud mee en doet een wijzigingsvoorstel als diff; pas na expliciet "Toepassen" verandert de editor.

## Inhoud (volgens de PR)
- Providers: OpenAI, Anthropic, Google, DeepSeek, Mistral, Ollama (hergebruikt de instellingen van de bestaande `ollama`-module).
- Nieuw `Core\Security\ContentSanitizer` (DOMDocument + whitelist), CLI `ai-studio:migrate`, idempotente migratie, `phpstan.neon`, testsuite `AiStudio`.
- Keys versleuteld (AES-256-GCM) in cf_settings onder `aistudio.provider.{slug}.api_key`; nooit naar de frontend, logs of audit.
- Elke POST-route: CSRF + PermissionMiddleware + RateLimitMiddleware. Permissie `aistudio.use` staat standaard alleen op rol admin.
- Documentatie: `docs/security-notes.md` in de Blueprint-repo.

## Afwijkingen van de opdracht (bewust, veilig)
- CSRF-token voor SSE zit in een header (fetch + stream), niet in de query: een token in de URL lekt via logs.
- Eigen settings-opslag omdat `SettingsRepository` ontsleutelde geheimen een uur in `storage/cache` bewaart (bestaande zwakte in de core; aparte issue gewenst).

## Openstaande punten
- Niet getest met echte API-calls of in een echte browser.
- Geen link in de admin-zijbalk; bereikbaar via `/admin/ai-studio`.
