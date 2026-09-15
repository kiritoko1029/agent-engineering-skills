#!/usr/bin/env python3
"""Validate this repository's constrained skill format and local Markdown links.

This is deliberately not a general YAML parser or an external-link checker.
Frontmatter contains exactly name and description as single-line plain strings
or JSON-compatible double-quoted strings. Python 3.10+, standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


NAME_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
GENERATED_TODO_RE = re.compile(
    r"\{\{\s*TODO(?:[:\s][^}\n]*)?\}\}|<TODO(?:[:\s][^>\n]*)?>"
    r"|<!--\s*TODO(?:[:\s][\s\S]*?)?-->",
    re.IGNORECASE,
)
LINK_RE = re.compile(
    r"!?\[[^\n]*?\]\(\s*(<[^>\n]+>|(?:\\.|[^()\s]|\([^()\n]*\))+)"
    r"(?:\s+[\"'][^\n]*?[\"'])?\s*\)"
)
REFERENCE_RE = re.compile(r"^ {0,3}\[[^]\n]+\]:\s*(<[^>\n]+>|\S+)", re.MULTILINE)
SCRIPT_RE = re.compile(r"`(scripts/[A-Za-z0-9_./-]+\.py)`")


def valid_name(name: str) -> bool:
    return len(name) < 64 and NAME_RE.fullmatch(name) is not None


def read_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("SKILL.md must begin with a frontmatter delimiter (---)")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("frontmatter is missing its closing delimiter") from exc
    values: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.fullmatch(r"(name|description):[ \t]*(.+)", line)
        if not match:
            raise ValueError("frontmatter supports only name/description single-line strings")
        key, value = match.groups()
        value = value.strip()
        if key in values:
            raise ValueError(f"duplicate frontmatter field: {key}")
        if value.startswith('"'):
            try:
                value = json.loads(value)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{key}: invalid double-quoted string") from exc
        elif value.startswith(("'", "[", "{", "|", ">", "&", "*", "!", "#")):
            raise ValueError(f"{key}: use a plain string or a double-quoted string")
        elif " #" in value or ": " in value:
            raise ValueError(f"{key}: quote values containing YAML comments or colon-space")
        elif value.lower() in {"null", "true", "false", "~"} or re.fullmatch(r"[-+]?\d+(?:\.\d+)?", value):
            raise ValueError(f"{key}: expected a string, not another scalar type")
        if not isinstance(value, str) or not value.strip() or "\n" in value or "\r" in value:
            raise ValueError(f"{key}: expected a nonempty single-line string")
        values[key] = value
    if set(values) != {"name", "description"}:
        raise ValueError("frontmatter requires both name and description")
    return values


def validate_skill(folder: Path) -> list[str]:
    errors: list[str] = []
    if not valid_name(folder.name):
        errors.append(f"{folder}: skill name must be kebab-case and shorter than 64 characters")
    entry = folder / "SKILL.md"
    if not entry.is_file():
        return errors + [f"{folder}: missing SKILL.md"]
    try:
        fields = read_frontmatter(entry)
        if fields["name"] != folder.name:
            errors.append(f"{entry}: frontmatter name must match folder name {folder.name!r}")
    except (OSError, UnicodeError, ValueError) as exc:
        errors.append(f"{entry}: {exc}")
    return errors


def without_fenced_code(content: str) -> str:
    """Mask fenced examples so illustrative links are not treated as live links."""
    result = []
    fence_char = ""
    fence_size = 0
    for line in content.splitlines(keepends=True):
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\r\n"))
        if not fence_char and match:
            fence_char, fence_size = match[1][0], len(match[1])
            result.append("\n")
        elif fence_char:
            if match and match[1][0] == fence_char and len(match[1]) >= fence_size and not match[2].strip():
                fence_char = ""
            result.append("\n")
        else:
            result.append(line)
    return "".join(result)


def local_link_error(repo: Path, document: Path, destination: str) -> str | None:
    destination = destination.strip("<>")
    destination = re.sub(r"\\([ ()])", r"\1", destination)
    if destination.startswith("#"):
        return None
    try:
        parsed = urlsplit(destination)
    except ValueError:
        return f"invalid link destination: {destination}"
    if parsed.scheme.lower() in {"http", "https", "mailto"}:
        return None
    if parsed.scheme or parsed.netloc:
        return f"unsupported link scheme: {destination}"
    local_path = unquote(parsed.path)
    if not local_path:
        return None
    if Path(local_path).is_absolute() or local_path.startswith(("/", "\\")):
        return f"local links must be relative to the document: {destination}"
    target = (document.parent / local_path).resolve()
    if not target.is_relative_to(repo):
        return f"local link escapes repository: {destination}"
    if not target.exists():
        return f"broken local link: {destination}"
    return None


def validate_codex_plugin(repo: Path) -> list[str]:
    """Check this repository's single-plugin layout, not the full Codex schema."""
    errors: list[str] = []
    documents = []
    for relative in (".codex-plugin/plugin.json", ".agents/plugins/marketplace.json"):
        try:
            document = json.loads((repo / relative).read_text(encoding="utf-8"))
            if not isinstance(document, dict):
                raise ValueError("expected a JSON object")
            documents.append(document)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"{relative}: {exc}")
    if errors:
        return errors
    manifest, marketplace = documents
    name = "agent-engineering-skills"
    if manifest.get("name") != name or marketplace.get("name") != name:
        errors.append("Codex plugin and marketplace names must be agent-engineering-skills")
    if not isinstance(manifest.get("version"), str) or not re.fullmatch(
        r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", manifest["version"]
    ):
        errors.append("Codex plugin version must be a stable major.minor.patch release")
    if manifest.get("skills") != "./skills/" or not (repo / "skills").is_dir():
        errors.append("Codex plugin skills must point to ./skills/")
    for field in ("apps", "mcpServers", "hooks"):
        if field in manifest:
            errors.append(f"skills-only Codex plugin must not declare {field}")
    expected = [{
        "name": name,
        "source": {"source": "local", "path": "./"},
        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        "category": "Productivity",
    }]
    if marketplace.get("plugins") != expected:
        errors.append("Codex marketplace must expose the repository root as one available local plugin")
    return errors


