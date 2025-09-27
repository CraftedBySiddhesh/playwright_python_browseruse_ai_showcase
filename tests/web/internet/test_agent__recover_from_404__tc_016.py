"""
@meta:
  TC: TC-016
  TITLE: Agentic — Recover from 404 on The-Internet
  OBJECTIVE: Agent recovers from error page and navigates correctly.
  INSTRUCTION: "Visit an invalid link to trigger 404, then recover to the home list and open ‘Frames’; confirm Frames page loads."
  EXPECTED: Frames page visible; transcript shows recovery steps.
  TAGS: [ai, internet, resilience, regression]
  MODE: ai_stub
"""

import pytest


@pytest.mark.regression
@pytest.mark.resilience
@pytest.mark.ai_stub
def test_agent_recover_from_404_tc_016(agent_runner) -> None:
  instructions = (
    "Visit an invalid link to trigger 404, then recover to the home list and open ‘Frames’; confirm Frames page loads."
  )
  result = agent_runner(
    instructions,
    case_id="TC-016",
    goals=["TC-016", "Agentic — Recover from 404"],
  )
  assert result.success
  assert result.events[0].observation == instructions
