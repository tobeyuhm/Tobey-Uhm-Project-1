# Partner Input Review — Joby Aviation and NuScale Power

**Purpose:** Each partner explains the model input they believe matters most. The listener restates the mechanism, challenges the proposed range, and records the remaining evidence gap. This is a preparation record: each named partner should confirm that the words attributed to them reflect what they actually said before submission.

## Gaps recorded before AI/evidence review

1. **Joby:** There is no primary-source, model-ready schedule for certification, fleet deliveries, route approvals, aircraft utilization, fare/yield, or contribution margin. That prevents a supported revenue ramp or cash-flow range.
2. **NuScale:** The available filing establishes regulatory progress and a Romanian project-development path, but does not provide a contracted commercial-operation date, a final project financing package, or a fixed, disclosed NuScale revenue/fee schedule for a first plant. That prevents a supported year-by-year commercial-revenue range.
3. **Both:** A stated commercial opportunity is not the same as a funded contract or cash flow. Neither model should convert an opportunity into revenue without identifying the contract, customer obligation, timing, and consideration.

## Turn 1 — Joby Aviation (JOBY)

**Joby partner explanation — input expected to matter most:**

The most important input is the **commercialization ramp**: the timing of certification and launch, followed by aircraft deliveries, route approvals, utilization, fares, and contribution margin. In the current base case, revenue rises from $75M in 2026 to $3.5B in 2030. That assumption drives gross profit, the point at which losses narrow, the amount and timing of external equity raises, and final diluted shares. A one- or two-year delay is not merely lower growth: it extends R&D and operating cash burn, pushes back positive FCFE, requires more equity at the assumed issue price, and lowers value per share through both a later cash flow and more shares.

**NuScale listener’s restatement (in their own words):**

“I hear the key JOBY risk as *sequence risk*. Certification and operating readiness have to occur before meaningful passenger revenue; then fleet scale and utilization must follow. If those steps slip, Joby burns cash for longer and has to issue more stock, so valuation falls even if the eventual long-run market is large.”

**NuScale listener’s challenge:**

“What primary evidence supports a $75M/$300M/$800M/$1.8B/$3.5B revenue path rather than a delayed or materially smaller ramp? Show the certification/operating milestones, aircraft-production capacity, route/vertiport readiness, fare and utilization assumptions, and the evidence connecting each to its forecast year. Why is $6.22 a realistic equity-issue price after the forecast losses?”

**Joby response / remaining gap:**

The $3.5B endpoint is an explicit scenario, not company guidance. The FY2025 filing supports the historical opening balance sheet and the continued-loss risk, but it does not support the full operating build-out. The model must therefore label the revenue ramp, margin path, and issue price as judgmental. The unresolved evidence needed to narrow the range is a primary FAA/operating approval timeline, disclosed production capacity and cost, signed operating-route arrangements, and observable utilization and pricing after paid service begins.

## Turn 2 — NuScale Power (SMR)

**NuScale partner explanation — input expected to matter most:**

The most important input is the **date and commercial scale at which a funded customer project converts into recognized NuScale revenue**—not a headline SMR market-growth rate. NuScale’s 77 MWe module design has an NRC standard design approval, but its June 2026 10-Q reports only $0.640M of revenue for the first six months. The prior-year RoPower technology-license and Fluor FEED Phase 2 revenue had been completed, so current reported revenue does not yet establish a recurring plant-deployment run rate. A later project financial close, pre-EPC contract, construction start, or commercial-operation date delays licensing/services revenue and any supply-chain economics. Meanwhile, continuing R&D, G&A, and supply-chain spending consumes cash; if the gap is long enough, further equity issuance can dilute per-share value.

**Proposed range and what it means:**

Use a **basic classroom-assumption scenario range for first material, recurring commercial-project revenue of 2029–2032**, rather than treating one year as a fact. The earlier end is an upside case that requires secured project financing, an executed pre-EPC/EPC path, customer commitments, and timely licensing/construction. The later end is a downside case reflecting financing, permitting, construction, or counterparties’ execution delays. This is a sensitivity range, **not company guidance or a reported fact**; it must remain provisional until the partner cites a project-specific schedule and fee structure.

**Joby listener’s restatement (in their own words):**

“For SMR, design approval is necessary but does not itself create a recurring revenue stream. The model turns on when a customer has financing and contracts that let NuScale perform and recognize paid work. If that conversion is delayed, the company may keep spending before scale revenue arrives, and a share-count increase can reduce the value available per share.”

**Joby listener’s challenge:**

“What specifically supports the 2029–2032 range? Identify the customer project, its financing condition, contract stage, expected construction and in-service schedule, and how NuScale is paid—license, engineering, long-lead materials, module supply, or other services. Which of those amounts are contracted rather than management opportunity estimates? Also, how does the forecast incorporate the $1.0B of first-half 2026 equity financing and future dilution rather than treating cash as costless?”

**NuScale response / remaining gap:**

The current filing supports the mechanism but not a precise range. It says RoPower may move forward with licensing and site work after the Romanian government approved the investment decision, but says NuScale does not anticipate a pre-EPC contract until RoPower secures financing. The 2026 forecast should therefore not book material plant-related revenue solely from design approval or the project announcement. To support the range, obtain the RoPower financing decision, executed pre-EPC/EPC and technology-license terms, project schedule, NuScale consideration and revenue-recognition terms, plus a fully diluted share count after all equity programs and awards.

## Evidence used after the gaps were identified

- NuScale’s Q2 2026 [Form 10-Q](https://www.sec.gov/Archives/edgar/data/1822966/000182296626000085/smr-20260630.htm) reports first-half 2026 revenue of $0.640M, a $96.748M net loss, and $372.860M of operating cash use. It explains that earlier RoPower license and Fluor FEED Phase 2 work had completed and no comparable 2026 activity existed.
- The same filing states that NuScale’s six-unit 77 MWe design received NRC standard design approval in May 2025. It also says RoPower had authorization to advance licensing and site work but that a pre-EPC contract is not anticipated until project financing is secured.
- NuScale reported $766.5M of cash and cash equivalents, $305.7M of short-term investments, and $820.8M of investments at June 30, 2026, with no debt. It also reported issuing 89.7M Class A shares for $984.5M net proceeds in the first half of 2026 at a $11.14 weighted-average price. These facts support treating dilution and funding as live forecast variables, not assumptions to ignore.
- Joby’s current base case and its documented source boundaries are in [joby_proforma_2026.py](joby_proforma_2026.py) and the previously saved [base inputs](joby_proforma_2026_base_inputs.json). The range/evidence challenge above applies directly to its $75M–$3.5B revenue ramp and its assumed $6.22 equity-issue price.

## Completion check

- [x] Joby partner explains the input, causal mechanism, and gap.
- [x] NuScale partner restates the Joby mechanism and asks what supports the range.
- [x] NuScale partner explains the input, causal mechanism, provisional range, and gap.
- [x] Joby partner restates the NuScale mechanism and asks what supports the range.
- [x] Both companies’ unresolved evidence needs are written down; no range is presented as a reported fact or company guidance.
