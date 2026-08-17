# Note for server-side Claude — wire the Atomic Sanskrit favicon into the Caddy site

**Date:** 2026-07-08
**Branch state:** `main` at `12a941b` (favicon assets) or later
**Audience:** Whoever maintains the Caddyfile and the HTML renderer that Caddy serves.

## What exists

Commit `12a941b` added the Atomic Sanskrit favicon assets to the manuscript
repo under `web/public/as/`. The mark is the
lotus-in-hex on the book's warm cream palette.

**Deploy these seven files** (into the served webroot, same `/as/` path
the Atomic Sanskrit pages live under):

| File | What it is |
|------|-----------|
| `favicon.ico` | 6 embedded sizes: 16, 32, 48, 64, 128, 256 (PNG-compressed). The universal fallback. |
| `favicon.svg` | Scalable mark; modern browsers prefer this. |
| `favicon-16x16.png` | Explicit 16px raster. |
| `favicon-32x32.png` | Explicit 32px raster. |
| `favicon-48x48.png` | Explicit 48px raster. |
| `favicon-512.png` | Large raster (PWA manifest / link previews). |
| `apple-touch-icon.png` | 180×180, iOS home-screen icon. |

**Do NOT deploy** anything matching `favicon-candidate-*` or
`*-preview.png` — those are design-iteration working artifacts that
happen to sit in the same directory.

## The fix — two parts

### 1. Head tags in the HTML template

Add to the `<head>` of every rendered page (TOC, chapters, Part openers):

```html
<link rel="icon" href="/as/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/as/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/as/apple-touch-icon.png">
```

Order matters: SVG first (modern browsers take it), `.ico` as the
`sizes="any"` fallback. The explicit PNG sizes are optional as link
tags — the `.ico` already embeds 16/32/48 — deploy them anyway so
they're addressable if a manifest or share-card needs them later.

Adjust the `/as/` prefix if the served URL scheme differs — match
wherever the site actually mounts the Atomic Sanskrit pages.

### 2. Root `/favicon.ico` in the Caddyfile

Browsers and crawlers request `/favicon.ico` at the site root
regardless of link tags. Point it at the same file:

```caddyfile
handle /favicon.ico {
    rewrite * /as/favicon.ico
    file_server
}
```

(Or simply copy `favicon.ico` to the webroot root as a second copy —
either works; the rewrite avoids the duplicate.)

If the site serves other projects besides Atomic Sanskrit at the root
and the root favicon should stay something else, skip the rewrite and
rely on the link tags alone — the `/as/…` pages will still show the
lotus-in-hex.

## Verification

1. `curl -sI https://<site>/as/favicon.ico` → `200`, `Content-Type: image/vnd.microsoft.icon` (or `image/x-icon`).
2. `curl -sI https://<site>/as/favicon.svg` → `200`, `image/svg+xml`.
3. `curl -sI https://<site>/favicon.ico` → `200` (if the root rewrite was added).
4. Load a chapter page in a browser, hard-refresh (⌘⇧R) — the tab shows the lotus-in-hex mark. Favicons cache aggressively; a normal reload may keep showing the old/blank icon. Private window is the quickest clean check.
5. iOS Safari → Share → Add to Home Screen — icon should be the mark, not a page screenshot.

## What NOT to do

- **Don't regenerate or re-encode the assets server-side.** The `.ico`
  was built with per-size tuning; re-exporting from the SVG loses the
  16px legibility pass.
- **Don't inline the SVG as a base64 data-URI in the template.** Keep it
  a file; it caches once across all pages.
- **Don't deploy the `favicon-candidate-*` / `*-preview.png` files** (worth
  repeating).
