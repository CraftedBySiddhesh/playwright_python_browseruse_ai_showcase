"""
@meta:
  TC: TC-007
  REQ: BK-SRCH-007
  TAGS: [e2e, regression]
  SITE: Books
  MODE: classic
"""

import pytest

from flows.books_flows import BooksFlows


@pytest.mark.regression
@pytest.mark.e2e
def test_search_travel_pagination_tc_007(page, base_urls, settings) -> None:
  flows = BooksFlows(page, base_urls["books"], settings.app.artifacts_dir)
  book = flows.search_and_open_first("travel")
  price = page.locator(".price_color").inner_text()
  assert price.startswith("£"), "Price should include currency symbol"
  assert book, "Book title should not be empty"
