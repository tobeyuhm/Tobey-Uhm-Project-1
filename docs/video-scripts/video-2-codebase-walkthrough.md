# Video 2 — Codebase and Validation Walkthrough (hard limit 5:00)

**Title for YouTube:** JOBY Project 1 — Video 2: Codebase and Validation Walkthrough
**On screen:** webcam thumbnail, VS Code with `Joby-research` open, and a terminal at the repo root.
**About 486 spoken words.** At a slow pace (~110 words a minute) that is about 4:25 of talking. Keep the scrolling and test runs quick so you finish before 5:00.
**Before recording:** write and commit `docs/locked-prediction.md`.

---

**[0:00] On screen: the repo folder tree**

This is my Joby repository. It flows from data, to the model, to tests, to a frozen output, to the app.

**[0:15] On screen: `data/joby_inputs_2026-09-01.json`**

Every input lives in this one file, with its units and a source. Cash comes from the June 2026 10-Q. The fleet and pricing are labeled judgment.

**[0:35] On screen: `joby/model.py` → `build_periods`**

The model starts from the June 30 balance sheet. The first period is July to December 2026, which is the full-year plan minus the actual first half, so nothing is double counted. Revenue is fleet times flight hours times price per hour, plus Blade services.

**[1:05] On screen: `run_statements`**

This builds the three linked statements. Free cash flow to the firm is EBIT minus cash taxes, plus depreciation, minus capex and working capital. If cash drops below $500 million, Joby issues stock. The code stops with an error if the balance sheet doesn't balance.

**[1:35] On screen: `compute_wacc`, then `value`**

The WACC is 12.7%, from CAPM with a beta of 1.8. `value` discounts every cash flow from September 1st, adds a terminal value, then bridges to equity: add cash, subtract the convertible notes and other claims, and divide by diluted shares. That gives 34 cents a share.

**[2:10] On screen: terminal → `python -m unittest discover -s tests -v`**

Now the tests. There are 23. They reproduce the Week 3 known answer, $27.50 a share, and catch the three bugs from my Lab 11 code. They also check that the balance sheet balances in every scenario. *(let it run)* All pass.

**[2:45] On screen: `docs/locked-prediction.md` → terminal `python locked_test.py`**

My riskiest claim is that the price needs more scale than the evidence supports. So my locked test cuts revenue per flight hour from $2,500 to $2,000. I wrote this prediction myself and committed it first. I predicted value would fall and the action would stay watch/defer. *(run)* Value fell from 34 cents to negative $1.34, so I was right on direction. But the action changed to do not initiate, because value went below zero. I also assumed costs stay fixed, but my model lets costs fall with price, so the real hit could be even worse.

**[3:30] On screen: `docs/validation-and-ai-use.md`, cold-run row**

One failure: on a fresh install the analysis crashed on a Windows text-encoding error. I fixed it and reran it clean. The biggest remaining risk is that the fleet ramp is my judgment.

**[3:55] On screen: `docs/validation-and-ai-use.md`, Section 4A reconciliation**

The locked test also showed me a weakness in my own model. My cost of revenue is a percentage of revenue, so when the fare drops, costs drop too. In real life, pilot pay, maintenance and charging cost per flight hour don't fall when fares fall. So my model probably understates how bad a fare cut would be. The next fix is to split the cost into a fixed cost per flight hour plus a margin.

**[4:20] On screen: `README.md`, setup section**

The test also gave me a new trigger. Value hits zero at about $2,390 per flight hour, only about 4% below my plan. So once Joby reports real fares, that's the first number I'll check.

**[4:40] On screen: terminal**

To reproduce everything, clone the repo, make a virtual environment, install the requirements, run `python analysis.py`, and then run the tests. *(stop by about 4:55)*
