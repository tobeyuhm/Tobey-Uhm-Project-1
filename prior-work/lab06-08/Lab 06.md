# Joby Aviation (NYSE: JOBY) DCF — Lab 06

Latest 10-K: fiscal year ended December 31, 2025; filed February 26, 2026. Amounts are USD millions unless noted. [SEC Form 10-K](https://www.sec.gov/Archives/edgar/data/1819848/000181984826000160/joby-20251231.htm)

| Input | Value | Unit / as-of date | Exact locator / basis |
|---|---:|---|---|
| Starting FCFF | -563.811 | USD millions, FY2025 | Cash Flows, p. 56, lines 1743–1766: CFO -509.893 less purchases of property and equipment 53.918. No interest-paid disclosure found. |
| Growth, Years 1–5 | 8%, 6%, 5%, 4%, 3% | Forecast placeholder, prepared Sept. 10, 2026 | Unresolved; training values retained. Item 7, pp. 37–47 states continued losses and negative operating cash flow until sustainable commercial operations. |
| WACC | 10% | Estimate placeholder, prepared Sept. 10, 2026 | Unresolved; training value retained and not presented as a company fact. |
| Terminal growth | 3% | Long-run assumption, prepared Sept. 10, 2026 | Analyst assumption for the long-run economy, not a Joby disclosure. |
| Cash | 240.810 | USD millions, Dec. 31, 2025 | Balance Sheet p. 52, line 1586. Short-term investments of 1,167.106 excluded. |
| Debt | 0.000 | USD millions, Dec. 31, 2025 | Balance Sheet, lines 1601–1610: no conventional debt. Subsequent event: 690.0 principal 0.75% converts issued Feb. 2, 2026. |
| Diluted shares | 826.240955 | million weighted-average shares, FY2025 | EPS Note 14, p. 89, lines 2920–2930; basic and diluted same because of antidilution. |
| JOBY price | $6.45 | Sept. 10, 2026, 5:00 AM reported pre-market | [Public quote](https://public.com/stocks/joby/pre-market); reverse-DCF target only. |

## Training sensitivity grid

The base case is the centre cell. Value falls as WACC rises and rises as terminal growth rises; the corners give the range.

| WACC \ terminal growth | 2% | 3% | 4% |
|---|---:|---:|---:|
| 9% | 28.60 | 32.94 | 39.02 |
| 10% | 24.36 | **27.50** | 31.69 |
| 11% | 21.06 | 23.41 | 26.44 |

## Reverse DCF

Training target price: $30.00. Bisection solves a uniform shift of **+1.7779 percentage points** added to all five explicit growth rates. Held fixed: starting FCFF 100; WACC 10%; terminal growth 3%; cash 50; debt 300; diluted shares 50; base growth rates 8%, 6%, 5%, 4%, 3%; bracket -5% to +10%.

This is one set of assumptions consistent with the target price, not proof of mispricing. Joby growth and WACC remain unresolved, so the program stays on the verified training case.

## Reasonableness and conditional call

Joby DCF value is **-$10.7963/share** versus a reported pre-market price of **$6.45**: outside the 0.5×–2× band. No inputs were adjusted. The most distrusted input is the Years 1–5 growth forecast, because training placeholder percentages applied to negative FCFF cannot model certification, launch, and commercial ramp timing.

**Watch-defer. Initiate only if Joby provides a sourced, credible path from negative FCFF to sustainable positive FCFF that resolves the Years 1–5 forecast and WACC; otherwise defer. Monitor quarterly operating cash burn and FAA certification/commercial-launch progress.**
