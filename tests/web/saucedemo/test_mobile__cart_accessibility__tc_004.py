"""
@meta:
  TC: TC-004
  REQ: SD-RESP-004
  TAGS: [e2e, device, regression]
  SITE: SauceDemo
  MODE: classic
"""

import pytest


@pytest.mark.regression
@pytest.mark.e2e
@pytest.mark.device
def test_mobile_cart_accessibility_tc_004(sauce_flow) -> None:
  _, visible = sauce_flow.ensure_mobile_cart_is_accessible(390, 844)
  assert visible, "Cart item should remain visible without scrolling"
  assert sauce_flow.page.viewport_size["width"] == 390
