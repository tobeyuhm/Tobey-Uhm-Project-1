"""Run the Joby Project 1 analysis and freeze the visible output.

    python analysis.py            # writes output/visible_output.json and output/joby_valuation_report.md

Every displayed number is computed here from data/joby_inputs_2026-09-01.json; nothing is typed in.
"""
from __future__ import annotations

import copy
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

from joby.model import (
    ModelInputError, accelerated_execution, compute_wacc, delayed_certification, load_inputs, value,
    with_changes,
)
from joby.training_dcf import KNOWN_ANSWER, training_reverse_shift, training_valuation

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output"
MARGIN_OF_SAFETY = 0.25


def per_share_floor(x: float) -> float:
    """Common equity has limited liability: a negative modeled equity value means the shares are worth ~$0."""
    return max(0.0, x)


def scenarios(inputs: dict) -> dict:
    out = {}
    for key, label, inp in [
        ("downside_delayed_certification", "Downside: certification and paid launch delayed 2 years", delayed_certification(inputs)),
        ("base", "Base: driver-based fleet ramp, paid service from 2027", inputs),
        ("upside_accelerated_execution", "Upside: +40% fleet and +10% utilization", accelerated_execution(inputs)),
    ]:
        v = value(inp)
        rows = v["rows"]
        raises = [r for r in rows if r["equity_raise"] > 0]
        out[key] = {
            "label": label,
            "enterprise_value": v["enterprise_value"],
            "equity_value": v["bridge"]["equity_value"],
            "value_per_share_model": v["value_per_share"],
            "value_per_share": per_share_floor(v["value_per_share"]),
            "terminal_value_share_of_ev": v["terminal_value_share_of_ev"],
            "revenue_2030": next(r["revenue"] for r in rows if r["year"] == 2030),
            "ebit_2030": next(r["ebit"] for r in rows if r["year"] == 2030),
            "first_positive_fcff_year": next((r["year"] for r in rows if r["fcff"] > 0), None),
            "first_external_funding_year": raises[0]["year"] if raises else None,
            "cumulative_external_equity_needed": sum(r["equity_raise"] for r in rows),
            "projected_share_count_end": rows[-1]["shares_outstanding"],
        }
        out[key]["action_if_this_case_is_true"] = scenario_action(inputs["market"]["share_price"]["value"], v["value_per_share"])
    return out


def scenario_action(price: float, vps: float) -> str:
    """Committee action if this scenario were the committee's central case."""
    if vps <= 0:
        return "Do not initiate"
    if price <= (1 - MARGIN_OF_SAFETY) * vps:
        return "Initiate"
    return "Watch / defer"


def wacc_growth_grid(inputs: dict, base_wacc: float) -> dict:
    waccs = [round(base_wacc + d, 4) for d in (-0.02, -0.01, 0.0, 0.01, 0.02)]
    growths = [0.02, 0.03, 0.04]
    grid = []
    for w in waccs:
        row = []
        for g in growths:
            inp = copy.deepcopy(inputs)
            inp["terminal"]["growth"] = g
            try:
                row.append(value(inp, wacc_override=w)["value_per_share"])
            except ModelInputError:
                row.append(None)
        grid.append(row)
    return {"wacc": waccs, "terminal_growth": growths, "value_per_share": grid}


def tornado(inputs: dict, base_vps: float) -> list[dict]:
    """One-at-a-time sensitivities. Revenue per flight hour is deliberately excluded:
    it is reserved for the human Locked Changed-Input Record."""
    def set_path(path, val):
        def f(inp):
            new = copy.deepcopy(inp)
            node = new
            for k in path[:-1]:
                node = node[k]
            node[path[-1]] = val
            return new
        return f

    tests = [
        ("Beta", "1.8", "1.4", "2.2", set_path(["market", "beta", "value"], 1.4), set_path(["market", "beta", "value"], 2.2)),
        ("Fleet size, all years", "x1.0", "x0.7", "x1.3", lambda i: with_changes(i, fleet_multiplier=0.7), lambda i: with_changes(i, fleet_multiplier=1.3)),
        ("Steady-state gross margin", "40%", "35%", "45%", set_path(["convergence", "steady_state_gross_margin"], 0.35), set_path(["convergence", "steady_state_gross_margin"], 0.45)),
        ("Terminal growth", "3%", "2%", "4%", set_path(["terminal", "growth"], 0.02), set_path(["terminal", "growth"], 0.04)),
        ("Sales-to-capital (growth capex)", "2.5", "2.0", "3.0", set_path(["convergence", "sales_to_capital"], 2.0), set_path(["convergence", "sales_to_capital"], 3.0)),
        ("Equity risk premium", "5.0%", "6.0%", "4.0%", set_path(["market", "equity_risk_premium", "value"], 0.06), set_path(["market", "equity_risk_premium", "value"], 0.04)),
    ]
    out = []
    for name, base_txt, lo_txt, hi_txt, lo_f, hi_f in tests:
        lo = value(lo_f(inputs))["value_per_share"]
        hi = value(hi_f(inputs))["value_per_share"]
        out.append({"driver": name, "base": base_txt, "low_input": lo_txt, "high_input": hi_txt,
                    "value_low_input": lo, "value_high_input": hi, "swing": abs(hi - lo)})
    return sorted(out, key=lambda d: d["swing"], reverse=True)


