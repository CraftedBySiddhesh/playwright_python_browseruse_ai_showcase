"""
@meta:
  TC: TC-006
  TITLE: Demoblaze — Remove From Cart
  OBJECTIVE: Removing item recalculates total.
  INSTRUCTION: "Add two phones to the cart, remove one, verify the total updates."
  EXPECTED: Total equals remaining item price.
  TAGS: [ai, e2e, demoblaze, regression]
  MODE: ai_stub
"""

import pytest


@pytest.mark.regression
@pytest.mark.e2e
@pytest.mark.ai_stub
def test_cart_remove_recalculates_tc_006(agent_runner) -> None:
  instructions = (
    "Add two phones to the cart, remove one, verify the total updates."
  )
  result = agent_runner(
    instructions,
    case_id="TC-006",
    goals=["TC-006", "Demoblaze — Remove From Cart"],
  )
  assert result.success
  assert result.events[0].observation == instructions
