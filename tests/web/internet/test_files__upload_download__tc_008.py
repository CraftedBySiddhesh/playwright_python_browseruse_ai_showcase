"""
@meta:
  TC: TC-008
  TITLE: The-Internet — Upload & Download
  OBJECTIVE: Upload shows filename; download exists on disk.
  INSTRUCTION: "Upload a small .txt file on File Upload, confirm filename appears, then go to File Download, download a file, and verify it exists locally."
  EXPECTED: Filename shown; file present in temp/downloads.
  TAGS: [ai, e2e, internet, files, regression]
  MODE: ai_stub
"""

import pytest


@pytest.mark.regression
@pytest.mark.e2e
@pytest.mark.files
@pytest.mark.ai_stub
def test_files_upload_download_tc_008(agent_runner) -> None:
  instructions = (
    "Upload a small .txt file on File Upload, confirm filename appears, then go to File Download, download a file, and verify it exists locally."
  )
  result = agent_runner(
    instructions,
    case_id="TC-008",
    goals=["TC-008", "The-Internet — Upload & Download"],
  )
  assert result.success
  assert result.events[0].observation == instructions
