# Validation and AI Use — Joby Aviation (JOBY), FIN 43900 Project 1

Tobey Uhm · This Markdown file is the working source; Brightspace `Validation-and-AI-Use.pdf` is the frozen record of the same content.

## 1. Decision, version, and as-of boundary

| Field | Value |
|---|---|
| Decision / user | Initiate, watch/defer, or do not initiate JOBY, for a buy-side investment committee with no current position |
| Result | **Watch / defer**; $0.00–$3.82 per share (base $0.34) vs $6.69 |
| Valuation date / price | Sept. 1, 2026 / $6.69 close (S9) |
| Source cutoff | Latest filing on or before Sept. 1, 2026: Q2 2026 10-Q, filed Aug. 6, 2026 (balance sheet June 30, 2026; cover shares Aug. 3, 2026). Nothing after Sept. 1, 2026 is used. |
| Repository / commit | `Joby-research`, branch `main`. Final submission commit: **[record the hash from `git log -1` after your last commit]** |
| Run | `python analysis.py` → `output/visible_output.json`, `output/joby_valuation_report.md` (timestamp printed in the report) |
| Environment | Python 3.13.15 (Windows 11), standard library only for the engine; Streamlit ≥1.40,<2 for the app |

## 2. Data and convention ledger

| Material input | Source | As-of / availability | Definition / units | Transformation / exclusion | Risk |
|---|---|---|---|---|---|
| Cash + short-term investments $2,263.826M | S4 10-Q balance sheet p. 3 | June 30, 2026; public Aug. 6 | USD M | Restricted cash ($1.3M current, $4.9M non-current) excluded. All counted as non-operating because H2 2026 burn is already in FCFF. | Liquidity is runway, not surplus. Shown via the funding schedule. |
| 2032 convertible notes $690.0M principal, 0.75%, conversion price $14.19, 48.63M if-converted shares; fair value $628.0M | S4 Note 6 | June 30, 2026 | USD M; shares M | Debt at principal in the bridge (value < $14.19). Fair value used for the WACC weight. | Treatment flips only if value > $14.19 (coded and tested). |
| Mortgage $30.75M at 6.784% | S4 Note 6 | June 30, 2026 | USD M | Debt | — |
| Warrants $21.505M; Blade EBITDA earnout up to $17.5M | S4 balance sheet, Notes 4 and 7 | June 30, 2026 | USD M | Warrants deducted at fair value, not added as shares. Earnout deducted at maximum. Sponsor earnout shares are already in the basic count, so their liability is not deducted. | Double counting is avoided by design. |
| Shares: basic 989.124M; RSUs 55.886M; RSAs 0.446M; early-exercised 0.533M; options 5.270M | S4 cover page and antidilution table | Aug. 3 / June 30, 2026 | M shares | Options counted at full dilution (strike not extracted) | Overstates dilution by < 0.5%. |
| H1 2026 actuals: revenue 62.885, COGS 47.101, R&D 372.132, SG&A 138.115, D&A 22.853, capex 106.559 | S4 statements pp. 4, 8 | Six months to June 30, 2026 | USD M | Removed from the FY2026 plan to form the July–Dec stub | — |
| Federal NOL $1,662.0M | S3 FY2025 10-K tax note | Dec. 31, 2025 | USD M | H1 2026 loss added; 80% usage limit | State NOLs ignored (conservative) |
| Risk-free 4.20% | S4 Note 3 (warrant valuation input) | June 30, 2026 | Annual rate | Used as rf in CAPM | Market rate on Sept. 1 may differ by a few bp |
| Beta 1.8; ERP 5.0%; Kd 8%; tax 24% | J1 (judgment) | Sept. 1, 2026 | Decimals | Tornado tests β 1.4–2.2 and ERP 4–6% | Discount rate is the second-largest value driver |
| FY2026 services revenue $120M | S7 guidance $115–125M (midpoint) | Aug. 12, 2026 | USD M | — | Management claim |
| Fleet, hours, $/flight hour, margins, opex, capex 2026–31; convergence; terminal | J2, J3 (judgment) | Sept. 1, 2026 | See inputs JSON | Fleet anchored to "5 aircraft flying, 12 in production" (S7) | Largest value driver. Reverse DCF quantifies it. |
| Price $6.69 | S9 (recorded in Lab 08, commit `a6e9520`) | Sept. 1, 2026 close | USD | — | Single-day price |

**Date discrepancy found and corrected:** Lab 06 and the Lab 11 code cite the FY2025 10-K as "filed Feb. 26, 2026". EDGAR's filing index shows **2026-02-27** (Edition A was right). Edition B and the source ledger use Feb. 27.

## 3. Validation register

