# Portfolio website context — 13 July 2026

This file records the state and evidence boundaries of the website overhaul so a later working session can resume without reconstructing the project history.

## Objective

Rework the portfolio into a concise quantitative-research site centered on methods, implementation evidence, and limitations. The tone should remain factual and restrained. The old KRNN/tail-risk feature is being replaced by two current projects while the volatility-surface project remains as the third research record.

No live WRDS access is available. Public website claims must therefore rely on retained outputs, deterministic synthetic demonstrations, or public data that is already present in the source repositories.

## Source repositories at this point in time

| Project | Local source | Commit reviewed | Public repository |
| --- | --- | --- | --- |
| SOFR curves and swap risk | `D:\PyCharmProjects\sofr-curve-swap-risk` | `2c01228d4f6f66b4c44d7eeaf1fa285a34eb19f9` | `https://github.com/ItsKamatis/sofr-curve-swap-risk` |
| Constrained portfolio construction | `D:\PyCharmProjects\constrained-portfolio-construction` | `ea748b81503aa8b596aff6dcd3c2e08afa03c4ff` | `https://github.com/ItsKamatis/constrained-portfolio-construction` |
| Volatility calibration and pricing | `D:\PyCharmProjects\VolSurf-Pricer` | `230751855ea0bf9f6874aadd68f2d2129caaa8e4` | `https://github.com/ItsKamatis/VolSurf_Pricer` |
| Website | `D:\PyCharmProjects\portfolio` | work began from `69b5c7f55f7c774e82bc5b385e2fa09afe4c4e7c` | `https://github.com/ItsKamatis/portfolio` |

The source repositories are evidence sources, not website build dependencies. Frozen rates and portfolio CSV inputs needed for the charts are copied into this repository. Do not modify the source projects from the website workflow unless a later task explicitly asks for source-project changes.

The website worktree already contained edits to the homepage, stylesheet, sitemap, README, and volatility page, plus an untracked volatility report/evidence bundle, before this overhaul began. The volatility source also had a dirty IDE/release state. Preserve that provenance when reviewing or committing the combined work.

## Current site structure

- `index.html`: research index and short profile.
- `sofr-curve-swap-risk.html`: curve construction, swap valuation, DV01, scenarios, and value-change explain.
- `portfolio-construction.html`: walk-forward construction, constraints, public synthetic results, attribution, and solver checks.
- `volatility-surface-research.html`: existing options calibration and pricing research record.
- `assets/css/research.css`: shared visual system for all pages.
- `assets/js/site.js`: re-aligns fragment links after fonts and images decode.
- `tools/build_research_figures.py`: rebuilds the six rates and portfolio figures from copied CSV evidence.
- `tools/validate_site.py`: checks page structure, local paths, fragment links, image alt text, duplicate IDs, link security attributes, sitemap coverage, selected tone checks, and CSS brace balance.

## Rates project: publishable evidence boundary

- The dated sample is 2 July 2026.
- Thirteen synthetic SOFR OIS quote tenors span 1W through 30Y.
- The curve is bootstrapped sequentially with Brent root solves, linear interpolation in log discount factors, and no extrapolation.
- The sample book contains three synthetic swaps and USD 47 million gross notional.
- Closing model value is approximately `-$55,490`; parallel DV01 is approximately `$4,440/bp`.
- The explained opening-to-closing value change is approximately `+$24,326`, with a zero identity difference in the sample output.
- Parallel, steepener, and flattener values are full-revaluation scenario changes after quote shocks and a complete curve rebuild.
- New York Fed SOFR and SOFR Index observations are real. Treasury yields are context only. OIS quotes, trades, amendments, and cash are synthetic.
- Describe the reconciliation as a **value-change explain**, not verified desk economic P&L.
- Do not imply dealer quotes, futures integration, multi-curve production architecture, or production trade controls.

The site copy includes the convention set: T+1 spot, annual legs, ACT/360, modified following, two-USNY-business-day payment lag, log-DF interpolation, and no extrapolation.

## Portfolio project: publishable evidence boundary

