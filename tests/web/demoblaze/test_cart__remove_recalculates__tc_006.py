"""
@meta:
  TC: TC-006
  REQ: DB-CART-006
  TAGS: [e2e, regression]
  SITE: Demoblaze
  MODE: classic
"""

import pytest

from flows.demoblaze_flows import DemoblazeFlows


@pytest.mark.regression
@pytest.mark.e2e
def test_cart_remove_recalculates_tc_006(page, base_urls) -> None:
  flow = DemoblazeFlows(page, base_urls["demoblaze"])
  total_before, total_after = flow.remove_item_and_get_total()
  assert total_before > total_after, "Total should decrease after removing one item"
  assert total_after > 0, "Remaining total should be greater than zero"
