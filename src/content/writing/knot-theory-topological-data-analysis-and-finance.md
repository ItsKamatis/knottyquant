---
title: "Knot Theory, Topological Data Analysis, and Finance"
slug: "knot-theory-topological-data-analysis-and-finance"
summary: "Knot theory has a clear role in studying physical entanglement. Its connection to finance is narrower and more speculative than the growing literature on topological data analysis."
published: 2026-07-14
topics:
  - "Topology"
  - "Topological data analysis"
  - "Financial markets"
  - "Risk"
status: "published"
seoDescription: "A careful distinction between knot theory and topological data analysis, with an evidence-based review of financial applications."
references:
  - label: "Niemyska et al. (2022), AlphaKnot"
    url: "https://academic.oup.com/nar/article/50/W1/W44/6591522"
  - label: "Rubach et al. (2024), AlphaKnot 2.0"
    url: "https://doi.org/10.1093/nar/gkae443"
  - label: "Racorean (2014), Braided and Knotted Stocks"
    url: "https://arxiv.org/abs/1404.6637"
  - label: "Racorean (2014), Decoding Stock Market Behavior"
    url: "https://arxiv.org/abs/1406.3531"
  - label: "Gidea and Katz (2018), Landscapes of crashes"
    url: "https://doi.org/10.1016/j.physa.2017.09.028"
  - label: "Ismail et al. (2022), Early warning signals"
    url: "https://doi.org/10.1016/j.physa.2021.126459"
  - label: "Guritanu, Barbierato, and Gatti (2025), Topological machine learning"
    url: "https://doi.org/10.3390/computers14100408"
  - label: "Gidea (2017), Critical transitions in financial networks"
    url: "https://arxiv.org/abs/1701.06081"
  - label: "Yen and Cheong (2021), Singapore and Taiwan markets"
    url: "https://doi.org/10.3389/fphy.2021.572216"
  - label: "Yen, Xia, and Cheong (2021), Financial market correlations"
    url: "https://doi.org/10.3390/e23091211"
  - label: "Acemoglu, Ozdaglar, and Tahbaz-Salehi (2015), Systemic risk"
    url: "https://doi.org/10.1257/aer.20130456"
  - label: "Souto (2023), Topological tail dependence"
    url: "https://doi.org/10.1016/j.jfds.2023.100107"
  - label: "Souto (2024), Corrigendum"
    url: "https://doi.org/10.1016/j.jfds.2024.100135"
  - label: "Kim et al. (2021), Flash crash"
    url: "https://doi.org/10.1016/j.topol.2020.107523"
  - label: "Goel, Filipovic, and Pasricha (2025), Sparse portfolio selection"
    url: "https://doi.org/10.1080/14697688.2025.2544762"
  - label: "Goel, Pasricha, and Kanniainen (2026), Sparse index tracking"
    url: "https://doi.org/10.1016/j.omega.2025.103432"
---

Topology studies properties of shape that survive continuous deformation. That broad description covers several distinct subjects. Knot theory studies entangled curves. Topological data analysis, or TDA, constructs summaries of the shape of data. They share mathematical ancestry, but they do not answer the same questions.

This distinction matters in finance. Direct attempts to treat market paths as braids or knots exist, but the evidence is exploratory. A larger literature uses persistent homology, a central TDA method, to summarize rolling return clouds, correlation networks, and time-delay embeddings. That work has produced credible research questions in market-state monitoring, volatility forecasting, and portfolio construction. It has not established a reliable crash predictor, a general source of trading alpha, or broad institutional adoption.

## 1. Knot theory and TDA are related but different

A mathematical knot is an embedding of a circle in three-dimensional space:

$$
K:S^1\hookrightarrow\mathbb{R}^3.
$$

Two knots are treated as equivalent if one can be continuously deformed into the other without cutting the curve or passing it through itself. Knot invariants, including the Alexander, Jones, and HOMFLY-PT polynomials, help distinguish equivalence classes.

TDA usually begins with a different object: a finite dataset equipped with a distance or similarity measure. For a point cloud $X$, a Vietoris-Rips complex at scale $\epsilon$ is

