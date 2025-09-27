"""
@meta:
  TC: TC-010
  REQ: PB-REG-010
  TAGS: [e2e, regression]
  SITE: Parabank
  MODE: classic
"""

import pytest

from flows.parabank_flows import ParabankFlows


@pytest.mark.regression
@pytest.mark.e2e
def test_register_login_tc_010(page, base_urls) -> None:
  flows = ParabankFlows(page, base_urls["parabank"])
  creds = flows.register_and_login()
  assert creds["username"].startswith("parabank"), "Username should use parabank prefix"
  assert len(creds["password"]) >= 12, "Password should meet length requirement"
