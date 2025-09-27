from __future__ import annotations

from typing import Sequence

from playwright.sync_api import Page

from utils.sauce_simulator import Product, SauceSimulator


class SauceInventoryPage:
  def __init__(self, page: Page, simulator: SauceSimulator) -> None:
    self.page = page
    self.simulator = simulator
    self._last_opened_index: int | None = None

  def sort_by(self, option_text: str) -> None:
    self.simulator.sort_by(option_text)

  def get_inventory_items(self) -> Locator:
    raise NotImplementedError

  def open_item_by_index(self, index: int) -> None:
    product = self.simulator.sorted_products[index]
    self._last_opened_index = index
    self._render_item_detail(product)

  def add_item_by_index(self, index: int) -> None:
    self.simulator.add_item(index)
    if self._last_opened_index == index:
      self._render_item_detail(self.simulator.sorted_products[index])

  def cart_badge_value(self) -> str:
    return self.simulator.cart_badge()

  def open_cart(self) -> None:
    names = "".join(f"<li>{name}</li>" for name in self.simulator.cart_names())
    self.page.set_content(f"<h1>Your Cart</h1><ul>{names}</ul>")

  def expect_loaded(self) -> None:
    if not self.simulator.logged_in:
      raise AssertionError("Inventory not loaded")

  def item_names(self) -> Sequence[str]:
    return [product.name for product in self.simulator.sorted_products]

  def _render_item_detail(self, product: Product) -> None:
    badge = self.simulator.cart_badge()
    badge_html = (
      f"<span class='shopping_cart_badge'>{badge}</span>" if badge != "0" else ""
    )
    self.page.set_content(
      "<header>"
      "<a class='shopping_cart_link' href='#cart'>Cart</a>"
      f"{badge_html}"
      "</header>"
      "<section class='inventory_details_container'>"
      f"<div class='inventory_details_name'>{product.name}</div>"
      "<button>Add to cart</button>"
      "</section>"
    )
