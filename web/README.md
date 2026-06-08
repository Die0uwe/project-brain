<!-- ============================================================
     Project Brain — DieOuwe Ecosysteem Kennisbank
     © 2026 DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     Licentie: CC BY-SA 4.0
     ============================================================ -->

# Web Viewer — Hosting Opties

> Design Architect analyse: HTML vs PHP voor de kennisbank viewer

---

## Aanbevolen: Optie A — Statische HTML (huidige implementatie)

**Bestand**: `web/index.html`

De viewer laadt markdown rechtstreeks van GitHub raw via `fetch()`.
Geen server nodig — werkt overal.

### Voordelen
- Gratis hosten op GitHub Pages, Netlify, Vercel, Cloudflare Pages
- Geen PHP/server vereist
- Altijd up-to-date (leest live van GitHub main branch)
- Werkt ook lokaal: open `index.html` in browser

### GitHub Pages activeren (aanbevolen)

```
1. github.com/Die0uwe/project-brain
2. Settings → Pages
3. Source: Deploy from branch
4. Branch: main · Folder: /web
5. Save → Live op: https://die0uwe.github.io/project-brain/
```

### Lokaal testen

```bash
# Simpele lokale server (Python):
cd web/
python3 -m http.server 8080
# Open: http://localhost:8080
```

---

## Optie B — PHP op slayeralliance.com

Wanneer kiezen voor PHP:
- Data wil je server-side filteren (bijv. alleen VERIFIED tonen)
- Je wil zoekfunctie met server-side indexing
- Integratie met WordPress / Slayer Alliance plugin gewenst

```php
<?php
// Simpele PHP proxy voor GitHub raw content
$page = $_GET['page'] ?? 'knowledge/known-bugs';
$page = preg_replace('/[^a-z0-9\-\/]/', '', $page); // sanitize

$url = "https://raw.githubusercontent.com/Die0uwe/project-brain/main/docs/{$page}.md";
$content = @file_get_contents($url);

if (!$content) {
    http_response_code(404);
    echo "Pagina niet gevonden";
    exit;
}

// Stuur als plain text terug (JS parsed het client-side)
header('Content-Type: text/plain; charset=utf-8');
header('Access-Control-Allow-Origin: *');
echo $content;
```

**Nadeel PHP**: Extra server overhead, WordPress integratie nodig.
**Voordeel PHP**: Server-side caching, WordPress shortcode mogelijk.

---

## Optie C — WordPress Shortcode (Slayer Alliance)

```php
// In sa-master.php of eigen plugin:
add_shortcode('brain_page', function($atts) {
    $page = sanitize_text_field($atts['page'] ?? 'knowledge/known-bugs');
    // Embed de HTML viewer met specifieke startpagina
    return '<div id="brain-embed" data-page="' . esc_attr($page) . '"></div>
            <script>/* init viewer met data-page */</script>';
});

// Gebruik op een WordPress pagina:
// [brain_page page="knowledge/compass-math"]
```

---

## Huidige keuze: GitHub Pages + statische HTML

Snelst, gratis, altijd live. Activeer GitHub Pages (stap hierboven) en de viewer is
direct bereikbaar via `https://die0uwe.github.io/project-brain/`.

<!-- ============================================================
     File    : web/README.md
     Version : 1.0.0  Created: 2026-06-08  Updated: 2026-06-08
     Status  : New
     DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     ============================================================ -->
