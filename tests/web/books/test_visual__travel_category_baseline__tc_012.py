"""
@meta:
  TC: TC-012
  REQ: BK-VIS-012
  TAGS: [visual, regression]
  SITE: Books
  MODE: classic
"""

import json
from pathlib import Path

import pytest

from flows.books_flows import BooksFlows


@pytest.mark.regression
@pytest.mark.visual
def test_visual_travel_category_baseline_tc_012(page, base_urls, settings) -> None:
  baseline_file = Path("configs/baselines/books_travel.json")
  baseline = json.loads(baseline_file.read_text())
  flows = BooksFlows(page, base_urls["books"], settings.app.artifacts_dir)
  snapshot_path = flows.capture_category_snapshot("Travel", "travel_grid")
  product_count = page.locator(".product_pod").count()
  tolerance = 2
  assert abs(product_count - baseline["title_count"]) <= tolerance, "Grid layout changed beyond tolerance"
  assert snapshot_path.exists(), "Snapshot should be captured to disk"
