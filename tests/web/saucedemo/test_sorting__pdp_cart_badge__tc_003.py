"""
@meta:
  TC: TC-003
  REQ: SD-CART-003
  TAGS: [e2e, regression]
  SITE: SauceDemo
  MODE: classic
"""

import pytest


@pytest.mark.regression
@pytest.mark.e2e
def test_sorting_pdp_cart_badge_tc_003(sauce_flow) -> None:
  first_item = sauce_flow.add_cheapest_item_and_open_cart()
  badge_value = sauce_flow.inventory_page.cart_badge_value()
  assert badge_value == "1", "Cart badge should show 1 after adding item"
  assert sauce_flow.cart_page.is_item_visible(first_item), "Cart should display selected item"
