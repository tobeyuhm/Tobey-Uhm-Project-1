# Joby Aviation (JOBY) — FCFF/WACC valuation and committee decision

**Decision user:** Buy-side investment committee with no current JOBY position  
**Valuation date:** 2026-09-01 · **Balance sheet:** 10-Q at 2026-06-30 · **Price:** $6.69 close on 2026-09-01  
**Units:** USD millions except per-share values (USD) and shares (millions)  
**Generated:** 2026-10-20T02:38:30Z (Python 3.13.15)

## Decision

**Watch / defer.** Valuation range $0.00–$3.82 per share (base $0.34) versus $6.69 market price.

Rule: Initiate only if price <= 75% of base value AND the FAA type certificate is issued; do not initiate if the upside-case value is $0 or liquidity covers < 12 months of modeled cash use; otherwise watch/defer.

## Scenarios (each run through the full linked statements)

| Scenario | EV | Equity value | Value/share | 2030 revenue | 2030 EBIT | First FCFF > 0 | External equity needed | Action if true |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Downside: certification and paid launch delayed 2 years | -7,391.4 | -5,887.4 | $0.00 (model -5.60, floored) | 257.5 | -1,029.8 | None | 12,661.0 | Do not initiate |
| Base: driver-based fleet ramp, paid service from 2027 | -1,151.7 | 352.3 | $0.34 | 1,132.5 | -691.5 | 2035 | 5,028.1 | Watch / defer |
| Upside: +40% fleet and +10% utilization | 2,514.6 | 4,018.6 | $3.82 | 1,655.9 | -482.1 | 2033 | 3,704.5 | Watch / defer |

## Discount rate

Cost of equity 13.20% (CAPM) · after-tax cost of debt 8.00% · debt weight 9.05% (market values: equity 6,617.2, debt 658.8) · **WACC 12.73%** · terminal growth 3.0%

## Enterprise-to-equity bridge (base)

| Step | USD m |
|---|---:|
| PV of explicit + convergence FCFF (2026 H2–2040) | -3,412.8 |
| PV of terminal value | 2,261.1 |
| PV of NOLs remaining after 2040 | 0.0 |
| **Enterprise value** | **-1,151.7** |
| + Cash and short-term investments (June 30, 2026) | 2,263.8 |
| − 0.75% convertible notes due 2032 (debt at principal) | -690.0 |
| − Mortgage loan | -30.8 |
| − Warrants at fair value | -21.5 |
| − Blade EBITDA earnout (maximum) | -17.5 |
| **Equity value** | **352.3** |
| ÷ Diluted shares (m) | 1,051.260 |
| **Value per share** | **$0.34** |

Terminal value share of EV: not meaningful because EV ≤ 0 — PV of terminal value ($2,261M) is smaller than the PV of pre-profit cash burn. The whole equity value rests on cash on hand plus a distant terminal value.

## Sensitivity: value per share, WACC × terminal growth

| WACC \ g | 2% | 3% | 4% |
|---|---:|---:|---:|
| 10.73% | $1.60 | $1.77 | $1.99 |
| 11.73% | $0.84 | $0.94 | $1.07 |
| 12.73% | $0.28 | $0.33 | $0.40 |
| 13.73% | $-0.15 | $-0.12 | $-0.09 |
| 14.73% | $-0.48 | $-0.47 | $-0.45 |

## One-at-a-time sensitivity (value per share, unfloored)

| Driver | Base | Low input → value | High input → value | Swing |
|---|---|---:|---:|---:|
| Fleet size, all years | x1.0 | x0.7 → $-2.21 | x1.3 → $2.50 | $4.71 |
| Steady-state gross margin | 40% | 35% → $-0.80 | 45% → $1.47 | $2.27 |
| Beta | 1.8 | 1.4 → $1.60 | 2.2 → $-0.41 | $2.01 |
| Equity risk premium | 5.0% | 6.0% → $-0.35 | 4.0% → $1.44 | $1.79 |
| Sales-to-capital (growth capex) | 2.5 | 2.0 → $0.08 | 3.0 → $0.50 | $0.42 |
| Terminal growth | 3% | 2% → $0.28 | 4% → $0.40 | $0.13 |

## Reverse DCF (what the market price implies)

To justify $6.69, the fleet in every forecast year must be **2.13×** the base plan (≈682 aircraft in average service in 2031; 2030 revenue ≈ $2,230M; 2040 revenue ≈ $20,494M). Held fixed: WACC, terminal growth, utilization, revenue per flight hour, margins, opex, capex schedule, bridge, and share count. This is one set of assumptions consistent with the price, not proof of mispricing.

## Liquidity and funding (base, linked statements)

Cash and short-term investments $2,263.8M; modeled FY2027 cash use $103.2M/month → **21.9 months** of runway before new funding. Toyota's second $250M tranche is pending and excluded.

Future equity raises are shown for liquidity and dilution, but they are **not** deducted again in per-share value: negative FCFF is already subtracted in EV, so counting the new shares too would double count the funding need.

## Base-case integrated statements (USD m)

