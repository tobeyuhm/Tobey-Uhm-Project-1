"""Integrated pro-forma statements -> FCFF -> WACC DCF -> equity bridge for Joby Aviation.

USD millions unless noted; shares in millions. Standard library only.

Conventions (stated once, used everywhere):
* Opening balance sheet is the latest filing available on the valuation date (10-Q, June 30, 2026).
* Period 1 is the July-December 2026 stub = FY2026 plan minus reported H1 2026 actuals.
* Cash flows are end-of-period; discount time is measured in years from the valuation date
  (Sept. 1, 2026), so the 2026 stub is discounted 0.33 years and FY2027 1.33 years.
* Reported cost lines (cost of revenue, R&D, SG&A) already contain D&A and stock-based
  compensation, exactly as in Joby's statements. D&A is added back in FCFF; stock-based
  compensation is NOT added back -- it is treated as an economic (cash-equivalent) cost so that
  future grants are not also counted as dilution.
* One discount rate (WACC) is passed explicitly to every discounting call.
"""
from __future__ import annotations

import copy
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUTS = ROOT / "data" / "joby_inputs_2026-09-01.json"
BALANCE_TOLERANCE = 0.01  # USD millions


class ModelInputError(ValueError):
    """Raised when inputs are incomplete or financially impossible."""


def load_inputs(path: Path | str = DEFAULT_INPUTS) -> dict:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


# ---------------------------------------------------------------------------
# Input validation -- the three defects found in the Lab 11 script are refused here.
# ---------------------------------------------------------------------------
def validate_inputs(inputs: dict) -> None:
    plan = inputs["operating_plan"]
    n_years = len(plan["years"])
    for key, values in plan.items():
        if isinstance(values, list) and len(values) != n_years:
            # Defect 1 (Lab 11): zip() silently truncated a 4-value path to four years.
            raise ModelInputError(
                f"operating_plan.{key} has {len(values)} values; expected {n_years} for years {plan['years']}"
            )
    conv = inputs["convergence"]
    if len(conv["revenue_growth"]) != len(conv["years"]):
        raise ModelInputError("convergence.revenue_growth must have one value per convergence year")
    wacc = compute_wacc(inputs)["wacc"]
    g = inputs["terminal"]["growth"]
    if g >= wacc:
        # Defect 3 (Lab 11): terminal growth >= discount rate gives a negative/infinite value.
        raise ModelInputError(f"Terminal growth {g:.2%} must be below WACC {wacc:.2%}")
    if g > 0.04:
        raise ModelInputError(f"Terminal growth {g:.2%} exceeds a defensible long-run nominal GDP growth rate (4%)")
    if inputs["terminal"]["return_on_new_invested_capital"] <= g:
        raise ModelInputError("Terminal RONIC must exceed terminal growth")
    if inputs["market"]["share_price"]["value"] <= 0:
        raise ModelInputError("Share price must be positive")


# ---------------------------------------------------------------------------
# Discount rate
# ---------------------------------------------------------------------------
def compute_wacc(inputs: dict) -> dict:
    m = inputs["market"]
    claims = inputs["bridge_claims"]
    shares = inputs["share_count"]["basic_shares_outstanding"]
    price = m["share_price"]["value"]
    cost_of_equity = m["risk_free_rate"]["value"] + m["beta"]["value"] * m["equity_risk_premium"]["value"]
    equity_mv = shares * price
    debt_mv = claims["convertible_notes_fair_value"] + claims["mortgage_loan_principal"]
    # Joby pays no cash tax for years (NOLs), so the interest tax shield is set to zero.
    after_tax_cost_of_debt = m["pretax_cost_of_debt"]["value"] * (1 - 0.0)
    weight_debt = debt_mv / (equity_mv + debt_mv)
    wacc = (1 - weight_debt) * cost_of_equity + weight_debt * after_tax_cost_of_debt
    return {
        "cost_of_equity": cost_of_equity,
        "after_tax_cost_of_debt": after_tax_cost_of_debt,
        "equity_market_value": equity_mv,
        "debt_market_value": debt_mv,
        "weight_debt": weight_debt,
        "wacc": wacc,
    }


