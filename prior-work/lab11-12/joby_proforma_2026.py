"""Joby Aviation five-year commercialization pro forma (USD millions except shares).

This is a separate, local submission file.  It does not import the ABG engine
because an auto retailer's inventory and floor-plan financing are not relevant
to a pre-commercial eVTOL developer.  Run with: py joby_proforma_2026.py
"""

from math import pow


YEARS = (2026, 2027, 2028, 2029, 2030)
MINIMUM_CASH = 300.0
EQUITY_ISSUE_PRICE = 6.22
COST_OF_EQUITY = 0.13
TERMINAL_GROWTH = 0.03
MARKET_PRICE = 6.22
MARKET_PRICE_DATE = "September 24, 2026 (intraday quote; replace with the close if submitting later)"

# This is deliberately an absolute commercialization ramp, not an arbitrary
# growth rate on $53.4M of FY2025 revenue.
REVENUE = (75.0, 300.0, 800.0, 1_800.0, 3_500.0)
GROSS_MARGIN = (0.35, 0.40, 0.45, 0.50, 0.55)
R_AND_D = (650.0, 700.0, 775.0, 850.0, 900.0)
SGA = (190.0, 240.0, 325.0, 425.0, 525.0)
CAPEX = (90.0, 125.0, 180.0, 240.0, 300.0)
TAX_RATE = 0.21

# The sensitivity routine starts every run from this immutable base set.  Scenario
# code must not mutate the module-level assumptions above or reuse a prior run's
# results; build_inputs() returns a fresh independent dictionary each time.
BASE_INPUTS = {
    "years": YEARS,
    "minimum_cash": MINIMUM_CASH,
    "equity_issue_price": EQUITY_ISSUE_PRICE,
    "cost_of_equity": COST_OF_EQUITY,
    "terminal_growth": TERMINAL_GROWTH,
    "revenue": REVENUE,
    "gross_margin": GROSS_MARGIN,
    "r_and_d": R_AND_D,
    "sga": SGA,
    "capex": CAPEX,
    "tax_rate": TAX_RATE,
}


def build_inputs():
    """Return a fresh base-case input set for one independent model run."""
    return {key: tuple(value) if isinstance(value, tuple) else value
            for key, value in BASE_INPUTS.items()}


FILING_2025 = "2025 10-K, filed Feb. 26, 2026, pp. 52-56, https://www.sec.gov/Archives/edgar/data/1819848/000181984826000160/joby-20251231.htm"
FILING_2024 = "2024 10-K, filed Feb. 27, 2025, pp. 50-53, https://www.sec.gov/Archives/edgar/data/1819848/000181984825000196/joby-20241231.htm"
FILING_2023 = "2023 10-K, filed Feb. 26, 2024, pp. 45-49, https://www.sec.gov/Archives/edgar/data/1819848/000181984824000125/joby-20231231.htm"

# FY2025 opening balance sheet, from 2025 10-K p. 52.  In this simplified model,
# ``cash`` means cash, cash equivalents, and short-term investments because all
# three are reported current liquid assets available to fund operations. Other assets and
# liabilities are the balancing residuals from the reported balance sheet.
OPENING = {
    "cash": 1_407.916,
    "ppe": 146.571,
    "other_assets": 240.582,
    "liabilities": 385.356,
    "equity": 1_409.713,
    "shares": 915.076698,
}


