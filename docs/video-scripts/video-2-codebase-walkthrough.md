# Video 2 — Codebase and Validation Walkthrough (hard limit 5:00; target ≈ 4:30)

**Title for YouTube:** JOBY Project 1 — Video 2: Codebase and Validation Walkthrough
**Setup:** webcam overlay; VS Code open on `Joby-research`; terminal open with Ctrl+` (it starts in the repo folder). Use Ctrl+G to jump to a line.
**Length:** about 400 spoken words, which is about 3:40 at a slow pace, plus about 50 seconds for running commands = **about 4:30**.

---

**[0:00] Explorer sidebar (folder tree)**

This is my Joby repository. It flows from data, to the model, to tests, to a frozen output, to the app.

**[0:15] `data/joby_inputs_2026-09-01.json`, line 20, then line 73**

Every input lives in this one file, with its units and a source. Cash comes from the June 2026 10-Q. The fleet and pricing are labeled judgment.

**[0:35] `joby/model.py`, line 122, `build_periods`**

The model starts from the June 30 balance sheet. The first period is July to December 2026, which is the full-year plan minus the actual first half, so nothing is double counted. Revenue is fleet times flight hours times price per hour, plus Blade services.

**[1:05] `model.py`, line 178, `run_statements`; point at lines 222, 234 and 247**

This builds the three linked statements. Free cash flow to the firm is EBIT minus cash taxes, plus depreciation, minus capex and working capital. If cash drops below $500 million, Joby issues stock. The code stops with an error if the balance sheet doesn't balance.

**[1:35] `model.py`, line 68 `compute_wacc`, then line 290 `value`, then line 320 bridge**

The WACC is 12.7%, from CAPM with a beta of 1.8. `value` discounts every cash flow from September 1st, adds a terminal value, then bridges to equity: add cash, subtract the convertible notes and other claims, and divide by diluted shares. That gives 34 cents a share.

**[2:10] `tests/test_model.py`, line 27 → terminal ▶ RUN `python -m unittest discover -s tests -v`**

Now the tests. There are 23. They reproduce the Week 3 known answer, $27.50 a share, and catch the three bugs from my Lab 11 code. They also check that the balance sheet balances in every scenario. *(wait for OK)* All pass.

**[2:45] `docs/locked-prediction.md` → terminal ▶ RUN `git log --oneline -6`, point at `1796d19`**

My riskiest claim is that the price needs more scale than the evidence supports. So my locked test cuts revenue per flight hour from $2,500 to $2,000. I wrote this prediction myself and committed it here, before running anything. I predicted value would fall and the action would stay watch/defer.

**[3:15] Terminal ▶ RUN `python locked_test.py`**

Value fell from 34 cents to negative $1.34, so I was right on direction. But the action changed to do not initiate, because value went below zero. That means a fare only about 4% below plan, around $2,390 an hour, flips the decision. That's now a monitoring trigger.

**[3:45] `docs/validation-and-ai-use.md`, line 54 (cold-run row)**

Two failure modes. First, on a fresh install the analysis crashed on a Windows text-encoding error. I fixed it and reran it clean. Second, the locked test exposed a limitation: my costs fall when the fare falls, but real pilot and maintenance costs don't. So the real downside is probably worse.

**[4:15] Terminal**

To reproduce it, clone the repo, install the requirements, and run `python analysis.py`. Thank you. *(stop ≈ 4:30)*

---

**After recording:** run `git checkout -- output` so that the committed locked-test record keeps its original run time.
