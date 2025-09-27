"""
@meta:
  TC: TC-005
  REQ: DB-ORD-005
  TAGS: [e2e, regression]
  SITE: Demoblaze
  MODE: classic
"""

import pytest

from flows.demoblaze_flows import DemoblazeFlows


@pytest.mark.regression
@pytest.mark.e2e
def test_order_laptop_checkout_tc_005(page, base_urls, test_artifact_dir) -> None:
  flow = DemoblazeFlows(page, base_urls["demoblaze"])
  confirmation = flow.add_category_item_and_checkout("Laptops")
  assert "Id:" in confirmation, "Confirmation should include ID"
  (test_artifact_dir / "confirmation.txt").write_text(confirmation, encoding="utf-8")
