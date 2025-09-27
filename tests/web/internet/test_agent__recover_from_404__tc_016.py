"""
@meta:
  TC: TC-016
  REQ: TI-AI-016
  TAGS: [ai, resilience, regression]
  SITE: Internet
  MODE: ai_stub
"""

import pytest


@pytest.mark.regression
@pytest.mark.resilience
@pytest.mark.ai_stub
def test_agent_recover_from_404_tc_016(agent_runner) -> None:
  instructions = (
    "Visit an invalid link to trigger 404, then recover to the home list and open 'Frames'; confirm Frames page loads."
  )
  result = agent_runner(instructions, case_id="TC-016", goals=["Recover from 404"])
  assert result.success
  assert any("Frames" in event.observation for event in result.events), "Transcript should mention Frames"
