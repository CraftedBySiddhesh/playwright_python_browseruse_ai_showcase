"""
@meta:
  TC: TC-017
  REQ: DB-AI-017
  TAGS: [ai, e2e, regression]
  SITE: Demoblaze
  MODE: ai_stub
"""

import pytest


@pytest.mark.regression
@pytest.mark.e2e
@pytest.mark.ai_stub
def test_agent_natural_language_filters_tc_017(agent_runner) -> None:
  instructions = (
    "Go to Laptops, choose a low-price option if available, add to cart, verify cart has one laptop."
  )
  result = agent_runner(instructions, case_id="TC-017", goals=["Demoblaze laptop intent"])
  assert result.success
  assert result.total_steps >= 3
