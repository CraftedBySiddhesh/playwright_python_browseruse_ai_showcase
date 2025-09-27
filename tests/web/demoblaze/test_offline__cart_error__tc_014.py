"""
@meta:
  TC: TC-014
  REQ: DB-OFF-014
  TAGS: [edge, resilience, regression]
  SITE: Demoblaze
  MODE: classic
"""

import pytest
from playwright.sync_api import expect

from flows.demoblaze_flows import DemoblazeFlows


@pytest.mark.regression
@pytest.mark.edge
@pytest.mark.resilience
def test_offline_cart_error_tc_014(context, page, base_urls) -> None:
  flow = DemoblazeFlows(page, base_urls["demoblaze"])
  flow.home.goto(base_urls["demoblaze"])
  context.set_offline(True)
  flow.home.open_cart()
  error_banner = page.locator(".modal-content, .alert").first
  expect(error_banner).to_be_visible()
  context.set_offline(False)
  page.reload()
  expect(page.get_by_role("link", name="Home")).to_be_visible()
  assert error_banner.count() >= 1, "Error banner should render when offline"
