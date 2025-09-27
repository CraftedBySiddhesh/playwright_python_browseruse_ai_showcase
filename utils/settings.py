from __future__ import annotations

from pathlib import Path
from typing import Any

import tomllib
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator


class TimeoutSettings(BaseModel):
  page_load: int = Field(30000, ge=0)
  locator: int = Field(10000, ge=0)


class PlaywrightSettings(BaseModel):
  slow_mo: int = 0
  traces: bool = True
  screenshots: str = "on"
  videos: str = "on"


class AppSettings(BaseModel):
  project_name: str = "playwright-ai-browser-use"
  artifacts_dir: Path = Path("reports")
  transcripts_dir: Path = Path("reports/ai_transcripts")
  seed: int = 42

  @field_validator("artifacts_dir", "transcripts_dir", mode="before")
  @classmethod
  def _ensure_path(cls, value: Any) -> Path:
    return Path(value)


class Settings(BaseModel):
  enable_agent: bool = False
  llm_provider: str = "stub"
  groq_api_key: str | None = None
  openai_api_key: str | None = None
  default_browser: str = "chromium"
  base_urls: dict[str, str]
  allow_list_domains: list[str]
  timeouts: TimeoutSettings
  playwright: PlaywrightSettings
  app: AppSettings

  @field_validator("llm_provider")
  @classmethod
  def _normalize_provider(cls, value: str) -> str:
    return value.lower()

  @property
  def use_live_provider(self) -> bool:
    if not self.enable_agent:
      return False
    if self.llm_provider == "stub":
      return False
    if self.llm_provider in {"groq", "openai"}:
      return bool(self.groq_api_key or self.openai_api_key)
    return False


def load_settings() -> Settings:
  load_dotenv()
  settings_path = Path("configs/settings.toml")
  if not settings_path.exists():
    raise FileNotFoundError(f"Settings file not found: {settings_path}")
  data = tomllib.loads(settings_path.read_text())
  app_data = data.get("app", {})
  timeouts_data = data.get("timeouts", {})
  playwright_data = data.get("playwright", {})
  allow_list = data.get("allow_list", {}).get("domains", [])

  env_values = {
    "enable_agent": _as_bool("ENABLE_AGENT", default=False),
    "llm_provider": _get_env("LLM_PROVIDER", default="stub"),
    "groq_api_key": _get_env("GROQ_API_KEY"),
    "openai_api_key": _get_env("OPENAI_API_KEY"),
    "default_browser": _get_env("DEFAULT_BROWSER", default="chromium"),
    "base_urls": {
      "sauce": _get_env("SAUCE_URL", default="https://www.saucedemo.com"),
      "demoblaze": _get_env("DEMOBLAZE_URL", default="https://demoblaze.com"),
      "books": _get_env("BOOKS_URL", default="https://books.toscrape.com"),
      "internet": _get_env("INTERNET_URL", default="https://the-internet.herokuapp.com"),
      "parabank": _get_env("PARABANK_URL", default="https://parabank.parasoft.com"),
      "reqres": _get_env("REQRES_URL", default="https://reqres.in"),
      "countries": _get_env(
        "COUNTRIES_GQL_URL", default="https://countries.trevorblades.com"
      ),
    },
    "allow_list_domains": allow_list,
    "timeouts": TimeoutSettings(**timeouts_data),
    "playwright": PlaywrightSettings(**playwright_data),
    "app": AppSettings(**app_data),
  }
  settings = Settings(**env_values)
  settings.app.artifacts_dir.mkdir(parents=True, exist_ok=True)
  settings.app.transcripts_dir.mkdir(parents=True, exist_ok=True)
  return settings


def _get_env(key: str, default: str | None = None) -> str | None:
  from os import getenv

  value = getenv(key)
  if value is None:
    return default
  return value


def _as_bool(key: str, default: bool = False) -> bool:
  value = _get_env(key)
  if value is None:
    return default
  return value.lower() in {"1", "true", "yes", "on"}
