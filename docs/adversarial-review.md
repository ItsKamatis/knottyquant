# KnottyQuant adversarial review — 14 July 2026

This record covers the local implementation at website base commit `49405c09d260c4201ad98b4bd124c78afa006ab8`. It is a release-preparation review, not a deployment record. No DNS change, deployment, commit, push, or publication was performed. The résumé is outside the approved scope and is not present in the site.

## Automated build and output checks

| Check | Result |
| --- | --- |
| Lockfile install | Passed; dependency graph already matched `pnpm-lock.yaml` |
| Astro type and content check | Passed; 23 files, 0 errors, 0 warnings, 0 hints |
| Static production build | Passed; 9 HTML pages plus RSS, robots, and sitemap output |
| Deterministic site validator | Passed; 9 pages reviewed, 8 indexable pages |
| Internal links and fragments | Passed, including retained legacy project fragments |
| Baseline public asset paths | Passed; all 46 prior `/images`, `/assets/docs`, and `/assets/data` paths remain present |
| Canonical, Open Graph, and structured metadata | Passed; no duplicated page metadata |
| Output scan | Passed; no prior-domain strings, placeholder text, missing image alt text, or disallowed promotional phrasing in generated pages |
| Git whitespace check | Passed |

The validator also checked exact filename case, required downloads, artifact hashes, RSS and sitemap coverage, image intrinsic dimensions, research-figure crop rules, identity boundaries, and the absence of external font calls.

## Cloudflare-local route checks

The production artifact was served through Wrangler so that the configured Cloudflare Static Assets behavior, rather than Astro's development routing, was under review.

- `/` returned 200; `/index.html` redirected once to `/` and retained a query string.
- All required `.html` project, index, About, and essay routes returned 200.
- Extensionless and trailing-slash project and essay variants returned 404 instead of silently replacing the route contract.
- An unknown path returned the branded page with a genuine 404 status; `/404.html` remained directly inspectable.
- RSS, robots, sitemap, favicon, social card, figures, data, and downloads returned the expected content types.
- Security and cache headers from `public/_headers` were present.

These results apply to the local Wrangler preview. They must be repeated against the eventual public hostname because DNS, TLS, redirect, cache, and WAF behavior are external to this artifact.

## Visual and accessibility review

The homepage, both indexes, About, the essay, and all three project pages were reviewed at 1440×900 and 390×844.

- All three navigation links remained visible at both widths.
- No page-level horizontal overflow or hidden content remained.
- Research figures retained their intrinsic proportions and were not cropped. Only the documented 16:9 project-card thumbnails used `object-fit: cover`.
- Equations, evidence tables, code, citations, and long links remained readable; wide material scrolled inside its own container.
- The skip link, keyboard focus treatment, landmark structure, heading order, color contrast, and reduced-motion rule were present.
- A table-of-contents link was clicked in the rendered project page and reached the correct target below the sticky header.

Lighthouse 13.4.0 results from the local production preview were:

| Page | Performance | Accessibility | Best practices | SEO |
| --- | ---: | ---: | ---: | ---: |
| Homepage | 100 | 100 | 100 | 100 |
| Rates project | 100 | 100 | 100 | 100 |
| TDA essay | 99 | 100 | 100 | 100 |

These are local measurements, not a guarantee of public-network performance.

## Research and evidence review

### Rates

The frozen CSVs were recomputed against the published statements. The closing value, total DV01, key-rate profile, four full-revaluation shocks, and five-part value-change identity agree with the website figures. The page labels OIS quotes and trades as synthetic, separates real New York Fed context, and calls the result a value-change explain rather than verified desk economic P&L. It does not claim futures calibration, live controls, dealer quotes, or production multi-curve infrastructure.

### Portfolio construction

The public summary contains 72 monthly decisions for each of the seven main long-only methods and the separately identified 130/30 appendix. All eight reported Sharpe bootstrap intervals cross zero. The public demonstration is identified as synthetic. The retained CRSP-derived panel is not redistributed, no retained-data weights or performance are published, and lack of current WRDS access is explicit. The page does not claim alpha, statistical significance, Nasdaq-100 replication, total-return data, Gurobi/MOSEK use, or an investable strategy.

### Volatility calibration

The downloadable 35-row claim ledger and 55-page technical note were checked against the condensed page. The archive size, weekly-refinement count, early-exercise comparison, numerical-pricing gaps, and closing-error summaries agree with the frozen evidence. Licensed option-chain records and credentials remain excluded. The local source repository is not presented as public.

### Knot theory and TDA essay

The essay distinguishes knot theory from persistent-homology-based TDA and separates demonstrated applications, promising research, and unestablished direct knot/braid signals. Crash, volatility, network, anomaly, and portfolio statements are attributed and bounded. It does not claim reliable crash prediction, persistent alpha, broad institutional adoption, or production use. AlphaKnot counts are described as computational classifications of predicted structures, not an experimental protein count or a general model error rate.

## External-link review

Twenty-one unique external links were checked. Directly accessible targets returned successfully. Publisher or profile endpoints that denied automated retrieval were resolved to their final URLs and checked separately. No failed target remained. The candidate volatility GitHub URL was removed because it returned 404 and the repository was not present in the reviewed public profile.

## Defects found and corrected

1. Currency strings in math-enabled MDX were initially interpreted as equation delimiters. They now use an HTML dollar entity, and the generated markup is valid.
2. Display equations and the essay's evidence table initially widened the mobile page. Each now scrolls within a bounded local container.
3. Project `<section>` identifiers duplicated automatically generated Markdown heading identifiers. The headings now use explicit markup, leaving every page ID unique.
4. The initial Astro sitemap used extensionless URLs. Its serializer now emits the contracted `.html` URLs.
5. A candidate public link for the volatility source returned 404. The link was removed and the materials section now states the actual public/private boundary.
6. The earlier site stretched research images. Figures now carry intrinsic dimensions with `width: 100%`, `height: auto`, and `object-fit: contain`; card crops are isolated and documented.
7. The first migration pass omitted the legacy `/images/og-quant-research.png` social-card path. It now serves the current brand card, and the validator requires the alias alongside the canonical `/og.png` asset.
8. The volatility project and paper records initially used a date that disagreed with the PDF title page and metadata. Both now use 12 July 2026.
9. About initially abbreviated the graduate credential as “MSc.” It now uses “MS in Quantitative Finance,” consistent with the credential wording.
10. The essay's statement about testing Topological Tail Dependence on S&P 100 stocks lacked its primary citation. The Souto and Moradi study is now linked in the text and included in the bibliography.

## Remaining release boundary

The local artifact is ready for owner review, but it is not public. The eventual release still requires a chosen commit, DNS exports, a recorded rollback deployment, Cloudflare host and redirect configuration, public WAF/challenge checks, search-console work, and public social-preview verification. Follow `docs/domain-cutover.md` and repeat this review against the live hostname before treating the migration as complete.