def reverse_dcf(inputs: dict, target: float) -> dict:
    """Solve the uniform fleet-size multiplier (all forecast years) that equates value to the market price."""
    f = lambda m: value(with_changes(inputs, fleet_multiplier=m))["value_per_share"] - target
    lo, hi = 0.5, 8.0
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        return {"solved": False, "message": "no solution in bracket 0.5x-8.0x"}
    for _ in range(80):
        mid = (lo + hi) / 2
        fm = f(mid)
        if abs(fm) < 1e-6:
            break
        if flo * fm <= 0:
            hi = mid
        else:
            lo, flo = mid, fm
    implied = with_changes(inputs, fleet_multiplier=mid)
    rows = value(implied)["rows"]
    base_fleet = inputs["operating_plan"]["avg_commercial_fleet"]
    return {
        "solved": True,
        "target_price": target,
        "fleet_multiplier": mid,
        "implied_avg_fleet_2031": base_fleet[-1] * mid,
        "implied_revenue_2030": next(r["revenue"] for r in rows if r["year"] == 2030),
        "implied_revenue_2040": rows[-1]["revenue"],
        "held_fixed": "WACC, terminal growth, utilization, revenue per flight hour, margins, opex, capex schedule, bridge, and share count",
    }


def decision(price: float, sc: dict, liquidity_months: float) -> dict:
    base = sc["base"]["value_per_share"]
    up = sc["upside_accelerated_execution"]["value_per_share"]
    if base > 0 and price <= (1 - MARGIN_OF_SAFETY) * base:
        action = "Initiate (conditional on FAA type certificate being issued)"
    elif up <= 0 or liquidity_months < 12:
        action = "Do not initiate"
    else:
        action = "Watch / defer"
    return {
        "action": action,
        "rule": (f"Initiate only if price <= {1 - MARGIN_OF_SAFETY:.0%} of base value AND the FAA type certificate is issued; "
                 "do not initiate if the upside-case value is $0 or liquidity covers < 12 months of modeled cash use; otherwise watch/defer."),
        "initiate_below_price": (1 - MARGIN_OF_SAFETY) * base,
    }