$$
\operatorname{VR}_{\epsilon}(X)
=
\left\{
\sigma\subseteq X:
d(x_i,x_j)\leq \epsilon
\ \text{for every}\ x_i,x_j\in\sigma
\right\}.
$$

As $\epsilon$ increases, these complexes form a filtration. Persistent homology records when connected components, loops, and higher-dimensional voids appear and disappear. A feature born at $b_i$ and dying at $d_i$ has lifetime

$$
\ell_i=d_i-b_i.
$$

A persistent $H_1$ class is a loop in a filtered simplicial complex. It is not automatically a knotted curve in three-dimensional space. No overcrossing or undercrossing information is required, and computing persistent homology does not generally produce a Jones polynomial. Saying that both methods are topological is accurate; treating them as interchangeable is not.


## 2. Direct knot and braid constructions in finance

A small set of papers has attempted a more literal transfer of knot theory to markets. In ["Braided and Knotted Stocks in the Stock Market"](https://arxiv.org/abs/1404.6637), Ovidiu Racorean arranges Dow Jones component price paths on a common chart, assigns overcrossings and undercrossings when paths cross, treats those crossings as braid generators, and closes the braid into a knot. Alexander-Conway and Jones polynomials are then computed for selected constructions. A related preprint, ["Decoding Stock Market Behavior with the Topological Quantum Computer"](https://arxiv.org/abs/1406.3531), proposes interpreting the resulting Jones polynomial as a market indicator.

These are mathematically imaginative constructions. They are not yet persuasive empirical finance.

Several choices occur before an invariant can be calculated: the assets and sample period, normalization, strand ordering, crossing convention, sampling frequency, and closure rule. Unless those choices are fixed before observing outcomes and shown to be stable under reasonable perturbations, the resulting knot may primarily encode the analyst's representation decisions.

The cited papers are arXiv preprints, and their own framing treats practical market applications as possibilities. They do not provide the walk-forward, benchmarked, transaction-cost-aware evidence required to treat a Jones polynomial as a trading or risk signal. The appropriate classification is exploratory direct knot theory, not validated quantitative finance.

## 3. Better-supported applications of TDA

The stronger financial literature concerns persistent homology rather than knot polynomials.

A common pipeline begins with an $N$-asset return vector and a rolling window:

$$
r_t=(r_{1t},\ldots,r_{Nt}),
\qquad
X_t=\{r_{t-W+1},\ldots,r_t\}.
$$

The researcher chooses a representation, distance, filtration, homology dimension, and summary such as a persistence landscape, landscape norm, persistent entropy, or Wasserstein distance between adjacent diagrams. Every one of those choices is part of the model.

### Structural change and market stress

[Gidea and Katz](https://doi.org/10.1016/j.physa.2017.09.028) applied rolling persistent homology to four U.S. equity indices around the dot-com and 2007-2009 crises. They documented changes in persistence-landscape norms around those historical episodes. [Ismail et al.](https://doi.org/10.1016/j.physa.2021.126459) combined landscape norms with critical-slowing-down indicators across U.S., Singaporean, and Malaysian markets and reported significant pre-crisis trends in selected indicators.

These studies show that topological summaries can characterize changes in historical market geometry. They should not be read as proof of a general crash-forecasting system. Much of the early evidence is retrospective, relies on a small number of exceptional episodes, and leaves substantial freedom in window and threshold selection.

A more recent study by [Guritanu, Barbierato, and Gatti](https://doi.org/10.3390/computers14100408) imposed a strictly causal warning rule on four U.S. indices. At its reported fixed operating point, precision and recall were both 0.5, with an average lead of roughly 34 days for successful early warnings. That is useful because it exposes both the signal and its limitations: a causal detector can produce advance warnings, but misses and false alarms remain material.

### Correlation networks and systemic-risk monitoring

Another approach converts rolling correlations into distances, often using

$$
d_{ij,t}=\sqrt{2\left(1-\rho_{ij,t}\right)},
$$

then studies a filtration of the resulting weighted network. [Gidea](https://arxiv.org/abs/1701.06081) documented changes in the persistent homology of a DJIA correlation network before the 2007-2008 crisis. [Yen and Cheong](https://doi.org/10.3389/fphy.2021.572216) used Betti numbers, persistence diagrams, entropy, and related summaries to compare market states in Singapore and Taiwan. [Yen, Xia, and Cheong](https://doi.org/10.3390/e23091211) combined TDA with correlation filtering and Ollivier-Ricci curvature in a case study of a Taiwan market crash. That work analyzes the geometry of one historical episode; it does not establish a general detector.

This is a plausible way to monitor the organization of market co-movement across thresholds. It is only systemic-risk-adjacent. A return-correlation network does not by itself identify balance-sheet exposures, liquidity channels, or causal shock propagation. Those mechanisms are central to financial-network models such as [Acemoglu, Ozdaglar, and Tahbaz-Salehi](https://doi.org/10.1257/aer.20130456). Persistent homology can summarize a dependence network; it does not convert that network into a causal contagion model.

### Volatility forecasting

[Souto](https://doi.org/10.1016/j.jfds.2023.100107) incorporated Wasserstein distances between persistence diagrams into nonlinear and neural-network forecasts of realized volatility. The paper reports improvements during turbulent periods. [Souto and Moradi](https://doi.org/10.1016/j.dajour.2024.100512) subsequently tested the approach on individual S&P 100 stocks.

This is a credible forecasting question: does a topological feature add information after ordinary volatility and dependence variables are included? The relevant comparison is incremental:

$$
y_{t+h}
=
\alpha+\beta^\top z_t+\gamma\,\phi(D_t)+\varepsilon_{t+h},
$$

where $z_t$ contains conventional predictors and $\phi(D_t)$ is a topological summary. The useful result is not that $\phi(D_t)$ fits a crisis sample; it is that it improves truly out-of-sample forecasts over strong baselines. The existing studies are encouraging, but this remains a developing literature. The original 2023 article also has a [corrigendum](https://doi.org/10.1016/j.jfds.2024.100135) adding missing figure attribution; it does not report a correction to the empirical results.

### Event and anomaly analysis

[Kim et al.](https://doi.org/10.1016/j.topol.2020.107523) used persistence landscapes and dynamic time-series methods to study the 2010 Flash Crash. This supports TDA as an event-analysis tool: it can reveal structure in a multivariate episode that is difficult to summarize with one volatility statistic.

One case study is not evidence of a general real-time anomaly detector. A production claim would require evaluation across many ordinary and extreme days, with the event definition and alert threshold fixed in advance.

### Portfolio construction

Recent peer-reviewed work has moved from market description to portfolio decisions. [Goel, Filipovic, and Pasricha](https://doi.org/10.1080/14697688.2025.2544762) introduced time-aware distances between persistence diagrams and landscapes for clustering stocks in sparse index-tracking and Markowitz portfolios. Their empirical study covers S&P data from 2009 through 2022, and the authors report improved sparse-portfolio results across several measures.

[Goel, Pasricha, and Kanniainen](https://doi.org/10.1016/j.omega.2025.103432) use persistent homology to inform regularization in sparse index tracking. Their 23-year S&P 500 study reports out-of-sample improvements over Elastic Net and SLOPE benchmarks, including risk and trading-cost measures.

These papers make portfolio construction one of the more concrete TDA research directions. They are also recent. Independent replication should examine point-in-time membership, survivorship controls, rebalancing conventions, turnover, cost assumptions, parameter stability, and whether the benefit survives simpler clustering or covariance features.

## 4. Evidence ladder

"Demonstrated" means that a method has been implemented and studied for the stated task. It does not mean production adoption or guaranteed economic value.

<div class="evidence-table" role="region" aria-label="Evidence ladder" tabindex="0">
  <table>
    <thead><tr><th>Status</th><th>Claim supported by current evidence</th><th>Main boundary</th></tr></thead>
    <tbody>
      <tr><td>Demonstrated</td><td>Knot invariants and closure methods can screen predicted protein structures for entanglement.</td><td>A computationally knotted model is not an experimentally confirmed protein knot.</td></tr>
      <tr><td>Demonstrated</td><td>Persistent homology can summarize rolling return clouds and correlation networks and distinguish some historical market states.</td><td>Much of the evidence is retrospective and episode-specific.</td></tr>
      <tr><td>Demonstrated</td><td>Topological features can be included in causal detection, forecasting, and optimization pipelines.</td><td>Pipeline feasibility is weaker evidence than durable incremental value.</td></tr>
      <tr><td>Promising</td><td>Persistence features may add information for realized-volatility forecasts during turbulent periods.</td><td>Evidence is still concentrated in a small literature and depends on representation choices.</td></tr>
      <tr><td>Promising</td><td>TDA-informed clustering or regularization may improve sparse portfolios and index tracking.</td><td>The strongest papers are recent and need independent replication.</td></tr>
      <tr><td>Promising</td><td>Topological monitoring may complement conventional measures of changing market dependence.</td><td>Correlation geometry does not establish contagion mechanisms or causal systemic risk.</td></tr>
      <tr><td>Unestablished</td><td>A Jones or Alexander polynomial derived from braided stock paths is a reliable trading indicator.</td><td>No convincing walk-forward, benchmarked, cost-aware validation has been presented.</td></tr>
      <tr><td>Unestablished</td><td>TDA reliably predicts crashes or eliminates false alarms.</td><td>Published causal tests still contain misses and false positives.</td></tr>
      <tr><td>Unestablished</td><td>TDA is broadly deployed by financial institutions or is a standard production technique.</td><td>Public research papers do not establish adoption.</td></tr>
      <tr><td>Unestablished</td><td>Topological features generate persistent alpha after realistic costs.</td><td>Most studies address description, forecasting, clustering, or tracking, not net alpha.</td></tr>
    </tbody>
  </table>
</div>

## 5. What a serious quantitative test requires

A useful TDA study should begin with a narrow decision problem: forecast realized volatility, identify a market state, estimate a portfolio risk penalty, or select assets. "Find market topology" is not a sufficiently testable objective.

The empirical design should then include:

1. **A pre-specified representation.** Define returns, scaling, universe, missing-data treatment, window length, distance, filtration, homology dimensions, and summary statistics using training data only.
2. **Strong ordinary baselines.** Compare against volatility, average correlation, covariance eigenvalues, drawdown, VIX where appropriate, HAR/GARCH forecasts, and non-topological clustering methods.
3. **Chronological evaluation.** Use expanding or rolling walk-forward tests. Purge or embargo observations when feature windows or forecast labels overlap.
4. **Nested tuning.** Choose window lengths, thresholds, and filtration settings inside each training fold rather than on the final test period.
5. **Ablation tests.** Remove topological features, replace them with low-order geometric summaries, shuffle temporal order, and test whether the claimed information is simply volatility or correlation in another form.
6. **Statistical and economic metrics.** Report forecast-loss comparisons, calibration, alert precision and recall, turnover, transaction costs, tracking error, drawdown, and sensitivity to execution assumptions.
7. **Cross-market replication.** Test multiple universes and market regimes without redefining the method for each crisis.
8. **Reproducibility.** Release code, configuration, data provenance, and a complete record of failed or unstable specifications.

The research question is therefore modest:

> After all modeling choices are fixed using past data, does a topological feature improve a defined out-of-sample decision relative to simpler information available at the same time?

That is a harder test than drawing a persistence diagram around a known crash. It is also the test that matters.

## 6. Conclusion

Direct knot theory and TDA should be kept separate.

Knot theory is directly useful when the object is an entangled curve, as in protein backbones. Mapping market paths into braids and calculating knot polynomials is possible, but the current finance evidence is speculative. It should be presented as an open construction, not a trading result.

TDA has a more substantial financial literature. Persistent homology has been used to study historical stress, changing correlation structure, realized volatility, flash crashes, and sparse portfolios. The careful conclusion is that these features may provide complementary descriptions of market structure. Their incremental forecasting value, stability, and usefulness after costs remain empirical questions.

KnottyQuant takes its name from a genuine mathematical idea, not from a claim that markets are literally knots. The relevant research habit is broader: define the object, preserve the distinction between a mathematical construction and economic evidence, and test whether a complicated representation earns its place.

## Primary references

1. Niemyska, W., et al. (2022). ["AlphaKnot: server to analyze entanglement in structures predicted by AlphaFold methods."](https://academic.oup.com/nar/article/50/W1/W44/6591522) *Nucleic Acids Research*, 50(W1), W44-W50.
2. Rubach, P., et al. (2024). ["AlphaKnot 2.0: a web server for the visualization of proteins' knotting and a database of knotted AlphaFold-predicted models."](https://doi.org/10.1093/nar/gkae443) *Nucleic Acids Research*, 52(W1), W187-W193.
3. Racorean, O. (2014). ["Braided and Knotted Stocks in the Stock Market: Anticipating the Flash Crashes."](https://arxiv.org/abs/1404.6637) arXiv:1404.6637.
4. Racorean, O. (2014). ["Decoding Stock Market Behavior with the Topological Quantum Computer."](https://arxiv.org/abs/1406.3531) arXiv:1406.3531.
5. Gidea, M., and Katz, Y. (2018). ["Topological data analysis of financial time series: Landscapes of crashes."](https://doi.org/10.1016/j.physa.2017.09.028) *Physica A*, 491, 820-834.
6. Ismail, M. S., Noorani, M. S. M., Ismail, M., Razak, F. A., and Alias, M. A. (2022). ["Early warning signals of financial crises using persistent homology."](https://doi.org/10.1016/j.physa.2021.126459) *Physica A*, 586, 126459.
7. Guritanu, E., Barbierato, E., and Gatti, A. (2025). ["Topological Machine Learning for Financial Crisis Detection."](https://doi.org/10.3390/computers14100408) *Computers*, 14(10), 408.
8. Gidea, M. (2017). ["Topology data analysis of critical transitions in financial networks."](https://arxiv.org/abs/1701.06081) arXiv:1701.06081.
9. Yen, P. T.-W., and Cheong, S. A. (2021). ["Using Topological Data Analysis and Persistent Homology to Analyze the Stock Markets in Singapore and Taiwan."](https://doi.org/10.3389/fphy.2021.572216) *Frontiers in Physics*, 9, 572216.
10. Yen, P. T.-W., Xia, K., and Cheong, S. A. (2021). ["Understanding Changes in the Topology and Geometry of Financial Market Correlations during a Market Crash."](https://doi.org/10.3390/e23091211) *Entropy*, 23(9), 1211.
11. Acemoglu, D., Ozdaglar, A., and Tahbaz-Salehi, A. (2015). ["Systemic Risk and Stability in Financial Networks."](https://doi.org/10.1257/aer.20130456) *American Economic Review*, 105(2), 564-608.
12. Souto, H. G. (2023). ["Topological tail dependence: Evidence from forecasting realized volatility."](https://doi.org/10.1016/j.jfds.2023.100107) *The Journal of Finance and Data Science*, 9, 100107.
13. Souto, H. G., and Moradi, A. (2024). ["A generalization of the Topological Tail Dependence theory: From indices to individual stocks."](https://doi.org/10.1016/j.dajour.2024.100512) *Decision Analytics Journal*, 12, 100512.
14. Souto, H. G. (2024). [Corrigendum to "Topological tail dependence."](https://doi.org/10.1016/j.jfds.2024.100135) *The Journal of Finance and Data Science*, 10, 100135.
15. Kim, W., Kim, Y.-J., Lee, G., and Kook, W. (2021). ["Investigation of flash crash via topological data analysis."](https://doi.org/10.1016/j.topol.2020.107523) *Topology and its Applications*, 301, 107523.
16. Goel, A., Filipovic, D., and Pasricha, P. (2025). ["Sparse portfolio selection via topological data analysis based clustering."](https://doi.org/10.1080/14697688.2025.2544762) *Quantitative Finance*, 25(8), 1261-1291.
17. Goel, A., Pasricha, P., and Kanniainen, J. (2026). ["Risk reduced sparse index tracking portfolio: A topological data analysis approach."](https://doi.org/10.1016/j.omega.2025.103432) *Omega*, 138, 103432.
