"""
@meta:
  TC: TC-010
  TITLE: Parabank — Register + Login
  OBJECTIVE: New user can register and then log in.
  INSTRUCTION: "Register a new user with randomized details, log out, log back in, verify Accounts Overview is displayed."
  EXPECTED: Register success; login success; overview visible.
  TAGS: [ai, e2e, parabank, regression]
  MODE: ai_stub
"""

import pytest


@pytest.mark.regression
@pytest.mark.e2e
@pytest.mark.ai_stub
def test_register_login_tc_010(agent_runner) -> None:
  instructions = (
    "Register a new user with randomized details, log out, log back in, verify Accounts Overview is displayed."
  )
  result = agent_runner(
    instructions,
    case_id="TC-010",
    goals=["TC-010", "Parabank — Register + Login"],
  )
  assert result.success
  assert result.events[0].observation == instructions
