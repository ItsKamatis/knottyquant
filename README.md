`# KnottyQuant

Static research website for `knottyquant.com`. The site is organized around three research projects, a writing collection, and a short About page. It uses Astro with static file output so the established `.html` project routes remain stable.

## Local workflow

The project requires Node.js, pnpm, and Python for the independent output validator.

```powershell
pnpm install --frozen-lockfile
python -m pip install -r requirements-dev.txt
pnpm check
pnpm build
pnpm validate
pnpm cloudflare:preview
```

`pnpm qa` runs the type check, production build, and site validator in sequence. Use `pnpm preview` for a quick Astro preview; use `pnpm cloudflare:preview` for the release-relevant check of the homepage proxy, `.html` routes, and genuine 404 responses.

## Route contract

- `/`
- `/research.html`
- `/writing.html`
- `/about.html`
- `/sofr-curve-swap-risk.html`
- `/portfolio-construction.html`
- `/volatility-surface-research.html`
- `/writing/knot-theory-topological-data-analysis-and-finance.html`
- `/404.html`
- `/rss.xml`

Astro is configured with `build.format: "file"` and `trailingSlash: "never"`. Cloudflare Workers Static Assets must retain `html_handling: "none"`; changing that option would redirect the public `.html` routes.

## Evidence and assets

Typed content records live under `src/content`. Public figures, frozen aggregate data, and downloadable research materials live under `public/` and keep their established `/images` and `/assets` URLs.

The rates demonstration uses synthetic OIS quotes and trades. The portfolio demonstration uses deterministic synthetic assets and factors; retained CRSP-derived data cannot be redistributed and does not require a live WRDS connection. Licensed option-chain data is excluded from the volatility project.

`tools/build_research_figures.py` rebuilds the rates and portfolio figures from the frozen public CSV files. `tools/validate_site.py` checks routes, links, metadata, structured data, image dimensions, artifact hashes, and content boundaries in the production output.

## Release boundary

This repository prepares the site and Cloudflare configuration but does not authorize deployment, DNS changes, commits, pushes, or publication. The domain cutover and rollback checklist is in `docs/domain-cutover.md`. The dated project record is `PROJECT_CONTEXT_2026-07-14_KNOTTYQUANT_PLAN.md`, and the latest verification record is `docs/adversarial-review.md`.
