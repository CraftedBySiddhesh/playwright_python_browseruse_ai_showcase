"""
@meta:
  TC: TC-011
  TITLE: Parabank — Transfer Funds Validation
  OBJECTIVE: Negative amount should be rejected.
  INSTRUCTION: "Attempt a funds transfer with a negative amount."
  EXPECTED: Inline validation or error blocks submission.
  TAGS: [ai, e2e, parabank, negative, regression]
  MODE: ai_stub
"""

import pytest


@pytest.mark.regression
@pytest.mark.e2e
@pytest.mark.negative
@pytest.mark.ai_stub
def test_transfer_negative_amount_tc_011(agent_runner) -> None:
  instructions = "Attempt a funds transfer with a negative amount."
  result = agent_runner(
    instructions,
    case_id="TC-011",
    goals=["TC-011", "Parabank — Transfer Funds Validation"],
  )
  assert result.success
  assert result.events[0].observation == instructions
