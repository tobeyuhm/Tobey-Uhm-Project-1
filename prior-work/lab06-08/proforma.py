"""ABG five-year pro forma and FCFE valuation (USD millions except per-share data)."""

YEARS = (2026, 2027, 2028, 2029, 2030)
GROWTH = 0.018
GROSS_MARGIN = 0.1705
SGA_TO_GROSS_PROFIT = (0.665, 0.655, 0.645, 0.645, 0.645)
DEPRECIATION_TO_OPENING_PPE = 82.4 / 3070.4
IMPAIRMENT = 120.0
CAPEX = 250.0
TAX_RATE = 0.255
INVENTORY_DAYS = 2135.8 / (17999.0 - 3071.7) * 365
FLOOR_PLAN_TO_INVENTORY = 2027.0 / 2135.8
OTHER_WORKING_CAPITAL_TO_CHANGE_REVENUE = 0.008
MINIMUM_CASH = 25.0
REVOLVER_LIMIT = 850.0
REVOLVER_RATE = 0.06
DEBT_REPAYMENT = 150.0
SHARE_BUYBACK = 150.0
FLOOR_PLAN_RATE = 0.0467
TERM_DEBT_RATE = 0.0544
COST_OF_EQUITY = 0.10
TERMINAL_GROWTH = 0.025
SHARES_OUTSTANDING = 17.951349

# FY2025 opening balance sheet (USD millions).
OPENING = {
    "revenue": 17999.0, "inventory": 2135.8, "ppe": 3070.4,
    "other_assets": 6371.6, "cash": 40.4, "floor_plan": 2027.0,
    "debt": 3572.0, "revolver": 0.0, "other_liabilities": 2127.5,
    "equity": 3891.7,
}


def assert_balanced(year, gap, cash):
    """Raise an error with the year and gap if the statements fail a required check."""
    if abs(gap) > 0.05:
        raise ValueError(f"{year}: balance-sheet gap is {gap:,.4f} million")
    if cash < MINIMUM_CASH - 0.05:
        raise ValueError(
            f"{year}: cash is {cash:,.4f} million, below the {MINIMUM_CASH:,.1f} million minimum"
        )


def forecast():
    opening = OPENING.copy()
    results = []

    for year, sga_ratio in zip(YEARS, SGA_TO_GROSS_PROFIT):
        revenue = opening["revenue"] * (1 + GROWTH)
        gross_profit = revenue * GROSS_MARGIN
        sga = gross_profit * sga_ratio
        depreciation = opening["ppe"] * DEPRECIATION_TO_OPENING_PPE
        operating_income = gross_profit - sga - depreciation - IMPAIRMENT
        interest = (
            opening["floor_plan"] * FLOOR_PLAN_RATE
            + opening["debt"] * TERM_DEBT_RATE
            + opening["revolver"] * REVOLVER_RATE
        )
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * TAX_RATE
        net_income = pretax_income - tax

        inventory = (revenue - gross_profit) * INVENTORY_DAYS / 365
        floor_plan = inventory * FLOOR_PLAN_TO_INVENTORY
        ppe = opening["ppe"] + CAPEX - depreciation
        change_revenue = revenue - opening["revenue"]
        change_other_working_capital = (
            OTHER_WORKING_CAPITAL_TO_CHANGE_REVENUE * change_revenue
        )
        other_assets = opening["other_assets"] + change_other_working_capital - IMPAIRMENT
        debt = opening["debt"] - DEBT_REPAYMENT
        other_liabilities = opening["other_liabilities"]
        equity = opening["equity"] + net_income - SHARE_BUYBACK

        change_inventory = inventory - opening["inventory"]
        change_floor_plan = floor_plan - opening["floor_plan"]
        fcfe = (
            net_income + depreciation + IMPAIRMENT - CAPEX - change_inventory
            - change_other_working_capital + change_floor_plan - DEBT_REPAYMENT
        )

        cash_before_revolver = opening["cash"] + fcfe - SHARE_BUYBACK
        if cash_before_revolver < MINIMUM_CASH:
            revolver_change = MINIMUM_CASH - cash_before_revolver
        else:
            revolver_change = -min(opening["revolver"], cash_before_revolver - MINIMUM_CASH)
        revolver = opening["revolver"] + revolver_change
        if revolver > REVOLVER_LIMIT + 0.05:
            raise ValueError(
                f"{year}: revolver balance {revolver:,.1f} exceeds its {REVOLVER_LIMIT:,.1f} million limit"
            )
        cash = cash_before_revolver + revolver_change

        total_assets = cash + inventory + ppe + other_assets
        total_liabilities = floor_plan + debt + revolver + other_liabilities
        gap = total_assets - total_liabilities - equity
        assert_balanced(year, gap, cash)

        result = {
            "year": year, "revenue": revenue, "gross_profit": gross_profit,
            "sga": sga, "depreciation": depreciation, "impairment": IMPAIRMENT,
            "operating_income": operating_income, "interest": interest,
            "pretax_income": pretax_income, "tax": tax, "net_income": net_income,
            "inventory": inventory, "ppe": ppe, "other_assets": other_assets,
            "cash": cash, "floor_plan": floor_plan, "debt": debt,
            "revolver": revolver, "other_liabilities": other_liabilities,
            "equity": equity, "fcfe": fcfe, "change_inventory": change_inventory,
            "change_other_working_capital": change_other_working_capital,
            "change_floor_plan": change_floor_plan, "revolver_change": revolver_change,
            "total_assets": total_assets, "total_liabilities": total_liabilities,
            "gap": gap,
        }
        results.append(result)
        opening = {**opening, **result}
    return results


