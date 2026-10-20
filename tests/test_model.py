"""Validation suite. Run from the repository root:  python -m unittest discover -s tests -v"""
from __future__ import annotations

import copy
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from joby.model import (  # noqa: E402
    ModelInputError, accelerated_execution, compute_wacc, delayed_certification, load_inputs,
    present_value, run_statements, value, with_changes,
)
from joby.training_dcf import KNOWN_ANSWER, training_reverse_shift, training_valuation  # noqa: E402


def load_legacy():
    spec = importlib.util.spec_from_file_location("legacy_proforma", ROOT / "legacy" / "joby_proforma_2026.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class KnownAnswer(unittest.TestCase):
    """Week 3 published training answers, run through the same present_value() used for Joby."""

    def test_training_dcf_twelve_lines(self):
        r = training_valuation()
        for got, want in zip(r["fcff"], KNOWN_ANSWER["fcff"]):
            self.assertAlmostEqual(got, want, places=3)
        for key in ("pv_explicit", "terminal_value", "pv_terminal", "enterprise_value", "equity_value", "value_per_share"):
            self.assertAlmostEqual(r[key], KNOWN_ANSWER[key], places=3, msg=key)
        self.assertAlmostEqual(r["tv_share"], KNOWN_ANSWER["tv_share"], places=4)

    def test_training_wacc_11_and_reverse_dcf(self):
        self.assertAlmostEqual(training_valuation(wacc=0.11)["value_per_share"], 23.41, places=2)
        self.assertAlmostEqual(training_reverse_shift() * 100, 1.7779, places=3)

    def test_terminal_value_discounted_five_not_six_years(self):
        r = training_valuation()
        self.assertAlmostEqual(r["pv_terminal"], present_value(r["terminal_value"], 5, 0.10), places=6)
        self.assertNotAlmostEqual(r["pv_terminal"], present_value(r["terminal_value"], 6, 0.10), places=1)

    def test_synthetic_bridge_from_edition_a(self):
        # Edition A synthetic check: EV 1,000 + cash 100 - debt 250 - NCI 20 - pension 10 = 820; / 100 = $8.20.
        self.assertAlmostEqual((1000 + 100 - 250 - 20 - 10) / 100, 8.20)


class RepairedDefects(unittest.TestCase):
    """The three defects found in the Lab 11 script are refused in both the new model and the repaired legacy file."""

    def setUp(self):
        self.inputs = load_inputs()
        self.legacy = load_legacy()

    def test_defect1_four_year_path_rejected(self):
        bad = copy.deepcopy(self.inputs)
        bad["operating_plan"]["capex"] = bad["operating_plan"]["capex"][:4]
        with self.assertRaises(ModelInputError):
            run_statements(bad)
        legacy_bad = self.legacy.build_inputs()
        legacy_bad["revenue"] = legacy_bad["revenue"][:4]
        with self.assertRaises(ValueError):
            self.legacy.forecast(legacy_bad)

    def test_defect2_single_discount_rate(self):
        legacy_inputs = self.legacy.build_inputs()
        legacy_inputs["cost_of_equity"] = 0.20
        rows = self.legacy.forecast(legacy_inputs)
        _, pv = self.legacy.value_per_share(rows, legacy_inputs)
        r, g = 0.20, legacy_inputs["terminal_growth"]
        expected = sum(row["fcfe"] / (1 + r) ** i for i, row in enumerate(rows, 1))
        expected += rows[-1]["fcfe"] * (1 + g) / (r - g) / (1 + r) ** len(rows)
        self.assertAlmostEqual(pv, expected, places=6)
        # New model: every PV uses the WACC passed in.
        v = value(self.inputs, wacc_override=0.15)
        for row in v["rows"]:
            self.assertAlmostEqual(row["pv_fcff"], row["fcff"] / 1.15 ** row["t"], places=6)

    def test_defect3_growth_at_or_above_discount_rate_rejected(self):
        bad = copy.deepcopy(self.inputs)
        bad["terminal"]["growth"] = 0.04
        with self.assertRaises(ModelInputError):
            value(bad, wacc_override=0.035)
        legacy_inputs = self.legacy.build_inputs()
        legacy_inputs["terminal_growth"] = 0.13
        with self.assertRaises(ValueError):
            self.legacy.value_per_share(self.legacy.forecast(legacy_inputs), legacy_inputs)

    def test_growth_above_gdp_rejected(self):
        bad = copy.deepcopy(self.inputs)
        bad["terminal"]["growth"] = 0.05
        with self.assertRaises(ModelInputError):
            value(bad)

    def test_legacy_lab11_results_unchanged_by_repair(self):
        rows = self.legacy.forecast()
        out = self.legacy.final_year_outputs(rows, self.legacy.build_inputs())
        self.assertAlmostEqual(out["operating_profit"], 375.1, delta=0.05)
        self.assertAlmostEqual(out["fcfe"], 121.2, delta=0.05)


class Accounting(unittest.TestCase):
    def setUp(self):
        self.inputs = load_inputs()

    def test_balance_sheet_balances_every_period_every_scenario(self):
        for inp in (self.inputs, delayed_certification(self.inputs), accelerated_execution(self.inputs)):
            for row in run_statements(inp):
                self.assertLess(abs(row["balance_gap"]), 0.01, row["label"])

    def test_h1_actuals_reconcile_to_10q_operating_loss(self):
        h1 = self.inputs["h1_2026_actual"]
        loss = h1["revenue"] - h1["cost_of_revenue"] - h1["research_and_development"] - h1["selling_general_admin"]
        self.assertAlmostEqual(loss, -494.463, places=3)

    def test_stub_plus_h1_equals_fy2026_plan(self):
        row = run_statements(self.inputs)[0]
        plan_revenue = self.inputs["operating_plan"]["services_revenue"][0]
        self.assertAlmostEqual(row["revenue"] + self.inputs["h1_2026_actual"]["revenue"], plan_revenue, places=6)

    def test_cash_never_below_floor(self):
        floor = self.inputs["other_drivers"]["minimum_liquidity"]
        for row in run_statements(self.inputs):
            self.assertGreaterEqual(row["cash"], floor - 1e-6)

    def test_fcff_identity(self):
        for r in run_statements(self.inputs):
            self.assertAlmostEqual(
                r["fcff"], r["ebit"] - r["unlevered_cash_tax"] + r["depreciation"] - r["capex"] - r["delta_nwc"], places=6)

    def test_inputs_not_mutated_by_scenarios(self):
        before = copy.deepcopy(self.inputs)
        delayed_certification(self.inputs)
        accelerated_execution(self.inputs)
        with_changes(self.inputs, fleet_multiplier=2.0)
        self.assertEqual(before, self.inputs)


class Bridge(unittest.TestCase):
    def setUp(self):
        self.inputs = load_inputs()
        self.v = value(self.inputs)

    def test_bridge_arithmetic(self):
        b = self.v["bridge"]
        rebuilt = (b["enterprise_value"] + b["plus_cash_and_short_term_investments"] + b["less_convertible_notes_principal"]
                   + b["less_mortgage_loan"] + b["less_warrants_fair_value"] + b["less_blade_ebitda_earnout"])
        self.assertAlmostEqual(rebuilt, b["equity_value"], places=6)
        self.assertAlmostEqual(b["value_per_share"], b["equity_value"] / b["diluted_shares"]["total"], places=9)

    def test_cash_is_added_not_subtracted(self):
        b = self.v["bridge"]
        self.assertGreater(b["plus_cash_and_short_term_investments"], 0)
        self.assertAlmostEqual(b["plus_cash_and_short_term_investments"], 2263.826, places=3)

    def test_convertible_treated_as_debt_below_conversion_price(self):
        self.assertLess(self.v["value_per_share"], 14.19)
        self.assertEqual(self.v["bridge"]["convertible_treatment"], "debt at principal")
        self.assertEqual(self.v["bridge"]["diluted_shares"]["convertible_if_converted"], 0.0)

    def test_diluted_share_count(self):
        self.assertAlmostEqual(self.v["bridge"]["diluted_shares"]["total"], 1051.259765, places=4)

    def test_wacc_components(self):
        w = compute_wacc(self.inputs)
        self.assertAlmostEqual(w["cost_of_equity"], 0.042 + 1.8 * 0.05, places=9)
        self.assertTrue(0.10 < w["wacc"] < 0.15)


class Directional(unittest.TestCase):
    """Economic direction checks: each must move value the way finance says it should."""

    def setUp(self):
        self.inputs = load_inputs()
        self.base = value(self.inputs)["value_per_share"]

    def test_higher_wacc_lowers_value(self):
        self.assertLess(value(self.inputs, wacc_override=self.base_wacc() + 0.01)["value_per_share"], self.base)

    def base_wacc(self):
        return compute_wacc(self.inputs)["wacc"]

    def test_delay_lowers_and_acceleration_raises_value(self):
        self.assertLess(value(delayed_certification(self.inputs))["value_per_share"], self.base)
        self.assertGreater(value(accelerated_execution(self.inputs))["value_per_share"], self.base)

    def test_more_fleet_raises_value(self):
        self.assertGreater(value(with_changes(self.inputs, fleet_multiplier=1.1))["value_per_share"], self.base)


if __name__ == "__main__":
    unittest.main()
