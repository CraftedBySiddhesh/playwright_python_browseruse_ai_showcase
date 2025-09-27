"""
@meta:
  TC: TC-012
  TITLE: BooksToScrape — Visual Baseline
  OBJECTIVE: Catch unintended UI changes on category grid.
  INSTRUCTION: "Capture a snapshot of the ‘Travel’ category grid and compare against baseline with a small tolerance; fail if diff exceeds tolerance."
  EXPECTED: Test fails on significant diff; baseline stored.
  TAGS: [ai, visual, books, regression]
  MODE: ai_stub
"""

import pytest


@pytest.mark.regression
@pytest.mark.visual
@pytest.mark.ai_stub
def test_visual_travel_category_baseline_tc_012(agent_runner) -> None:
  instructions = (
    "Capture a snapshot of the ‘Travel’ category grid and compare against baseline with a small tolerance; fail if diff exceeds tolerance."
  )
  result = agent_runner(
    instructions,
    case_id="TC-012",
    goals=["TC-012", "BooksToScrape — Visual Baseline"],
  )
  assert result.success
  assert result.events[0].observation == instructions
