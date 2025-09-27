"""
@meta:
  TC: TC-001
  TITLE: SauceDemo — E2E Smoke Checkout
  OBJECTIVE: Happy path checkout validates order completion.
  PRECONDITIONS: User: standard_user/secret_sauce.
  INSTRUCTION: "Log into SauceDemo, sort items by Price (low to high), add the two cheapest products to the cart, open the cart, proceed to checkout, enter any valid details, and complete the order."
  EXPECTED: Thank-you/confirmation page appears with completion text.
  ARTIFACTS: trace, video, cart + confirmation screenshots, transcript.
  TAGS: [ai, e2e, sauce, smoke, regression]
  MODE: ai_stub
"""

import pytest


@pytest.mark.regression
@pytest.mark.smoke
@pytest.mark.e2e
@pytest.mark.ai_stub
def test_checkout_happy_path_tc_001(agent_runner) -> None:
    instructions = (
        "Log into SauceDemo, sort items by Price (low to high), add the two cheapest products to the cart, "
        "open the cart, proceed to checkout, enter any valid details, and complete the order."
    )
    result = agent_runner(
        instructions,
        case_id="TC-001",
        goals=["TC-001", "SauceDemo — E2E Smoke Checkout"],
    )
    assert result.success
    assert result.events[0].observation == instructions