def present_value(cash_flow: float, years: float, rate: float) -> float:
    """End-of-period discounting. Shared by the Joby DCF and the training known-answer test."""
    return cash_flow / (1 + rate) ** years


# ---------------------------------------------------------------------------
# Operating drivers for each period
# ---------------------------------------------------------------------------
def _explicit_year_drivers(inputs: dict, i: int) -> dict:
    p = inputs["operating_plan"]
    fleet_mult = inputs.get("_scenario", {}).get("fleet_multiplier", 1.0)
    price_mult = inputs.get("_scenario", {}).get("revenue_per_hour_multiplier", 1.0)
    evtol_rev = (
        p["avg_commercial_fleet"][i] * fleet_mult
        * p["flight_hours_per_aircraft"][i]
        * p["revenue_per_flight_hour_usd"][i] * price_mult
        / 1_000_000
    )
    services = p["services_revenue"][i]
    cogs = evtol_rev * (1 - p["evtol_gross_margin"][i]) + services * (1 - p["services_gross_margin"][i])
    return {
        "year": p["years"][i],
        "evtol_revenue": evtol_rev,
        "services_revenue": services,
        "revenue": evtol_rev + services,
        "cost_of_revenue": cogs,
        "rnd": p["research_and_development"][i],
        "sga": p["selling_general_admin"][i],
        "capex": p["capex"][i],
    }


def build_periods(inputs: dict) -> list[dict]:
    """Return operating drivers for the 2026 stub, FY2027-2031 explicit years, and 2032-2040 convergence."""
    valuation = date.fromisoformat(inputs["valuation_date"])
    plan = inputs["operating_plan"]
    h1 = inputs["h1_2026_actual"]
    periods = []
    for i, year in enumerate(plan["years"]):
        d = _explicit_year_drivers(inputs, i)
        t_end = (date(year, 12, 31) - valuation).days / 365.25
        if year == 2026:
            # Stub: July-December 2026 = full-year plan minus reported H1 actuals.
            d.update(
                label="2026 H2",
                revenue=d["revenue"] - h1["revenue"],
                services_revenue=d["services_revenue"] - h1["revenue"],
                cost_of_revenue=d["cost_of_revenue"] - h1["cost_of_revenue"],
                rnd=d["rnd"] - h1["research_and_development"],
                sga=d["sga"] - h1["selling_general_admin"],
                capex=d["capex"] - h1["capex"],
                fraction=0.5,
            )
        else:
            d.update(label=f"FY{year}", fraction=1.0)
        d["t"] = t_end
        d["stage"] = "explicit"
        periods.append(d)

    # Convergence: revenue growth fades; gross margin converges to steady state over the first
    # four years; R&D and SG&A behave as largely fixed costs (operating leverage) with floors
    # expressed as a share of revenue.
    conv = inputs["convergence"]
    last = periods[-1]
    start_gm = 1 - last["cost_of_revenue"] / last["revenue"]
    revenue, rnd, sga = last["revenue"], last["rnd"], last["sga"]
    for k, (year, growth) in enumerate(zip(conv["years"], conv["revenue_growth"]), start=1):
        w = min(1.0, k / conv["gross_margin_convergence_years"])
        prior_revenue = revenue
        revenue = revenue * (1 + growth)
        gm = start_gm + (conv["steady_state_gross_margin"] - start_gm) * w
        rnd = max(rnd * (1 + conv["rnd_nominal_growth"]), revenue * conv["steady_state_rnd_pct_revenue"])
        sga = max(sga * (1 + conv["sga_growth_share_of_revenue_growth"] * growth),
                  revenue * conv["steady_state_sga_pct_revenue"])
        periods.append({
            "year": year, "label": f"FY{year}", "fraction": 1.0, "stage": "convergence",
            "t": (date(year, 12, 31) - valuation).days / 365.25,
            "revenue": revenue, "evtol_revenue": None, "services_revenue": None,
            "cost_of_revenue": revenue * (1 - gm), "rnd": rnd, "sga": sga,
            "growth_capex": (revenue - prior_revenue) / conv["sales_to_capital"],
            "capex": None,  # maintenance (= D&A) + growth capex, set in the statement engine
        })
    return periods


