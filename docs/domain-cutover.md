# KnottyQuant domain cutover and rollback

This is a preparation checklist. The current implementation phase does not authorize deployment, DNS changes, redirects, publication, commits, or pushes.

## Target state

- Canonical origin: `https://knottyquant.com`.
- Apex HTTPS serves the Astro production artifact.
- `http://knottyquant.com`, `http://www.knottyquant.com`, and `https://www.knottyquant.com` redirect to the HTTPS apex in one hop.
- Requests to `joshuacolmenar.com` and `www.joshuacolmenar.com` redirect permanently to the same path on `knottyquant.com` and preserve the query string.
- Existing `.html` project URLs remain unchanged.
- Old-domain redirects remain active indefinitely.

## Before making any external change

1. Run `pnpm install --frozen-lockfile`, `python -m pip install -r requirements-dev.txt`, and `pnpm qa` from a clean working state.
2. Preview the exact `dist/` artifact with `pnpm cloudflare:preview` and complete the desktop/mobile review in `docs/adversarial-review.md`.
3. Record the publication commit SHA and the currently deployed rollback commit SHA.
4. Export DNS records for the new domain and the prior domain from Cloudflare.
5. Save the current redirect rules, Workers routes, custom-domain bindings, TLS settings, WAF rules, and cache rules.
6. Confirm access to the registrar, Cloudflare, Google Search Console, and Bing Webmaster Tools.
7. Reduce DNS TTLs in advance only if the current DNS setup makes that useful; record the original values so they can be restored.

## Build artifact checks

- Confirm `dist/index.html` and every required `.html` route exist.
- Confirm `dist/404.html`, `dist/rss.xml`, `dist/robots.txt`, and `dist/sitemap-index.xml` exist.
- Confirm public `/images`, `/assets/docs`, `/assets/data`, and `/_astro` files load with the expected content types.
- Scan `dist/` for the prior domain, placeholder text, managed challenge HTML, and stale personal-brand assets.
- Confirm all canonical URLs, Open Graph URLs, RSS entries, and sitemap entries use `https://knottyquant.com`.
- Confirm the sitemap lists the `.html` page URLs and excludes `404.html`.
- Confirm the social-card and favicon requests return the assets directly, without a challenge page or HTML response.

## Cloudflare Workers Static Assets

The committed `wrangler.jsonc` is intentionally configured as:

```json
{
  "assets": {
    "directory": "./dist",
    "html_handling": "none",
    "not_found_handling": "404-page"
  }
}
```

Do not replace `html_handling: "none"` with Cloudflare's default HTML handling. The default can redirect `.html` requests to extensionless paths and would break the route contract.

Before publishing, create or select the Cloudflare Worker, bind `knottyquant.com` and `www.knottyquant.com` as custom domains as appropriate, and verify that only the intended production artifact is uploaded. Use the current Cloudflare static-assets documentation during the actual release because dashboard labels and deployment commands can change.

## Redirect rules

### Apex homepage

The artifact includes these static rules:

```text
/index.html / 301
/ /index.html 200
```

The second rule is an internal proxy that keeps the browser at `/`. Test it through Wrangler before publication. An explicit `/index.html` request must redirect once to `/`.

### HTTP and www

Create host/scheme redirect rules that send all HTTP and `www` variants directly to:

```text
https://knottyquant.com${path-and-query}
```

Avoid an HTTP-to-HTTPS hop followed by a separate `www`-to-apex hop. Test all four host/scheme variants with a nested path and query string.

### Prior domain

Use a Cloudflare Bulk Redirect, Redirect Rule, or dedicated redirect Worker for `joshuacolmenar.com` and its `www` host. The redirect target must be:

```text
https://knottyquant.com${path-and-query}
```

Use a permanent redirect only after the new site passes acceptance. Preserve case, path, and query string. Do not redirect every request to the homepage. Keep the prior domain, TLS certificate, and redirect configuration active indefinitely.

## DNS and TLS

- Verify apex and `www` records resolve only to the intended Cloudflare application.
- Remove stale A, AAAA, CNAME, Pages, or Worker-route records that could split traffic, but only after the saved DNS export is complete.
- Use Full (strict) TLS where an origin certificate is relevant.
- Confirm Universal SSL covers both apex and `www` before enabling permanent redirects.
- Enable automatic HTTPS rewrites only if it does not mask mixed-content defects in the artifact.
- Restore normal DNS TTLs after the release is stable.

## Public-page and WAF checks

Cloudflare managed challenges must not be presented to ordinary requests for:

- public HTML routes;
- `robots.txt`;
- `sitemap-index.xml` and sitemap children;
- `rss.xml`;
- `og.png` and `images/favicon.svg`;
- CSS, fonts, research figures, data, and downloadable documents.

Scope any bot, WAF, or rate-limit exceptions narrowly enough to keep public pages indexable without weakening unrelated administrative surfaces. Verify with a signed-out browser, a command-line client, and social-preview user agents where possible.

## Launch verification

Test each item from an uncached connection:

- `/` returns 200 with the KnottyQuant homepage.
- `/index.html` returns one permanent redirect to `/`.
- Each required `.html` route returns 200.
- Extensionless and trailing-slash project variants are not silently canonicalized.
- An unknown path returns the branded page with a genuine 404 status.
- The five downloadable research documents, eight research-output CSVs, and the public artifact manifest return 200.
- Research images preserve their proportions at desktop and mobile widths.
- Canonical, Open Graph, and structured-data URLs use the HTTPS apex.
- `robots.txt` points to the production sitemap.
- The sitemap contains every indexable `.html` route and no 404 route.
- The RSS item uses the canonical `.html` essay URL.
- HTTP, `www`, and prior-domain requests preserve path/query and reach the apex in one hop.
- No response body is a managed challenge page.

## Search and previews

1. Add or verify the `knottyquant.com` domain property in Google Search Console and Bing Webmaster Tools.
2. Submit `https://knottyquant.com/sitemap-index.xml` after the public checks pass.
3. Use change-of-address tooling for the prior domain only after same-path redirects are stable.
4. Inspect representative URLs in both search consoles and request indexing for the homepage, Research, Writing, About, the three projects, and the essay.
5. Refresh representative social previews for the homepage, one project, and the essay; verify title, description, image, and canonical URL.
6. Monitor crawl errors, redirect chains, duplicate canonicals, and 404 volume during the first weeks.

## Rollback

Rollback is triggered by route loss, challenge pages on public resources, TLS failure, redirect loops, corrupted downloads, materially broken rendering, or missing canonical/search files.

1. Re-deploy the recorded prior artifact or prior Worker version.
2. Restore the saved Worker routes, custom-domain bindings, redirect rules, WAF/cache settings, and DNS export.
3. Disable the prior-domain permanent redirect only if it prevents access to the restored site; otherwise keep it consistent with the restored canonical host.
4. Purge only the affected Cloudflare cache entries, then retest apex, `www`, HTTP, project routes, 404 behavior, assets, and search files.
5. Record the failure, the rollback time, affected URLs, and the corrective change before another launch attempt.

Do not delete the saved DNS export or prior deployment reference after a successful cutover.
