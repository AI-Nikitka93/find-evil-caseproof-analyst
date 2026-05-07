from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
PUBLIC_REPO_URL = "https://github.com/AI-Nikitka93/find-evil-caseproof-analyst"
REQUIRED_FILES = (
    "README.md",
    "LICENSE",
    "docs/architecture.md",
    "docs/dataset_documentation.md",
    "docs/accuracy_report.md",
    "docs/judge_try_it_out.md",
    "docs/final_submission_package.md",
    "docs/demo_video_script.md",
    "docs/demo_narration_notes.md",
    "docs/public_real_execution_log_sample.jsonl",
    "docs/public_real_traceability_packet.md",
    "docs/reviewer_traceability_walkthrough.md",
    "scripts/demo_rehearsal.py",
)
SUPPORTED_VIDEO_HOST_MARKERS = (
    "youtube.com",
    "youtu.be",
    "vimeo.com",
    "youku.com",
)


@dataclass(frozen=True, slots=True)
class GateStatus:
    ok: bool
    detail: str


@dataclass(frozen=True, slots=True)
class GitSyncStatus:
    ok: bool
    detail: str


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _run_git(root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )


def get_git_sync_status(root: Path = PROJECT_ROOT) -> GitSyncStatus:
    if not (root / ".git").exists():
        return GitSyncStatus(ok=False, detail="not a git checkout")

    status = _run_git(root, ["status", "--short"])
    if status.returncode != 0:
        return GitSyncStatus(ok=False, detail=(status.stderr or status.stdout).strip() or "git status failed")
    if status.stdout.strip():
        return GitSyncStatus(ok=False, detail="dirty working tree")

    upstream = _run_git(root, ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"])
    if upstream.returncode != 0:
        return GitSyncStatus(ok=False, detail="no upstream branch configured")

    divergence = _run_git(root, ["rev-list", "--left-right", "--count", "HEAD...@{u}"])
    if divergence.returncode != 0:
        return GitSyncStatus(ok=False, detail=(divergence.stderr or divergence.stdout).strip() or "git divergence check failed")
    parts = divergence.stdout.strip().split()
    if len(parts) != 2:
        return GitSyncStatus(ok=False, detail=f"unexpected divergence output: {divergence.stdout.strip()}")
    ahead, behind = (int(parts[0]), int(parts[1]))
    if ahead or behind:
        return GitSyncStatus(ok=False, detail=f"branch not synced with upstream: ahead={ahead}, behind={behind}")

    remote = _run_git(root, ["remote", "get-url", "origin"])
    if remote.returncode != 0 or PUBLIC_REPO_URL not in remote.stdout.strip().removesuffix(".git"):
        return GitSyncStatus(ok=False, detail="origin is not the expected public repository")

    return GitSyncStatus(ok=True, detail=f"clean and synced with {upstream.stdout.strip()}")


def is_supported_video_url(value: str | None) -> bool:
    if not value:
        return False
    if value.strip().upper() == "DEMO_VIDEO_URL":
        return False
    parsed = urlparse(value.strip())
    if parsed.scheme != "https" or not parsed.netloc:
        return False
    host = parsed.netloc.lower()
    return any(marker in host for marker in SUPPORTED_VIDEO_HOST_MARKERS)


def _is_devpost_url(value: str | None) -> bool:
    if not value:
        return False
    parsed = urlparse(value.strip())
    return parsed.scheme == "https" and parsed.netloc.lower().endswith("devpost.com") and bool(parsed.path.strip("/"))


def _check_required_files(root: Path) -> GateStatus:
    missing = [path for path in REQUIRED_FILES if not (root / path).is_file()]
    if missing:
        return GateStatus(ok=False, detail="missing: " + ", ".join(missing))
    return GateStatus(ok=True, detail="all required submission files exist")


def _check_public_repo_links(root: Path) -> GateStatus:
    surfaces = ("README.md", "docs/final_submission_package.md")
    missing = [path for path in surfaces if PUBLIC_REPO_URL not in _read(root / path)]
    if missing:
        return GateStatus(ok=False, detail="missing public repo URL in: " + ", ".join(missing))
    return GateStatus(ok=True, detail="public repository URL is linked from README and final submission package")


def _check_license(root: Path) -> GateStatus:
    text = _read(root / "LICENSE") if (root / "LICENSE").is_file() else ""
    if "MIT License" not in text:
        return GateStatus(ok=False, detail="LICENSE is missing MIT License text")
    return GateStatus(ok=True, detail="MIT license is present")


def _check_public_trace(root: Path) -> GateStatus:
    path = root / "docs" / "public_real_execution_log_sample.jsonl"
    if not path.is_file():
        return GateStatus(ok=False, detail="public real execution log sample is missing")
    tools: set[str] = set()
    has_correction = False
    for index, line in enumerate(_read(path).splitlines(), start=1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            return GateStatus(ok=False, detail=f"invalid JSONL line {index}")
        tools.add(str(payload.get("tool_name", "")))
        has_correction = has_correction or bool(payload.get("correction_reason"))
    required = {"case_open_readonly", "verify_claim"}
    missing = sorted(required - tools)
    if missing:
        return GateStatus(ok=False, detail="public trace missing tools: " + ", ".join(missing))
    if not has_correction:
        return GateStatus(ok=False, detail="public trace has no visible self-correction reason")
    return GateStatus(ok=True, detail="public trace includes evidence opening and self-correction")


def _check_demo_rehearsal_assets(root: Path) -> GateStatus:
    from scripts.demo_rehearsal import build_demo_rehearsal_report

    report = build_demo_rehearsal_report(root=root, case_id="CASE-RD01")
    if report["status"] != "ready":
        return GateStatus(ok=False, detail="demo rehearsal blocked: " + ", ".join(report["blockers"]))
    return GateStatus(ok=True, detail="demo rehearsal assets prove real evidence, artifact depth, and self-correction")


def _check_required_markdown_links(root: Path) -> GateStatus:
    surfaces = (
        "README.md",
        "docs/final_submission_package.md",
        "docs/judge_try_it_out.md",
        "docs/reviewer_traceability_walkthrough.md",
    )
    broken: list[str] = []
    link_pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    for surface in surfaces:
        path = root / surface
        if not path.is_file():
            broken.append(f"{surface}:missing_surface")
            continue
        for match in link_pattern.finditer(_read(path)):
            target = match.group(1).strip().strip("<>")
            if not target or target.startswith("#") or "://" in target or target.startswith("mailto:"):
                continue
            target_path = (path.parent / target.split("#", 1)[0]).resolve()
            try:
                target_path.relative_to(root.resolve())
            except ValueError:
                broken.append(f"{surface}:{target}")
                continue
            if not target_path.exists():
                broken.append(f"{surface}:{target}")
    if broken:
        return GateStatus(ok=False, detail="broken local markdown links: " + ", ".join(broken[:10]))
    return GateStatus(ok=True, detail="required README/submission/runbook markdown links resolve locally")


def build_final_submission_audit(
    *,
    root: Path = PROJECT_ROOT,
    demo_video_url: str | None = None,
    devpost_url: str | None = None,
    git_status: GitSyncStatus | None = None,
) -> dict[str, Any]:
    git_status = git_status if git_status is not None else get_git_sync_status(root)

    local_gates = {
        "required_files": _check_required_files(root),
        "public_repo_links": _check_public_repo_links(root),
        "license": _check_license(root),
        "public_trace": _check_public_trace(root),
        "demo_rehearsal_assets": _check_demo_rehearsal_assets(root),
        "required_markdown_links": _check_required_markdown_links(root),
        "public_repo_sync": GateStatus(ok=git_status.ok, detail=git_status.detail),
    }
    external_gates = {
        "demo_video_url": GateStatus(
            ok=is_supported_video_url(demo_video_url),
            detail="supported public video URL is present" if is_supported_video_url(demo_video_url) else "missing YouTube, Vimeo, or Youku URL",
        ),
        "devpost_url": GateStatus(
            ok=_is_devpost_url(devpost_url),
            detail="Devpost project URL is present" if _is_devpost_url(devpost_url) else "missing submitted Devpost project URL",
        ),
    }
    blockers = [name for name, gate in {**local_gates, **external_gates}.items() if not gate.ok]
    total = len(local_gates) + len(external_gates)
    score = round(100 * (total - len(blockers)) / total)
    return {
        "status": "ready" if not blockers else "blocked",
        "score": score,
        "blockers": blockers,
        "local_gates": {name: asdict(gate) for name, gate in local_gates.items()},
        "external_gates": {name: asdict(gate) for name, gate in external_gates.items()},
        "public_repo_url": PUBLIC_REPO_URL,
        "supported_video_hosts": list(SUPPORTED_VIDEO_HOST_MARKERS),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit final FIND EVIL submission readiness.")
    parser.add_argument("--demo-video-url", default=None, help="Public YouTube, Vimeo, or Youku URL.")
    parser.add_argument("--devpost-url", default=None, help="Submitted Devpost project URL.")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report = build_final_submission_audit(demo_video_url=args.demo_video_url, devpost_url=args.devpost_url)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=True))
    else:
        print(f"Final submission status: {report['status']} ({report['score']}/100)")
        for group_name in ("local_gates", "external_gates"):
            print(group_name + ":")
            for name, gate in report[group_name].items():
                marker = "PASS" if gate["ok"] else "BLOCK"
                print(f"  {marker:5} {name} - {gate['detail']}")
    if args.strict and report["status"] != "ready":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
