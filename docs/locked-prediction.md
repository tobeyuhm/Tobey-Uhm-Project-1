# Locked Changed-Input Prediction

> Write this before running `python locked_test.py`. Commit this file by itself, then run the test.
> `locked_test.py` will not run until this file is committed and no `[WRITE HERE]` is left.

**Author:** Tobey Uhm
**Written (date/time, ET):** October 19, 2026, 9:21 PM ET
**AI assistance on this prediction:** None.

## The change (fixed by the test runner)

- **Material input:** revenue per eVTOL flight hour, every forecast year.
- **Old → new:** $2,500 → $2,000 per flight hour in 2027 (×0.8), with the same +2.5%/yr escalation after 2027. USD per flight hour.
- **Everything else unchanged:** fleet, utilization, margins, R&D, SG&A, capex, WACC, terminal growth, bridge, share count.

## My prediction (before execution)

**1. Expected direction of base value per share ($0.34 today):**

Down.

**2. Rough size and why (the causal path through revenue → gross profit → EBIT → FCFF → EV):**

A 20% cut to revenue per flight hour ($2,500 down to $2,000) causes an immediate, severe compression across the entire financial waterfall. Because flight operating costs, pilot payroll, and maintenance reserve assumptions remain unchanged, gross profit absorbs the entire dollar loss, leading to severe gross margin contraction. This drop flows directly dollar-for-dollar into EBIT, pushing initial operating losses much deeper and delaying breakeven operations by several forecast years. Lower EBIT reduces operating cash flow, drastically worsening Free Cash Flow to Firm (FCFF) across all early ramp years. Consequently, discounted cash flows turn heavily negative in the intermediate period, shrinking Enterprise Value (EV). After deducting net debt/bridge liabilities, the equity value base per share will fall significantly below the current $0.34, likely turning deeply negative or compressing toward $0.00 without additional external capital injection adjustments.

**3. Expected direction of cumulative new equity needed:**

Up.

**4. Expected effect on the committee action (Watch / defer today):**

Unchanged (retains Watch / defer). The initial recommendation is already to defer investment; worsening unit economics, larger cash burn, and depressed equity per share will only reinforce the rationale to remain on hold and avoid capital deployment until commercial flight hour monetization improves.

**5. What result would surprise me, and what I would check first if it happens:**

It would surprise me if the base value per share increased, stayed flat, or fell by less than 20%, or if cumulative equity requirements remained constant despite the 20% revenue haircut. If this occurs, I would first check the test runner's discounting script and bridge formulas to verify whether flight hour revenues were dynamically tied to variable costs (erroneously lowering expenses alongside revenue) or if the model inadvertently capped dilution/minimum cash thresholds rather than reflecting true financing burn.
