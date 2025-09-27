"""
@meta:
  TC: TC-019
  TITLE: API — ReqRes Create User + Schema
  OBJECTIVE: Validate POST create response and schema.
  INSTRUCTION: "POST /api/users with name='morpheus', job='leader'; expect 201, body includes id and createdAt, schema types match."
  EXPECTED: Status 201; JSON schema validated.
  TAGS: [ai, api, reqres, regression]
  MODE: ai_stub
"""

import pytest


@pytest.mark.regression
@pytest.mark.api
@pytest.mark.ai_stub
def test_create_user_schema_tc_019(agent_runner) -> None:
  instructions = (
    "POST /api/users with name='morpheus', job='leader'; expect 201, body includes id and createdAt, schema types match."
  )
  result = agent_runner(
    instructions,
    case_id="TC-019",
    goals=["TC-019", "ReqRes — Create User + Schema"],
  )
  assert result.success
  assert result.events[0].observation == instructions