| Claim / output | Failure mode | Test and expected result | Actual result | Disposition | Evidence |
|---|---|---|---|---|---|
| Discounting and Gordon-terminal convention | Terminal value discounted 6 years; wrong rate | Week 3 known answer: 12 lines within $0.01; $27.4974; WACC 11% → $23.41; reverse shift ≈ +1.78 pts | All match ($27.4974; +1.7779 pts) | Pass | `tests/test_model.py::KnownAnswer` |
| Enterprise-to-equity sign convention | Cash subtracted instead of added | Edition A synthetic bridge = $8.20; Joby bridge cash > 0 and rebuilds to equity value | $8.20; rebuild exact | Pass | `test_synthetic_bridge_from_edition_a`, `Bridge` tests |
| Lab 11 defect 1 | `zip()` silently drops a fifth year | Four-value path must raise | Raises in the new model and the repaired legacy script | Fixed | `test_defect1_four_year_path_rejected` |
| Lab 11 defect 2 | Terminal value discounted at the module constant, explicit years at the input rate | With r = 20%, PV equals a hand formula using one rate | Equal to 6 dp | Fixed | `test_defect2_single_discount_rate` |
| Lab 11 defect 3 | g ≥ r accepted → negative or infinite terminal value | g = 13% vs r = 13% must raise; g > 4% rejected | Raises | Fixed | `test_defect3_…`, `test_growth_above_gdp_rejected` |
| Repair does not change the Lab 11 record | Fix alters published results | 2030 operating profit $375.1M; FCFE $121.2M | Unchanged | Pass | `test_legacy_lab11_results_unchanged_by_repair`; `legacy/repaired_run_output.txt` |
| Linked statements | Balance sheet does not balance; cash below floor | \|gap\| < $0.01M every period, every scenario; cash ≥ $500M floor | Max gap 0.0000 | Pass | `Accounting` tests; statement table in the report |
| Stub construction | H1 double counted | H1 opex reconciles to the 10-Q operating loss −$494.463M; stub + H1 = FY2026 plan | Exact | Pass | `test_h1_actuals_reconcile…`, `test_stub_plus_h1…` |
| Scenario independence | A scenario mutates the base inputs | Deep-copy check | Base unchanged | Pass | `test_inputs_not_mutated_by_scenarios` |
| Economic direction | Wrong-sign driver | Higher WACC ↓ value; delay ↓; acceleration ↑; more fleet ↑ | All as expected | Pass | `Directional` tests |
| FY2026 cash use vs guidance | Model burn inconsistent with management | H2 2026 modeled cash use (ex-SBC, incl. interest income) vs $385–415M guided | First draft (capex $230M) about $90M heavier than guidance. FY2026 capex reset to $200M (H2 $93M). Remaining gap ≈ SBC treated as cost. | Qualified | `data/joby_inputs_2026-09-01.json` capex |
| Convergence design (highest-risk modeling claim) | Linear ratio interpolation ignores fixed-cost leverage | Review whether opex scales like a fixed cost after certification | Draft gave −$1.21/share with R&D at 33% of revenue in 2031 falling only linearly. Redesigned: R&D +2%/yr and SG&A at half of revenue growth, with 8%/10% floors → $0.34. The change rests on cost structure, not on matching the price (still 5% of price). | Corrected | Draft was not committed; the redesign is in the first commit `8fc1a0a` (`joby/model.py`, convergence block) |
| Highest-risk decision claim: "price requires more scale than evidence supports" | Result driven by WACC, not scale | Reverse DCF on fleet with WACC held; WACC × g grid | 2.13× fleet needed; no grid cell (10.7–14.7%, 2–4%) reaches $6.69 | Supports claim | Report: Reverse DCF, grid |
| Recommendation-changing downside | Downside is cosmetic | Two-year certification delay through the linked statements | EV −$7.39B; new equity $12.7B; action → **Do not initiate** | Recommendation changes | Report: Scenarios |
| Reproducibility (cold run) | README insufficient | Fresh `git clone`, new venv, `pip install -r requirements.txt`, `python analysis.py`, tests, `streamlit run app.py` | **First failure:** `UnicodeEncodeError` (cp1252 console, '−' character) in `analysis.py` print. Fixed in commit `8f813c3`. Rerun: analysis OK, 23 tests OK, Streamlit health HTTP 200; about 3 min including install. | Fixed | Section 3a |
| App rendering | `$…$` rendered as LaTeX math in Streamlit | Visual check of the range metric | "$0.00–$3.82" was shown as math. Dollar signs escaped (commit after `8f813c3`). | Fixed | `app.py` |

### 3a. Cold-run log (Oct. 19, 2026, ET)

```
COLD RUN START 2026-10-19T20:12:40-04:00   (fresh clone into a new folder; new venv)
pip OK
UnicodeEncodeError: 'charmap' codec can't encode character '−'   <- first failure (analysis.py print)
RERUN after fix 2026-10-19T20:16:00-04:00 commit 8f813c3
analysis OK
Ran 23 tests ... OK
streamlit health HTTP 200
```

