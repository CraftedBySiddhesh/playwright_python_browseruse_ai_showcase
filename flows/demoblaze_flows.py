from __future__ import annotations

from playwright.sync_api import Page

from pages.demoblaze_home_page import DemoblazeHomePage


class DemoblazeFlows:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url
        self.home = DemoblazeHomePage(page)

    def add_category_item_and_checkout(self, category: str) -> str:
        self.home.goto(self.base_url)
        self.home.open_category(category)
        item_name = self.home.open_first_item()
        self.home.add_current_item_to_cart()
        self.home.open_cart()
        rows = self.home.cart_rows()
        assert rows.count() >= 1, "Item should be present in cart"
        assert item_name, "Product name should not be blank"
        confirmation = self.home.place_order(
            name="Test User",
            country="USA",
            city="Austin",
            card="4111111111111111",
            month="05",
            year="2025",
        )
        assert "Id:" in confirmation, "Confirmation should include an ID"
        return confirmation

    def remove_item_and_get_total(self) -> tuple[int, int]:
        self.home.goto(self.base_url)
        self.home.open_category("Phones")
        self.home.open_first_item()
        self.home.add_current_item_to_cart()
        self.page.go_back()
        self.home.open_first_item()
        self.home.add_current_item_to_cart()
        self.home.open_cart()
        rows = self.home.cart_rows()
        assert rows.count() >= 2, "Two phones should be present"
        prices = []
        for idx in range(rows.count()):
            price_cell = rows.nth(idx).locator("td").nth(2)
            prices.append(int(price_cell.inner_text()))
        self.home.delete_first_row()
        self.page.wait_for_function("document.querySelectorAll('#tbodyid tr').length === 1")
        total_text = self.page.locator("#totalp").inner_text()
        return sum(prices), int(total_text or 0)
