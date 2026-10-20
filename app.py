"""Joby committee app. Run:  streamlit run app.py

Panel 1 renders the frozen, validated output (output/visible_output.json) exactly as submitted.
Panel 2 is a live what-if that calls the same analysis engine (joby/model.py); it never types in
a result and never overwrites the frozen output.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import streamlit as st

from joby.model import ModelInputError, accelerated_execution, delayed_certification, load_inputs, value, with_changes

OUTPUT = Path(__file__).with_name("output") / "visible_output.json"

st.set_page_config(page_title="Joby (JOBY) committee decision", layout="wide")
st.title("Joby Aviation (JOBY) — Investment-committee decision system")

if not OUTPUT.exists():
    st.error("output/visible_output.json is missing. Run `python analysis.py` first.")
    st.stop()

r = json.loads(OUTPUT.read_text(encoding="utf-8"))
rng = r["valuation_range_per_share"]

st.caption(f"{r['decision_user']} · valuation date {r['valuation_date']} · balance sheet {r['balance_sheet_date']} · "
           f"{r['units']} · frozen run {r['run']['generated_utc']}")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Committee action", r["decision"]["action"])
c2.metric("Market price (Sept. 1, 2026)", f"${r['price']['value']:.2f}")
c3.metric("Base value / share", f"${rng['base']:.2f}")
c4.metric("Range (downside–upside)", f"\\${rng['low']:.2f}–\\${rng['high']:.2f}")
st.write(f"**Decision rule:** {r['decision']['rule']}".replace("$", "\\$"))

st.subheader("Scenarios — each run through the linked statements")
st.table([{
    "Scenario": s["label"],
    "Value/share": f"${s['value_per_share']:.2f}",
    "EV ($m)": f"{s['enterprise_value']:,.0f}",
    "2030 revenue ($m)": f"{s['revenue_2030']:,.0f}",
    "First FCFF > 0": s["first_positive_fcff_year"] or "none by 2040",
    "New equity needed ($m)": f"{s['cumulative_external_equity_needed']:,.0f}",
    "Action if true": s["action_if_this_case_is_true"],
} for s in r["scenarios"].values()])

rv = r["reverse_dcf"]
if rv["solved"]:
    st.info(f"**Reverse DCF:** \\${rv['target_price']:.2f} requires {rv['fleet_multiplier']:.2f}× the base fleet in every year "
            f"(≈{rv['implied_avg_fleet_2031']:.0f} aircraft in service in 2031; 2030 revenue ≈ \\${rv['implied_revenue_2030']:,.0f}M).")

left, right = st.columns(2)
with left:
    st.subheader("Enterprise-to-equity bridge (base)")
    b = r["bridge"]
    st.table([{"Step": k.replace("_", " "), "USD m": f"{b[k]:,.1f}"} for k in (
        "enterprise_value", "plus_cash_and_short_term_investments", "less_convertible_notes_principal",
        "less_mortgage_loan", "less_warrants_fair_value", "less_blade_ebitda_earnout", "equity_value")]
        + [{"Step": "diluted shares (m)", "USD m": f"{b['diluted_shares']['total']:,.3f}"},
           {"Step": "value per share ($)", "USD m": f"{b['value_per_share']:.2f}"}])
with right:
    st.subheader("Value per share: WACC × terminal growth")
    grid = r["sensitivity_wacc_x_terminal_growth"]
    st.table([{"WACC": f"{w:.2%}", **{f"g={g:.0%}": f"${v:.2f}" for g, v in zip(grid["terminal_growth"], row)}}
              for w, row in zip(grid["wacc"], grid["value_per_share"])])

st.subheader("Reversal triggers")
for t in r["reversal_triggers"]:
    st.write("•", t.replace("$", "\\$"))

st.divider()
st.header("Live what-if (recomputed by the analysis engine; frozen output above is unchanged)")
inputs = load_inputs()
col_a, col_b, col_c = st.columns(3)
case = col_a.selectbox("Operating case", ["Base", "Delayed certification (2 yrs)", "Accelerated execution"])
fleet = col_b.slider("Fleet multiplier (all years)", 0.5, 3.0, 1.0, 0.05)
beta = col_c.slider("Beta", 1.0, 2.6, float(inputs["market"]["beta"]["value"]), 0.1)
g = col_a.slider("Terminal growth", 0.01, 0.04, float(inputs["terminal"]["growth"]), 0.005)
gm = col_b.slider("Steady-state gross margin", 0.25, 0.55, float(inputs["convergence"]["steady_state_gross_margin"]), 0.01)

live = copy.deepcopy(inputs)
live["market"]["beta"]["value"] = beta
live["terminal"]["growth"] = g
live["convergence"]["steady_state_gross_margin"] = gm
if case.startswith("Delayed"):
    live = delayed_certification(live)
elif case.startswith("Accelerated"):
    live = accelerated_execution(live)
live = with_changes(live, fleet_multiplier=fleet)
try:
    v = value(live)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("WACC", f"{v['wacc']:.2%}")
    m2.metric("Enterprise value ($m)", f"{v['enterprise_value']:,.0f}")
    m3.metric("Value / share (floored at $0)", f"${max(0.0, v['value_per_share']):.2f}",
              delta=f"{max(0.0, v['value_per_share']) - r['price']['value']:+.2f} vs price")
    m4.metric("New equity needed ($m)", f"{sum(x['equity_raise'] for x in v['rows']):,.0f}")
    st.line_chart({"Revenue": [x["revenue"] for x in v["rows"]], "FCFF": [x["fcff"] for x in v["rows"]]})
    st.caption("Periods: 2026 H2, FY2027 … FY2040. USD millions.")
except ModelInputError as error:
    st.error(f"Input rejected by the model: {error}")

st.caption("Educational project for FIN 43900 (Purdue). Not investment advice.")