ASSUMPTION_TABLE = """
ASSUMPTION SET
Value                                      Label      Reason
FY2025 opening cash $1,407.916M            History    Cash, cash equivalents, plus short-term investments reported on the FY2025 balance sheet; grouped as cash in this simplified model.
FY2025 opening PP&E $146.571M              History    Reported net property and equipment at December 31, 2025.
FY2025 opening other assets $240.582M      History    Total assets less cash and PP&E; grouped solely to keep the simplified model tied to the filing.
FY2025 opening liabilities $385.356M       History    Reported total liabilities at December 31, 2025.
FY2025 opening equity $1,409.713M          History    Reported total stockholders' equity at December 31, 2025.
FY2025 shares 915.077M                     History    Shares issued and outstanding at December 31, 2025.
2026-30 revenue: 75/300/800/1,800/3,500    Judgment   I model a staged launch and route build-out, not a percentage growth rate on a tiny pre-commercial revenue base. Certification, fleet deployment, and customer demand would change it.
2026-30 gross margin: 35/40/45/50/55%      Judgment   Early operations should carry low utilization and fixed operating costs; margin improves only as routes and aircraft utilization scale. Actual service pricing, maintenance, and load factor data would change it.
2026-30 R&D: 650/700/775/850/900           Judgment   Engineering, certification, manufacturing-readiness, and autonomy work remain material throughout the forecast. A certification decision or a disclosed production plan would change it.
2026-30 SG&A: 190/240/325/425/525          Judgment   Commercial operations require selling, dispatch, regulatory, and corporate infrastructure. A disclosed launch geography or staffing plan would change it.
2026-30 capex: 90/125/180/240/300          Judgment   Fleet, tooling, facilities, and operating infrastructure must grow with launch. Company guidance or signed fleet/facility commitments would change it.
Depreciation = 22.86% of opening PP&E      History    FY2025 property-and-equipment depreciation of $33.5M divided by FY2025 ending PP&E of $146.571M; held constant as a simplification.
21% cash tax rate on positive pretax income Judgment  Joby has losses and a tax rate is not meaningful historically. I use the U.S. federal statutory rate only after profitability; tax attributes and foreign mix would change it.
$300M cash floor                            Judgment   I retain a large buffer because Joby is pre-commercial and depends on continued development spending. A funded runway plan or contracted cash inflows would change it.
Equity funding at $6.22/share               Judgment   The model raises only what is needed to preserve the cash floor, at the September 24, 2026 quoted price. A future offering price, debt financing, or strategic investment would change it.
No floor plan                                History    None: Joby reported no inventory in its FY2023-25 balance sheets and is not a vehicle dealer; dealer floor-plan debt is inapplicable.
13% cost of equity                           Judgment   A pre-profit aerospace company has unusually high execution, regulatory, and dilution risk. A defensible beta/capital-structure analysis would change it.
3% terminal growth                           Judgment   This is a mature-economy long-run constraint, not management guidance. A sustainable mature aviation growth outlook would change it.
$6.22 market quote (Sept. 24, 2026)         History    The observed market comparison quote is not used to produce the model value; it is shown only for the required same-share-count question.
""".strip()


HISTORY = (
    # Metric, FY2023, FY2024, FY2025, filing source for each year.
    ("Revenue", 1.032, 0.136, 53.425, FILING_2023, FILING_2024, FILING_2025),
    ("Gross profit (revenue - cost of revenue)", 0.832, 0.069, 24.097, FILING_2023, FILING_2024, FILING_2025),
    ("SG&A", 105.877, 119.667, 162.587, FILING_2023, FILING_2024, FILING_2025),
    ("Net income (loss)", -513.050, -608.034, -929.842, FILING_2023, FILING_2024, FILING_2025),
    ("Inventory", "None reported", "None reported", "None reported", FILING_2023, FILING_2024, FILING_2025),
    ("PP&E, net", 103.430, 120.954, 146.571, FILING_2023, FILING_2024, FILING_2025),
    ("Stockholders' equity", 1_034.362, 912.363, 1_409.713, FILING_2023, FILING_2024, FILING_2025),
)


