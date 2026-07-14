# KnottyQuant website context — 14 July 2026

This point-in-time record preserves the decisions, evidence boundaries, implementation contract, and release status of the KnottyQuant overhaul. Read this file and `PROJECT_CONTEXT_2026-07-13.md` before changing the site or its research claims.

## Scope and status

The portfolio is being rebuilt as a static Astro site for `https://knottyquant.com`. The public structure is Research, Writing, and About. KnottyQuant is the primary identity; Joshua Colmenar is identified prominently only on About. Historical downloadable research artifacts may retain their original authorship inside the files themselves.

The implementation phase does not include deployment, DNS changes, commits, pushes, or external publication. The prior live domain, `joshuacolmenar.com`, is referenced only in migration documentation and this context record. No résumé is included; the user explicitly removed it from scope.

Work began from website commit `49405c09d260c4201ad98b4bd124c78afa006ab8` on local `main`. The public repository is `https://github.com/ItsKamatis/portfolio`.

## Brand and editorial decisions

- Name: KnottyQuant.
- Canonical origin: `https://knottyquant.com`.
- Homepage deck: “Quantitative research, projects, and writing on derivatives, risk, portfolio construction, numerical methods, and topology.”
- The name refers to knot theory as a study of entanglement and to the broader relationship with topology. Knot theory and topological data analysis are explicitly distinguished.
- Tone is factual, restrained, and method-led. Avoid prestige language, inflated capability claims, generic slogans, and claims of production use or investable performance.
- Public research pages state assumptions, distinguish evidence from interpretation, and document limitations.
- The site has no analytics, database, CMS, newsletter, or required client-side JavaScript.

## Route contract

Astro uses `output: "static"`, `build.format: "file"`, and `trailingSlash: "never"` so established `.html` routes remain stable.

| Route | Output | Purpose |
| --- | --- | --- |
| `/` | `dist/index.html` | Concise landing page |
| `/research.html` | `dist/research.html` | Projects and paper index |
| `/writing.html` | `dist/writing.html` | Writing index |
| `/about.html` | `dist/about.html` | Joshua’s background, contact, and editorial principles |
| `/sofr-curve-swap-risk.html` | same-named file | Rates project |
| `/portfolio-construction.html` | same-named file | Portfolio project |
| `/volatility-surface-research.html` | same-named file | Options project |
| `/writing/knot-theory-topological-data-analysis-and-finance.html` | nested file | First essay |
| `/404.html` | `dist/404.html` | Branded not-found page |
| `/rss.xml` | `dist/rss.xml` | Published writing feed |

Project pages retain their earlier fragment identifiers as alias anchors. Public `/images`, `/assets/docs`, and `/assets/data` URLs are preserved by storing source assets under `public/`.

## Source repositories and reviewed states

| Project | Local source | Commit reviewed | Public repository |
| --- | --- | --- | --- |
| SOFR curve and swap risk | `D:\PyCharmProjects\sofr-curve-swap-risk` | `2c01228d4f6f66b4c44d7eeaf1fa285a34eb19f9` | `https://github.com/ItsKamatis/sofr-curve-swap-risk` |
| Constrained portfolio construction | `D:\PyCharmProjects\constrained-portfolio-construction` | `ea748b81503aa8b596aff6dcd3c2e08afa03c4ff` | `https://github.com/ItsKamatis/constrained-portfolio-construction` |
| Volatility calibration and pricing | `D:\PyCharmProjects\VolSurf-Pricer` | `230751855ea0bf9f6874aadd68f2d2129caaa8e4` | Not public at this review point |

These repositories are evidence sources, not website build dependencies. Do not modify them from the site workflow unless explicitly requested. The website contains frozen public data and figures needed for its own build.

## Research evidence boundaries

### SOFR curve, swaps, and value-change explain

- Dated sample: opening 1 July 2026 and closing 2 July 2026.
- Thirteen synthetic SOFR OIS tenors from 1W through 30Y.
- One-curve research implementation using sequential Brent solves, log-linear discount-factor interpolation, and no extrapolation.
- Closing book: three synthetic swaps and USD 47m gross notional; opening book: two swaps.
- Closing model value: `-$55,489.98`; desk-positive parallel DV01: approximately `$4,439.54/bp`.
- Full-revaluation changes: parallel +25 bp `-$110,823.97`, parallel -25 bp `+$111,147.06`, steepener `+$110,428.81`, flattener `-$109,534.28`.
- The five value-change components reconcile to `+$24,325.73` with zero identity difference.
- New York Fed SOFR and SOFR Index observations are real. Treasury yields are context only. OIS quotes, trades, amendments, and cash are synthetic.
- Call this a value-change explain, not verified desk economic P&L. Do not claim futures calibration, executable dealer quotes, multi-curve production architecture, or live controls.

### Constrained portfolio construction

- Public demonstration: deterministic synthetic assets and factors, 12 assets, 72 monthly decisions from January 2020 through December 2025.
- Main comparison: seven long-only methods. Exact-cardinality CVaR uses eight holdings. A 130/30 formulation is a mathematical appendix only.
- Methods include equal weight, GMV, shrinkage mean-variance, frontier maximum Sharpe with a documented GMV fallback, historical joint CVaR, benchmark-relative construction, and exact-cardinality CVaR.
- Estimation uses 50% mean shrinkage to the cross-sectional grand mean and Ledoit–Wolf covariance.
- The benchmark-relative defaults are a 20% cap, 8% ex-ante tracking-error limit, 30% one-way turnover limit, FF5 plus momentum active-exposure controls, and 10 bp one-way transaction costs.
- A retained CRSP-derived price-only panel is evaluated locally without live WRDS access. It is not redistributed, omits dividends, and uses a current-constituent universe. No retained-data performance or weights are published.
- All public Sharpe uncertainty intervals cross zero. Do not claim alpha, statistical significance, Nasdaq-100 replication, total returns, sector constraints, Brinson attribution, Gurobi/MOSEK use, or an investable strategy.

