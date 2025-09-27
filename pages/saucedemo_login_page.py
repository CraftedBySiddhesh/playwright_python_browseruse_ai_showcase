from __future__ import annotations

from playwright.sync_api import Page, expect


class SauceLoginPage:
  def __init__(self, page: Page) -> None:
    self.page = page

  def goto(self, url: str) -> None:
    self.page.goto(url)
    expect(self.page.get_by_role("heading", name="Swag Labs")).to_be_visible()

  def login(self, username: str, password: str) -> None:
    self.page.get_by_placeholder("Username").fill(username)
    self.page.get_by_placeholder("Password").fill(password)
    self.page.get_by_role("button", name="Login").click()

  def expect_error(self, message: str) -> None:
    error = self.page.locator("[data-test='error']")
    expect(error).to_be_visible()
    expect(error).to_have_text(message)

  def is_login_page(self) -> bool:
    return self.page.get_by_placeholder("Username").is_visible()
