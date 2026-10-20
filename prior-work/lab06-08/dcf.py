# Training inputs (USD millions unless noted)
STARTING_FCFF = 100.0
GROWTH_RATES = [0.08, 0.06, 0.05, 0.04, 0.03]
WACC = 0.10
TERMINAL_GROWTH = 0.03
NON_OPERATING_CASH = 50.0
DEBT = 300.0
DILUTED_SHARES = 50.0

WACC_VALUES = [0.09, 0.10, 0.11]
TERMINAL_GROWTH_VALUES = [0.02, 0.03, 0.04]
TARGET_SHARE_PRICE = 30.00
SHIFT_LOWER_BOUND = -0.05
SHIFT_UPPER_BOUND = 0.10


def valuation(wacc, terminal_growth, shift=0.0):
    rates = [rate + shift for rate in GROWTH_RATES]
    if terminal_growth >= wacc:
        raise ValueError("Terminal growth must be less than WACC.")
    if any(rate <= -1 for rate in rates):
        raise ValueError("A yearly growth rate cannot be -100% or below.")
    fcff, prior = [], STARTING_FCFF
    for rate in rates:
        prior *= 1 + rate
        fcff.append(prior)
    pv_explicit = sum(cf / (1 + wacc) ** year for year, cf in enumerate(fcff, 1))
    terminal_value = fcff[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
    pv_terminal = terminal_value / (1 + wacc) ** 5
    enterprise_value = pv_explicit + pv_terminal
    equity_value = enterprise_value + NON_OPERATING_CASH - DEBT
    return fcff, pv_explicit, terminal_value, pv_terminal, enterprise_value, equity_value, equity_value / DILUTED_SHARES, pv_terminal / enterprise_value


def reverse_dcf():
    if SHIFT_LOWER_BOUND >= SHIFT_UPPER_BOUND:
        return None, "invalid bounds: lower bound must be below upper bound"
    if any(rate + bound <= -1 for rate in GROWTH_RATES for bound in (SHIFT_LOWER_BOUND, SHIFT_UPPER_BOUND)):
        return None, "invalid bracket: a yearly growth rate would be -100% or below"
    lo, hi = SHIFT_LOWER_BOUND, SHIFT_UPPER_BOUND
    flo = valuation(WACC, TERMINAL_GROWTH, lo)[6] - TARGET_SHARE_PRICE
    fhi = valuation(WACC, TERMINAL_GROWTH, hi)[6] - TARGET_SHARE_PRICE
    if flo * fhi > 0:
        return None, "no solution in this bracket"
    for _ in range(100):
        mid = (lo + hi) / 2
        fmid = valuation(WACC, TERMINAL_GROWTH, mid)[6] - TARGET_SHARE_PRICE
        if abs(fmid) < 1e-10:
            return mid, None
        if flo * fmid <= 0:
            hi = mid
        else:
            lo, flo = mid, fmid
    return None, "no solution found to the required precision"


def main():
    if len(GROWTH_RATES) != 5:
        raise ValueError("Enter exactly five yearly growth rates.")
    if DILUTED_SHARES <= 0:
        raise ValueError("Diluted shares must be greater than zero.")
    fcff, pv_explicit, tv, pv_tv, ev, equity, per_share, tv_share = valuation(WACC, TERMINAL_GROWTH)
    for year, cash_flow in enumerate(fcff, 1):
        print(f"FCFF Year {year}: {cash_flow:.4f}")
    print(f"Present value of explicit FCFF: {pv_explicit:.4f}")
    print(f"Terminal value at Year 5: {tv:.4f}")
    print(f"Present value of terminal value: {pv_tv:.4f}")
    print(f"Enterprise value: {ev:.4f}")
    print(f"Equity value: {equity:.4f}")
    print(f"Value per diluted share: {per_share:.4f}")
    print(f"PV of terminal value as share of enterprise value: {tv_share:.4f}")
    print("\nSensitivity: value per diluted share ($)")
    print("WACC \\ terminal growth | " + " | ".join(f"{g:.0%}" for g in TERMINAL_GROWTH_VALUES))
    print("--- | --- | --- | ---")
    for wacc in WACC_VALUES:
        cells = [f"{wacc:.0%}"]
        for growth in TERMINAL_GROWTH_VALUES:
            cells.append("invalid" if growth >= wacc else f"{valuation(wacc, growth)[6]:.2f}")
        print(" | ".join(cells))
    shift, message = reverse_dcf()
    print("\nReverse DCF")
    print(f"Target share price: {TARGET_SHARE_PRICE:.2f}")
    print(f"Held fixed: starting FCFF={STARTING_FCFF:.4f}, WACC={WACC:.2%}, terminal growth={TERMINAL_GROWTH:.2%}, cash={NON_OPERATING_CASH:.4f}, debt={DEBT:.4f}, diluted shares={DILUTED_SHARES:.4f}, base growth rates={GROWTH_RATES}")
    print(f"Search bracket: {SHIFT_LOWER_BOUND:+.2%} to {SHIFT_UPPER_BOUND:+.2%} uniform shift to all five explicit growth rates")
    print(f"Uniform growth-rate shift: {message}" if message else f"Uniform growth-rate shift: {shift:+.4%} ({shift * 100:+.4f} points)")


if __name__ == "__main__":
    main()