RATIOS = (
    ("Gross margin", "80.62%", "50.74%", "45.10%", "Calculated from revenue and cost of revenue in each cited 10-K"),
    ("SG&A / gross profit", "12,725.60%", "173,430.43%", "674.72%", "Calculated; early revenue makes this ratio non-comparable"),
    ("Inventory days", "N/A — no inventory", "N/A — no inventory", "N/A — no inventory", "No inventory balance reported in the cited balance sheets"),
    ("Depreciation / ending PP&E", "23.59%", "24.55%", "22.86%", "P&E note: $24.4M/$103.430M; $29.7M/$120.954M; $33.5M/$146.571M"),
    ("Capex: filing cash-flow field", "$30.597M", "$40.617M", "$53.918M", "Purchases of property and equipment in each 10-K cash-flow statement"),
    ("Capex: data-provider field", "Unresolved", "Unresolved", "Unresolved", "No data-provider figure is treated as fact; the filing figure above is used"),
    ("Effective tax rate", "-0.03% (N/M)", "-0.02% (N/M)", "-0.14% (N/M)", "Reported income-tax expense / loss before tax; negative denominators make the result not meaningful"),
    ("Reported revenue growth", "N/M (base-year revenue zero)", "-86.82%", "39,183.09%", "Calculated from reported revenue; small bases make it non-comparable"),
    ("Organic / same-store growth disclosed", "Unresolved — not disclosed", "Unresolved — not disclosed", "Unresolved — not disclosed", "Joby is not a store-based business; no same-store metric found in these 10-Ks"),
)


def assert_balanced(year, gap, cash, minimum_cash):
    """Refuse an invalid forecast; do not silence this check."""
    if abs(gap) > 0.05:
        raise ValueError(f"{year}: balance-sheet gap is {gap:,.4f} million")
    if cash < minimum_cash - 0.05:
        raise ValueError(
            f"{year}: cash is {cash:,.4f} million, below the {minimum_cash:,.1f} million floor"
        )


def forecast(inputs=None):
    """Run one full linked forecast from an independent input dictionary."""
    inputs = build_inputs() if inputs is None else inputs
    opening = OPENING.copy()
    result = []
    depreciation_rate = 33.5 / 146.571
    for year, revenue, margin, r_and_d, sga, capex in zip(
        inputs["years"], inputs["revenue"], inputs["gross_margin"],
        inputs["r_and_d"], inputs["sga"], inputs["capex"],
    ):
        gross_profit = revenue * margin
        depreciation = opening["ppe"] * depreciation_rate
        operating_income = gross_profit - r_and_d - sga - depreciation
        tax = max(0.0, operating_income) * inputs["tax_rate"]
        net_income = operating_income - tax
        ppe = opening["ppe"] + capex - depreciation
        cash_before_funding = opening["cash"] + net_income + depreciation - capex
        external_equity_raise = max(0.0, inputs["minimum_cash"] - cash_before_funding)
        cash = cash_before_funding + external_equity_raise
        shares_issued = external_equity_raise / inputs["equity_issue_price"]
        equity = opening["equity"] + net_income + external_equity_raise
        shares = opening["shares"] + shares_issued
        assets = cash + ppe + opening["other_assets"]
        liabilities_and_equity = opening["liabilities"] + equity
        gap = assets - liabilities_and_equity
        assert_balanced(year, gap, cash, inputs["minimum_cash"])
        fcfe_before_funding = net_income + depreciation - capex
        result.append({
            "year": year, "revenue": revenue, "gross_profit": gross_profit, "net_income": net_income,
            "ppe": ppe, "capex": capex, "depreciation": depreciation, "equity_raise": external_equity_raise,
            "cash": cash, "shares": shares, "gap": gap, "fcfe": fcfe_before_funding,
        })
        opening.update({"cash": cash, "ppe": ppe, "equity": equity, "shares": shares})
    return result


def value_per_share(rows, inputs=None):
    """Illustrative equity value: PV of pre-funding FCFE plus terminal value."""
    inputs = build_inputs() if inputs is None else inputs
    pv = 0.0
    for index, row in enumerate(rows, start=1):
        pv += row["fcfe"] / pow(1 + inputs["cost_of_equity"], index)
    terminal_fcfe = rows[-1]["fcfe"]
    terminal_value = terminal_fcfe * (1 + inputs["terminal_growth"]) / (
        inputs["cost_of_equity"] - inputs["terminal_growth"]
    )
    pv += terminal_value / pow(1 + COST_OF_EQUITY, len(rows))
    return pv / rows[-1]["shares"], pv


