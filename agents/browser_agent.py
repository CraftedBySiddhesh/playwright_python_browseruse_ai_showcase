from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path

from ai.providers import ProviderProtocol, get_provider
from utils.logger import configure_logger
from utils.settings import Settings, load_settings

logger = configure_logger("browser_agent")


@dataclass
class AgentEvent:
  step: int
  action: str
  observation: str
  url: str | None = None
  screenshot_path: str | None = None
  timestamp: float = field(default_factory=lambda: time.time())


@dataclass
class AgentResult:
  success: bool
  message: str
  events: list[AgentEvent]
  total_steps: int


def run_instructions(
  instructions: str,
  goals: list[str] | None = None,
  time_budget_s: int = 120,
  allow_domains: list[str] | None = None,
  settings: Settings | None = None,
) -> AgentResult:
  settings = settings or load_settings()
  provider = get_provider(settings)
  allowed = allow_domains or settings.allow_list_domains
  goals = goals or []

  logger.info(
    "Agent invoked",
    extra={
      "instructions": instructions,
      "goals": goals,
      "time_budget_s": time_budget_s,
      "allowed": allowed,
    },
  )

  start = time.time()
  events: list[AgentEvent] = [
    AgentEvent(step=1, action="receive_instructions", observation=instructions),
    AgentEvent(step=2, action="set_goals", observation=", ".join(goals) or "no_goals"),
    AgentEvent(
      step=3,
      action="configure_guardrails",
      observation=f"allow={allowed}; budget={time_budget_s}s",
    ),
  ]

  if not allowed:
    raise ValueError("Allow list must not be empty")

  transcript_id = _extract_case_id(goals) or f"session_{int(start)}"
  summary = _execute_provider(provider, instructions, goals, time_budget_s, allowed, events)
  success = True
  total_steps = len(events)

  _persist_transcript(settings, transcript_id, events)
  duration = time.time() - start
  logger.info(
    "Agent execution completed",
    extra={
      "transcript_id": transcript_id,
      "duration": duration,
      "steps": total_steps,
      "success": success,
    },
  )
  return AgentResult(success=success, message=summary, events=events, total_steps=total_steps)


def _execute_provider(
  provider: ProviderProtocol,
  instructions: str,
  goals: list[str],
  time_budget_s: int,
  allowed: list[str],
  events: list[AgentEvent],
) -> str:
  logger.debug(
    "Executing agent provider",
    extra={
      "time_budget_s": time_budget_s,
      "allowed": allowed,
    },
  )
  summary = provider.generate(instructions)
  events.append(
    AgentEvent(
      step=len(events) + 1,
      action="complete",
      observation=f"Stub provider summary: {summary}",
    )
  )
  return summary


def _extract_case_id(goals: list[str]) -> str | None:
  for goal in goals:
    if goal.startswith("TC-"):
      return goal
  return None


def _persist_transcript(settings: Settings, transcript_id: str, events: list[AgentEvent]) -> None:
  transcript_dir = Path(settings.app.transcripts_dir)
  transcript_dir.mkdir(parents=True, exist_ok=True)
  path = transcript_dir / f"{transcript_id}.jsonl"
  with path.open("w", encoding="utf-8") as handle:
    for event in events:
      handle.write(json.dumps(event.__dict__) + "\n")
