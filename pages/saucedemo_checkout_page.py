from __future__ import annotations

from playwright.sync_api import Page, expect


class SauceCheckoutPage:
  def __init__(self, page: Page) -> None:
    self.page = page

  def complete_step_one(self, first_name: str, last_name: str, postal_code: str) -> None:
    expect(self.page.get_by_role("heading", name="Checkout: Your Information")).to_be_visible()
    self.page.get_by_placeholder("First Name").fill(first_name)
    self.page.get_by_placeholder("Last Name").fill(last_name)
    self.page.get_by_placeholder("Zip/Postal Code").fill(postal_code)
    self.page.get_by_role("button", name="Continue").click()

  def finish(self) -> None:
    expect(self.page.get_by_role("heading", name="Checkout: Overview")).to_be_visible()
    self.page.get_by_role("button", name="Finish").click()

  def expect_thank_you(self) -> str:
    heading = self.page.get_by_role("heading", name="THANK YOU FOR YOUR ORDER")
    expect(heading).to_be_visible()
    body = self.page.locator(".complete-text")
    expect(body).to_be_visible()
    return body.inner_text()