def print_history():
    print("\nTHREE-YEAR HISTORY — USD MILLIONS; EVERY ITEM TRACED TO A FILING")
    print(f"{'Metric':42} {'FY2023':>16} {'FY2024':>16} {'FY2025':>16}")
    for metric, y23, y24, y25, s23, s24, s25 in HISTORY:
        print(f"{metric:42} {str(y23):>16} {str(y24):>16} {str(y25):>16}")
        print(f"  Sources: FY23 {s23}; FY24 {s24}; FY25 {s25}")
    print("\nHand-confirmed: FY2025 revenue $53.425M and FY2025 PP&E $146.571M were read directly from the FY2025 10-K.")


def print_ratios():
    print("\nRATIO TABLE")
    print(f"{'Ratio':42} {'FY2023':>22} {'FY2024':>22} {'FY2025':>22}")
    for metric, y23, y24, y25, note in RATIOS:
        print(f"{metric:42} {y23:>22} {y24:>22} {y25:>22}\n  Source/basis: {note}")


SENSITIVITY_DRIVERS = {
    "revenue": {
        "label": "Commercialization revenue path",
        "unit": "USD millions",
        "lower": "-30% multiplier in every forecast year",
        "higher": "+30% multiplier in every forecast year",
    },
    "gross_margin": {
        "label": "Gross-margin path",
        "unit": "percent of revenue",
        "lower": "-10 percentage points in every forecast year",
        "higher": "+10 percentage points in every forecast year",
    },
}


def scenario_inputs(driver, case):
    """Return a fresh base copy with exactly one stated driver changed."""
    inputs = build_inputs()
    if case == "base":
        return inputs
    if driver == "revenue":
        multiplier = {"lower": 0.70, "higher": 1.30}[case]
        inputs["revenue"] = tuple(value * multiplier for value in inputs["revenue"])
    elif driver == "gross_margin":
        point_shift = {"lower": -0.10, "higher": 0.10}[case]
        inputs["gross_margin"] = tuple(
            value + point_shift for value in inputs["gross_margin"]
        )
    else:
        raise ValueError(f"Unknown sensitivity driver: {driver}")
    return inputs


def final_year_outputs(rows, inputs):
    """Return consistent signed operating-profit and pre-funding FCFE outputs."""
    row = rows[-1]
    operating_profit = (
        row["gross_profit"] - inputs["r_and_d"][-1]
        - inputs["sga"][-1] - row["depreciation"]
    )
    return {
        "operating_profit": operating_profit,
        "fcfe": row["fcfe"],
        "row": row,
    }


def changed_keys(inputs):
    """Audit that a scenario differs from the base set only as declared."""
    base = build_inputs()
    return [key for key in base if inputs[key] != base[key]]


def format_path(values, decimals=1, suffix=""):
    return " / ".join(f"{value:.{decimals}f}{suffix}" for value in values)


def print_accounting_checks(rows, inputs):
    print("  Accounting checks (gap; cash-floor status):")
    for row in rows:
        gap_ok = abs(row["gap"]) <= 0.05
        cash_ok = row["cash"] >= inputs["minimum_cash"] - 0.05
        print(
            f"    {row['year']}: {row['gap']:+.1f}M; "
            f"cash ${row['cash']:.1f}M >= ${inputs['minimum_cash']:.1f}M: "
            f"{gap_ok and cash_ok}"
        )


