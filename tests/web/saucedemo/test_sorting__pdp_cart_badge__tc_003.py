"""
@meta:
  TC: TC-003
  TITLE: SauceDemo — Sorting + PDP + Cart
  OBJECTIVE: Sorting order reflected; add from PDP updates badge.
  INSTRUCTION: "Sort by low-to-high, open the cheapest product’s details, add to cart, verify cart badge is 1."
  EXPECTED: Badge 1; PDP shows correct product.
  TAGS: [ai, e2e, sauce, regression]
  MODE: ai_stub
"""

import pytest


@pytest.mark.regression
@pytest.mark.e2e
@pytest.mark.ai_stub
def test_sorting_pdp_cart_badge_tc_003(agent_runner) -> None:
    instructions = "Sort by low-to-high, open the cheapest product’s details, add to cart, verify cart badge is 1."
    result = agent_runner(
        instructions,
        case_id="TC-003",
        goals=["TC-003", "SauceDemo — Sorting + PDP + Cart"],
    )
    assert result.success
    assert result.events[0].observation == instructions
