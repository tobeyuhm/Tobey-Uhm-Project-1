# R — Locked Changed-Input Record: Joby Aviation

**Status:** Prediction locked before the first changed-input run; lower/base/higher runs completed and reconciled on 2026-09-29.

**Timestamp:** 2026-09-29T13:56:53-04:00  
**Base model:** `py joby_proforma_2026.py`  
**Model currency and scale:** USD millions, except shares (millions) and per-share data.

## Comparison design

Each sensitivity run will change **one independent operating input only**. All other base inputs, including R&D, SG&A, capex, minimum cash, financing rule, equity-issue price, discount rate, and terminal-growth assumption, stay unchanged. Revenue and gross margin are selected from the existing Joby assumption table; neither is a copied auto-retailer assumption or a calculated statement total.

| Driver | Base values by forecast year | Lower case | Higher case | Units / years | Reason for range |
|---|---|---|---|---|---|
| Commercialization revenue path | 2026–30: 75 / 300 / 800 / 1,800 / 3,500 | Apply a **−30% multiplier** to each annual base value: 52.5 / 210 / 560 / 1,260 / 2,450 | Apply a **+30% multiplier** to each annual base value: 97.5 / 390 / 1,040 / 2,340 / 4,550 | USD millions; 2026–30 | Judgmental range around the current staged-launch scenario. Joby’s reported pre-commercial/ancillary revenue history does not support a mechanical growth rate. Certification, paid launch, aircraft deliveries, routes, utilization, and demand can move the commercial ramp materially. |
| Gross-margin path | 2026–30: 35% / 40% / 45% / 50% / 55% | Apply a **−10 percentage-point shift** in every forecast year: 25% / 30% / 35% / 40% / 45% | Apply a **+10 percentage-point shift** in every forecast year: 45% / 50% / 55% / 60% / 65% | Percent of revenue; 2026–30 | Judgmental operating-efficiency range. It captures uncertainty in utilization, price/yield, maintenance, dispatch, and fixed-cost absorption as commercial service scales. This is a percentage-point shift, not a 10% relative change. |

## Common outputs and definitions

Use these same signed outputs for the base case and every single-input run.

| Output | Base result | Definition / treatment |
|---|---:|---|
| Final-year operating profit | **$375.1M** | 2030 gross profit less R&D, SG&A, and depreciation; USD millions. |
| Final-year free cash flow | **$121.2M** | 2030 **FCFE before funding** as defined in this simplified model: net income + depreciation − capex; USD millions. It remains signed in every scenario. |
| Value per share | **Unavailable for sensitivity conclusion** | The script prints a **−$1.41 illustrative** per-share figure, but it uses a Gordon terminal value over a still-transitioning, externally equity-funded cash-flow path. That is not a defensible valuation conclusion here. Do not replace it with a fabricated terminal value; compare operating profit and signed FCFE instead. |

## Locked prediction — show partner before the run

**Change:** Commercialization revenue path, base → lower. Apply the −30% multiplier to each 2026–30 annual revenue input: $75M/$300M/$800M/$1,800M/$3,500M → **$52.5M/$210M/$560M/$1,260M/$2,450M**. Gross margin remains at 35%/40%/45%/50%/55%, and every other independent input remains at base.

**Expected direction and rough size:** 2030 operating profit and pre-funding FCFE should both fall. Holding the 2030 margin constant at 55%, the immediate final-year gross-profit reduction is approximately **$577.5M** (($3,500M − $2,450M) × 55%). Before any indirect financing effects, operating profit and FCFE should each be roughly $578M lower. Lower interim cash generation should also trigger more or earlier equity funding under the $300M cash-floor rule, increasing dilution. Per-share value remains unavailable under the comparison convention above.

**Why:** revenue reaches gross profit only through the unchanged margin; that lower gross profit flows dollar-for-dollar into operating profit and, absent a tax change, into the model’s FCFE. The cash-floor financing rule turns persistent cash shortfalls into equity issuance.

## Partner pre-run check

