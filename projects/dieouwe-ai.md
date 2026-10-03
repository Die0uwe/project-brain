---
id: dieouwe-ai
type: ai
bijgewerkt: 2026-10-03
---
# DIEOUWE AI (eigen model)

## Doel
Eigen lokaal AI-model op Ouwe's pc (Open WebUI + Ollama in Docker), bereikbaar via een Cloudflare Tunnel. ScriptSpace gebruikt het als derde AI-aanbieder naast DeepSeek en Gemini.

## Bekend (bron: docs/EIGEN-MODEL.md in scriptspace-cms)
- Keten: browser, scriptspace.nl (PHP-proxy op STRATO), `ai.<domein>` via Cloudflare, Tunnel, pc met Docker (Open WebUI + Ollama).
- Open WebUI luistert alleen lokaal (127.0.0.1:3000); signup uit.
- In ScriptSpace configureer je het via `ai_custom` in `config.php` (OpenAI-compatibel `/chat/completions`); beheerders hebben een verbindingstest.
- Blueprint CMS heeft eveneens een Ollama-module met Open WebUI-koppeling, zie [blueprint-cms](blueprint-cms.md).

## Veiligheid
Sleutels en tunnel-URL's horen in `config.php`/wachtwoordmanager, nooit in de brain.

## Openstaande punten
Modelkeuze, hardware en de echte domeinnaam: onbekend/te verifiëren (bewust niet in de bron vastgelegd).
