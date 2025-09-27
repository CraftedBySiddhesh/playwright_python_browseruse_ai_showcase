from __future__ import annotations

from pathlib import Path
from typing import Callable

import pytest
from playwright.sync_api import Browser, BrowserContext, Page

from agents.browser_agent import AgentResult, run_instructions
from utils.settings import Settings, load_settings


@pytest.fixture(scope="session")
def settings() -> Settings:
  return load_settings()


@pytest.fixture(scope="session")
def base_urls(settings: Settings) -> dict[str, str]:
  return settings.base_urls


@pytest.fixture(scope="session")
def allow_domains(settings: Settings) -> list[str]:
  return settings.allow_list_domains


@pytest.fixture
def test_artifact_dir(settings: Settings, request: pytest.FixtureRequest) -> Path:
  slug = request.node.name.replace("::", "_")
  path = Path(settings.app.artifacts_dir) / "artifacts" / slug
  path.mkdir(parents=True, exist_ok=True)
  return path


@pytest.fixture
def browser_context_args(settings: Settings, test_artifact_dir: Path) -> dict[str, object]:
  video_dir = Path(settings.app.artifacts_dir) / "videos"
  video_dir.mkdir(parents=True, exist_ok=True)
  return {
    "record_video_dir": str(video_dir),
    "base_url": settings.base_urls.get("internet"),
    "viewport": {"width": 1280, "height": 720},
  }


@pytest.fixture
def context(browser: Browser, browser_context_args: dict[str, object], test_artifact_dir: Path):
  context = browser.new_context(**browser_context_args)
  context.tracing.start(screenshots=True, snapshots=True, sources=True)
  yield context
  trace_path = test_artifact_dir / "trace.zip"
  context.tracing.stop(path=str(trace_path))
  context.close()


@pytest.fixture
def page(context: BrowserContext) -> Page:  # type: ignore[override]
  page = context.new_page()
  return page


@pytest.fixture
def agent_runner(
  settings: Settings,
  allow_domains: list[str],
) -> Callable[[str, str, list[str] | None], AgentResult]:
  def _runner(instructions: str, case_id: str, goals: list[str] | None = None) -> AgentResult:
    goals_list = goals or []
    if case_id not in goals_list:
      goals_list.append(case_id)
    return run_instructions(
      instructions=instructions,
      goals=goals_list,
      allow_domains=allow_domains,
      settings=settings,
    )

  return _runner


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
  outcome = yield
  rep = outcome.get_result()
  setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(autouse=True)
def capture_artifacts(request: pytest.FixtureRequest, page: Page, test_artifact_dir: Path):
  yield
  rep = getattr(request.node, "rep_call", None)
  if rep and rep.failed:
    screenshot_path = test_artifact_dir / "failure.png"
    page.screenshot(path=screenshot_path, full_page=True)