| Check | NuScale partner confirmation | Joby partner confirms |
|---|---|---|
| Revenue values are USD millions, not percentages; the lower and higher cases are a ±30% multiplier applied to every stated year. | Confirmed. | ☐ |
| Gross-margin alternatives are percentage-point shifts: −10 or +10 points in every year, not a ±10% relative change. | Confirmed. | ☐ |
| Revenue and gross margin will be run separately; only one independent input changes in a run. | Confirmed. | ☐ |
| The shared outputs are 2030 operating profit and signed 2030 pre-funding FCFE. Per-share value is marked unavailable, not manufactured. | Confirmed. | ☐ |
| The prediction and two ranges were shown before either changed-input run. | Confirmed. | ☐ |

**Partner pre-run confirmation:** “The NuScale partner confirmed that Joby revenue is measured in USD millions, that the gross-margin cases are percentage-point shifts rather than percentage changes, and that revenue and margin are tested one at a time. The partner also confirmed that operating profit and signed FCFE before funding are the comparable outputs and that value per share should remain unavailable rather than be manufactured from an unsupported terminal value.”

**Unresolved item to resolve before running:** The ±30% revenue and ±10 percentage-point margin ranges are labelled judgment because no primary evidence currently translates certification, fleet deployment, utilization, fares, and cost per route into a forecast-year range. They are suitable as transparent sensitivity bounds, not as company guidance.

## Actual results — reconciled after the runs

All six lower/base/higher scenarios completed with only the declared independent driver changed. Every annual balance-sheet gap and cash-floor check passed; no run was invalid. The sensitivity program then rebuilt the base input set and reran it: the restored inputs, statements, 2030 operating profit, and 2030 FCFE exactly matched the first base run.

| Driver and case | Actual input path, 2026–30 | 2030 operating profit | Change from base | 2030 FCFE before funding | Change from base |
|---|---|---:|---:|---:|---:|
| Revenue — lower | $52.5M / $210.0M / $560.0M / $1,260.0M / $2,450.0M | **−$202.4M** | **−$577.5M** | **−$377.5M** | **−$498.7M** |
| Revenue — base | $75.0M / $300.0M / $800.0M / $1,800.0M / $3,500.0M | **$375.1M** | **$0.0M** | **$121.2M** | **$0.0M** |
| Revenue — higher | $97.5M / $390.0M / $1,040.0M / $2,340.0M / $4,550.0M | **$952.6M** | **+$577.5M** | **$577.5M** | **+$456.2M** |
| Gross margin — lower | 25.0% / 30.0% / 35.0% / 40.0% / 45.0% | **$25.1M** | **−$350.0M** | **−$155.3M** | **−$276.5M** |
| Gross margin — base | 35.0% / 40.0% / 45.0% / 50.0% / 55.0% | **$375.1M** | **$0.0M** | **$121.2M** | **$0.0M** |
| Gross margin — higher | 45.0% / 50.0% / 55.0% / 60.0% / 65.0% | **$725.1M** | **+$350.0M** | **$397.7M** | **+$276.5M** |

Value per share remains **unavailable** for this comparison. The program retains the signed FCFE results rather than treating a terminal value over the externally funded transition period as a valuation result.

### Spans and the result to explain

| Driver | 2030 operating-profit span | 2030 FCFE-before-funding span |
|---|---:|---:|
| Revenue path | **$1,155.0M** | **$955.0M** |
| Gross-margin path | **$700.0M** | **$553.0M** |

Over these stated ranges, the **revenue path** has the larger span for both output measures. This is a range-dependent comparison: its ±30% revenue range is not commensurate with the gross-margin ±10-percentage-point range, so the result does not establish that revenue is inherently the more important economic driver in every possible range.

### Locked prediction reconciliation

