# What only you can do before 11:59 PM ET, Oct. 19, 2026

Nobody else can write these items for you, including an AI. Each one is an assertion of fact in your name, or (for #1) a prediction that has to be yours and written before the run. Write only what is true.

## 1. Human-authored prediction for the Locked Changed-Input Record (required) — about 15 min

1. Open `docs/locked-prediction.md` and replace every `[WRITE HERE]` in your own words. **Do not use AI.** The test changes revenue per flight hour from $2,500 to $2,000. Predict the direction and rough size for value per share, new equity needed, and the committee action, and say why.
2. Commit that file **by itself**:
   ```
   git add docs/locked-prediction.md
   git commit -m "Lock human prediction for changed-input test"
   ```
3. Run `python locked_test.py`, then:
   ```
   git add output/locked_test_result.*
   git commit -m "Preserve locked changed-input result"
   ```
4. Fill in Section 4A of `docs/validation-and-ai-use.md` by hand: the timestamp and hash, before/after values, actual decision effect, reconciliation with your prediction, and a diagnosis if you were wrong.

## 2. Attestations — add these to Research-Evolution / Validation-and-AI-Use **only if true**

| # | Statement to make in your own words | Where | Why it is needed |
|---|---|---|---|
| A | Edition A (Lab 03, Sept. 1, 2026) was prepared without project-specific generative-AI assistance, before the Brightspace receipt. | Top of `docs/research-evolution.md` | The receipt transcription notes that your Q3 checkout answer contained the Edition A text in place of the requested attestation. If the statement is not fully true, describe what happened instead (AI Boundary Card: "Do not fabricate an earlier version or conceal the event"). |
| B | The prediction in `docs/locked-prediction.md` was written by me, before execution, without AI assistance. | Section 4A | Required field of the Locked Changed-Input Record. |
| C | I reviewed and own every assumption, the valuation range, and the Watch / defer recommendation. | End of `docs/decision-memo.md` | Ownership. Your videos must defend these numbers. |
| D | AI-use register: the exact tool/model names and versions **as shown to you**, plus dates, for Codex and ChatGPT. | Section 5 rows marked **[student]** | The checklist requires the "exposed tool/model/version and interaction date". Only you saw them. |
| E | Eric Boyd's quoted exchanges accurately reflect what occurred, and he reviewed the prediction before execution. (You confirmed this in chat on Oct. 19; keep the statement and its date.) | Section 4B (already entered) | Partner attribution. |

## 3. Recording and submission steps

1. **Push the repository to GitHub** under the name `Joby-research` (instructor feedback from Lab 4). Grant the instructional team access if it is private, and check access while logged out or by invitation.
2. **Record the three videos** (scripts in `docs/video-scripts/`) with a small webcam view. Upload each as **Unlisted** on YouTube with its own descriptive title. Hard limits: **3:00 / 5:00 / 5:00**.
3. **Correct the transcripts:** start from the YouTube captions and fix finance terms, tickers, names, and numbers. Save them as `docs/transcript-video-1.txt`, `-2.txt`, `-3.txt` using the template header. The scripts are **not** transcripts; transcripts must match what you actually said.
4. **Fill `docs/project-submission-manifest.csv`:** repository URL, the three video URLs/titles/durations, timestamp indices, access check, and final commit hash. Then run:
   ```
   python ../03_Course_materials/FIN43900-Fall2026-main/lessons/week-07/starter/project_audit.py docs/project-submission-manifest.csv
   ```
5. **Regenerate the PDFs** after your edits (`python tools/build_pdfs.py`). Upload to Brightspace: `Research-Evolution.pdf`, `Decision-Memo.pdf`, `Validation-and-AI-Use.pdf`, the three transcript `.txt` files, and the manifest. Save the receipt.

## What is not needed

- More partner statements: resolved on Oct. 19.
- A direct Brightspace receipt export: the transcription is acceptable as long as it is labeled as a transcription, which it is. Add a screenshot if you can get one.
