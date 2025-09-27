"""
@meta:
  TC: TC-002
  REQ: SD-AUTH-002
  TAGS: [e2e, negative, regression]
  SITE: SauceDemo
  MODE: classic
"""

import pytest
from playwright.sync_api import expect

from pages.saucedemo_login_page import SauceLoginPage


@pytest.mark.regression
@pytest.mark.e2e
@pytest.mark.negative
def test_login_negative_password_tc_002(page, base_urls) -> None:
  login_page = SauceLoginPage(page)
  login_page.goto(base_urls["sauce"])
  login_page.login("standard_user", "bad_pass")
  login_page.expect_error("Epic sadface: Username and password do not match any user in this service")
  assert login_page.is_login_page(), "User should remain on login page after failure"
