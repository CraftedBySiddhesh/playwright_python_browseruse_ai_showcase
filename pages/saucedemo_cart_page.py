from __future__ import annotations

from playwright.sync_api import Page, expect


class SauceCartPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def expect_item_names(self) -> list[str]:
        expect(self.page.get_by_role("heading", name="Your Cart")).to_be_visible()
        return self.page.locator(".inventory_item_name").all_text_contents()

    def proceed_to_checkout(self) -> None:
        self.page.get_by_role("button", name="Checkout").click()

    def is_item_visible(self, item_name: str) -> bool:
        locator = self.page.locator(".inventory_item_name", has_text=item_name)
        if locator.count() == 0:
            return False
        return locator.first.is_visible()