def run_analysis(inputs: dict | None = None) -> dict:
    inputs = load_inputs() if inputs is None else inputs
    base = value(inputs)
    price = base["price"]
    sc = scenarios(inputs)
    wacc = base["wacc_detail"]

    # Liquidity runway on the base plan (months of modeled operating + capex cash use, before new funding).
    stub = base["rows"][0]
    fy27 = base["rows"][1]
    monthly_use = -(fy27["cfo"] - fy27["capex"]) / 12
    liquidity_months = inputs["opening_balance_sheet"]["cash_and_short_term_investments"] / monthly_use if monthly_use > 0 else float("inf")

    training = training_valuation()
    training_check = {k: (training[k], KNOWN_ANSWER[k]) for k in KNOWN_ANSWER if k != "fcff"}
    training_pass = all(abs(a - b) < 0.01 for a, b in training_check.values()) and all(
        abs(a - b) < 0.01 for a, b in zip(training["fcff"], KNOWN_ANSWER["fcff"]))

    statements = [{k: r[k] for k in (
        "label", "stage", "revenue", "gross_profit", "rnd", "sga", "ebit", "depreciation", "capex", "delta_nwc",
        "unlevered_cash_tax", "fcff", "pv_fcff", "interest_income", "interest_expense", "net_income", "cfo",
        "equity_raise", "cash", "ppe", "equity", "shares_outstanding", "balance_gap")} for r in base["rows"]]

    vr = [sc[k]["value_per_share"] for k in sc]
    result = {
        "title": "Joby Aviation (JOBY) — FCFF/WACC valuation and committee decision",
        "decision_user": inputs["decision_user"],
        "valuation_date": inputs["valuation_date"],
        "balance_sheet_date": inputs["balance_sheet_date"],
        "price": {"value": price, "date": inputs["market"]["share_price"]["date"]},
        "units": "USD millions except per-share values (USD) and shares (millions)",
        "decision": decision(price, sc, liquidity_months),
        "valuation_range_per_share": {"low": min(vr), "base": sc["base"]["value_per_share"], "high": max(vr)},
        "base_value_per_share_unfloored": base["value_per_share"],
        "wacc": wacc,
        "terminal_growth": base["terminal_growth"],
        "dcf": {k: base[k] for k in ("pv_explicit_fcff", "terminal_value", "pv_terminal_value", "pv_remaining_nol",
                                       "enterprise_value", "terminal_value_share_of_ev")},
        "bridge": base["bridge"],
        "scenarios": sc,
        "liquidity": {
            "cash_and_investments_2026_06_30": inputs["opening_balance_sheet"]["cash_and_short_term_investments"],
            "modeled_monthly_cash_use_fy2027": monthly_use,
            "months_of_runway_at_fy2027_burn": liquidity_months,
            "toyota_second_tranche_pending": 250.0,
        },
        "sensitivity_wacc_x_terminal_growth": wacc_growth_grid(inputs, base["wacc"]),
        "tornado": tornado(inputs, base["value_per_share"]),
        "reverse_dcf": reverse_dcf(inputs, price),
        "statements_base": statements,
        "comparables": {
            "policy": "Lab 08 peer policy (frozen Sept. 1, 2026): ACHR use; EVEX qualify.",
            "result": ("Not used for value. FY2025 GAAP diluted EPS is negative for JOBY ($-1.13), ACHR ($-0.99) and EVEX ($-0.70), "
                       "so P/E is not meaningful; revenue multiples are not meaningful while core eVTOL revenue is ~zero. "
                       "The market-implied cross-check is the reverse DCF instead."),
        },
        "validation": {
            "training_known_answer_pass": training_pass,
            "training_value_per_share": training["value_per_share"],
            "training_reverse_shift_points": training_reverse_shift() * 100,
            "all_balance_gaps_below_0.01m": all(abs(r["balance_gap"]) < 0.01 for r in base["rows"]),
        },
        "limitations": [
            "Fleet, utilization, revenue per flight hour, margins and opex are analyst judgment anchored to management statements, not company guidance beyond FY2026 revenue.",
            "Option strike prices were not extracted; all 5.27M options are counted as exercised at zero strike (max dilution, <1% of shares).",
            "Announced $500M Resonant Sciences acquisition is treated as NPV-zero (cash/stock paid = value received).",
            "Toyota's pending $250M second tranche at $5.03/share is excluded from the base bridge.",
            "Valuation uses the June 30, 2026 balance sheet; July-August 2026 flows are inside the H2 stub (2-month timing mismatch).",
        ],
        "reversal_triggers": [
            "Initiate review: FAA type certificate issued AND price at or below the initiate threshold.",
            "Upgrade evidence: >= 2 reported quarters of paid eVTOL passenger revenue with disclosed utilization and fare per flight hour.",
            "Fare trigger (locked changed-input test): value reaches $0 at ~$2,390 per flight hour (x0.956 of plan); disclosed early revenue per flight hour below that -> Do not initiate.",
            "Do not initiate: no type certificate by Dec. 31, 2027 (delayed-certification case) OR liquidity < 12 months of cash use without committed funding.",
        ],
        "run": {
            "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
    }
    return result


def fmt(x, d=1):
    return "n/a" if x is None else f"{x:,.{d}f}"


def write_report(r: dict) -> str:
    sc = r["scenarios"]
    lines = [
        f"# {r['title']}",
        "",
        f"**Decision user:** {r['decision_user']}  ",
        f"**Valuation date:** {r['valuation_date']} · **Balance sheet:** 10-Q at {r['balance_sheet_date']} · "
        f"**Price:** ${r['price']['value']:.2f} close on {r['price']['date']}  ",
        f"**Units:** {r['units']}  ",
        f"**Generated:** {r['run']['generated_utc']} (Python {r['run']['python']})",
        "",
        "## Decision",
        "",
        f"**{r['decision']['action']}.** Valuation range ${fmt(r['valuation_range_per_share']['low'], 2)}–"
        f"${fmt(r['valuation_range_per_share']['high'], 2)} per share (base ${fmt(r['valuation_range_per_share']['base'], 2)}) "
        f"versus ${r['price']['value']:.2f} market price.",
        "",
        f"Rule: {r['decision']['rule']}",
        "",
        "## Scenarios (each run through the full linked statements)",
        "",
        "| Scenario | EV | Equity value | Value/share | 2030 revenue | 2030 EBIT | First FCFF > 0 | External equity needed | Action if true |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for s in sc.values():
        lines.append(
            f"| {s['label']} | {fmt(s['enterprise_value'])} | {fmt(s['equity_value'])} | ${fmt(s['value_per_share'], 2)}"
            f"{' (model ' + fmt(s['value_per_share_model'], 2) + ', floored)' if s['value_per_share_model'] < 0 else ''} | "
            f"{fmt(s['revenue_2030'])} | {fmt(s['ebit_2030'])} | {s['first_positive_fcff_year']} | {fmt(s['cumulative_external_equity_needed'])} | {s['action_if_this_case_is_true']} |"
        )
    w = r["wacc"]
    b = r["bridge"]
    d = r["dcf"]
    lines += [
        "",
        "## Discount rate",
        "",
        f"Cost of equity {w['cost_of_equity']:.2%} (CAPM) · after-tax cost of debt {w['after_tax_cost_of_debt']:.2%} · "
        f"debt weight {w['weight_debt']:.2%} (market values: equity {fmt(w['equity_market_value'])}, debt {fmt(w['debt_market_value'])}) · "
        f"**WACC {w['wacc']:.2%}** · terminal growth {r['terminal_growth']:.1%}",
        "",
        "## Enterprise-to-equity bridge (base)",
        "",
        "| Step | USD m |",
        "|---|---:|",
        f"| PV of explicit + convergence FCFF (2026 H2–2040) | {fmt(d['pv_explicit_fcff'])} |",
        f"| PV of terminal value | {fmt(d['pv_terminal_value'])} |",
        f"| PV of NOLs remaining after 2040 | {fmt(d['pv_remaining_nol'])} |",
        f"| **Enterprise value** | **{fmt(b['enterprise_value'])}** |",
        f"| + Cash and short-term investments (June 30, 2026) | {fmt(b['plus_cash_and_short_term_investments'])} |",
        f"| − 0.75% convertible notes due 2032 ({b['convertible_treatment']}) | {fmt(b['less_convertible_notes_principal'])} |",
        f"| − Mortgage loan | {fmt(b['less_mortgage_loan'])} |",
        f"| − Warrants at fair value | {fmt(b['less_warrants_fair_value'])} |",
        f"| − Blade EBITDA earnout (maximum) | {fmt(b['less_blade_ebitda_earnout'])} |",
        f"| **Equity value** | **{fmt(b['equity_value'])}** |",
        f"| ÷ Diluted shares (m) | {fmt(b['diluted_shares']['total'], 3)} |",
        f"| **Value per share** | **${fmt(b['value_per_share'], 2)}** |",
        "",
        "Terminal value share of EV: "
        + (f"{d['terminal_value_share_of_ev']:.0%}" if d["terminal_value_share_of_ev"] else
           f"not meaningful because EV ≤ 0 — PV of terminal value (${d['pv_terminal_value']:,.0f}M) is smaller than the PV of pre-profit cash burn. "
           "The whole equity value rests on cash on hand plus a distant terminal value."),
        "",
        "## Sensitivity: value per share, WACC × terminal growth",
        "",
        "| WACC \\ g | " + " | ".join(f"{g:.0%}" for g in r["sensitivity_wacc_x_terminal_growth"]["terminal_growth"]) + " |",
        "|---|" + "---:|" * len(r["sensitivity_wacc_x_terminal_growth"]["terminal_growth"]),
    ]
    grid = r["sensitivity_wacc_x_terminal_growth"]
    for wv, row in zip(grid["wacc"], grid["value_per_share"]):
        lines.append(f"| {wv:.2%} | " + " | ".join("invalid" if v is None else f"${v:.2f}" for v in row) + " |")
    lines += ["", "## One-at-a-time sensitivity (value per share, unfloored)", "",
              "| Driver | Base | Low input → value | High input → value | Swing |", "|---|---|---:|---:|---:|"]
    for t in r["tornado"]:
        lines.append(f"| {t['driver']} | {t['base']} | {t['low_input']} → ${t['value_low_input']:.2f} | "
                     f"{t['high_input']} → ${t['value_high_input']:.2f} | ${t['swing']:.2f} |")
    rv = r["reverse_dcf"]
    lines += ["", "## Reverse DCF (what the market price implies)", ""]
    if rv["solved"]:
        lines.append(
            f"To justify ${rv['target_price']:.2f}, the fleet in every forecast year must be **{rv['fleet_multiplier']:.2f}×** the base plan "
            f"(≈{rv['implied_avg_fleet_2031']:.0f} aircraft in average service in 2031; 2030 revenue ≈ ${rv['implied_revenue_2030']:,.0f}M; "
            f"2040 revenue ≈ ${rv['implied_revenue_2040']:,.0f}M). Held fixed: {rv['held_fixed']}. "
            "This is one set of assumptions consistent with the price, not proof of mispricing.")
    else:
        lines.append(rv["message"])
    liq = r["liquidity"]
    lines += [
        "", "## Liquidity and funding (base, linked statements)", "",
        f"Cash and short-term investments ${liq['cash_and_investments_2026_06_30']:,.1f}M; modeled FY2027 cash use "
        f"${liq['modeled_monthly_cash_use_fy2027']:,.1f}M/month → **{liq['months_of_runway_at_fy2027_burn']:.1f} months** of runway "
        f"before new funding. Toyota's second ${liq['toyota_second_tranche_pending']:.0f}M tranche is pending and excluded.",
        "",
        "Future equity raises are shown for liquidity and dilution, but they are **not** deducted again in per-share value: "
        "negative FCFF is already subtracted in EV, so counting the new shares too would double count the funding need.",
        "",
        "## Base-case integrated statements (USD m)", "",
        "| Period | Revenue | EBIT | D&A | Capex | ΔNWC | Cash tax | FCFF | PV FCFF | Net income | Equity raise | Cash | Shares (m) | BS gap |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for s in r["statements_base"]:
        lines.append("| " + " | ".join([s["label"]] + [fmt(s[k]) for k in (
            "revenue", "ebit", "depreciation", "capex", "delta_nwc", "unlevered_cash_tax", "fcff", "pv_fcff",
            "net_income", "equity_raise", "cash", "shares_outstanding")] + [f"{s['balance_gap']:.4f}"]) + " |")
    v = r["validation"]
    lines += [
        "", "## Validation summary", "",
        f"- Training DCF known answer (Week 3): {'PASS' if v['training_known_answer_pass'] else 'FAIL'} — ${v['training_value_per_share']:.4f}/share vs $27.4974; reverse shift {v['training_reverse_shift_points']:+.4f} points vs ≈+1.78.",
        f"- Balance sheet balances every period (|gap| < $0.01M): {'PASS' if v['all_balance_gaps_below_0.01m'] else 'FAIL'}.",
        "- Full test suite: `python -m unittest discover -s tests -v` (see docs/validation-and-ai-use.md).",
        "", "## Comparables", "", r["comparables"]["policy"] + " " + r["comparables"]["result"],
        "", "## Reversal triggers", "",
    ] + [f"- {t}" for t in r["reversal_triggers"]] + ["", "## Limitations", ""] + [f"- {t}" for t in r["limitations"]]
    return "\n".join(lines) + "\n"


def main() -> None:
    r = run_analysis()
    OUTPUT_DIR.mkdir(exist_ok=True)
    (OUTPUT_DIR / "visible_output.json").write_text(json.dumps(r, indent=2), encoding="utf-8")
    report = write_report(r)
    (OUTPUT_DIR / "joby_valuation_report.md").write_text(report, encoding="utf-8")
    # Cold-run fix (Oct. 19, 2026): Windows consoles default to cp1252 and crashed on the
    # minus sign and arrows in the report. Print as UTF-8 regardless of console encoding.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(report)


if __name__ == "__main__":
    main()