def print_table(title, lines, results):
    print(f"\n{title} (USD millions)")
    print(f"{'':32}" + "".join(f"{row['year']:>13}" for row in results))
    for label, key in lines:
        print(f"{label:32}" + "".join(f"{row[key]:>13,.1f}" for row in results))


def value_equity(results):
    if TERMINAL_GROWTH >= COST_OF_EQUITY:
        raise ValueError("terminal growth must be lower than cost of equity")
    pv_explicit_fcfe = sum(
        row["fcfe"] / (1 + COST_OF_EQUITY) ** period
        for period, row in enumerate(results, start=1)
    )
    terminal_fcfe = results[-1]["fcfe"] + DEBT_REPAYMENT
    terminal_value = terminal_fcfe * (1 + TERMINAL_GROWTH) / (COST_OF_EQUITY - TERMINAL_GROWTH)
    pv_terminal_value = terminal_value / (1 + COST_OF_EQUITY) ** 5
    return pv_explicit_fcfe + pv_terminal_value, pv_terminal_value


def main():
    results = forecast()
    print_table("Income Statement", (
        ("Revenue", "revenue"), ("Gross profit", "gross_profit"),
        ("SG&A", "sga"), ("Depreciation", "depreciation"),
        ("Impairment", "impairment"), ("Operating income", "operating_income"),
        ("Interest", "interest"), ("Pretax income", "pretax_income"),
        ("Tax", "tax"), ("Net income", "net_income"),
    ), results)
    print_table("Balance Sheet", (
        ("Cash", "cash"), ("Inventory", "inventory"), ("PP&E", "ppe"),
        ("Other assets", "other_assets"), ("Total assets", "total_assets"),
        ("Floor plan", "floor_plan"), ("Debt", "debt"), ("Revolver", "revolver"),
        ("Other liabilities", "other_liabilities"), ("Equity", "equity"),
        ("Total liabilities", "total_liabilities"),
    ), results)
    cash_flow_rows = [
        {**row, "capex": CAPEX, "debt_repayment": DEBT_REPAYMENT,
         "share_buyback": SHARE_BUYBACK} for row in results
    ]
    print_table("Cash Flow Statement", (
        ("Net income", "net_income"), ("Depreciation", "depreciation"),
        ("Impairment", "impairment"), ("Capital spending", "capex"),
        ("Change in inventory", "change_inventory"),
        ("Change in other working capital", "change_other_working_capital"),
        ("Change in floor plan", "change_floor_plan"),
        ("Debt repayment", "debt_repayment"), ("FCFE", "fcfe"),
        ("Share buyback", "share_buyback"), ("Revolver change", "revolver_change"),
        ("Ending cash", "cash"),
    ), cash_flow_rows)

    print("\nChecks")
    for row in results:
        print(f"{row['year']}: assets - liabilities - equity = {row['gap']:.1f}; "
              f"cash >= minimum: {row['cash'] >= MINIMUM_CASH}")

    equity_value, pv_terminal_value = value_equity(results)
    print("\nFCFE Valuation")
    print(f"Equity value: ${equity_value:,.2f} million")
    print(f"Share of value after 2030: {pv_terminal_value / equity_value:.2%}")
    print(f"Value per share: ${equity_value / SHARES_OUTSTANDING:,.2f}")


if __name__ == "__main__":
    main()
