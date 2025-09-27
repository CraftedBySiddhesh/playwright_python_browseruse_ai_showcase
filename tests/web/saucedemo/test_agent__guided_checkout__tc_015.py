"""
@meta:
  TC: TC-015
  REQ: SD-AI-015
  TAGS: [ai, e2e, regression]
  SITE: SauceDemo
  MODE: ai_stub
"""

import pytest


@pytest.mark.regression
@pytest.mark.e2e
@pytest.mark.ai_stub
def test_agent_guided_checkout_tc_015(agent_runner, allow_domains) -> None:
  instructions = (
    "Go to SauceDemo, log in, add the two cheapest items, proceed to checkout, and finish the order; "
    "if any field is missing, ask me and then continue."
  )
  result = agent_runner(instructions, case_id="TC-015", goals=["SauceDemo guided checkout"])
  assert result.success, "Agent should complete guided checkout"
  assert result.total_steps >= 3, "Agent should record multiple steps"
