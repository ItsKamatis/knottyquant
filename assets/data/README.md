# Published figure inputs

These files are frozen inputs for the six rates and portfolio figures on the website. They make chart regeneration independent of a live WRDS connection and independent of the neighboring source repositories.

## Lineage

| Figure | Input files | Source project commit | Classification |
| --- | --- | --- | --- |
| `rates-curve.png` | `rates/curve_nodes.csv` | `2c01228d4f6f66b4c44d7eeaf1fa285a34eb19f9` | Synthetic OIS sample output |
| `rates-risk.png` | `rates/key_rate_dv01.csv`, `rates/scenarios.csv` | `2c01228d4f6f66b4c44d7eeaf1fa285a34eb19f9` | Synthetic OIS and trade sample output |
| `rates-value-change.png` | `rates/pnl_waterfall.csv` | `2c01228d4f6f66b4c44d7eeaf1fa285a34eb19f9` | Synthetic trade, amendment, and cash sample output |
| `portfolio-growth.png` | `portfolio/monthly_results.csv` | `ea748b81503aa8b596aff6dcd3c2e08afa03c4ff` | Deterministic synthetic public demonstration |
| `portfolio-tradeoffs.png` | `portfolio/summary.csv` | `ea748b81503aa8b596aff6dcd3c2e08afa03c4ff` | Deterministic synthetic public demonstration |
| `portfolio-attribution.png` | `portfolio/active_attribution.csv` | `ea748b81503aa8b596aff6dcd3c2e08afa03c4ff` | Deterministic synthetic public demonstration |

`portfolio/bootstrap_uncertainty.csv` is a published diagnostic download rather than a figure input. File sizes and SHA-256 checksums are recorded in `artifact_manifest.csv`.

Rebuild the figures from the repository root with:

```powershell
python -m pip install -r tools\requirements.txt
python tools\build_research_figures.py
```
