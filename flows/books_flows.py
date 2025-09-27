from __future__ import annotations

from pathlib import Path

from playwright.sync_api import Page

from pages.books_home_page import BooksHomePage


class BooksFlows:
  def __init__(self, page: Page, base_url: str, artifacts_dir: Path) -> None:
    self.page = page
    self.base_url = base_url
    self.artifacts_dir = artifacts_dir
    self.home = BooksHomePage(page)

  def search_and_open_first(self, term: str) -> str:
    self.home.goto(self.base_url)
    self.home.search(term)
    self.home.go_to_next_page()
    book = self.home.open_first_book()
    price = self.home.get_price_text()
    assert price.startswith("£"), "Price should be prefixed with pound sign"
    return book

  def capture_category_snapshot(self, category: str, baseline_name: str) -> Path:
    self.home.goto(f"{self.base_url}/catalogue/category/books/{category.lower()}_2/index.html")
    target = self.artifacts_dir / f"{baseline_name}.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    self.home.capture_grid_snapshot(str(target))
    return target
