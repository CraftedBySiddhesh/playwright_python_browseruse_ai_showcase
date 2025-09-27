"""
@meta:
  TC: TC-014
  TITLE: Demoblaze — Network Offline Edge Case
  OBJECTIVE: App shows graceful error offline.
  INSTRUCTION: "Open Demoblaze home, then go offline, open Cart, verify user-friendly error (no crash). Restore network after assertions."
  EXPECTED: Error UX present; app recovers when online.
  TAGS: [ai, edge, demoblaze, resilience, regression]
  MODE: ai_stub
"""

import pytest


@pytest.mark.regression
@pytest.mark.edge
@pytest.mark.resilience
@pytest.mark.ai_stub
def test_offline_cart_error_tc_014(agent_runner) -> None:
  instructions = (
    "Open Demoblaze home, then go offline, open Cart, verify user-friendly error (no crash). Restore network after assertions."
  )
  result = agent_runner(
    instructions,
    case_id="TC-014",
    goals=["TC-014", "Demoblaze — Network Offline Edge Case"],
  )
  assert result.success
  assert result.events[0].observation == instructions
