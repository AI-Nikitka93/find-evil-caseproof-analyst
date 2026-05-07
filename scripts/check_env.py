from __future__ import annotations

import argparse
import json
import os
import subprocess
import shutil
import sys
from dataclasses import asdict, dataclass
from typing import Any


REQUIRED_SIFT_BINARIES = ("mmls", "fls", "icat", "log2timeline.py", "psort.py", "rip.pl")
TOOL_ALIASES = {
    "rip.pl": ("rip.pl", "regripper"),
}
DEFAULT_WSL_DISTRO = "Ubuntu"
OPTIONAL_API_ENV_VARS = {
    "FIND_EVIL_AGENT_PROVIDER": "Optional AI runtime selector: auto, groq, openrouter, or anthropic.",
    "ANTHROPIC_API_KEY": "Implemented Anthropic runtime for src.agent.",
    "ANTHROPIC_MODEL": "Optional Anthropic model override for src.agent.",
    "GOOGLE_API_KEY": "Candidate Gemini runtime key if a Gemini adapter is added.",
    "GEMINI_MODEL": "Optional Gemini model override for a future adapter.",
    "GROQ_API_KEY": "Implemented Groq free-plan runtime key for src.agent.",
    "GROQ_MODEL": "Optional Groq model override.",
    "OPENROUTER_API_KEY": "Implemented OpenRouter free or low-cost runtime key for src.agent.",
    "OPENROUTER_MODEL": "Optional OpenRouter model override.",
    "OPENAI_API_KEY": "Candidate OpenAI Responses runtime key if an adapter is added.",
    "OPENAI_MODEL": "Optional OpenAI model override for a future adapter.",
    "MCP_SERVER_COMMAND": "Python launcher used by src.agent to start python -m src.server.",
}
LOCAL_ENV_FILE = ".env.local"


@dataclass(slots=True)
class BinaryCheck:
    name: str
    found: bool
    path: str | None
    runtime: str = "native"


@dataclass(slots=True)
class EnvVarCheck:
    name: str
    configured: bool
    valid: bool
    purpose: str


def _candidate_names(name: str) -> tuple[str, ...]:
    return TOOL_ALIASES.get(name, (name,))


def _find_native_binary(name: str) -> str | None:
    for candidate in _candidate_names(name):
        found = shutil.which(candidate)
        if found:
            return found
    return None


def _find_wsl_binary(name: str, distro: str) -> str | None:
    if not shutil.which("wsl"):
        return None
    for candidate in _candidate_names(name):
        try:
            result = subprocess.run(
                ["wsl", "-d", distro, "--", "sh", "-lc", f"command -v {candidate}"],
                capture_output=True,
                text=True,
                check=False,
                encoding="utf-8",
                errors="replace",
                timeout=30,
            )
        except subprocess.TimeoutExpired:
            continue
        found = result.stdout.strip().splitlines()
        if result.returncode == 0 and found:
            return f"wsl:{distro}:{found[0]}"
    return None


def check_binary(name: str) -> BinaryCheck:
    runtime = os.environ.get("FIND_EVIL_TOOL_RUNTIME", "auto").strip().lower() or "auto"
    distro = os.environ.get("FIND_EVIL_WSL_DISTRO", DEFAULT_WSL_DISTRO).strip() or DEFAULT_WSL_DISTRO

    native_path = _find_native_binary(name)
    if native_path:
        return BinaryCheck(name=name, found=True, path=native_path, runtime="native")
    if runtime in {"auto", "wsl"}:
        wsl_path = _find_wsl_binary(name, distro)
        if wsl_path:
            return BinaryCheck(name=name, found=True, path=wsl_path, runtime="wsl")
    return BinaryCheck(name=name, found=False, path=None, runtime=runtime)


def check_env_var(name: str, purpose: str) -> EnvVarCheck:
    value = os.environ.get(name)
    configured = bool(value)
    valid = False
    if value:
        try:
            value.encode("ascii")
            valid = not any(character.isspace() for character in value)
        except UnicodeEncodeError:
            valid = False
    return EnvVarCheck(name=name, configured=configured, valid=valid, purpose=purpose)


def load_local_env_file(path: str = LOCAL_ENV_FILE) -> None:
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and value and key not in os.environ:
                os.environ[key] = value


def build_environment_report() -> dict[str, Any]:
    load_local_env_file()
    binaries = [check_binary(name) for name in REQUIRED_SIFT_BINARIES]
    api_env = [check_env_var(name, purpose) for name, purpose in OPTIONAL_API_ENV_VARS.items()]
    missing_required = [item.name for item in binaries if not item.found]
    runtime = "blocked"
    found_runtimes = {item.runtime for item in binaries if item.found}
    if not missing_required:
        runtime = "wsl" if found_runtimes == {"wsl"} else "native"
    agent_provider_ready = any(
        item.name in {"GROQ_API_KEY", "OPENROUTER_API_KEY", "ANTHROPIC_API_KEY"} and item.configured and item.valid
        for item in api_env
    )
    return {
        "status": "ok" if not missing_required else "blocked",
        "tool_runtime": runtime,
        "required_sift_binaries": [asdict(item) for item in binaries],
        "missing_required_sift_binaries": missing_required,
        "api_environment": [asdict(item) for item in api_env],
        "secrets_redacted": True,
        "ready_for_real_sift_run": not missing_required and agent_provider_ready,
    }


def _print_text_report(report: dict[str, Any]) -> None:
    print(f"Environment status: {report['status']}")
    print("Required SIFT binaries:")
    for item in report["required_sift_binaries"]:
        marker = "FOUND" if item["found"] else "MISSING"
        path = item["path"] or "-"
        print(f"  {marker:7} {item['name']} {path}")
    print("API environment:")
    for item in report["api_environment"]:
        marker = "SET" if item["configured"] else "missing"
        print(f"  {marker:7} {item['name']} - {item['purpose']}")
    print(f"Ready for real SIFT run: {report['ready_for_real_sift_run']}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check FIND EVIL local runtime prerequisites.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    parser.add_argument("--strict", action="store_true", help="Return non-zero when required SIFT binaries are missing.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report = build_environment_report()
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=True))
    else:
        _print_text_report(report)
    if args.strict and report["missing_required_sift_binaries"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
