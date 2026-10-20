"""Week 3 training DCF (synthetic teaching case) re-run through the project's discounting function.

This proves `present_value` and the Gordon terminal-value convention on the published known
answer before the same functions are trusted on Joby. Training inputs are NOT Joby data.
"""
from __future__ import annotations

from joby.model import ModelInputError, present_value

TRAINING = {
    "starting_fcff": 100.0,
    "growth_rates": [0.08, 0.06, 0.05, 0.04, 0.03],
    "wacc": 0.10,
    "terminal_growth": 0.03,
    "cash": 50.0,
    "debt": 300.0,
    "diluted_shares": 50.0,
}

KNOWN_ANSWER = {
    "fcff": [108.0, 114.48, 120.2040, 125.0122, 128.7625],
    "pv_explicit": 448.4408,
    "terminal_value": 1894.6486,
    "pv_terminal": 1176.4277,
    "enterprise_value": 1624.8685,
    "equity_value": 1374.8685,
    "value_per_share": 27.4974,
    "tv_share": 0.7240,
}


def training_valuation(case: dict = TRAINING, wacc: float | None = None, shift: float = 0.0) -> dict:
    wacc = case["wacc"] if wacc is None else wacc
    g = case["terminal_growth"]
    if len(case["growth_rates"]) != 5:
        raise ModelInputError("Enter exactly five yearly growth rates")
    if g >= wacc:
        raise ModelInputError("Terminal growth must be below WACC")
    fcff, prior = [], case["starting_fcff"]
    for rate in case["growth_rates"]:
        prior *= 1 + rate + shift
        fcff.append(prior)
    pv_explicit = sum(present_value(cf, year, wacc) for year, cf in enumerate(fcff, 1))
    tv = fcff[-1] * (1 + g) / (wacc - g)
    pv_tv = present_value(tv, 5, wacc)
    ev = pv_explicit + pv_tv
    equity = ev + case["cash"] - case["debt"]
    return {
        "fcff": fcff, "pv_explicit": pv_explicit, "terminal_value": tv, "pv_terminal": pv_tv,
        "enterprise_value": ev, "equity_value": equity,
        "value_per_share": equity / case["diluted_shares"], "tv_share": pv_tv / ev,
    }


def training_reverse_shift(target: float = 30.0, lo: float = -0.05, hi: float = 0.10) -> float:
    f = lambda s: training_valuation(shift=s)["value_per_share"] - target
    flo = f(lo)
    if flo * f(hi) > 0:
        raise ModelInputError("No solution in bracket")
    for _ in range(200):
        mid = (lo + hi) / 2
        fm = f(mid)
        if abs(fm) < 1e-10:
            break
        if flo * fm <= 0:
            hi = mid
        else:
            lo, flo = mid, fm
    return mid