# ---------------------------------------------------------------------------
# Integrated statements
# ---------------------------------------------------------------------------
def run_statements(inputs: dict) -> list[dict]:
    validate_inputs(inputs)
    ob = inputs["opening_balance_sheet"]
    od = inputs["other_drivers"]
    claims = inputs["bridge_claims"]
    tax_rate = inputs["market"]["marginal_tax_rate"]["value"]
    price = inputs["market"]["share_price"]["value"]
    issue_price = price * (1 - od["equity_issue_discount_to_price"])
    nol_limit = inputs["tax"]["nol_usage_limit"]
    h1 = inputs["h1_2026_actual"]

    cash = ob["cash_and_short_term_investments"]
    ppe = ob["ppe_net"]
    other_assets = ob["total_assets"] - cash - ppe
    debt = ob["long_term_debt_carrying"]
    other_liabilities = ob["total_liabilities"] - debt
    equity = ob["stockholders_equity"]
    shares = inputs["share_count"]["basic_shares_outstanding"]
    # H1 2026 operating loss is already in the June 30 equity; it still adds to the NOL pool.
    h1_ebit = h1["revenue"] - h1["cost_of_revenue"] - h1["research_and_development"] - h1["selling_general_admin"]
    nol_unlevered = inputs["tax"]["federal_nol_2025_12_31"] + max(0.0, -h1_ebit)
    nol_levered = nol_unlevered
    annual_interest = 0.0075 * claims["convertible_notes_principal"] + 0.06784 * claims["mortgage_loan_principal"]

    rows = []
    prior_revenue_annual = None
    for p in build_periods(inputs):
        f = p["fraction"]
        dep = od["depreciation_rate_on_opening_ppe"] * ppe * f
        capex = p["capex"] if p["capex"] is not None else dep + p["growth_capex"]
        revenue = p["revenue"]
        gross_profit = revenue - p["cost_of_revenue"]
        ebit = gross_profit - p["rnd"] - p["sga"]

        # Working capital moves with annualized revenue.
        annual_revenue = revenue / f
        if prior_revenue_annual is None:
            delta_nwc = 0.0
        else:
            delta_nwc = od["nwc_pct_of_revenue_change"] * (annual_revenue - prior_revenue_annual)
        prior_revenue_annual = annual_revenue

        # Unlevered cash tax (for FCFF), with the 80% NOL limitation.
        unlevered_tax, nol_unlevered = _cash_tax(ebit, nol_unlevered, tax_rate, nol_limit)
        fcff = ebit - unlevered_tax + dep - capex - delta_nwc

        # Levered income statement.
        interest_income = od["interest_income_rate_on_cash"] * cash * f
        interest_expense = annual_interest * f
        ebt = ebit + interest_income - interest_expense
        levered_tax, nol_levered = _cash_tax(ebt, nol_levered, tax_rate, nol_limit)
        net_income = ebt - levered_tax

        # Cash flow statement and funding rule.
        cfo = net_income + dep - delta_nwc
        cash_before_funding = cash + cfo - capex
        equity_raise = max(0.0, od["minimum_liquidity"] - cash_before_funding)
        new_shares = equity_raise / issue_price
        cash = cash_before_funding + equity_raise

        # Balance sheet roll-forward.
        ppe = ppe + capex - dep
        other_assets = other_assets + delta_nwc
        equity = equity + net_income + equity_raise
        shares = shares + new_shares
        assets = cash + ppe + other_assets
        liabilities_and_equity = debt + other_liabilities + equity
        gap = assets - liabilities_and_equity
        if abs(gap) > BALANCE_TOLERANCE:
            raise ModelInputError(f"{p['label']}: balance sheet does not balance (gap {gap:,.4f})")

        rows.append({
            "label": p["label"], "year": p["year"], "stage": p["stage"], "t": p["t"], "fraction": f,
            "revenue": revenue, "evtol_revenue": p["evtol_revenue"], "services_revenue": p["services_revenue"],
            "gross_profit": gross_profit, "rnd": p["rnd"], "sga": p["sga"], "ebit": ebit,
            "ebit_margin": ebit / revenue if revenue else None,
            "depreciation": dep, "capex": capex, "delta_nwc": delta_nwc,
            "unlevered_cash_tax": unlevered_tax, "fcff": fcff,
            "interest_income": interest_income, "interest_expense": interest_expense,
            "net_income": net_income, "cfo": cfo,
            "cash_before_funding": cash_before_funding, "equity_raise": equity_raise, "new_shares": new_shares,
            "cash": cash, "ppe": ppe, "other_assets": other_assets, "debt": debt,
            "other_liabilities": other_liabilities, "equity": equity, "shares_outstanding": shares,
            "balance_gap": gap, "nol_remaining_unlevered": nol_unlevered,
        })
    return rows


