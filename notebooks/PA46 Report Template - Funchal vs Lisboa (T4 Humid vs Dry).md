# PA46 – Technical Report Template (Funchal vs Lisboa, T4 Humid vs Dry Regime)

Data Stream Mining – Practical Assignment I · Photography and Audiovisual Equipment Storage

**Students:** \[FILL: Student A, number\] · \[FILL: Student B, number\] **Group:** \[FILL: GroupYY\] **Seed:** \[FILL: e.g. 42\]

## 0. How to use this template

**0a. Assignment card (fixed – do not change).**

| Item | Value |
| --- | --- |
| Code | PA46 |
| City A / City B | Funchal / Lisboa (order as on the card; confirm which student owns which city) |
| Business scenario | Photography and Audiovisual Equipment Storage |
| Target | T4 Humid vs Dry Regime: τH = Q0.50(H) from pooled warm-up of both cities; y\_t = 1 if H\_t ≥ τH, else 0 |
| Card question | Which city has the more favourable humidity regime from an environmental-control perspective? |
| Files to submit | PA46\_GroupYY\_Report.pdf and PA46\_GroupYY\_Audit.zip |

**0b. Rules that cost marks if broken (Chapter 18).** Never use humidity(t) to predict y\_t. Estimate τH once from pooled warm-up and freeze it. No random split. Evaluate before learning. Same chronological history for every model. Document every deletion or correction. Reported numbers must be reproducible from the audit ZIP.

**0c. Where your research questions live in the report.**

| Research question | Primary section | Evidence type |
| --- | --- | --- |
| RQ1 Baseline occurrence, persistence, diurnal cycle, HVAC runtime | 3, 4, 5 | Descriptive/temporal |
| RQ2 Fungal zone, condensation, ESD, cost threshold | 3, 4, 5 (data), 8 (cost assumptions) | Descriptive + explicit assumptions |
| RQ3 Lead time, FN vs FP cost, model efficiency | 6, 7, 8 | Predictive + computational |

**0d. Scope warnings (important for the Business Understanding and Limitations marks).**

- The target is a **median split**, so pooled warm-up class balance is about 50/50. Event frequency **differs by city**, and that difference is the comparison. Accuracy is less misleading than for rare events but still report Precision, Recall, Macro-F1 and the confusion matrix.
- **Fungal risk (RH > 60–65 %)** and **ESD risk (low RH)** use thresholds different from τH. Treat them as clearly labelled *supplementary descriptive thresholds* with a cited source. They are not the official target and must not replace it.
- **Condensation** needs indoor conditions; the data are outdoor. Frame it as an outdoor temperature-drop/humidity-surge association, not as measured indoor condensation.
- **HVAC runtime and financial thresholds** are not in the dataset. Present runtime as a *proxy* (hours with y\_t = 1 or RH above a stated setpoint) and costs as *labelled illustrative assumptions with a sensitivity analysis*. Never state invented costs as facts.
- **AI policy:** every interpretation, discussion, recommendation and conclusion must be written by you. Fill the placeholders yourselves.

**0e. Page budget (body 6–8 pages; cover, references, appendix excluded).**

| Section | Pages |
| --- | --- |
| 1 Context | 0.4 |
| 2 Data and stream | 0.9 |
| 3 Funchal | 0.9 |
| 4 Lisboa | 0.9 |
| 5 Comparison | 0.9 |
| 6 Experiment | 0.9 |
| 7 Results | 1.4 |
| 8 Recommendations | 0.7 |
| 9 Limitations | 0.3 |
| 10 AI statement | 0.2 |
| Total | about 7.5 |

**0f. Rubric map (what earns full marks).**

| Component (weight) | Full-marks evidence | Sections |
| --- | --- | --- |
| Business understanding (10 %) | Decision stated, card read correctly, claims limited to humidity evidence | 1, 8, 9 |
| Data preparation and stream (15 %) | Chronology, quality checks, warm-up, frozen τH, reproducible preprocessing | 2 |
| City-level analysis (15 %) | Equal treatment of both cities, statistics, temporal behaviour, class distribution, windows, business interpretation | 3, 4 |
| Features and target (15 %) | Correct T4, warm-up-only threshold, leak-free features, justified Rep A vs Rep B | 2, 6 |
| DSM methodology (20 %) | Prequential protocol, five models, same histories, correct metrics, cost per event | 6, 7 |
| Interpretation and recommendations (15 %) | Evidence linked across data, metrics, cost, operations; two separate recommendations | 5, 7, 8 |
| Reproducibility (10 %) | README, versions, seed, parameters, traceable outputs | 2, 6, Audit ZIP |

