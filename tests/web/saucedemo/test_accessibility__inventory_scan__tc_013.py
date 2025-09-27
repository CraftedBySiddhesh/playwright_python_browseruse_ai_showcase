"""
@meta:
  TC: TC-013
  REQ: SD-A11Y-013
  TAGS: [a11y, regression]
  SITE: SauceDemo
  MODE: classic
"""

import pytest
from playwright_axe import Axe


@pytest.mark.regression
@pytest.mark.a11y
def test_accessibility_inventory_scan_tc_013(sauce_flow, test_artifact_dir) -> None:
  axe = Axe(sauce_flow.page)
  results = axe.run()
  violations = [v for v in results["violations"] if "critical" in v.get("impact", "")]  # type: ignore[index]
  (test_artifact_dir / "a11y.json").write_text(axe.report(results), encoding="utf-8")
  assert not violations, f"Critical accessibility violations detected: {violations}"
  assert "violations" in results, "Axe results should contain violations key"
