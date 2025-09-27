from __future__ import annotations

from playwright.sync_api import Page

from pages.parabank_pages import ParabankHomePage, ParabankRegisterPage, ParabankTransferPage
from utils.data import random_password, random_username


class ParabankFlows:
  def __init__(self, page: Page, base_url: str) -> None:
    self.page = page
    self.base_url = base_url
    self.home = ParabankHomePage(page)
    self.register_page = ParabankRegisterPage(page)
    self.transfer_page = ParabankTransferPage(page)

  def register_and_login(self) -> dict[str, str]:
    self.home.goto(self.base_url)
    self.home.open_register()
    username = random_username("parabank")
    password = random_password(12)
    user_data = {
      "customer.firstName": "Test",
      "customer.lastName": "User",
      "customer.address.street": "123 Main",
      "customer.address.city": "Austin",
      "customer.address.state": "TX",
      "customer.address.zipCode": "73301",
      "customer.phoneNumber": "5551234567",
      "customer.ssn": "123-45-6789",
      "customer.username": username,
      "customer.password": password,
      "repeatedPassword": password,
    }
    self.register_page.register(user_data)
    self.home.expect_overview()
    self.home.logout()
    self.home.login(username, password)
    self.home.expect_overview()
    return {"username": username, "password": password}

  def attempt_negative_transfer(self) -> str:
    self.home.goto(self.base_url)
    self.home.login("john", "demo")
    self.transfer_page.open()
    self.transfer_page.attempt_transfer("-100")
    message = self.transfer_page.validation_message()
    assert "amount" in message.lower(), "Validation message should mention amount"
    return message
