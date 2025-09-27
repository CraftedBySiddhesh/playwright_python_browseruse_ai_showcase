from __future__ import annotations

from playwright.sync_api import Page

from utils.sauce_simulator import SauceSimulator


class SauceLoginPage:
    def __init__(self, page: Page, simulator: SauceSimulator | None = None) -> None:
        self.page = page
        self.simulator = simulator or SauceSimulator()

    def goto(self, url: str) -> None:
        self.simulator.reset()
        self._render_login_page()

    def login(self, username: str, password: str) -> None:
        success = self.simulator.attempt_login(username, password)
        if not success:
            self._render_login_page()

    def expect_error(self, message: str) -> None:
        from playwright.sync_api import expect

        error_locator = self.page.locator("[data-test='error']")
        expect(error_locator).to_have_text(message)

    def is_login_page(self) -> bool:
        return not self.simulator.logged_in

    def _render_login_page(self) -> None:
        error_html = ""
        if self.simulator.error_message:
            error_html = (
                "<div class='error-message-container' data-test='error'>"
                f"{self.simulator.error_message}"
                "</div>"
            )

        self.page.set_content(
            "<main>"
            "<h1>Swag Labs</h1>"
            f"{error_html}"
            "<form>"
            "<input data-test='username' />"
            "<input data-test='password' type='password' />"
            "<button data-test='login-button'>Login</button>"
            "</form>"
            "</main>"
        )
