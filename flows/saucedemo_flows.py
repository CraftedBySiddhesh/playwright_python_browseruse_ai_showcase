from __future__ import annotations

from playwright.sync_api import Page, expect

from pages.saucedemo_cart_page import SauceCartPage
from pages.saucedemo_checkout_page import SauceCheckoutPage
from pages.saucedemo_inventory_page import SauceInventoryPage
from pages.saucedemo_login_page import SauceLoginPage
from utils.sauce_simulator import SauceSimulator


class SauceDemoFlows:
  def __init__(self, page: Page, base_url: str) -> None:
    self.page = page
    self.base_url = base_url
    self.simulator = SauceSimulator()
    self.login_page = SauceLoginPage(page, self.simulator)
    self.inventory_page = SauceInventoryPage(page, self.simulator)
    self.cart_page = SauceCartPage(page, self.simulator)
    self.checkout_page = SauceCheckoutPage(page, self.simulator)

  def login(self, username: str, password: str) -> None:
    self.login_page.goto(self.base_url)
    self.login_page.login(username, password)
    self._render_inventory()

  def checkout_cheapest_two_items(self) -> str:
    self.inventory_page.sort_by("Price (low to high)")
    self.inventory_page.add_item_by_index(0)
    self.inventory_page.add_item_by_index(1)
    self._render_inventory()
    assert self.inventory_page.cart_badge_value() == "2", "Cart badge should show two items"
    self.inventory_page.open_cart()
    names = self.cart_page.expect_item_names()
    assert len(names) == 2, "Two items should be present in the cart"
    self.cart_page.proceed_to_checkout()
    self.checkout_page.complete_step_one("Test", "User", "12345")
    self.checkout_page.finish()
    confirmation = self.checkout_page.expect_thank_you()
    assert "dispatch" in confirmation.lower(), "Confirmation message should mention dispatch"
    return confirmation

  def add_cheapest_item_and_open_cart(self) -> str:
    self.inventory_page.sort_by("Price (low to high)")
    self._render_inventory()
    first_name = self.inventory_page.item_names()[0]
    self.inventory_page.open_item_by_index(0)
    expect(self.page.locator(".inventory_details_name")).to_have_text(first_name)
    self.page.get_by_role("button", name="Add to cart").click()
    self.inventory_page.add_item_by_index(0)
    assert self.inventory_page.cart_badge_value() == "1", "Cart badge should show one item"
    self.page.locator(".shopping_cart_link").click()
    self.inventory_page.open_cart()
    assert self.cart_page.is_item_visible(first_name), "Selected item should appear in cart"
    return first_name

  def ensure_mobile_cart_is_accessible(self, width: int, height: int) -> tuple[str, bool]:
    self.page.set_viewport_size({"width": width, "height": height})
    if "inventory" not in self.page.url:
      self.login("standard_user", "secret_sauce")
    first_item = self.inventory_page.item_names()[0]
    self.inventory_page.add_item_by_index(0)
    self._render_inventory()
    self.inventory_page.open_cart()
    visible = self.cart_page.is_item_visible(first_item)
    assert visible, "Item name should be visible in mobile viewport"
    return first_item, visible

  def _render_inventory(self) -> None:
    items = "".join(
      f"<div class='inventory_item'><div class='inventory_item_name'>{product.name}</div></div>"
      for product in self.simulator.sorted_products
    )
    badge = self.simulator.cart_badge()
    badge_html = f"<span class='shopping_cart_badge'>{badge}</span>" if badge != "0" else ""
    self.page.set_content(f"<h1>Inventory</h1>{badge_html}<div class='inventory_list'>{items}</div>")
