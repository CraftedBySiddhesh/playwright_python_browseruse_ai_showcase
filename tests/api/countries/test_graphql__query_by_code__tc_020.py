"""
@meta:
  TC: TC-020
  TITLE: API — Countries GraphQL Query by Code
  OBJECTIVE: Validate GraphQL query response fields.
  INSTRUCTION: "Query code='IN' returning name, capital, currency; all fields must be non-empty."
  EXPECTED: Fields present & non-empty; types correct.
  TAGS: [ai, api, graphql, countries, regression]
  MODE: ai_stub
"""

import pytest


@pytest.mark.regression
@pytest.mark.api
@pytest.mark.graphql
@pytest.mark.ai_stub
def test_graphql_query_by_code_tc_020(agent_runner) -> None:
  instructions = (
    "Query code='IN' returning name, capital, currency; all fields must be non-empty."
  )
  result = agent_runner(
    instructions,
    case_id="TC-020",
    goals=["TC-020", "Countries GraphQL Query"],
  )
  assert result.success
  assert result.events[0].observation == instructions
