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

## AI Studio (module / branch feature/ai-studio)
- **Onbekend/te verifiëren.** In deze sessie bestaat op GitHub geen branch `feature/ai-studio` en geen pull request in Die0uwe/Blueprint-CMS (branches: `main`, `plan/editors-plugins`; PR-lijst leeg). In de code staat geen verwijzing naar ai-studio. Het bestaande AI-onderdeel is de Ollama-module (`modules/ollama`, blocks `ollama-chat` en `ollama-assistant`, permissies `ollama.use`/`ollama.admin`).
- Zodra de branch/PR bestaat: kaart [blueprint-cms-ai-studio](blueprint-cms-ai-studio.md) aanvullen.

## Openstaande punten
- README noemt de clone-URL `Bluprint-CMS` en de CI-badge `bluprint-cms` (typefout; de repo heet Blueprint-CMS).
- Backlog uit docs/ROADMAP.md fase 0 (migratierunner, i18n-dekking, forum-cascade).
- Beheer-skill: onbekend.