## 1. Business Context and Objective

*Page target 0.4. Rubric: Business understanding (10 %).*

**1a. Business scenario.** \[FILL: who stores photography and audiovisual equipment (cameras, lenses, sensors, recorders, rental stock); what environmental failure modes matter (fungus on lens coatings, condensation on electronics, ESD during handling); who decides and what they decide (choose a storage/rental location and size the dehumidification plan).\]

**1b. Decision and card question.** State verbatim: *Which city has the more favourable humidity regime from an environmental-control perspective?* Then restate in your own words what "favourable" means: \[FILL: fewer and shorter high-humidity episodes, lower predicted dehumidification workload, lower asset-damage exposure\].

**1c. Study design in one paragraph.** \[FILL: Funchal and Lisboa hourly Open-Meteo streams; T4 event; two representations; five incremental models; two separate recommendations.\] Say explicitly that the model does not make the business decision.

**1d. Research questions.** List RQ1–RQ3 with the sub-questions as numbered items (RQ1a–d, RQ2a–d, RQ3a–c). Add one sentence per RQ saying which kind of evidence answers it (descriptive, assumption-based, or predictive).

**1e. Scope statement.** \[FILL: this study uses humidity-related weather evidence only; rent, wages, building envelope, indoor HVAC specs, tax, transport and insurance are outside the dataset.\]

## 2. Data and Stream Construction

*Page target 0.9. Rubric: Data preparation (15 %), Features and target (15 %), Reproducibility (10 %).*

### 2.1 Stream configuration

**2.1a. Source and retrieval.** Open-Meteo \[FILL: archive/historical API endpoint, retrieval date, parameters\]. Coordinates: Funchal \[FILL lat, lon\], Lisboa \[FILL lat, lon\]. Cite the data source in References.

**2.1b. Period and resolution.** \[FILL: start date to end date, hourly, N observations per city, timezone setting and why identical for both cities, handling of daylight-saving changes in Lisboa\].

**2.1c. Variables.** Temperature, relative humidity, precipitation, wind speed. \[FILL: exact Open-Meteo variable names and units.\]

**2.1d. Chronology and alignment.** \[FILL: sorted by timestamp, duplicates checked, gaps checked, both cities aligned on identical timestamps, evaluation order preserved.\]

**2.1e. Warm-up rule.** \[FILL: first X % or first N hours of both streams pooled; same rule for both cities; the evaluation stream starts immediately after.\]

**2.1f. Data quality log (small table).**

| Check | Funchal | Lisboa | Action taken |
| --- | --- | --- | --- |
| Missing values | \[FILL\] | \[FILL\] | \[FILL\] |
| Duplicate or out-of-order timestamps | \[FILL\] | \[FILL\] | \[FILL\] |
| Impossible values (RH outside 0–100, negative precipitation or wind) | \[FILL\] | \[FILL\] | \[FILL\] |
| Extreme but valid values kept | \[FILL\] | \[FILL\] | Kept, documented |

State explicitly that extreme values were **not** removed unless shown to be invalid.

### 2.2 Target and temporal alignment

**2.2a. Threshold.** τH = Q0.50 of relative humidity over the **pooled warm-up** of Funchal and Lisboa = \[FILL value\] %. Estimated once, frozen before evaluation, never recomputed.

**2.2b. Target.** y\_t = 1 if H\_t ≥ τH, else 0. Report the warm-up class balance (pooled and per city).

**2.2c. Leakage control.** Current RH(t) defines y\_t, so RH(t) is **not** a predictor. Valid inputs: temperature(t−1), RH(t−1), precipitation(t−1), wind(t−1) and rolling features ending at t−1. \[FILL: one sentence on how your code enforces this, e.g. shift(1) before rolling.\]