- The public demonstration is deterministic and synthetic: 12 assets and 72 monthly holding periods from January 2020 through December 2025.
- Seven long-only methods are in the primary comparison; a 130/30 construction appears only as a separate appendix method.
- Methods include equal weight, global minimum variance, shrinkage mean-variance, max-Sharpe frontier search with a GMV fallback, historical joint CVaR, benchmark-relative construction, and exact-cardinality CVaR.
- Means use 50% shrinkage to the cross-sectional grand mean; covariance uses Ledoit-Wolf shrinkage.
- The benchmark-relative defaults shown on the page are a 20% position cap, 8% ex-ante tracking-error limit, 30% one-way turnover limit, active Fama-French five-factor plus momentum exposure controls, and a 10 bp one-way cost model.
- The exact-cardinality mixed-integer run selects exactly eight holdings in every synthetic holding period using SciPy/HiGHS.
- Public Sharpe uncertainty intervals cross zero. Do not claim alpha, statistical significance, or an investable strategy.
- Retained CRSP-derived price history is evaluated locally without live WRDS, but it has a current-constituent/survivorship boundary and omits dividends. Do not publish its performance or weights.
- Do not claim sector/Brinson attribution, total returns, Gurobi/MOSEK use, or a validated investable 130/30 strategy.

## Website evidence artifacts

Copied data:

- `assets/data/rates/curve_nodes.csv`
- `assets/data/rates/key_rate_dv01.csv`
- `assets/data/rates/pnl_waterfall.csv`
- `assets/data/portfolio/summary.csv`
- `assets/data/portfolio/bootstrap_uncertainty.csv`
- `assets/data/portfolio/monthly_results.csv`
- `assets/data/portfolio/active_attribution.csv`
- `assets/data/rates/scenarios.csv`
- `assets/data/artifact_manifest.csv`

Generated figures:

- `images/research/rates-curve.png`
- `images/research/rates-risk.png`
- `images/research/rates-value-change.png`
- `images/research/portfolio-growth.png`
- `images/research/portfolio-tradeoffs.png`
- `images/research/portfolio-attribution.png`

Downloadable rates artifact:

- `assets/docs/SOFR_Curve_Swap_Risk_2026-07-02.xlsx`

The figures are generated from the copied evidence files. Their SHA-256 hashes, source commits, and classifications are recorded in `assets/data/artifact_manifest.csv`. Rebuild them from the website root with:

```powershell
python tools\build_research_figures.py
```

## Design and writing decisions

- Shared palette: warm paper, deep green, muted rust, restrained sage.
- Shared typography: Source Serif 4 for research titles, IBM Plex Sans for body copy, IBM Plex Mono for labels and numerical metadata.
- Pages separate the question, method, implementation, evidence, and limitations.
- Synthetic and retained-data boundaries are placed next to the relevant figures or claims, not only in a footer disclaimer.
- Avoid inflated labels such as “institutional-grade,” “production-ready,” “cutting-edge,” or claims of outperformance.
- Keep the project names descriptive rather than promotional.

## Verification completed during the overhaul

- Rates source tests: 27 passed at the reviewed source commit.
- Portfolio source tests: 28 passed and 1 skipped without the retained licensed data root at the reviewed source commit.
- Static validator: `python tools\validate_site.py`.
- Whitespace check: `git diff --check`.
- Browser review: desktop 1280×720 and mobile 390×844, including top-level pages and deep links to methods, risk, evidence, attribution, and limits.
- Browser checks covered horizontal overflow, missing images, duplicate IDs, chart rendering, responsive grids, and fragment-link alignment after assets load.
- Follow-up image correction: all image elements retain intrinsic `width`/`height` metadata for layout stability, while the shared stylesheet applies `height: auto` so responsive width changes preserve the original aspect ratio. The stylesheet cache key is `20260713b`.

## Remaining workflow boundary

The website changes are local. Do not deploy, push, or replace the current hosting configuration without explicit user authorization. Before any later publication step, rerun the figure generator, site validator, whitespace check, and a final browser smoke test. Review `git status` carefully because the website worktree already contained user changes and volatility-report artifacts when this overhaul began.
