"""
@meta:
  TC: TC-002
  TITLE: SauceDemo — Negative Login Validation
  OBJECTIVE: Wrong password shows error and blocks login.
  INSTRUCTION: "Try logging into SauceDemo using username standard_user and the wrong password bad_pass."
  EXPECTED: Error banner; still on login page.
  TAGS: [ai, e2e, sauce, negative, regression]
  MODE: ai_stub
"""

import pytest


@pytest.mark.regression
@pytest.mark.e2e
@pytest.mark.negative
@pytest.mark.ai_stub
def test_login_negative_password_tc_002(agent_runner) -> None:
    instructions = (
        "Try logging into SauceDemo using username standard_user and the wrong password bad_pass."
    )
    result = agent_runner(
        instructions,
        case_id="TC-002",
        goals=["TC-002", "SauceDemo — Negative Login Validation"],
    )
    assert result.success
    assert result.events[0].observation == instructions