Limitation: this cold run used a fresh clone and environment on the author's machine. A README-only run by another person was not recorded.

## 4. Locked Changed-Input Record — human prediction first; AI closed during execution

### 4A. Final-model record (Project 1 model)

The test runner (`locked_test.py`) fixes the material input before anyone predicts: **revenue per eVTOL flight hour, all years, $2,500 → $2,000 in 2027 (×0.8), same escalation**. Nothing else changes. This input is deliberately absent from every sensitivity table in the frozen output, so the result was not visible before the prediction. The runner refuses to execute until `docs/locked-prediction.md` has no blanks and is committed. It records that commit hash and writes `output/locked_test_result.md`.

#### Precommit before the run and before any AI assistance on the prediction

Prediction written Oct. 19, 2026, 9:21 PM ET by Tobey Uhm; AI assistance on the prediction: none. Full text: `docs/locked-prediction.md`.

| Precommit timestamp | Repository commit | Material input | Old → new value / units | Expected output direction | Expected decision effect |
|---|---|---|---|---|---|
| 2026-10-19 21:22:24 ET (`1796d19`). A follow-up commit at 21:22:31 (`a0f877b`) removed placeholder text from the instruction line only; the prediction is unchanged. The runner recorded `a0f877b`. | `1796d195b752…`, `a0f877b5131a…` | Revenue per eVTOL flight hour | $2,500 → $2,000 USD per flight hour in 2027 (×0.8); +2.5%/yr thereafter | Value per share **down**, "significantly below $0.34 … likely deeply negative or toward $0.00". Cumulative new equity **up**. Mechanism: costs unchanged, so gross profit absorbs the entire revenue loss. | **Unchanged: Watch / defer** |

#### Preserved execution result

Run 2026-10-19 21:23:20 ET, commit `ab64e4d`; result committed in `2227cf7`. A first run at 21:23:03 ET wrote the same result files and then crashed while printing to the console (the same Windows cp1252 `UnicodeEncodeError` found in the cold run). The print was fixed in `ab64e4d` and rerun. Before/after outputs were checked identical to the first run.

| Output | Before | After | Change |
|---|---:|---:|---:|
| Value per share (unfloored) | $0.34 | **−$1.34** (floored $0.00) | −$1.67 |
| Enterprise value ($M) | −1,151.7 | −2,911.3 | −1,759.6 |
| 2030 revenue ($M) | 1,132.5 | 938.7 | −193.9 |
| 2030 FCFF ($M) | −1,020.2 | −1,091.7 | −71.5 |
| Cumulative new equity ($M) | 5,028.1 | 5,937.4 | +909.3 |
| Committee action | Watch / defer | **Do not initiate** | **changed** |

| Prediction reconciliation | Failure diagnosis | Evidence path |
|---|---|---|
| **Value direction: correct.** Value fell from $0.34 to −$1.34; modeled equity is below zero, so the shares are worth about $0. The predicted size ("deeply negative or toward $0.00") was right. **New equity: correct.** It rose by $909M. **Mechanism: partly wrong.** I predicted that unchanged costs would make gross profit absorb 100% of the lost revenue. In the model, eVTOL cost of revenue is set as revenue × (1 − gross margin), so costs fall with price. In 2030 gross profit fell $77.5M on a $193.9M revenue drop (40% = the 2030 margin), not $193.9M. This is the case my item 5 said I would check first. **Decision effect: wrong.** I predicted Watch / defer would hold; it changed to **Do not initiate**. | **Why value still fell so much** despite the smaller per-year hit: the loss compounds. Revenue is 18–20% lower every year, and the fixed R&D/SG&A costs stay the same, so operating leverage is lost and the convergence stage starts from a smaller 2031 base. PV of explicit FCFF fell about $1.09B and PV of terminal value fell about $0.80B. **Why my decision prediction failed:** I reasoned that worse economics "reinforce" deferral, but I did not apply the committee rule: an action of "Do not initiate" applies whenever value is ≤ $0. The base equity cushion was only $352M, so a $1.76B fall in EV wipes it out. **Model limitation exposed:** holding margin % constant when price falls is generous. Pilot, maintenance and energy cost per flight hour do not fall with fares, so the true downside is likely **larger** than modeled. The next model version should split eVTOL cost into a per-flight-hour cost plus a margin. **Decision consequence:** revenue per flight hour is decision-critical. Value reaches $0 at about **×0.956 (~$2,390 per flight hour in 2027)**, only 4.4% below the base assumption. This adds a monitoring trigger: if disclosed early revenue per flight hour is below about $2,390, move to **Do not initiate**. | `output/locked_test_result.md`, `output/locked_test_result.json`; prediction `docs/locked-prediction.md`; commits `1796d19`, `a0f877b`, `ab64e4d`, `2227cf7` |

