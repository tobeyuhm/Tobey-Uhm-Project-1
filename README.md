# Joby-research — Joby Aviation (JOBY) initiation decision

FIN 43900 Project 1 (Corporate Finance Application) · Tobey Uhm · valuation date **September 1, 2026**

## Finance decision and intended user

A **buy-side investment committee with no current position** must decide whether to **initiate, watch/defer, or not initiate** coverage of Joby Aviation, a pre-commercial eVTOL air-taxi developer. Horizon: through FAA type certification and the first two years of paid service (re-review at each quarterly filing). As-of boundary: only evidence available on Sept. 1, 2026 (latest filing = Q2 2026 10-Q, filed Aug. 6, 2026; price = $6.69 Sept. 1 close).

**Result (frozen):** **Watch / defer.** FCFF/WACC value range **$0.00–$3.82 per share** (base **$0.34**) versus a **$6.69** market price. The reverse DCF shows the price requires ~**2.1×** the base-case fleet in every year. A two-year certification delay drives modeled equity value below zero → **Do not initiate**.

## Visible result (no execution needed)

- [`output/joby_valuation_report.md`](output/joby_valuation_report.md) — inputs, as-of dates, scenarios, bridge, WACC, sensitivity grid, tornado, reverse DCF, linked statements, validation summary, triggers, limitations.
- [`output/visible_output.json`](output/visible_output.json) — the same frozen contract the app renders.

## Setup and run (clean machine, ~3 minutes)

```bash
git clone <repository-url> Joby-research
cd Joby-research
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt  # only Streamlit; the engine is standard-library Python 3.10+
python analysis.py               # rebuilds output/ and prints the report
python -m unittest discover -s tests -v   # 23 validation tests
streamlit run app.py             # committee app (frozen output + live what-if)
```

No credentials are needed; `.env.example` is intentionally empty. Recorded cold run: see `docs/validation-and-ai-use.md` (first failure: Windows console encoding — fixed in commit `8f813c3`).

## Repository map

| Path | Role |
|---|---|
| `data/joby_inputs_2026-09-01.json` | Every material input with units, label (History / Market / Judgment) and source id |
| `data/source_ledger.csv` | Source id → filing, filed date, period, page/note, URL |
| `joby/model.py` | Integrated statements (IS/BS/CF, funding rule, NOLs) → FCFF → WACC → DCF → enterprise-to-equity bridge; scenario builders; input validation |
| `joby/training_dcf.py` | Week 3 synthetic known-answer DCF run through the same `present_value()` |
| `analysis.py` | Runs base/scenarios/sensitivity/reverse DCF/decision rule; writes `output/` |
| `app.py` | Streamlit committee app: renders the frozen output; live what-if calls the same engine |
| `locked_test.py` | AI-closed runner for the human-authored Locked Changed-Input Record (refuses to run until `docs/locked-prediction.md` is written and committed) |
| `tests/test_model.py` | Known answers, repaired defects, accounting identities, bridge, directional checks |
| `legacy/joby_proforma_2026.py` | Lab 11 script with its three defects repaired (original preserved unchanged in the evidence package) |
| `docs/` | Research evolution, decision memo, validation and AI-use record (Markdown + PDF), locked prediction, corrected video transcripts, submission manifest |
| `tools/build_pdfs.py` | Renders the three Brightspace PDFs from `docs/*.md` (`pip install -r requirements-docs.txt`; uses Edge/Chrome headless) |

Flow: **evidence (data/) → analysis (joby/, analysis.py) → tests → frozen output (output/) → app.py**.

## Data sources and point-in-time boundary

SEC filings: FY2025 10-K (filed Feb. 27, 2026) and Q2 2026 10-Q (filed Aug. 6, 2026) for the opening balance sheet (June 30, 2026), H1 2026 actuals, convertible notes, dilutive securities (cover-page shares Aug. 3, 2026), NOLs and the 4.20% risk-free rate. Management guidance (Q2 call, Aug. 12, 2026) anchors FY2026 revenue and cash use. Price: $6.69 close, Sept. 1, 2026. Nothing dated after Sept. 1, 2026 is used. Full ledger: `data/source_ledger.csv`.

## Financial conventions

- USD millions; shares in millions; end-of-period cash flows discounted from Sept. 1, 2026 (2026 stub = July–Dec 2026 = FY2026 plan − reported H1).
- FCFF = EBIT − unlevered cash tax (24%, NOLs with the 80% limit) + D&A − capex − ΔNWC. Stock-based compensation is treated as a real cost (not added back), so future grants are not also counted as dilution.
- WACC = 12.73%: CAPM cost of equity 13.2% (rf 4.20%, β 1.8, ERP 5.0%), 8% pre-tax debt cost with no tax shield (no cash taxes for years), market-value weights (debt 9.1%).
- Explicit drivers 2026–2031 (fleet × flight hours × revenue/flight hour + Blade/services), rule-based convergence 2032–2040, value-driver terminal value: FCFF = NOPAT × (1+g) × (1 − g/RONIC), g = 3% (< ~4% long-run nominal GDP), RONIC 15%.
- Bridge: + cash & short-term investments $2,263.8M; − 2032 convertible notes at $690.0M principal (conversion price $14.19 > value → debt); − mortgage $30.75M; − warrants at $21.5M fair value; − Blade earnout $17.5M; ÷ 1,051.26M diluted shares (basic 989.12M + RSUs/RSAs/early-exercised + all options).
- Future equity raises from the linked statements are reported for liquidity/dilution but are not deducted again in per-share value (negative FCFF is already in EV).

## Validation and changed-input tests

23 automated tests (`tests/test_model.py`): Week 3 known answers (12 lines, $27.4974, WACC 11% → $23.41, reverse shift +1.7779 pts), Edition A synthetic bridge ($8.20), the three repaired Lab 11 defects, balance sheet balances every period in every scenario, H1 2026 actuals reconcile to the 10-Q operating loss (−$494.463M), FCFF identity, bridge arithmetic, convert treatment, diluted shares, and directional checks. The Locked Changed-Input Record is in `docs/validation-and-ai-use.md`.

## Known limitations, monitoring, and reversal triggers

- The operating ramp (fleet, utilization, revenue per flight hour, margins) is analyst judgment; the market price implies ~2.1× the base fleet.
- Option strikes were not extracted (counted at full dilution, <1% of shares); Resonant acquisition treated as NPV-zero; Toyota's pending $250M tranche excluded.
- **Fare trigger (from the locked changed-input test):** value reaches $0 if revenue per flight hour is ~4.4% below plan (~$2,390); a $2,000 fare gives −$1.34/share → Do not initiate.
- **Initiate** only if the FAA type certificate is issued **and** price ≤ 75% of the base value; **upgrade evidence**: two quarters of paid eVTOL revenue with disclosed utilization and fare per flight hour; **do not initiate** if no type certificate by Dec. 31, 2027 or liquidity < 12 months of cash use without committed funding.

*Educational project for FIN 43900 (Purdue). Not investment advice.*
