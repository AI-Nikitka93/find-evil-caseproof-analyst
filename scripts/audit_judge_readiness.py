from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.judge_readiness import build_judge_readiness_report, render_judge_readiness_markdown
from scripts.final_submission_audit import GitSyncStatus


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit FIND EVIL judge-criterion readiness.")
    parser.add_argument("--demo-video-url", default=None, help="Public YouTube, Vimeo, or Youku URL.")
    parser.add_argument("--devpost-url", default=None, help="Submitted Devpost project URL.")
    parser.add_argument("--write-doc", action="store_true", help="Write docs/judge_max_readiness_report.md.")
    parser.add_argument(
        "--assume-public-repo-sync",
        action="store_true",
        help="Generate the report for the post-commit/post-push package while final_submission_audit still verifies git state independently.",
    )
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    git_status = GitSyncStatus(ok=True, detail="assumed clean and synced after commit/push") if args.assume_public_repo_sync else None
    report = build_judge_readiness_report(
        root=PROJECT_ROOT,
        demo_video_url=args.demo_video_url,
        devpost_url=args.devpost_url,
        git_status=git_status,
    )
    if args.write_doc:
        output_path = PROJECT_ROOT / "docs" / "judge_max_readiness_report.md"
        output_path.write_text(render_judge_readiness_markdown(report), encoding="utf-8")
        report = build_judge_readiness_report(
            root=PROJECT_ROOT,
            demo_video_url=args.demo_video_url,
            devpost_url=args.devpost_url,
            git_status=git_status,
        )
        output_path.write_text(render_judge_readiness_markdown(report), encoding="utf-8")

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=True))
    else:
        summary = report["criterion_score_summary"]
        print(f"Judge readiness status: {report['status']} ({summary['total']}/{summary['max_total']})")
        for criterion, score in summary["scores"].items():
            print(f"  {criterion}: {score}/17")
        if report["submission_gate"]["blockers"]:
            print("External blockers: " + ", ".join(report["submission_gate"]["blockers"]))

    if args.strict and not report["criterion_score_summary"]["all_criteria_at_17"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