**2.2d. Alignment checklist.** Lags strictly before t; windows end at t−1; threshold from warm-up only; any scaling fitted on warm-up or incrementally; chronology kept. Tick each in the audit ZIP README.

**2.2e. Supplementary descriptive thresholds (not targets).** Fungal-risk RH threshold \[FILL: 60 % or 65 %, cite source\]; low-RH/ESD threshold \[FILL: value, cite source or justify as a warm-up quantile\]. Say these are used only in Sections 3–5.

## 3. City A Analysis: Funchal

*Page target 0.9. Primary owner: Student \[FILL\]. Rubric: City-level analysis (15 %). Use identical structure in Section 4.*

**3a. Descriptive statistics (table).** Mean, SD, min, quartiles, max for temperature, RH, precipitation, wind over the evaluation stream. \[FILL table\]

**3b. Temporal evolution.** Monthly or seasonal RH and rolling mean (24 h / 7 d). \[FILL: what changes over the year and why it matters to a storage operator.\]

**3c. Target frequency and class distribution.** Share of y\_t = 1 in warm-up and evaluation; evolution of rolling event rate (e.g. 30-day window); is class balance stable? \[FILL\]

**3d. Persistence (RQ1b).** Distribution of consecutive-hour run lengths of y\_t = 1: median, mean, 90th percentile, longest run, share of events in blocks ≥ 6 h. Conclusion: brief spikes or sustained blocks? \[FILL\]

**3e. Diurnal profile (RQ1c).** Event probability by hour of day, summarised as morning / day / night. Define the periods \[FILL, e.g. 06–12, 12–20, 20–06\] and justify them. \[FILL\]

**3f. HVAC workload proxy (RQ1d).** Hours per year with y\_t = 1 and average daily active hours. Label as a proxy for dehumidifier runtime, not an engineering estimate. \[FILL\]

**3g. Asset-risk exposure (RQ2a, RQ2c).** Share of hours with RH above the fungal threshold; share below the ESD threshold; longest continuous exposure. \[FILL\]

**3h. Condensation association (RQ2b).** Relationship between 1-hour temperature drop (T(t−1) − T(t−2)) and subsequent RH rise (correlation or conditional event rate after drops ≥ X °C). Note the outdoor-vs-indoor caveat. \[FILL\]

**3i. Extreme observations.** Highest-humidity episodes and what they mean operationally. Kept, not removed. \[FILL\]

**3j. Figure 1 (original analysis).** Suggested: 3-panel figure with rolling event rate, run-length histogram, hour-of-day profile. Caption must state the finding, not "stream profile". \[FILL caption\]

**3k. Business interpretation.** Two to three sentences linking 3c–3h to equipment storage. \[FILL – written by you\]

## 4. City B Analysis: Lisboa

*Page target 0.9. Primary owner: Student \[FILL\]. Mirror Section 3 exactly (4a–4k).*

**4a–4k.** Repeat items 3a–3k for Lisboa with identical statistics, windows, thresholds and figure design. Unequal treatment of the two cities is explicitly penalised. \[FILL each\]

## 5. Comparative Data Analysis

*Page target 0.9. This is the evidence for the **Business Recommendation**. Rubric: City-level analysis and Interpretation.*

**5a. Side-by-side summary table.**

| Metric | Funchal | Lisboa | Difference |
| --- | --- | --- | --- |
| Event rate (y = 1), evaluation | \[FILL\] | \[FILL\] | \[FILL\] |
| Median / P90 run length (h) | \[FILL\] | \[FILL\] | \[FILL\] |
| Share of events in blocks ≥ 6 h | \[FILL\] | \[FILL\] | \[FILL\] |
| Event rate morning / day / night | \[FILL\] | \[FILL\] | \[FILL\] |
| Hours/year y = 1 (HVAC proxy) | \[FILL\] | \[FILL\] | \[FILL\] |
| Hours/year RH above fungal threshold | \[FILL\] | \[FILL\] | \[FILL\] |
| Hours/year RH below ESD threshold | \[FILL\] | \[FILL\] | \[FILL\] |
| Seasonal variability of rolling event rate (SD) | \[FILL\] | \[FILL\] | \[FILL\] |

