"""
@meta:
  TC: TC-017
  TITLE: Agentic — Natural-Language Filters on Demoblaze
  OBJECTIVE: Agent interprets category/price intent and adds to cart.
  INSTRUCTION: "Go to Laptops, choose a low-price option if available, add to cart, verify cart has one laptop."
  EXPECTED: Cart count 1; transcript shows NL → actions.
  TAGS: [ai, demoblaze, e2e, regression]
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
  result = agent_runner(
    instructions,
    case_id="TC-017",
    goals=["TC-017", "Agentic — Natural-Language Filters"],
  )
  assert result.success
  assert result.events[0].observation == instructions
  assert result.total_steps >= 3