def print_trace(rows, inputs):
    """Keep final-year statement detail visible for tracing any selected result."""
    row = rows[-1]
    operating_profit = final_year_outputs(rows, inputs)["operating_profit"]
    print("  2030 trace (USD millions except shares):")
    print(
        f"    Revenue {row['revenue']:.1f}; gross profit {row['gross_profit']:.1f}; "
        f"R&D {inputs['r_and_d'][-1]:.1f}; SG&A {inputs['sga'][-1]:.1f}; "
        f"depreciation {row['depreciation']:.1f}; operating profit {operating_profit:.1f}."
    )
    print(
        f"    Net income {row['net_income']:.1f}; capex {row['capex']:.1f}; "
        f"FCFE before funding {row['fcfe']:.1f}; equity raise {row['equity_raise']:.1f}; "
        f"cash {row['cash']:.1f}; shares {row['shares']:.1f}; balance-sheet gap {row['gap']:.1f}."
    )


def run_sensitivity_case(driver, case):
    """Run a complete scenario and retain invalid runs rather than ranking them."""
    inputs = scenario_inputs(driver, case)
    allowed_changes = [] if case == "base" else [driver]
    actual_changes = changed_keys(inputs)
    audit_ok = actual_changes == allowed_changes
    try:
        rows = forecast(inputs)
        return {
            "case": case, "inputs": inputs, "rows": rows, "valid": audit_ok,
            "audit_ok": audit_ok, "actual_changes": actual_changes,
            "outputs": final_year_outputs(rows, inputs), "error": None,
        }
    except ValueError as error:
        return {
            "case": case, "inputs": inputs, "rows": None, "valid": False,
            "audit_ok": audit_ok, "actual_changes": actual_changes,
            "outputs": None, "error": str(error),
        }


def print_sensitivity_analysis(base_rows_first):
    """Print lower/base/higher cases, then restore and verify the base model."""
    print("\nONE-AT-A-TIME SENSITIVITY ANALYSIS")
    print("Every scenario begins from a fresh base input copy.  Linked accounting recalculates.")
    print("Value per share: unavailable for this comparison. The existing terminal-value output is illustrative, not a defensible valuation conclusion for an externally funded transition path.")
    print("Free cash flow label: FCFE before funding = net income + depreciation - capex (USD millions).")

    for driver, specification in SENSITIVITY_DRIVERS.items():
        print(f"\nDRIVER: {specification['label']} ({specification['unit']})")
        print(f"  Lower: {specification['lower']}; higher: {specification['higher']}.")
        cases = [run_sensitivity_case(driver, case) for case in ("lower", "base", "higher")]
        base_case = next(item for item in cases if item["case"] == "base")
        if not base_case["valid"]:
            print(f"  Base run invalid: {base_case['error']}")
            continue

        base_outputs = base_case["outputs"]
        valid_outputs = []
        for item in cases:
            inputs = item["inputs"]
            if driver == "revenue":
                actual_input = format_path(inputs["revenue"], suffix="M")
            else:
                actual_input = format_path(
                    tuple(value * 100 for value in inputs["gross_margin"]), suffix="%"
                )
            print(f"\n  {item['case'].upper()} input values: {actual_input}")
            print(
                f"  Independent-input audit: changed {item['actual_changes'] or 'none'}; "
                f"expected {([driver] if item['case'] != 'base' else []) or 'none'}; "
                f"pass: {item['audit_ok']}"
            )
            if not item["valid"]:
                print(f"  INVALID RUN — not ranked: {item['error'] or 'input-change audit failed'}")
                continue
            outputs = item["outputs"]
            operating_change = outputs["operating_profit"] - base_outputs["operating_profit"]
            fcfe_change = outputs["fcfe"] - base_outputs["fcfe"]
            print(
                f"  2030 operating profit: ${outputs['operating_profit']:,.1f}M "
                f"(change from base: {operating_change:+,.1f}M)"
            )
            print(
                f"  2030 FCFE before funding: ${outputs['fcfe']:,.1f}M "
                f"(change from base: {fcfe_change:+,.1f}M)"
            )
            print("  Value per share: unavailable (see valuation limitation above).")
            print_accounting_checks(item["rows"], inputs)
            print_trace(item["rows"], inputs)
            valid_outputs.append(outputs)

        if valid_outputs:
            operating_span = max(item["operating_profit"] for item in valid_outputs) - min(
                item["operating_profit"] for item in valid_outputs
            )
            fcfe_span = max(item["fcfe"] for item in valid_outputs) - min(
                item["fcfe"] for item in valid_outputs
            )
            print(f"\n  Output span across valid lower/base/higher cases:")
            print(f"    2030 operating profit span: ${operating_span:,.1f}M")
            print(f"    2030 FCFE before funding span: ${fcfe_span:,.1f}M")

    restored_inputs = build_inputs()
    restored_rows = forecast(restored_inputs)
    restored_outputs = final_year_outputs(restored_rows, restored_inputs)
    first_outputs = final_year_outputs(base_rows_first, build_inputs())
    inputs_match = restored_inputs == build_inputs()
    outputs_match = (
        restored_outputs["operating_profit"] == first_outputs["operating_profit"]
        and restored_outputs["fcfe"] == first_outputs["fcfe"]
        and restored_rows == base_rows_first
    )
    print("\nRESTORED-BASE CHECK")
    print(f"  Fresh base inputs match the original base set: {inputs_match}")
    print(f"  Restored base outputs and linked statements match the first base run: {outputs_match}")
    print_trace(restored_rows, restored_inputs)


