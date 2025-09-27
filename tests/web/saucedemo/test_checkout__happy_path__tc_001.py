"""
@meta:
  TC: TC-001
  REQ: SD-ORD-001
  TAGS: [e2e, smoke, regression]
  SITE: SauceDemo
  MODE: classic
"""

import pytest


@pytest.mark.regression
@pytest.mark.smoke
@pytest.mark.e2e
def test_checkout_happy_path_tc_001(sauce_flow) -> None:
  confirmation = sauce_flow.checkout_cheapest_two_items()
  assert "dispatch" in confirmation.lower(), "Confirmation should mention dispatch"
  assert "THANK YOU" in sauce_flow.page.get_by_role("heading", name="THANK YOU FOR YOUR ORDER").inner_text()
