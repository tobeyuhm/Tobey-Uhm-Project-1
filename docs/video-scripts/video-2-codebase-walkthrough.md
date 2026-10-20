# Video 2 — Detailed Codebase and Validation Walkthrough (hard limit 5:00; target 4:40)

**Title for YouTube:** JOBY Project 1 — Video 2: Codebase and Validation Walkthrough
**On screen:** webcam thumbnail, VS Code with the `Joby-research` repository, and a terminal.
**Before recording:** finish `docs/locked-prediction.md`, commit it, and have the terminal open at the repo root. About 620 spoken words.

---

**[0:00] On screen: the repository tree in VS Code**

This is the Joby-research repository. The flow is evidence, then analysis, then tests, then frozen output, then the app. `data/` holds the inputs and the source ledger. `joby/model.py` is the engine. `analysis.py` runs everything and writes `output/`. `app.py` is the committee app. `tests/` holds the validation suite, and `locked_test.py` runs my changed-input test.

**[0:25] On screen: `data/joby_inputs_2026-09-01.json`, then `data/source_ledger.csv`**

Every material input lives in one JSON file with units, a label (history, market or judgment) and a source ID. For example, cash plus short-term investments of $2,263.826 million comes from source S4, the Q2 2026 10-Q balance sheet. The share count comes from the cover page. The convertible notes ($690 million at a $14.19 conversion price) come from Note 6. The fleet, utilization and price per flight hour are labeled **Judgment**, source J2. The ledger maps each ID to the filing, the filed date and the page.

**[1:00] On screen: `joby/model.py`, `build_periods`**

`build_periods` makes the timeline. The first period is a July-to-December 2026 stub: the full-year plan minus the actual first half from the 10-Q. That way I start from the June 30 balance sheet and never double count H1. Revenue is fleet times flight hours times revenue per flight hour, plus Blade services. From 2032 to 2040 a convergence stage fades growth and treats R&D and SG&A as mostly fixed costs.

**[1:35] On screen: `run_statements`**

`run_statements` is the integrated three-statement engine. EBIT feeds two tax calculations. The unlevered one, with net operating losses and the 80% limit, is for FCFF. The levered one is for net income. FCFF is EBIT minus cash tax, plus D&A, minus capex, minus the change in working capital. Stock-based compensation is not added back; I treat it as a real cost. The cash-flow statement has a funding rule: if cash falls below $500 million, Joby issues equity at a 10% discount. The balance sheet then rolls forward, and the code raises an error if assets don't equal liabilities plus equity within one cent.

**[2:15] On screen: `compute_wacc` and `value`**

`compute_wacc` is CAPM: 4.2% risk-free, beta 1.8, 5% premium, so a 13.2% cost of equity. The weights are market values, which gives a 12.73% WACC. `value` discounts every FCFF from September 1st at that single rate. The terminal value uses NOPAT times one plus g times one minus g over RONIC. Then comes the bridge: add cash, subtract the converts at principal (they're out of the money), subtract the mortgage, warrants and earnout, and divide by 1,051 million diluted shares. That's 34 cents.

**[2:55] On screen: terminal running `python -m unittest discover -s tests -v`**

Now validation. There are 23 tests. The first group reproduces the Week 3 known answer through the same discounting function: $27.4974 a share. The `RepairedDefects` tests cover three bugs in my Lab 11 script: a four-year path silently accepted, a different discount rate on the terminal value, and growth above the discount rate accepted. Each now raises an error, and the Lab 11 results are unchanged. Other tests check that the balance sheet balances in every scenario and that H1 ties to the 10-Q operating loss of minus $494.463 million. All pass.

**[3:30] On screen: `docs/locked-prediction.md`, `git log -2`, then run `python locked_test.py`**

My highest-risk claim is that the price needs more commercial scale than the evidence supports, so my locked test changes a revenue driver: revenue per flight hour, from $2,500 to $2,000. I wrote this prediction myself, without AI, and committed it here: *[read the commit time]*. I predicted *[read your prediction]*. Running it now… value per share went from 34 cents to *[read]*, and the action *[stayed / changed]*. *[One sentence: matched, or why not.]*

**[4:10] On screen: the validation register, cold-run row**

One failure mode. On a clean clone, `analysis.py` crashed with a Unicode error because the Windows console uses cp1252. I fixed it in commit 8f813c3 and reran: analysis OK, 23 tests OK, app healthy. The unresolved risk is that the fleet ramp is judgment; a two-year certification delay takes value to zero.

**[4:35] To reproduce:** clone, make a venv, `pip install -r requirements.txt`, `python analysis.py`. *(end ≤ 4:45)*
