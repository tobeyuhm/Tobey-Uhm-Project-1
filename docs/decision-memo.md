# Decision Memo — Joby Aviation (NYSE: JOBY)

**To:** Buy-side investment committee (no current position) · **From:** Tobey Uhm, equity research analyst · **Valuation date:** September 1, 2026 · **Price:** $6.69 (Sept. 1 close)

## 1. Decision and committee ask

**Recommendation: Watch / defer — do not initiate a position at $6.69.** Our FCFF/WACC valuation gives **$0.00–$3.82 per share** (base **$0.34**). The market price is above even the upside case. **Committee ask:** approve keeping JOBY on the watch list, take no position, and re-review at each quarterly filing against the triggers in Section 4. We would initiate only if (a) the FAA type certificate is issued **and** (b) the price is at or below 75% of our updated base value.

## 2. Valuation and strongest evidence

| Case (linked statements → FCFF → WACC 12.73%) | Value/share | 2030 revenue | First FCFF > 0 | New equity needed | Action if this case is true |
|---|---:|---:|---:|---:|---|
| Downside: certification and paid launch delayed 2 years | $0.00 (model −$5.60) | $258M | none by 2040 | $12.7B | Do not initiate |
| **Base:** paid service from 2027, 320 aircraft in average service by 2031 | **$0.34** | $1,133M | 2035 | $5.0B | Watch / defer |
| Upside: +40% fleet, +10% utilization | $3.82 | $1,656M | 2033 | $3.7B | Watch / defer |

- **Bridge (base, USD M):** enterprise value −$1,151.7 + cash and short-term investments $2,263.8 − 2032 convertible notes $690.0 (the $14.19 conversion price is above our value, so we treat them as debt) − mortgage $30.8 − warrants $21.5 − Blade earnout $17.5 = **equity value $352.3**, divided by **1,051.26M diluted shares**. Source: Q2 2026 10-Q, balance sheet at June 30, 2026, and the cover page (989.1M shares on Aug. 3, 2026).
- **Why the value is low:** the PV of all FCFF from 2026 H2 to 2040 is about −$3.4B (burn through 2034 outweighs the positive 2035–40 flows); the terminal value is worth only +$2.3B in PV. Equity value is almost entirely today's cash.
- **What the price implies (reverse DCF):** holding everything else fixed, $6.69 requires **2.13×** our fleet in every year, about 680 aircraft in average service by 2031 and about $2.2B of revenue in 2030.
- **Facts vs. judgment:** the balance sheet, share count, convertible notes, H1 2026 results (revenue $62.9M, operating loss $494.5M), NOLs ($1.66B federal) and FY2026 revenue guidance ($115–125M) come from filings or management. The fleet ramp, utilization, $2,500 per flight hour and margins are our judgment (`data/joby_inputs_2026-09-01.json`).
- **Comparables:** Under our Sept. 1 peer policy, Archer is used and Eve is qualified, but both have negative GAAP EPS and immaterial revenue. P/E and EV/revenue are therefore not meaningful, and the reverse DCF serves as the market cross-check.

## 3. Material assumptions and sensitivities

| Driver (one at a time) | Low input → value | High input → value | Swing |
|---|---:|---:|---:|
| Fleet size, all years (×0.7 / ×1.3) | −$2.21 | $2.50 | $4.71 |
| Steady-state gross margin (35% / 45%) | −$0.80 | $1.47 | $2.27 |
| Beta (1.4 / 2.2) | $1.60 | −$0.41 | $2.01 |
| Equity risk premium (6% / 4%) | −$0.35 | $1.44 | $1.79 |
| Sales-to-capital (2.0 / 3.0) | $0.08 | $0.50 | $0.42 |
| Terminal growth (2% / 4%) | $0.28 | $0.40 | $0.13 |

WACC × terminal growth grid: $1.99 at 10.7%/4% and −$0.47 at 14.7%/3%. **No cell reaches $6.69.** The two decisive drivers are commercial scale and the discount rate. Terminal growth hardly matters because EV is negative. Treat these as conditional outcomes, not probabilities.

## 4. Risks, failure conditions, and monitoring triggers

| Trigger | Metric and threshold | Window | Effect |
|---|---|---|---|
| Certification | FAA type certificate issued (stage 5 complete) | Check each 10-Q/10-K | Necessary condition to initiate |
| Paid-service evidence | ≥ 2 quarters of paid eVTOL passenger revenue with disclosed aircraft in service, utilization and revenue per flight hour | From first paid quarter | Replace judgment inputs; re-value |
| Valuation | Price ≤ 75% of updated base value | Continuous | Initiate (together with certification) |
| Delay | No type certificate by Dec. 31, 2027 | Dec. 31, 2027 | Downside case applies → **Do not initiate** |
| Liquidity | Cash and investments < 12 months of cash use without committed funding (today: $2.26B ≈ 22 months at the modeled FY2027 burn) | Each filing | **Do not initiate** |
| Fare economics | Disclosed revenue per flight hour below ~$2,390 (value reaches $0 at ×0.956 of the $2,500 base; locked test: $2,000 gives −$1.34) | First paid quarters | **Do not initiate** |
| Dilution / financing | New equity priced below our base value, or Toyota's $250M second tranche failing to close | Each financing | Lower the value; tighten the triggers |

**Principal risks:** certification timing; manufacturing ramp and unit cost; utilization and fares that are not yet observable; about $5B of further equity funding needed in the base case; capital allocation (the $500M Resonant acquisition is treated as NPV-zero).

## 5. Action requested and next review

Approve **Watch / defer, no position**. The next review comes with the Q3 2026 10-Q, where we will update the bridge, cash use against the $385–415M H2 guidance, and certification status. AI-tool use and every material check are recorded in **Validation-and-AI-Use.pdf** (`docs/validation-and-ai-use.md`). The reproducible model and frozen output are in the `Joby-research` repository (`output/joby_valuation_report.md`).

*Educational project, not investment advice.*