| Period | Revenue | EBIT | D&A | Capex | ΔNWC | Cash tax | FCFF | PV FCFF | Net income | Equity raise | Cash | Shares (m) | BS gap |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2026 H2 | 57.1 | -525.5 | 23.0 | 93.4 | 0.0 | 0.0 | -596.0 | -572.8 | -489.6 | 0.0 | 1,703.8 | 989.1 | 0.0000 |
| FY2027 | 141.6 | -1,050.0 | 60.1 | 300.0 | 1.4 | 0.0 | -1,291.3 | -1,101.0 | -997.6 | 35.1 | 500.0 | 995.0 | 0.0000 |
| FY2028 | 229.7 | -1,036.0 | 108.0 | 380.0 | 4.4 | 0.0 | -1,312.4 | -992.4 | -1,025.8 | 1,302.2 | 500.0 | 1,211.2 | 0.0000 |
| FY2029 | 518.9 | -941.9 | 162.4 | 460.0 | 14.5 | 0.0 | -1,253.9 | -841.2 | -931.6 | 1,243.7 | 500.0 | 1,417.8 | 0.0000 |
| FY2030 | 1,132.5 | -691.5 | 221.9 | 520.0 | 30.7 | 0.0 | -1,020.2 | -607.2 | -681.2 | 1,010.0 | 500.0 | 1,585.5 | 0.0000 |
| FY2031 | 1,942.4 | -331.2 | 281.6 | 560.0 | 40.5 | 0.0 | -650.1 | -343.2 | -320.9 | 639.9 | 500.0 | 1,691.8 | 0.0000 |
| FY2032 | 2,913.7 | -80.2 | 337.2 | 725.7 | 48.6 | 0.0 | -517.3 | -242.2 | -70.0 | 507.0 | 500.0 | 1,776.0 | 0.0000 |
| FY2033 | 4,079.1 | 235.8 | 414.9 | 881.1 | 58.3 | 11.3 | -300.0 | -124.6 | 234.2 | 290.3 | 500.0 | 1,824.2 | 0.0000 |
| FY2034 | 5,302.9 | 569.9 | 508.2 | 997.7 | 61.2 | 27.4 | -8.1 | -3.0 | 552.3 | 0.0 | 501.7 | 1,824.2 | 0.0000 |
| FY2035 | 6,469.5 | 880.2 | 606.1 | 1,072.7 | 58.3 | 42.3 | 313.0 | 102.3 | 847.8 | 0.0 | 824.4 | 1,824.2 | 0.0000 |
| FY2036 | 7,504.6 | 1,199.2 | 699.4 | 1,113.5 | 51.8 | 57.6 | 675.9 | 196.0 | 1,162.2 | 0.0 | 1,520.9 | 1,824.2 | 0.0000 |
| FY2037 | 8,405.2 | 1,479.6 | 782.2 | 1,142.4 | 45.0 | 71.0 | 1,003.3 | 258.1 | 1,452.3 | 0.0 | 2,567.9 | 1,824.2 | 0.0000 |
| FY2038 | 9,161.6 | 1,715.5 | 854.3 | 1,156.9 | 37.8 | 82.3 | 1,292.7 | 295.0 | 1,711.8 | 0.0 | 3,939.3 | 1,824.2 | 0.0000 |
| FY2039 | 9,711.3 | 1,857.2 | 914.8 | 1,134.7 | 27.5 | 89.1 | 1,520.7 | 307.9 | 1,892.4 | 0.0 | 5,584.3 | 1,824.2 | 0.0000 |
| FY2040 | 10,099.8 | 1,956.5 | 958.8 | 1,114.1 | 19.4 | 358.5 | 1,423.2 | 255.5 | 1,647.7 | 0.0 | 7,057.2 | 1,824.2 | 0.0000 |

## Validation summary

- Training DCF known answer (Week 3): PASS — $27.4974/share vs $27.4974; reverse shift +1.7779 points vs ≈+1.78.
- Balance sheet balances every period (|gap| < $0.01M): PASS.
- Full test suite: `python -m unittest discover -s tests -v` (see docs/validation-and-ai-use.md).

## Comparables

Lab 08 peer policy (frozen Sept. 1, 2026): ACHR use; EVEX qualify. Not used for value. FY2025 GAAP diluted EPS is negative for JOBY ($-1.13), ACHR ($-0.99) and EVEX ($-0.70), so P/E is not meaningful; revenue multiples are not meaningful while core eVTOL revenue is ~zero. The market-implied cross-check is the reverse DCF instead.

## Reversal triggers

- Initiate review: FAA type certificate issued AND price at or below the initiate threshold.
- Upgrade evidence: >= 2 reported quarters of paid eVTOL passenger revenue with disclosed utilization and fare per flight hour.
- Fare trigger (locked changed-input test): value reaches $0 at ~$2,390 per flight hour (x0.956 of plan); disclosed early revenue per flight hour below that -> Do not initiate.
- Do not initiate: no type certificate by Dec. 31, 2027 (delayed-certification case) OR liquidity < 12 months of cash use without committed funding.

## Limitations

- Fleet, utilization, revenue per flight hour, margins and opex are analyst judgment anchored to management statements, not company guidance beyond FY2026 revenue.
- Option strike prices were not extracted; all 5.27M options are counted as exercised at zero strike (max dilution, <1% of shares).
- Announced $500M Resonant Sciences acquisition is treated as NPV-zero (cash/stock paid = value received).
- Toyota's pending $250M second tranche at $5.03/share is excluded from the base bridge.
- Valuation uses the June 30, 2026 balance sheet; July-August 2026 flows are inside the H2 stub (2-month timing mismatch).
