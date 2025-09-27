"""
@meta:
  TC: TC-015
  TITLE: Agentic — Guided Checkout on SauceDemo
  OBJECTIVE: Agent completes checkout via NL; clarifies missing fields.
  INSTRUCTION: "Go to SauceDemo, log in, add the two cheapest items, proceed to checkout, and finish the order; if any field is missing, ask me and then continue."
  EXPECTED: Order completes; transcript shows clarifying Q&A if needed.
  TAGS: [ai, e2e, sauce, smoke, regression]
  MODE: ai_stub
"""

import pytest


@pytest.mark.regression
@pytest.mark.e2e
@pytest.mark.smoke
@pytest.mark.ai_stub
def test_agent_guided_checkout_tc_015(agent_runner) -> None:
  instructions = (
    "Go to SauceDemo, log in, add the two cheapest items, proceed to checkout, and finish the order; "
    "if any field is missing, ask me and then continue."
  )
  result = agent_runner(
    instructions,
    case_id="TC-015",
    goals=["TC-015", "Agentic — Guided Checkout on SauceDemo"],
  )
  assert result.success
  assert result.events[0].observation == instructions
  assert result.total_steps >= 3