Post-run analysis (the cost trace by year and the breakeven price search) was done with Claude Opus 5.5 after execution and checked against the result files. The prediction itself had no AI assistance.

### 4B. Lab 11 record (supporting evidence, preserved unchanged)

On the Lab 11 FCFE model: commercialization revenue −30% each year ($75/300/800/1,800/3,500M → $52.5/210/560/1,260/2,450M). **Prediction:** 2030 operating profit and FCFE both fall by about $577.5M; equity funding rises. **Actual:** operating profit −$577.5M (as predicted). FCFE −$498.7M, because the lower case pays no 21% cash tax. **Reconciliation:** direction right; FCFE size overstated by the $78.8M tax effect. Full record: `04_Completed_Joby_work/joby_locked_changed_input_record.md`. Recorded timestamp 2026-09-29T13:56:53-04:00.

**Partner:** Eric Boyd (esboyd@purdue.edu), NuScale partner, reviewed the prediction and ranges **before execution** and the result afterward. On Oct. 19, 2026 the student confirmed that the quoted Lab 11/12 exchanges accurately reflect what occurred.

**Chronology disclosure:** the earliest preserved commit (`c8d96ec`, 2026-09-29 14:05:22) already contains both the prediction and the results. The pre-run state is therefore attested by the student and partner, not by an independent pre-execution snapshot. Record 4A exists to provide a properly committed prediction.

## 5. Named AI-use register

| Tool / model surface and exposed version | Interaction date | Material task | Output / claim used or considered | Independent check | Disposition | Effect on decision |
|---|---|---|---|---|---|---|
| OpenAI Codex — **[student: exact surface/model shown]** | Sept. 3, 2026 (Lab 04 report); Sept. 10–29 (Labs 06–11 code) | Drafted the Lab 04 report; generated `dcf.py`, `peer_pe.py`, `joby_proforma_2026.py` | Report prose; Lab 11 pro forma and sensitivity code | Sources checked by student (report footer); Week 3 known answers; partner recomputation in Lab 11 | Accepted with checks. Three defects later found (below). | Built the Lab 11 FCFE model that Edition B replaces |
| ChatGPT — **[student: model/version shown]** | **[student: date]**, Oct. 2026 | Reviewed the evidence package; identified gaps and three code defects; drafted partner-exchange wording for confirmation | "Defects: four-year path accepted; inconsistent discount rate; g ≥ r accepted." "FCFE model ≠ required FCFF/WACC." | Each defect reproduced by a failing test, then repaired; student confirmed the partner quotes on Oct. 19 | Defects **accepted** (verified); the FCFF requirement **accepted** | Triggered the FCFF rebuild |
| Anthropic Claude, Claude Code desktop app, model **Claude Opus 5.5 (`claude-opus-5-5`)** | Oct. 19, 2026 | Extracted Q2 2026 10-Q and FY2025 10-K data; designed and coded the FCFF/WACC model, tests, app and locked-test runner; drafted README, memo, Edition B, this record and the video scripts | (a) 10-Q figures: cash + ST investments $2,263.826M, 989,124,237 shares, $690M notes at $14.19, antidilution table. (b) A convergence design giving −$1.21/share. (c) A first FY2026 capex of $230M. | (a) The AI's web summary was re-checked against the downloaded SEC HTML text; every bridge number was matched to the filing line. (b) Reviewed against cost behavior. (c) Compared with H2 cash-use guidance. (d) 23 tests plus a cold run. | (a) **Accepted** after verification. (b) **Corrected** (fixed-cost leverage). (c) **Corrected** to $200M. | Produced the valuation range and decision evidence. The student reviewed and owns all assumptions and the recommendation. |

No credentials, private data or full chat logs are included. Video scripts drafted with Claude were read and adapted by the student, who owns every spoken claim.

## 6. Limitations, monitoring, and kill / escalation rules

- **Judgment-heavy ramp:** fleet, utilization, revenue per flight hour and margins are not disclosed. Replace them with reported figures after two paid quarters.
- **Not modeled:** option strikes (full dilution assumed); the Resonant acquisition (NPV-zero); Toyota's pending $250M (excluded); state NOLs; lease liabilities (treated as operating); the 2-month gap between the June 30 balance sheet and the Sept. 1 valuation date.
- **Discount rate:** β and ERP are judgment. ±0.4 β moves value by about $1–1.3/share.
- **Kill / escalation:** **Do not initiate** if there is no FAA type certificate by Dec. 31, 2027, or if liquidity falls below 12 months of cash use without committed funding. **Escalate for an initiate review** only when the type certificate is issued and the price is at or below 75% of the updated base value. Re-run `python analysis.py` with each 10-Q.
