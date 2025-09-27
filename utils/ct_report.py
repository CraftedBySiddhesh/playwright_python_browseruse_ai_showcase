from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest


@dataclass
class _CaseResult:
    nodeid: str
    name: str
    path: str
    suite: str
    markers: list[str]
    start: datetime | None = None
    stop: datetime | None = None
    outcome: str | None = None
    duration: float = 0.0
    details: dict[str, Any] = field(default_factory=dict)
    keywords: list[str] = field(default_factory=list)


class CTRFPlugin:
    def __init__(self, output_path: Path) -> None:
        self.output_path = output_path
        self.start_time = datetime.now(UTC)
        self.start_perf = time.perf_counter()
        self.results: dict[str, _CaseResult] = {}
        self.result_order: list[str] = []
        self._wallclock: dict[str, float] = {}

    @staticmethod
    def _now() -> datetime:
        return datetime.now(UTC)

    @staticmethod
    def _format_ts(value: datetime | None) -> str | None:
        if value is None:
            return None
        return value.isoformat().replace("+00:00", "Z")

    def pytest_sessionstart(self, session: pytest.Session) -> None:  # noqa: D401 - hook signature
        self.start_time = self._now()
        self.start_perf = time.perf_counter()

    def pytest_collection_modifyitems(
        self, session: pytest.Session, config: pytest.Config, items: list[pytest.Item]
    ) -> None:
        for item in items:
            nodeid = item.nodeid
            if nodeid not in self.results:
                suite = "::".join(nodeid.split("::")[:-1])
                markers = sorted(marker.name for marker in item.iter_markers())
                keywords = sorted(k for k in item.keywords if not k.startswith("pytestmark"))
                case = _CaseResult(
                    nodeid=nodeid,
                    name=item.name,
                    path=str(Path(item.location[0])),
                    suite=suite,
                    markers=markers,
                    keywords=keywords,
                )
                self.results[nodeid] = case
                self.result_order.append(nodeid)

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        case = self.results.setdefault(
            report.nodeid,
            _CaseResult(
                nodeid=report.nodeid,
                name=report.nodeid.split("::")[-1],
                path=str(Path(report.location[0])),
                suite="::".join(report.nodeid.split("::")[:-1]),
                markers=sorted(report.keywords),
            ),
        )

        if report.when == "setup" and case.start is None:
            case.start = self._now()
            self._wallclock[report.nodeid] = time.perf_counter()

        if report.when == "call":
            case.duration += report.duration
            outcome = self._resolve_outcome(report)
            case.outcome = outcome
            if outcome in {"failed", "broken"}:
                case.details = {"message": self._extract_longrepr(report)}
            elif outcome in {"xfailed", "xpassed"}:
                case.details = {"xfail": report.wasxfail}
        elif report.when == "setup" and report.skipped:
            case.duration += report.duration
            case.outcome = "skipped"
            case.details = {"reason": self._extract_skip_reason(report)}
        elif report.when == "teardown":
            case.duration += report.duration

        if report.when == "teardown" or (report.skipped and report.when == "setup"):
            start_perf = self._wallclock.pop(report.nodeid, None)
            if start_perf is not None:
                elapsed = time.perf_counter() - start_perf
                if elapsed > case.duration:
                    case.duration = elapsed
            case.stop = self._now()

    def pytest_sessionfinish(self, session: pytest.Session, exitstatus: int) -> None:
        self._write_report(exitstatus)

    def _write_report(self, exitstatus: int) -> None:
        if not self.output_path:
            return

        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        stop_time = self._now()
        duration = time.perf_counter() - self.start_perf

        tests_payload = []
        summary_counts = {
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "xfailed": 0,
            "xpassed": 0,
            "broken": 0,
        }

        for nodeid in self.result_order:
            case = self.results[nodeid]
            status = case.outcome or "skipped"
            if status in summary_counts:
                summary_counts[status] += 1
            else:
                summary_counts.setdefault(status, 0)
                summary_counts[status] += 1

            tests_payload.append(
                {
                    "id": case.nodeid,
                    "name": case.name,
                    "suite": case.suite,
                    "file": case.path,
                    "status": status,
                    "start": self._format_ts(case.start),
                    "stop": self._format_ts(case.stop),
                    "duration": round(case.duration, 6),
                    "markers": case.markers,
                    "keywords": case.keywords,
                    "details": case.details,
                }
            )

        payload = {
            "$schema": "https://raw.githubusercontent.com/saucelabs/saucectl/main/schema/ctf.json",
            "version": "0.1.0",
            "generated": self._format_ts(stop_time),
            "run": {
                "id": str(uuid.uuid4()),
                "framework": "pytest",
                "name": "pytest suite",
                "status": "passed" if exitstatus == 0 else "failed",
                "start": self._format_ts(self.start_time),
                "stop": self._format_ts(stop_time),
                "duration": round(duration, 6),
            },
            "summary": summary_counts,
            "tests": tests_payload,
        }

        with self.output_path.open("w", encoding="utf-8") as stream:
            json.dump(payload, stream, indent=2)

    @staticmethod
    def _resolve_outcome(report: pytest.TestReport) -> str:
        if report.failed:
            return "xfailed" if getattr(report, "wasxfail", False) else "failed"
        if report.skipped:
            if getattr(report, "wasxfail", False):
                return "xpassed"
            return "skipped"
        return "passed"

    @staticmethod
    def _extract_longrepr(report: pytest.TestReport) -> str:
        longrepr = getattr(report, "longrepr", None)
        if not longrepr:
            return ""
        if isinstance(longrepr, str):
            return longrepr
        if hasattr(longrepr, "reprcrash"):
            return str(longrepr)
        return str(longrepr)

    @staticmethod
    def _extract_skip_reason(report: pytest.TestReport) -> str:
        longrepr = getattr(report, "longrepr", None)
        if not longrepr:
            return ""
        if isinstance(longrepr, tuple) and len(longrepr) >= 3:
            return str(longrepr[2])
        return str(longrepr)


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("ctreport")
    group.addoption(
        "--ctreport",
        action="store",
        dest="ctreport_path",
        default="",
        help="Write Common Test Report Format (CTRF) JSON to the given path.",
    )


def pytest_configure(config: pytest.Config) -> None:
    option = config.getoption("ctreport_path")
    if option:
        plugin = CTRFPlugin(Path(option))
        config._ctreport_plugin = plugin  # type: ignore[attr-defined]
        config.pluginmanager.register(plugin, "ctreport-plugin")


def pytest_unconfigure(config: pytest.Config) -> None:
    plugin = getattr(config, "_ctreport_plugin", None)
    if plugin is not None:
        config.pluginmanager.unregister(plugin)
        delattr(config, "_ctreport_plugin")
