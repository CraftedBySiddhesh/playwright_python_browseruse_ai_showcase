"""
@meta:
  TC: TC-008
  REQ: TI-FILE-008
  TAGS: [e2e, files, regression]
  SITE: Internet
  MODE: classic
"""

from pathlib import Path

import pytest

from flows.internet_flows import InternetFlows


@pytest.mark.regression
@pytest.mark.e2e
@pytest.mark.files
def test_files_upload_download_tc_008(page, base_urls, tmp_path, settings) -> None:
  upload_file = tmp_path / "sample.txt"
  upload_file.write_text("hello world", encoding="utf-8")
  flows = InternetFlows(page, base_urls["internet"], tmp_path)
  uploaded_name, downloaded = flows.upload_and_download(upload_file)
  assert downloaded.exists(), "Downloaded file should be saved"
  assert uploaded_name == upload_file.name
