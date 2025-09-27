from __future__ import annotations

from playwright.sync_api import Page, expect


class DemoblazeHomePage:
  def __init__(self, page: Page) -> None:
    self.page = page

  def goto(self, url: str) -> None:
    self.page.goto(url)
    expect(self.page.get_by_role("link", name="Home")).to_be_visible()

  def open_category(self, category: str) -> None:
    self.page.get_by_role("link", name=category, exact=True).click()

  def open_first_item(self) -> str:
    first = self.page.locator(".card-title a").first
    name = first.inner_text()
    first.click()
    return name

  def add_current_item_to_cart(self) -> None:
    with self.page.expect_event("dialog") as dialog_info:
      self.page.get_by_role("button", name="Add to cart").click()
    dialog_info.value.accept()

  def open_cart(self) -> None:
    self.page.get_by_role("link", name="Cart").click()

  def cart_rows(self):
    return self.page.locator("#tbodyid tr")

  def delete_first_row(self) -> None:
    self.cart_rows().first.get_by_role("link", name="Delete").click()

  def place_order(self, name: str, country: str, city: str, card: str, month: str, year: str) -> str:
    self.page.get_by_role("button", name="Place Order").click()
    modal = self.page.locator("#orderModal")
    expect(modal).to_be_visible()
    self.page.locator("#name").fill(name)
    self.page.locator("#country").fill(country)
    self.page.locator("#city").fill(city)
    self.page.locator("#card").fill(card)
    self.page.locator("#month").fill(month)
    self.page.locator("#year").fill(year)
    self.page.get_by_role("button", name="Purchase").click()
    confirmation = self.page.locator(".sweet-alert")
    expect(confirmation).to_be_visible()
    text = confirmation.inner_text()
    self.page.get_by_role("button", name="OK").click()
    return text
