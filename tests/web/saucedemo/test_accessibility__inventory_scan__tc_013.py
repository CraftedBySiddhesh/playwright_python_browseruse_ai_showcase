"""
@meta:
  TC: TC-013
  TITLE: SauceDemo — Accessibility Audit (WCAG-A)
  OBJECTIVE: Quick a11y scan on inventory page after login.
  INSTRUCTION: "Run an accessibility scan on the inventory page after login; record violations and fail on critical issues."
  EXPECTED: No critical WCAG-A violations.
  TAGS: [ai, a11y, sauce, regression]
  MODE: ai_stub
"""

import pytest


@pytest.mark.regression
@pytest.mark.a11y
@pytest.mark.ai_stub
def test_accessibility_inventory_scan_tc_013(agent_runner) -> None:
    instructions = "Run an accessibility scan on the inventory page after login; record violations and fail on critical issues."
    result = agent_runner(
        instructions,
        case_id="TC-013",
        goals=["TC-013", "SauceDemo — Accessibility Audit"],
    )
    assert result.success
    assert result.events[0].observation == instructions