The predicted lower-revenue result was directionally correct: 2030 operating profit fell by the predicted **$577.5M**. The predicted FCFE decrease of roughly $577.5M was too large. Actual FCFE fell by **$498.7M** because the base case has positive 2030 operating income and therefore pays the model’s 21% cash tax, while the lower-revenue case has a loss and pays no cash tax. The tax change offsets $78.8M of the gross-profit decline. Linked accounting recalculated as intended; no other independent input was changed.

## Partner exchange records — complete together, in your own words

### Exchange 2: result check

**Showed:** Revenue-lower result beside revenue-base result, including the 2030 trace and annual check block in [visible output](joby_proforma_2026_sensitivity_output.txt).

**NuScale partner’s Joby result check:** “The NuScale partner recomputed the revenue-lower changes: 2030 operating profit changed by −$577.5M (−$202.4M minus $375.1M), and FCFE before funding changed by −$498.7M (−$377.5M minus $121.2M). The partner confirmed that R&D, SG&A, capex, tax rate, cash floor, issue price, cost of equity, and terminal growth remained at base; revenue was the only independent input changed. The partner asked why FCFE declined by less than operating profit. I explained that the base case pays a 21% cash tax on positive operating income, while the lower-revenue case has a loss and pays no cash tax. The avoided tax offsets part of the reduction in FCFE.”

**Joby partner’s check of NuScale analysis — basic classroom assumption, not company guidance or a reported fact:** “For a basic NuScale comparison, the partner modeled first material recurring commercial-project revenue beginning in 2030 in the base case and delayed it to 2032 in the lower case. The partner held cost assumptions, cash policy, share-issuance policy, and discount-rate assumptions constant while changing only commercial-revenue timing. I checked that this was one independent driver rather than a simultaneous change to revenue and expenses. I asked whether the 2030 base timing was supported by a financed project and executable pre-EPC/EPC path. The partner explained that the timing is a transparent sensitivity assumption, not company guidance, and should be refined using evidence on RoPower financing, contracts, construction timing, and NuScale’s fee structure.”

### Exchange 3: driver comparison

**Question for Joby presenter:** “Could revenue’s larger span reflect the selected ±30% range rather than an inherently larger business importance?”

**Mechanistic answer:** Yes. The ranking is only over the ranges tested. In this model, a 30% change to 2030 revenue changes gross profit by revenue × the unchanged 55% margin; the ±10-point margin sensitivity changes gross profit by 2030 revenue × 10 points. Different justified ranges could change the span ranking.

**NuScale partner’s summary:** “The NuScale partner summarized that Joby’s revenue path has the larger output span over the selected ranges, but that this does not prove revenue is always more important than gross margin. The ranking partly reflects the chosen ±30% revenue range compared with the ±10-percentage-point margin range.”

**Joby partner’s NuScale question and partner answer — basic classroom assumption, not company guidance or a reported fact:** “I asked whether NuScale’s commercial-revenue timing could appear to be the largest driver merely because the tested delay range is wide. The NuScale partner answered yes: a 2029–2032 timing range creates a large span because it moves potential revenue across multiple years. The conclusion is therefore limited to the selected timing range and should not be treated as a probability-weighted forecast.”

## Individual conclusion and learning reflection

**Individual conclusion:** “Over the selected ranges, Joby’s commercialization revenue path is the main driver of both 2030 operating profit and FCFE before funding. This does not change my valuation conclusion because per-share value remains unavailable under the model’s externally funded transition path. It does change my research priority: I would focus on evidence for certification timing, fleet production capacity, route approvals, utilization, pricing, and contribution margin before relying on the $3.5B 2030 revenue scenario. The most surprising result was that lower revenue reduced FCFE by less than operating profit; the difference came from the lower case avoiding cash taxes rather than from an error in the sensitivity calculation.”

**Learning reflection:** “One-at-a-time sensitivity changes one independent assumption while holding all other independent assumptions at their base values, then lets linked statements recalculate. The selected input range affects the ranking because a wider range can create a larger output span even if the underlying business driver is not inherently more important. A sensitivity table is not a forecast probability because it shows conditional outcomes for chosen scenarios; it does not state how likely any scenario is or assign probabilities to the cases.”