**5b. Statistical support.** Add uncertainty to key differences: bootstrap CI over blocks (e.g. weekly blocks, to respect autocorrelation) or a two-proportion comparison with a stated caveat about autocorrelation. \[FILL\]

**5c. Figure 2 (original analysis).** Suggested: overlaid hour-of-day profiles and run-length distributions for both cities. Caption states the finding. \[FILL\]

**5d. Answers to RQ1 and RQ2 (data-based).** One short paragraph each: RQ1a lower baseline city; RQ1b persistence; RQ1c diurnal; RQ1d workload; RQ2a fungal exposure; RQ2b condensation; RQ2c ESD. Write what the evidence supports and what it does not. \[FILL – written by you\]

**5e. Trade-off statement.** One city may have fewer high-humidity hours but more low-humidity (ESD) hours. State this honestly and say how it affects "favourable". \[FILL\]

## 6. Data Stream Mining Experiment

*Page target 0.9. Rubric: DSM methodology (20 %), Features and target (15 %), Reproducibility (10 %).*

### 6.1 Feature representations

|  | Representation A (previous state) | Representation B (temporal context) |
| --- | --- | --- |
| Features | temperature(t−1), RH(t−1), precipitation(t−1), wind(t−1) | All of A plus the items below |
| Delta | – | ΔRH or ΔT: value(t−1) − value(t−2) |
| Rolling mean | – | \[FILL: RH 6 h and/or 24 h, ending at t−1\] |
| Rolling SD | – | \[FILL: window, variable\] |
| Recent-condition feature | – | \[FILL: share of y = 1 in previous 24 h, or rainy hours in previous 24 h\] |

**6.1a.** Justify window sizes for humidity operations (e.g. 6 h = short HVAC response, 24 h = daily cycle). Confirm all windows end at t−1. \[FILL\]

**6.1b.** Hypothesis: Does recent temporal context improve event prediction over the latest observation alone? \[FILL: expected direction and why\]

### 6.2 Models and parameters

| Model | Library/class | Key parameters | Seed |
| --- | --- | --- | --- |
| 1 Gaussian Naive Bayes | \[FILL\] | defaults \[FILL\] | – |
| 2 Online Logistic Regression | \[FILL\] | learning rate, scaler \[FILL\] | \[FILL\] |
| 3 Hoeffding Tree | \[FILL\] | grace period, δ, split criterion \[FILL\] | \[FILL\] |
| 4 Online Bagging | \[FILL\] | base learner, ensemble size \[FILL\] | \[FILL\] |
| 5 Adaptive Random Forest | \[FILL\] | n\_models, drift detector \[FILL\] | \[FILL\] |
| Optional: persistence baseline ŷ\_t = 1\[RH(t−1) ≥ τH\] | own code | none | – |

The persistence baseline is an optional addition that costs nothing and is leak-free. It does not replace the five mandatory models. Include optional learners only if justified.

### 6.3 Evaluation protocol

**6.3a.** PREDICT → EVALUATE → LEARN on every event in chronological order, after the warm-up. State whether the warm-up is also used to pre-train models and keep this identical for all models. \[FILL\]

**6.3b.** Held constant: target, τH, features per representation, history, warm-up, metrics, seed. Changed one at a time: model, then representation, then city. \[FILL\]

**6.3c.** Fresh model instance for every city × representation × model run (2 × 2 × 5 = 20 runs, plus optional baseline).

**6.3d.** Metrics: Accuracy, Macro-F1, Precision (class 1), Recall (class 1), confusion matrix; prediction time per event and update time per event (µs, measured the same way and on the same machine for all models); optional model size (nodes, ensemble size). State cumulative vs windowed metrics, and the window length if windowed. \[FILL\]

**6.3e.** Timing method: \[FILL: perf\_counter around predict and learn, hardware, warm cache, repetitions, how timing overhead from feature computation is handled\].

**6.3f.** Environment: Python \[FILL\], packages and versions \[FILL\], period \[FILL\], seed \[FILL\].

### 6.4 Cost-sensitive evaluation design (RQ3b)

**6.4a.** Define expected cost per event: Cost = (C\_FN · FN + C\_FP · FP) / N. C\_FN = damage and replacement exposure from an undetected humidity episode; C\_FP = energy and wear from an unnecessary dehumidifier activation.

