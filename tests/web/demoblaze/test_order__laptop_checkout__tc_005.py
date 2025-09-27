"""
@meta:
  TC: TC-005
  TITLE: Demoblaze — Place Order Flow
  OBJECTIVE: Laptops → add to cart → place order succeeds.
  INSTRUCTION: "Go to Laptops, add any laptop to the cart, place the order with any sample details, and confirm a purchase confirmation with an ID appears."
  EXPECTED: Modal with confirmation + ID.
  TAGS: [ai, e2e, demoblaze, regression]
  MODE: ai_stub
"""

import pytest


@pytest.mark.regression
@pytest.mark.e2e
@pytest.mark.ai_stub
def test_order_laptop_checkout_tc_005(agent_runner) -> None:
    instructions = "Go to Laptops, add any laptop to the cart, place the order with any sample details, and confirm a purchase confirmation with an ID appears."
    result = agent_runner(
        instructions,
        case_id="TC-005",
        goals=["TC-005", "Demoblaze — Place Order Flow"],
    )
    assert result.success
    assert result.events[0].observation == instructions
