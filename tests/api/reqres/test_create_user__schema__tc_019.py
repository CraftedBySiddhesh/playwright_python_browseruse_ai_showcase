"""
@meta:
  TC: TC-019
  REQ: RQ-API-019
  TAGS: [api, regression]
  SITE: ReqRes
  MODE: classic
"""

import pytest
import requests
from jsonschema import validate


@pytest.mark.regression
@pytest.mark.api
def test_create_user_schema_tc_019(base_urls) -> None:
  url = f"{base_urls['reqres']}/api/users"
  payload = {"name": "morpheus", "job": "leader"}
  response = requests.post(url, json=payload, timeout=10)
  assert response.status_code == 201, "Expected HTTP 201 Created"
  body = response.json()
  schema = {
    "type": "object",
    "required": ["name", "job", "id", "createdAt"],
    "properties": {
      "name": {"type": "string"},
      "job": {"type": "string"},
      "id": {"type": "string"},
      "createdAt": {"type": "string"},
    },
  }
  validate(instance=body, schema=schema)
  assert body["name"] == payload["name"]
  assert body["job"] == payload["job"]
