---
id: blueprint-cms
type: repo
bijgewerkt: 2026-10-03
bron_repo: Die0uwe/Blueprint-CMS
---
# Blueprint CMS (voorheen Community Fusion CMS)

## Doel
Modulair PHP-community-CMS voor gaming, streamers en gilden (guild management, WoW-data, Discord/Twitch/YouTube/Kick, Ollama-AI). Bron: README.md, CHANGELOG.md en docs/ROADMAP.md in de repo.

## Stack
- PHP 8.3+, MariaDB 10.11+ of MySQL 8.0+, Twig 3, PSR-4 (namespace `CommunityFusion\`, modules onder `CommunityFusion\Modules\...`).
- `vendor/` (alleen productie-dependencies) staat sinds v1.28.0 in git, zodat een kale git-clone/ZIP direct draait op FTP-only hosting.
- Licentie GPL-3.0-or-later. Repo is publiek: https://github.com/Die0uwe/Blueprint-CMS

## Versie en status
- Versie 1.28.0 (2026-09-30) op `main`.
- Branch `plan/editors-plugins` loopt 16 commits voor op main (o.a. v1.28.1-beveiligingsfix voor pakketinstallatie, PluginManager, bericht-editor). Niet gemerged; staat niet in de changelog van main.

## Structuur
- `src/Core/` kernel (DI-container, Router, Auth/RBAC/JWT, Block, Queue, Marketplace, Security, Template).
- `src/Modules/` core-modules: Users, News, Pages, Forum, Blog, Downloads, Contact, Gallery, I18n, Roles, Settings, Themes, Media, Menus, Logs, Marketplace, Blocks.
- `modules/` 11 installeerbare modules: discord, twitch, warcraft, guild-management, minecraft, fivem, ollama, google, battlenet, youtube, kick (elk met `module.json`).
- `themes/` (default, gaming-dark), `installer/` web-installer, `cli/` (migrate, module:install, cache clear, queue worker), `public/` is de document root.

## Build, test, deploy
- Geen build-stap. Installatie via web-installer (`/installer/`).
- CI (`.github/workflows/ci.yml`): PHP 8.3 en 8.4, `composer validate`, PHP-lint, PHPUnit (`composer test`), PHPStan level 8 (`composer stan`), PHPCS PSR-12 (`composer cs`), schema-import tegen MariaDB 10.11.
- Deploy: uploaden naar hosting (o.a. Strato); `vendor/` is meegecommit.

## Belangrijke beslissingen
- Module-systeem met `module.json` (slug, permissies, settings-schema, blocks).
- Audit-reeks v1.25.x: privilege-escalatie (rollen/priority), stored XSS in blog, guild/ollama-adminpanels zonder permissie: gefixt. Resterende backlog in docs/ROADMAP.md.
- S12 (premium ecosysteem) bewust uitgesteld.
- Het RBAC-model is de basis voor [scriptspace-cms](scriptspace-cms.md).

## AI Studio (modules/ai-studio)
- Gemerged via PR #1 (commit 1ffa64a, 2026-10-03): chat met zes providers naast een eigen editor met diff-voorstellen. Zie [blueprint-cms-ai-studio](blueprint-cms-ai-studio.md).

## Wachtwoord vergeten en herstellen
- Gemerged via PR #2 (2026-10-04, commits 3ade252 en 4ca844d). Routes `/wachtwoord-vergeten` en `/wachtwoord-herstellen/{token}`, tabel `cf_password_resets` (bestaande installaties: `php cli/console.php migrate`), `Core\Auth\PasswordResetService`, docs in `docs/password-reset.md`.
- Token 256 bit, alleen de hash opgeslagen, 60 minuten, eenmalig; limieten 3 per account en 5 per IP per uur; na een reset worden oudere sessies ongeldig.
- Meegenomen fix: `CsrfProtection::verify()` accepteerde een leeg token zonder sessietoken.
- Bekend en niet aangepast: `Request::ip()` vertrouwt `X-Forwarded-For` blind; CI-stap PHPStan faalt al op main (441 fouten op heel `src`, na PR #3 nog 433).

## Inloggen met GitHub, Google en Discord
- Gemerged via PR #3 (2026-10-04, commit 10054bc). De knoppen stonden er al maar geen OAuth-login kon slagen: sessiecookie `SameSite=Strict` verloor de state bij de terugkeer van de provider (nu `Lax`), een lege state kwam door de controle, geblokkeerde gebruikers kregen een nieuw account, netwerkfouten gaven een 500.
- Nieuw: `modules/github`, `Core\Auth\OAuth\OAuthLoginFlow` (gedeelde flow voor alle vijf providers), `OAuthProviders` (knoppen alleen voor providers die aanstaan en Client ID + Secret hebben), `SafeRedirect`. Admin: Marketplace, Providers & API-instellingen; opslaan met sleutels schakelt de module in. Docs: `docs/oauth-login.md`. Geen migratie nodig.
- Bewust geen automatische koppeling op e-mailadres (registratie controleert adressen niet).
- Niet getest met echte sleutels bij GitHub/Google/Discord; wel end-to-end tegen een nep-provider (69 controles) en 100 PHPUnit-tests.

## Openstaande punten
- README noemt de clone-URL `Bluprint-CMS` en de CI-badge `bluprint-cms` (typefout; de repo heet Blueprint-CMS).
- Backlog uit docs/ROADMAP.md fase 0 (migratierunner, i18n-dekking, forum-cascade).
- Beheer-skill: onbekend.