**6.4b.** Because real costs are unknown, analyse the **ratio r = C\_FN / C\_FP** over a range (e.g. 1, 2, 5, 10, 20, 50) and report the ratio at which model rankings change. Cite any figure taken from the literature or vendor data and label the rest as illustrative assumptions. \[FILL\]

## 7. Results and Discussion

*Page target 1.4. Rubric: DSM methodology and Interpretation (15 %). Do not narrate numbers; link evidence.*

### 7.1 Predictive performance – Funchal

**7.1a. Results table (Rep A and Rep B, five models).**

| Model | Rep | Accuracy | Macro-F1 | Precision | Recall |
| --- | --- | --- | --- | --- | --- |
| GNB | A / B | \[FILL\] | \[FILL\] | \[FILL\] | \[FILL\] |
| Online LR | A / B | \[FILL\] | \[FILL\] | \[FILL\] | \[FILL\] |
| Hoeffding Tree | A / B | \[FILL\] | \[FILL\] | \[FILL\] | \[FILL\] |
| Online Bagging | A / B | \[FILL\] | \[FILL\] | \[FILL\] | \[FILL\] |
| ARF | A / B | \[FILL\] | \[FILL\] | \[FILL\] | \[FILL\] |

**7.1b. Confusion matrices** for the best and the baseline model (full set in appendix). \[FILL\]

**7.1c. Interpretation.** Class balance in Funchal, how metrics relate (e.g. Precision vs Recall), effect of Rep B over Rep A, and what this means for pre-activating dehumidifiers. \[FILL – written by you\]

### 7.2 Predictive performance – Lisboa

**7.2a–7.2c.** Same table, confusion matrices and interpretation for Lisboa. Compare with Funchal: is one stream harder to predict, and does that relate to persistence or event rate in Section 5? \[FILL\]

### 7.3 Lead time and persistence (RQ3a)

**7.3a.** Does 1-hour-ahead information give usable warning? Compare against the persistence baseline: do the incremental models add value beyond "it was humid an hour ago"? Discuss what lead time one hourly step really provides relative to dehumidifier ramp-up. \[FILL\]

**7.3b.** Optional: error analysis around transitions (dry → humid) where false negatives concentrate. \[FILL\]

### 7.4 Computational evidence and efficiency trade-off (RQ3c)

**7.4a. Cost table.**

| Model | Prediction µs/event | Update µs/event | Size (optional) | Macro-F1 gain vs GNB |
| --- | --- | --- | --- | --- |
| GNB | \[FILL\] | \[FILL\] | \[FILL\] | 0 |
| Online LR | \[FILL\] | \[FILL\] | \[FILL\] | \[FILL\] |
| Hoeffding Tree | \[FILL\] | \[FILL\] | \[FILL\] | \[FILL\] |
| Online Bagging | \[FILL\] | \[FILL\] | \[FILL\] | \[FILL\] |
| ARF | \[FILL\] | \[FILL\] | \[FILL\] | \[FILL\] |

**7.4b. Figure 3 (original analysis).** Cost–performance plot (Macro-F1 or Recall against update time) for both cities, plus the expected-cost-vs-r curves from 6.4. Caption states the finding. \[FILL\]

**7.4c. Interpretation.** Is the gain over GNB large enough to justify the extra cost at hourly arrival? Note that at hourly data every model is far below real-time limits, so justification rests on deployment simplicity, memory and drift handling rather than speed. \[FILL – written by you\]

### 7.5 Cost asymmetry (RQ3b)

**7.5a.** Using the real FN and FP counts, show expected cost per event against r for each model; identify the r above which a high-Recall model is preferable. \[FILL\]

**7.5b.** Answer: is FN significantly costlier than FP in this scenario, and what evidence or assumption supports it? \[FILL – written by you\]

## 8. Business and Technical Recommendations

*Page target 0.7. Two separate recommendations. Rubric: Interpretation and recommendations (15 %).*

### 8.1 Business Recommendation (answers the card question)

**8.1a. Recommended city:** \[FILL\].

**8.1b. Supporting evidence (descriptive and temporal only):** event rate, persistence, diurnal profile, HVAC workload proxy, fungal and ESD exposure, seasonal variability (cite Section 5 numbers). \[FILL\]

