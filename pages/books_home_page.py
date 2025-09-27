from __future__ import annotations

from playwright.sync_api import Page, expect


class BooksHomePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self, url: str) -> None:
        self.page.goto(url)
        expect(self.page.get_by_role("link", name="All products")).to_be_visible()

    def search(self, term: str) -> None:
        self.page.locator("#id_q").fill(term)
        self.page.locator("input[type='submit']").click()

    def open_first_book(self) -> str:
        first = self.page.locator("ol.row li article h3 a").first
        name = first.inner_text()
        first.click()
        return name

    def go_to_next_page(self) -> None:
        next_button = self.page.get_by_role("link", name="next")
        if next_button.is_visible():
            next_button.click()

    def get_price_text(self) -> str:
        price = self.page.locator(".price_color")
        expect(price).to_be_visible()
        return price.inner_text()

    def capture_grid_snapshot(self, path: str) -> None:
        grid = self.page.locator(".row").first
        grid.screenshot(path=path)