def main():
    base_inputs_first = build_inputs()
    rows = forecast(base_inputs_first)
    print_history()
    print_ratios()
    print(f"\n{ASSUMPTION_TABLE}")
    print("\nFIVE-YEAR PRO FORMA — USD MILLIONS EXCEPT SHARES")
    print(f"{'Year':>6} {'Revenue':>10} {'Net income':>12} {'Capex':>10} {'Equity raise':>14} {'Cash':>12} {'Shares M':>12} {'Check':>10}")
    for row in rows:
        print(f"{row['year']:>6} {row['revenue']:>10.1f} {row['net_income']:>12.1f} {row['capex']:>10.1f} {row['equity_raise']:>14.1f} {row['cash']:>12.1f} {row['shares']:>12.1f} {row['gap']:>10.1f}")
    per_share, equity_value = value_per_share(rows, base_inputs_first)
    print(f"\nCHECK BLOCK: every year has a $0.0M gap and cash at or above the ${MINIMUM_CASH:.0f}M floor.")
    print("Revolver: none. Joby has no dealer floor-plan line; funding need is modeled as external equity issuance, which causes dilution.")
    print(f"Illustrative value: ${equity_value:,.1f}M equity value / {rows[-1]['shares']:,.1f}M projected shares = ${per_share:,.2f} per share.")
    print(f"On the same projected share count, the model says ${per_share:,.2f} per share while JOBY was quoted at ${MARKET_PRICE:.2f} on {MARKET_PRICE_DATE} — which commercialization, dilution, or discount-rate assumption explains the difference?")
    print("\nPARTNER REVIEW — DRAFTED PARTNER EXCHANGE")
    print("Partner attack to record: Why assume revenue reaches $3.5B by 2030 when the company has not guided that number, and what evidence would make you reduce it?")
    print("My answer: I used it as an explicit scenario endpoint rather than guidance because the current $53.4M revenue base cannot be extrapolated mechanically. I would reduce it if certification, fleet production, route approvals, or service demand lag the staged launch required by the forecast.")
    print("My attack for my partner: Your equity-issue price should not simply equal today's quote; why is that price achievable after several cash-burn years, and what evidence would make you use a discount or debt instead?")
    print("Partner answer: NuScale’s model uses an assumed future equity-issue price below its recent trading level because repeated cash-burn years and project-financing uncertainty could require a discount. I would revise that assumption if NuScale secures project financing, contracted customer payments, or non-dilutive funding that reduces the need for equity issuance.")
    print_sensitivity_analysis(rows)


if __name__ == "__main__":
    main()