**8.1c. Operational meaning:** \[FILL: what the storage operator should expect and how to size or schedule dehumidification\].

**8.1d. Cost and maintenance threshold (RQ2d).** Present the break-even logic: preventive HVAC cost per year versus expected loss avoided (asset value × damage probability reduction). Show it as a formula with labelled illustrative inputs and a sensitivity range, not as a fact. \[FILL\]

**8.1e. Caveat:** weather humidity is one factor only; predictive scores did not determine this choice.

### 8.2 Technical Recommendation

**8.2a. Recommended streaming approach:** \[FILL: model, representation, window sizes\].

**8.2b. Justification:** event detection (Recall, Precision), class balance, Rep A vs Rep B, prediction and update cost, memory, implementation complexity, behaviour over time, and cost-asymmetry result. \[FILL\]

**8.2c. Deployment notes:** \[FILL: retraining or drift handling, monitoring metric, threshold or decision-rule adjustment for r, fallback to the persistence or GNB baseline\].

**8.2d. Conditions under which the recommendation would change.** \[FILL\]

## 9. Limitations

*Page target 0.3. Rubric: claims must not exceed the evidence.*

**9a. Data:** outdoor reanalysis data versus indoor storage conditions; hourly resolution; single historical period; possible reanalysis smoothing.

**9b. Target:** median-split definition makes events relative to the pooled pair; threshold would differ for another pair; τH is not a damage threshold.

**9c. Experimental:** single seed or limited repeats; default hyperparameters; autocorrelation in the data; timing depends on hardware and Python overhead.

**9d. Business:** cost figures are assumptions; no building, HVAC or insurance data; rent, labour, logistics excluded.

**9e. What would strengthen the study:** \[FILL: longer period, indoor sensors, hyperparameter tuning, repeated seeds\].

## 10. AI Assistance Statement

Adapt truthfully, e.g.: *Generative AI tools were used to assist with Python debugging, plotting syntax and code organisation. They were not used to interpret experimental results or produce the analysis, discussion, business recommendation, technical recommendation, or evidence-based conclusions.* If no AI was used, state that instead. \[FILL\]

## 11. References

Cite: Open-Meteo data source and API; each library (e.g. River or scikit-multiflow equivalents, NumPy, pandas, matplotlib) with version; algorithm papers (Gaussian Naive Bayes, Hoeffding Tree, Online Bagging, Adaptive Random Forest, prequential evaluation); sources for the fungal RH range and ESD humidity thresholds; sources for any cost figure. \[FILL\]

## 12. Optional Appendix

Only if needed: full confusion matrices, hyperparameter table, extra plots, quality-log detail. Not counted in the page limit; do not rely on it for key arguments.

## 13. Audit ZIP README template (PA46\_GroupYY/README.md)

- Assignment code PA46; student names and numbers; City A Funchal, City B Lisboa; scenario Photography and Audiovisual Equipment Storage; target T4; historical period; Python version; package versions; random seed.
- Folder map: src/, data/ (raw snapshots or retrieval script and date), results/ (metrics.csv, configurations.csv), figures/, requirements.txt.
- Reproduction steps: install, run script, expected outputs.
- Map every table and figure in the report to the file or script that produced it.
- Leakage and protocol statement: τH value and where frozen, lag/rolling construction line, predict-evaluate-learn loop location.

## 14. Final self-check before submission

- [ ] draftinstructions set to false in main.tex; placeholders removed; body 6–8 pages.
- [ ] Section order unchanged; margins and font untouched.
- [ ] τH from pooled warm-up, frozen, value reported.
- [ ] RH(t) absent from every feature set; all windows end at t−1.
- [ ] Both representations × five models × two cities all reported, same history.
- [ ] Accuracy, Macro-F1, Precision, Recall, confusion matrix, prediction and update time reported.
- [ ] At least two original analyses (e.g. run-length, hour-of-day, rolling event rate, cost curves) and each figure supports an argument.
- [ ] Business and Technical Recommendations separate; limitations stated; AI statement truthful.
- [ ] Files named PA46\_GroupYY\_Report.pdf and PA46\_GroupYY\_Audit.zip; both students can explain everything.
