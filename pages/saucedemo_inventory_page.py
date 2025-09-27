from __future__ import annotations

from typing import Sequence

from playwright.sync_api import Locator, Page, expect


class SauceInventoryPage:
  def __init__(self, page: Page) -> None:
    self.page = page

  def sort_by(self, option_text: str) -> None:
    self.page.locator("[data-test='product_sort_container']").select_option(label=option_text)

  def get_inventory_items(self) -> Locator:
    return self.page.locator(".inventory_item")

  def open_item_by_index(self, index: int) -> None:
    items = self.get_inventory_items()
    items.nth(index).locator("a.inventory_item_name").click()

  def add_item_by_index(self, index: int) -> None:
    self.get_inventory_items().nth(index).get_by_role("button", name="Add to cart").click()

  def cart_badge_value(self) -> str:
    badge = self.page.locator(".shopping_cart_badge")
    if badge.count() == 0:
      return "0"
    return badge.first.inner_text()

  def open_cart(self) -> None:
    self.page.locator(".shopping_cart_link").click()

  def expect_loaded(self) -> None:
    expect(self.page.locator(".inventory_list")).to_be_visible()

  def item_names(self) -> Sequence[str]:
    return self.page.locator(".inventory_item_name").all_text_contents()
