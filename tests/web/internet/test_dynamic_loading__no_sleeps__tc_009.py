"""
@meta:
  TC: TC-009
  TITLE: The-Internet — Dynamic Loading (No Sleeps)
  OBJECTIVE: Wait for async content with proper waits.
  INSTRUCTION: "Open Dynamic Loading Example 2, start loading, wait until complete, confirm ‘Hello World!’ appears—no fixed sleeps."
  EXPECTED: Content only after loader finishes.
  TAGS: [ai, e2e, internet, resilience, regression]
  MODE: ai_stub
"""

import pytest


@pytest.mark.regression
@pytest.mark.e2e
@pytest.mark.resilience
@pytest.mark.ai_stub
def test_dynamic_loading_no_sleeps_tc_009(agent_runner) -> None:
  instructions = (
    "Open Dynamic Loading Example 2, start loading, wait until complete, confirm ‘Hello World!’ appears—no fixed sleeps."
  )
  result = agent_runner(
    instructions,
    case_id="TC-009",
    goals=["TC-009", "The-Internet — Dynamic Loading"],
  )
  assert result.success
  assert result.events[0].observation == instructions