def _cash_tax(taxable: float, nol: float, rate: float, limit: float) -> tuple[float, float]:
    if taxable <= 0:
        return 0.0, nol - taxable
    used = min(nol, limit * taxable)
    return rate * (taxable - used), nol - used


# ---------------------------------------------------------------------------
# DCF and enterprise-to-equity bridge
# ---------------------------------------------------------------------------
def diluted_shares(inputs: dict, include_convertible: bool) -> dict:
    s = inputs["share_count"]
    parts = {
        "basic_shares_outstanding": s["basic_shares_outstanding"],
        "unvested_rsus": s["unvested_rsus"],
        "unvested_restricted_stock_awards": s["unvested_restricted_stock_awards"],
        "unvested_early_exercised_options": s["unvested_early_exercised_options"],
        "options_outstanding": s["options_outstanding"],
        "convertible_if_converted": inputs["bridge_claims"]["convertible_if_converted_shares"] if include_convertible else 0.0,
    }
    parts["total"] = sum(parts.values())
    return parts


def value(inputs: dict, wacc_override: float | None = None) -> dict:
    """Run the full model and return statements, DCF, bridge, and per-share value."""
    rows = run_statements(inputs)
    w = compute_wacc(inputs)
    wacc = w["wacc"] if wacc_override is None else wacc_override
    g = inputs["terminal"]["growth"]
    if g >= wacc:
        raise ModelInputError(f"Terminal growth {g:.2%} must be below the discount rate {wacc:.2%}")
    ronic = inputs["terminal"]["return_on_new_invested_capital"]
    tax_rate = inputs["market"]["marginal_tax_rate"]["value"]

    for r in rows:
        r["pv_fcff"] = present_value(r["fcff"], r["t"], wacc)
    pv_explicit = sum(r["pv_fcff"] for r in rows)

    final = rows[-1]
    if final["nol_remaining_unlevered"] > 0:
        # Remaining NOLs are valued separately as their undiscounted shield in the final year (small).
        nol_value = present_value(final["nol_remaining_unlevered"] * tax_rate, final["t"], wacc)
    else:
        nol_value = 0.0
    nopat_next = final["ebit"] * (1 - tax_rate) * (1 + g)
    terminal_fcff = nopat_next * (1 - g / ronic)
    terminal_value = terminal_fcff / (wacc - g)
    pv_terminal = present_value(terminal_value, final["t"], wacc)
    enterprise_value = pv_explicit + pv_terminal + nol_value

    claims = inputs["bridge_claims"]
    cash = inputs["opening_balance_sheet"]["cash_and_short_term_investments"]

    def bridge(convert_as_equity: bool) -> dict:
        convert_claim = 0.0 if convert_as_equity else claims["convertible_notes_principal"]
        equity_value = (
            enterprise_value + cash - convert_claim - claims["mortgage_loan_principal"]
            - claims["warrant_liability_fair_value"] - claims["blade_ebitda_earnout_max"]
        )
        sh = diluted_shares(inputs, include_convertible=convert_as_equity)
        return {
            "enterprise_value": enterprise_value,
            "plus_cash_and_short_term_investments": cash,
            "less_convertible_notes_principal": -convert_claim,
            "less_mortgage_loan": -claims["mortgage_loan_principal"],
            "less_warrants_fair_value": -claims["warrant_liability_fair_value"],
            "less_blade_ebitda_earnout": -claims["blade_ebitda_earnout_max"],
            "equity_value": equity_value,
            "diluted_shares": sh,
            "value_per_share": equity_value / sh["total"],
            "convertible_treatment": "if-converted (equity)" if convert_as_equity else "debt at principal",
        }

    as_debt = bridge(False)
    as_equity = bridge(True)
    # Holders convert only when the stock is worth more than the $14.19 conversion price.
    chosen = as_equity if as_equity["value_per_share"] > claims["convertible_conversion_price"] else as_debt

    return {
        "rows": rows,
        "wacc": wacc,
        "wacc_detail": w,
        "terminal_growth": g,
        "pv_explicit_fcff": pv_explicit,
        "terminal_value": terminal_value,
        "pv_terminal_value": pv_terminal,
        "pv_remaining_nol": nol_value,
        "enterprise_value": enterprise_value,
        "terminal_value_share_of_ev": pv_terminal / enterprise_value if enterprise_value > 0 else None,
        "bridge": chosen,
        "value_per_share": chosen["value_per_share"],
        "price": inputs["market"]["share_price"]["value"],
    }


