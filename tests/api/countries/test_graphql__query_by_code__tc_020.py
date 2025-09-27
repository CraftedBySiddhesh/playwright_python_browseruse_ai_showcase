"""
@meta:
  TC: TC-020
  REQ: CT-GQL-020
  TAGS: [api, graphql, regression]
  SITE: Countries
  MODE: classic
"""

import pytest
import requests


@pytest.mark.regression
@pytest.mark.api
@pytest.mark.graphql
def test_graphql_query_by_code_tc_020(base_urls) -> None:
  url = base_urls["countries"]
  query = """
  query GetCountry($code: ID!) {
    country(code: $code) {
      name
      capital
      currency
    }
  }
  """
  response = requests.post(url, json={"query": query, "variables": {"code": "IN"}}, timeout=10)
  assert response.status_code == 200, "Expected 200 from Countries API"
  data = response.json()["data"]["country"]
  assert all(data[field] for field in ("name", "capital", "currency")), "All fields should be non-empty"
  assert data["currency"].isupper(), "Currency should be uppercase"