def validate_zcode_plugin(repo: Path) -> list[str]:
    """Check this repository's single-plugin ZCode layout, not the full ZCode schema."""
    errors: list[str] = []
    documents = []
    for relative in (".zcode-plugin/plugin.json", "marketplace.json"):
        try:
            document = json.loads((repo / relative).read_text(encoding="utf-8"))
            if not isinstance(document, dict):
                raise ValueError("expected a JSON object")
            documents.append(document)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"{relative}: {exc}")
    if errors:
        return errors
    manifest, marketplace = documents
    name = "agent-engineering-skills"
    if manifest.get("name") != name or marketplace.get("name") != name:
        errors.append("ZCode plugin and marketplace names must be agent-engineering-skills")
    if not isinstance(manifest.get("version"), str) or not re.fullmatch(
        r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", manifest["version"]
    ):
        errors.append("ZCode plugin version must be a stable major.minor.patch release")
    if manifest.get("skills") != "skills" or not (repo / "skills").is_dir():
        errors.append("ZCode plugin skills must point to skills/")
    for field in ("commands", "agents", "hooks", "mcpServers"):
        if field in manifest:
            errors.append(f"skills-only ZCode plugin must not declare {field}")
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1 or not isinstance(plugins[0], dict):
        return errors + ["ZCode marketplace must expose the repository root as one local plugin"]
    entry = plugins[0]
    if entry.get("name") != name or entry.get("source") != "./":
        errors.append("ZCode marketplace must expose the repository root as one local plugin")
    if entry.get("version") != manifest.get("version"):
        errors.append("ZCode marketplace version must match the plugin manifest for update detection")
    return errors


def validate_repository(repo: Path) -> list[str]:
    repo = repo.resolve()
    errors: list[str] = validate_codex_plugin(repo) + validate_zcode_plugin(repo)
    skills_dir = repo / "skills"
    folders = sorted(path for path in skills_dir.iterdir() if path.is_dir()) if skills_dir.is_dir() else []
    if not folders:
        errors.append(f"{skills_dir}: expected at least one skill directory")
    for folder in folders:
        errors.extend(validate_skill(folder))
    for document in sorted(repo.rglob("*.md")):
        if any(part in {".git", ".venv", "node_modules"} for part in document.relative_to(repo).parts):
            continue
        try:
            content = document.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{document}: {exc}")
            continue
        # Explicit generated TODO markers remain invalid even inside examples.
        if GENERATED_TODO_RE.search(content):
            errors.append(f"{document}: unresolved generated TODO marker")
        prose = without_fenced_code(content)
        for script in SCRIPT_RE.findall(prose):
            # Skill instructions use paths relative to their own directory;
            # repository guides may instead show commands from the repo root.
            error = local_link_error(repo, document, script)
            if error:
                error = local_link_error(repo, repo / "README.md", script)
            if error:
                errors.append(f"{document}: script reference: {error}")
        prose = re.sub(r"(`+).*?\1", "", prose)
        destinations = [match[1] for match in LINK_RE.finditer(prose)]
        destinations.extend(match[1] for match in REFERENCE_RE.finditer(prose))
        for destination in destinations:
            error = local_link_error(repo, document, destination)
            if error:
                errors.append(f"{document}: {error}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="repository to validate")
    args = parser.parse_args()
    errors = validate_repository(args.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"Validation failed: {len(errors)} issue(s).")
        return 1
    print("Validation passed: Codex and ZCode plugin layouts, skill metadata, explicit TODO markers, and local Markdown links.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
