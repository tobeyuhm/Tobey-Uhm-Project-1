# Lab 08 - JOBY Comparable-Company Valuation Comparison

## Target, date, and peer policy

**Target:** Joby Aviation, Inc. (`JOBY`)  
**Valuation and price date:** September 1, 2026  
**Policy:** A direct comparable must share JOBY's pre-revenue, certification-dependent, capital-intensive eVTOL air-taxi model and exposure to manufacturing scale-up and commercialization risk. Adjacent electric-aviation or autonomy companies are qualified when their customer base or revenue model differs. Mature airlines, defense primes, conventional EV makers, and charter brokers are excluded.

## Source-supported candidate decisions

All EPS below is annual GAAP diluted loss per common share in U.S. dollars. No adjusted EPS or quarterly EPS is used.

| Company | Decision | Price on Sept. 1, 2026 | FY2025 GAAP diluted EPS | Fiscal year-end / publication date | Source locator and rationale |
|---|---|---:|---:|---|---|
| JOBY | Target | **$6.69** | $(1.13) | Dec. 31, 2025 / Feb. 27, 2026 | [FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1819848/000181984826000160/joby-20251231.htm), Statements of Operations (p. 53) and Note 14 (p. 88). [Stock Analysis historical table](https://stockanalysis.com/stocks/joby/history/), Sept. 1, 2026 close. Nasdaq was the starting page but did not return its dated table. |
| Archer (`ACHR`) | **Use** | **$5.56** | $(0.99) | Dec. 31, 2025 / Mar. 2, 2026 | [FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1824502/000182450226000019/achr-20251231.htm), Item 1, Business (pp. 1-2), and Statements of Operations (p. 38). [FY2025 IR release](https://investors.archer.com/news/news-details/2026/Archer-Announces-Fourth-Quarter-and-Full-Year-2025-Results-US-and-UAE-Air-Taxi-Pilot-Programs-On-Track-for-2026/default.aspx). [Stock Analysis historical table](https://stockanalysis.com/stocks/achr/history/), Sept. 1, 2026 close. Midnight is built for air-taxi operations; Archer is pursuing certification, network buildout, and manufacturing scale-up. Its defense/hybrid-autonomy program is a retained difference. |
| Eve (`EVEX`) | **Qualify** | **$2.20** | $(0.70) | Dec. 31, 2025 / Mar. 16, 2026 | [FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1823652/000155485526000300/evex-20251231.htm), Item 1, Business (pp. 5-7), Note 13 (p. 86), and certification/operator risks (pp. 20-21). [FY2025 IR release](https://ir.eveairmobility.com/news-events/press-releases/detail/106/eve-holding-inc-reports-fourth-quarter-and-fy2025-results). [Stock Analysis historical table](https://stockanalysis.com/stocks/evex/history/), Sept. 1, 2026 close. It shares certification and production risk, but plans aircraft sales, support services, and UATM while relying on third-party operators. |

No investigated candidate was excluded. No uninvestigated company was entered in the calculator.

## P/E validation and changed-peer check

Only JOBY, Archer, and Eve are in `peer_pe.py`. P/E is unusable: JOBY's FY2025 annual GAAP diluted EPS is $(1.13), while Archer's is $(0.99) and Eve's is $(0.70). A price divided by a negative EPS produces a negative multiple, not a meaningful P/E. The same-date Nasdaq prices are also unresolved, but a price would not cure the negative earnings denominator.

Manual Archer check: `$5.56 / $(0.99) = -5.62x`, which is not meaningful because annual EPS is negative. Eve is likewise `$2.20 / $(0.70) = -3.14x`. Removing Archer should not change an implied JOBY price because there are no usable P/E peers before removal. Archer remains `use`; it is not excluded to improve an answer. The calculator's positive-price and positive-EPS gate would report no usable peers and no removal estimate. `py peer_pe.py` and `python peer_pe.py` could not run in this environment because both launchers were inaccessible; no runtime output is claimed.

## Method comparison and conditional call

| Method | JOBY result and date | Main limitation |
|---|---|---|
| Week 3 DCF | **Unresolved as of Sept. 1, 2026.** The saved `dcf.py` is the synthetic training case, not a JOBY model. | Its $100M FCFF, $50M cash, $300M debt, 50M shares, and 10% WACC conflict with JOBY filing data. A JOBY DCF requires a forecast FCFF path and a defended discount rate. |
| Peer P/E | **Unusable as of Sept. 1, 2026; no range or reference estimate.** | Annual GAAP diluted EPS is negative for JOBY and both admitted peers. |

**Decision:** **Watch / defer; do not initiate.** I withhold a numerical range because there is no company-specific JOBY DCF and no usable P/E range. I do not average the methods: DCF values enterprise cash flows before a bridge to equity, while P/E values the common-equity claim.

## Skeptical review and reversal evidence

**Weakest supported assumption:** that a JOBY valuation range exists. The saved DCF is synthetic, so using it as JOBY valuation would create company and valuation-object mismatch. **Judgment: accept.** The FY2025 JOBY 10-K reports different cash, debt, shares, and losses from the training case.

**P/E criticism:** negative annual GAAP EPS makes P/E unusable. **Judgment: accept.** The cited Note 14/Statements/Note 13 support the respective negative earnings values. The missing Nasdaq prices remain **unresolved**, but are not the sole limitation. Averaging DCF and P/E is **rejected** because neither produces a valid JOBY value and their valuation objects differ.

**Answer to the skeptical question:** Current sources do not show that JOBY can become cash-generative before material additional equity financing. Its FY2025 filing targets first passengers in 2026 but states it expects ongoing losses and negative operating cash flow until sustainable commercial operations; production cost, utilization, demand, fees, and other unit-economics inputs remain uncertain. The $1.408B year-end cash/investment balance is liquidity, not proof of profitability. See [JOBY FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1819848/000181984826000160/joby-20251231.htm), Item 1 and MD&A pp. 41-42.

**What would change the decision:** FAA certification and operating approval, plus disclosed production cost, utilization, fares, contribution margin, capital needs, and financing evidence demonstrating a route to positive operating cash flow without material unexpected dilution. Certification delay, poor production/unit-cost evidence, weak demand, or dilutive financing would reinforce the defer decision.
