"""
@meta:
  TC: TC-007
  TITLE: BooksToScrape — Search & Pagination
  OBJECTIVE: Search “travel”, paginate, open first result.
  INSTRUCTION: "Search for ‘travel’, go to the next page if available, open the first book, and confirm the product page shows a price."
  EXPECTED: Price visible and formatted.
  TAGS: [ai, e2e, books, regression]
  MODE: ai_stub
"""

import pytest


@pytest.mark.regression
@pytest.mark.e2e
@pytest.mark.ai_stub
def test_search_travel_pagination_tc_007(agent_runner) -> None:
    instructions = "Search for ‘travel’, go to the next page if available, open the first book, and confirm the product page shows a price."
    result = agent_runner(
        instructions,
        case_id="TC-007",
        goals=["TC-007", "BooksToScrape — Search & Pagination"],
    )
    assert result.success
    assert result.events[0].observation == instructions