### Volatility calibration and option pricing

- The project and paper publication date is 12 July 2026, matching the technical note.
- Full private archive: 238 raw files across seven assets. Closing panel: six assets, eight August 2025 dates, 48 contexts, and 2,400 valid valuations.
- The project covers expiry-level carry, contract routing, bounded Brent implied-volatility inversion, raw SVI, explicit calendar and butterfly repair, exercise style, and numerical comparison.
- Guarded weekly refinement changed 7 of 24 August slices. Later transfer evidence was limited, so the result is framed as a narrow family policy rather than a general improvement.
- Negative results remain visible: eSSVI is a local candidate; the local-window fit won some contexts but lost in aggregate; American normalization did not yield a promoted replacement.
- Licensed option chains and credentials are excluded. Public figures and aggregate evidence do not make the quote-level archive independently reconstructible.
- The 55-page PDF is the complete record. It retains Joshua’s name inside the artifact; this is an explicit historical-artifact exception to the HTML identity rule.
- The prior candidate GitHub URL returned 404 during the external-link review, so no source-repository link is published for this project. Do not imply that the local source or later frozen-release paths are public.

## Writing evidence boundary

The first essay is “Knot Theory, Topological Data Analysis, and Finance.” It distinguishes direct knot theory from persistent-homology applications. Direct braid and Jones-polynomial market constructions are classified as exploratory and insufficiently validated. The essay does not claim reliable crash prediction, persistent alpha, broad institutional use, or production adoption.

AlphaKnot counts are described as predicted models classified computationally as knotted, not experimentally confirmed proteins or an AlphaFold error rate. Claims about recent portfolio papers are attributed to the authors and framed as requiring independent replication.

## Technical and visual system

- Astro `6.4.8`, TypeScript strict mode, pnpm lockfile.
- Typed content collections: `projects`, `writing`, and `papers`.
- Static Markdown/MDX, server-rendered KaTeX, syntax highlighting, sitemap, and RSS.
- Shared layouts and components for navigation, metadata, project cards, figures, code, evidence tables, data boundaries, and limitations.
- Palette: paper `#F7F5EF`, ink `#18201D`, muted `#65706B`, border `#D8D3C8`, accent `#1F5C4D`, code `#111916`.
- Self-hosted Source Serif 4, IBM Plex Sans, and IBM Plex Mono; licenses are preserved under `public/assets/fonts/licenses/`.
- Reading width is 720px; research figures may use up to 960px.
- Research images retain intrinsic dimensions and use `width: 100%`, `height: auto`, and `object-fit: contain`. Only card thumbnails use the documented 16:9 crop with `object-fit: cover`.
- No grid texture, offset shadows, decorative badges, entrance animations, competing accents, or decorative knot logo.
- The social card is `public/og.png` at 1730×909. The legacy `/images/og-quant-research.png` path serves the same current card so existing asset links remain valid. The favicon is a typographic KQ mark.
- Structured data uses WebSite and Organization for KnottyQuant; Person appears only on About. Project and essay authorship is KnottyQuant.

## Cloudflare preparation and release boundary

`wrangler.jsonc` prepares Cloudflare Workers Static Assets with `html_handling: "none"` and `not_found_handling: "404-page"`. This choice is necessary because Cloudflare’s default HTML handling would redirect `.html` routes. `public/_redirects` maps the apex homepage internally to `/index.html` while redirecting an explicit `/index.html` request to `/`.

The eventual cutover must establish the HTTPS apex as canonical, redirect `www` and HTTP in one hop, and preserve path and query when redirecting the prior domain. Old-domain redirects should remain indefinitely. Managed challenge pages must not appear on public HTML, robots, sitemap, asset, or social-preview requests. See `docs/domain-cutover.md` for the operational checklist.

No deployment or DNS change has been performed. Before an eventual cutover, record the deployed commit and export both domains’ DNS configurations for rollback.

## Build and verification

From the repository root:

```powershell
pnpm install --frozen-lockfile
python -m pip install -r requirements-dev.txt
pnpm check
pnpm build
pnpm validate
pnpm cloudflare:preview
```

`pnpm qa` combines the type check, build, and validator. The validator checks routes, links, fragments, metadata, structured data, images, artifact hashes, sitemap/RSS coverage, the old-domain exclusion, identity boundaries, and disallowed promotional language. Use `pnpm cloudflare:preview`, rather than the Astro preview alone, to recheck the homepage proxy, literal `.html` routes, and genuine 404 behavior.

The 14 July 2026 production build completed with zero Astro diagnostics and nine generated pages. The deterministic site validator passed. Cloudflare-local route checks, desktop/mobile visual checks, external-link review, research-evidence checks, and Lighthouse results are recorded in `docs/adversarial-review.md`. Re-run that full suite and `git diff --check` after any content or design change.

## Remaining external steps

1. Review the finished local site and research wording.
2. Choose a publication commit only after that review.
3. Export current DNS and note the deployed rollback commit.
4. Follow `docs/domain-cutover.md` for Cloudflare, redirects, search consoles, sitemap submission, social previews, and rollback.
5. Keep the old-domain redirect indefinitely.

Do not infer authorization to deploy, modify DNS, commit, push, or publish from this record.
