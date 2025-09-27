"""
@meta:
  TC: TC-011
  REQ: PB-TRANS-011
  TAGS: [e2e, negative, regression]
  SITE: Parabank
  MODE: classic
"""

import pytest

from flows.parabank_flows import ParabankFlows


@pytest.mark.regression
@pytest.mark.e2e
@pytest.mark.negative
def test_transfer_negative_amount_tc_011(page, base_urls) -> None:
  flows = ParabankFlows(page, base_urls["parabank"])
  message = flows.attempt_negative_transfer()
  assert "amount" in message.lower(), "Validation message should mention amount"
  assert "success" not in message.lower(), "Transfer should not succeed"
