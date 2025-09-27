from __future__ import annotations

from playwright.sync_api import Page, expect


class ParabankHomePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self, url: str) -> None:
        self.page.goto(url)
        expect(self.page.get_by_role("link", name="home")).to_be_visible()

    def login(self, username: str, password: str) -> None:
        self.page.locator("name=username").fill(username)
        self.page.locator("name=password").fill(password)
        self.page.locator("input[value='Log In']").click()

    def logout(self) -> None:
        self.page.get_by_role("link", name="Log Out").click()

    def expect_overview(self) -> None:
        expect(self.page.get_by_role("heading", name="Accounts Overview")).to_be_visible()

    def open_register(self) -> None:
        self.page.get_by_role("link", name="Register").click()


class ParabankRegisterPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def register(self, user_data: dict[str, str]) -> None:
        for field, value in user_data.items():
            locator = self.page.locator(f"input[name='{field}']")
            if locator.count() == 0:
                continue
            locator.fill(value)
        self.page.locator("input[value='Register']").click()
        expect(self.page.get_by_text("Your account was created successfully")).to_be_visible()


class ParabankTransferPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self) -> None:
        self.page.get_by_role("link", name="Transfer Funds").click()

    def attempt_transfer(self, amount: str) -> None:
        self.page.locator("input[name='amount']").fill(amount)
        self.page.locator("input[type='submit']").click()

    def validation_message(self) -> str:
        error = self.page.locator("span.error")
        if error.count() > 0:
            return error.first.inner_text()
        return self.page.locator("div#rightPanel").inner_text()
