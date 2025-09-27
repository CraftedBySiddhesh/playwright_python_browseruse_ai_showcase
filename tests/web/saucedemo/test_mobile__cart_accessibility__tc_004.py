"""
@meta:
  TC: TC-004
  TITLE: SauceDemo — Mobile Responsiveness
  OBJECTIVE: Inventory/cart usable on 390×844 viewport.
  INSTRUCTION: "In a mobile viewport ~390×844, log in, add any item, open the cart, and verify the item name is visible without horizontal scrolling."
  EXPECTED: No overflow; cart item fully visible.
  TAGS: [ai, e2e, sauce, device, regression]
  MODE: ai_stub
"""

import pytest


@pytest.mark.regression
@pytest.mark.e2e
@pytest.mark.device
@pytest.mark.ai_stub
def test_mobile_cart_accessibility_tc_004(agent_runner) -> None:
    instructions = "In a mobile viewport ~390×844, log in, add any item, open the cart, and verify the item name is visible without horizontal scrolling."
    result = agent_runner(
        instructions,
        case_id="TC-004",
        goals=["TC-004", "SauceDemo — Mobile Responsiveness"],
    )
    assert result.success
    assert result.events[0].observation == instructions
