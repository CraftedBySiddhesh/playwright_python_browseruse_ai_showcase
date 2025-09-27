from __future__ import annotations

from pathlib import Path

from playwright.sync_api import Page, expect


class InternetHomePage:
  def __init__(self, page: Page) -> None:
    self.page = page

  def goto(self, url: str) -> None:
    self.page.goto(url)
    expect(self.page.get_by_role("heading", name="Available Examples")).to_be_visible()

  def open_example(self, name: str) -> None:
    self.page.get_by_role("link", name=name).click()


class FileUploadPage:
  def __init__(self, page: Page) -> None:
    self.page = page

  def upload_file(self, file_path: Path) -> None:
    self.page.locator("#file-upload").set_input_files(str(file_path))
    self.page.locator("#file-submit").click()

  def uploaded_filename(self) -> str:
    expect(self.page.get_by_role("heading", name="File Uploaded!")).to_be_visible()
    return self.page.locator("#uploaded-files").inner_text()


class FileDownloadPage:
  def __init__(self, page: Page) -> None:
    self.page = page

  def download_first_file(self, download_dir: Path) -> Path:
    with self.page.expect_download() as download_info:
      self.page.locator("#content a").first.click()
    download = download_info.value
    target_path = download_dir / download.suggested_filename
    download.save_as(target_path)
    return target_path


class DynamicLoadingExampleTwo:
  def __init__(self, page: Page) -> None:
    self.page = page

  def start_loading(self) -> None:
    self.page.get_by_role("button", name="Start").click()

  def wait_for_finish(self) -> None:
    finish = self.page.locator("#finish h4")
    expect(finish).to_have_text("Hello World!")
