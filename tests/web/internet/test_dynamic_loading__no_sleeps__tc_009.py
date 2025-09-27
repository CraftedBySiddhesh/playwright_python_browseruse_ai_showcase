"""
@meta:
  TC: TC-009
  REQ: TI-DYN-009
  TAGS: [e2e, resilience, regression]
  SITE: Internet
  MODE: classic
"""

import pytest

from flows.internet_flows import InternetFlows


@pytest.mark.regression
@pytest.mark.e2e
@pytest.mark.resilience
def test_dynamic_loading_no_sleeps_tc_009(page, base_urls, tmp_path) -> None:
  flows = InternetFlows(page, base_urls["internet"], tmp_path)
  flows.wait_for_dynamic_loading()
  message = page.locator("#finish h4").inner_text()
  assert message == "Hello World!", "Expected asynchronous content to load"
