from __future__ import annotations

from pathlib import Path

from playwright.sync_api import Page, expect

from pages.internet_portal_pages import (
  DynamicLoadingExampleTwo,
  FileDownloadPage,
  FileUploadPage,
  InternetHomePage,
)


class InternetFlows:
  def __init__(self, page: Page, base_url: str, download_dir: Path) -> None:
    self.page = page
    self.base_url = base_url
    self.download_dir = download_dir
    self.home = InternetHomePage(page)
    self.upload_page = FileUploadPage(page)
    self.download_page = FileDownloadPage(page)
    self.dynamic_loading = DynamicLoadingExampleTwo(page)

  def upload_and_download(self, upload_file: Path) -> tuple[str, Path]:
    self.home.goto(self.base_url)
    self.home.open_example("File Upload")
    self.upload_page.upload_file(upload_file)
    uploaded = self.upload_page.uploaded_filename()
    assert upload_file.name == uploaded, "Uploaded filename should match"
    self.page.go_back()
    self.home.open_example("File Download")
    downloaded = self.download_page.download_first_file(self.download_dir)
    assert downloaded.exists(), "Downloaded file should exist"
    return uploaded, downloaded

  def wait_for_dynamic_loading(self) -> None:
    self.home.goto(self.base_url)
    self.home.open_example("Dynamic Loading")
    self.page.get_by_role("link", name="Example 2: Element rendered after the fact").click()
    self.dynamic_loading.start_loading()
    self.dynamic_loading.wait_for_finish()

  def trigger_404_and_recover(self) -> None:
    self.home.goto(self.base_url + "/does-not-exist")
    expect(self.page.get_by_text("Not Found")).to_be_visible()
    self.page.go_back()
    self.home.open_example("Frames")
    expect(self.page.get_by_role("heading", name="Frames")).to_be_visible()