# ---------------------------------------------------------------------------
# Scenario helpers -- each returns a fresh deep copy; the base dictionary is never mutated.
# ---------------------------------------------------------------------------
def with_changes(inputs: dict, **scenario) -> dict:
    new = copy.deepcopy(inputs)
    new.setdefault("_scenario", {}).update(scenario)
    return new


def delayed_certification(inputs: dict, years: int = 2) -> dict:
    """Causal downside: paid eVTOL service starts `years` later; development spend runs longer."""
    new = copy.deepcopy(inputs)
    p = new["operating_plan"]

    def shift(values, fill_count, fill_value=None):
        fill = [values[1] if fill_value is None else fill_value] * fill_count
        return [values[0]] + fill + values[1:len(values) - fill_count]

    p["avg_commercial_fleet"] = [0] + [0] * years + p["avg_commercial_fleet"][1:len(p["years"]) - years]
    p["flight_hours_per_aircraft"] = [0] + [0] * years + p["flight_hours_per_aircraft"][1:len(p["years"]) - years]
    p["evtol_gross_margin"] = [0.0] + [0.0] * years + p["evtol_gross_margin"][1:len(p["years"]) - years]
    p["research_and_development"] = shift(p["research_and_development"], years)
    p["selling_general_admin"] = shift(p["selling_general_admin"], years)
    p["capex"] = shift(p["capex"], years)
    new["_scenario_label"] = f"Certification and paid launch delayed {years} years"
    return new


def accelerated_execution(inputs: dict) -> dict:
    new = copy.deepcopy(inputs)
    p = new["operating_plan"]
    p["avg_commercial_fleet"] = [round(x * 1.4, 1) for x in p["avg_commercial_fleet"]]
    p["flight_hours_per_aircraft"] = [min(2200, x * 1.1) for x in p["flight_hours_per_aircraft"]]
    new["_scenario_label"] = "Faster fleet ramp (+40% aircraft) and +10% utilization"
    return new
