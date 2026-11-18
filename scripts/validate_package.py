"""Check the public Skill package without network access or dependencies."""

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

NAME = "tripo-studio-mcp"
SKILL = Path("skills") / NAME
MARKETPLACES = (
    ".agents/plugins/marketplace.json",
    ".claude-plugin/marketplace.json",
    ".cursor-plugin/marketplace.json",
)
PUBLIC_HOSTS = {"studio.tripo3d.ai", "www.tripo3d.ai", "gltf-transform.dev",
                "agent-plugins.org", "github.com"}
INTERNAL = re.compile(
    r"feishu\.cn|larksuite\.com|devops\.tripo3d\.ai|vast-internal\.com|"
    r"\b(?:env-forrest-mcp|env-creation|env-base)\b|\.svc\.cluster\.local|"
    r"github\.com[:/]vast-enterprise(?:/|\b)",
    re.IGNORECASE,
)
LINK = re.compile(r"\]\(<?([^\s)>]+)>?(?:\s+[\"'][^)]*[\"'])?\)")
URL = re.compile(r"(?:https?://|(?<!:)//)[^\s<>\"'`\)\]]+", re.IGNORECASE)


def validate(root):
    errors = []

    def problem(path, message):
        errors.append(f"{path}: {message}")

    def manifest(path):
        try:
            value = json.loads((root / path).read_text())
            if isinstance(value, dict):
                return value
        except (OSError, ValueError):
            pass
        problem(path, "expected a readable JSON object")
        return {}

    versions = set()
    for path in ("plugin.json", ".claude-plugin/plugin.json", ".cursor-plugin/plugin.json"):
        data = manifest(path)
        if data.get("name") != NAME or not isinstance(data.get("description"), str) or not data["description"].strip():
            problem(path, "expected the shared plugin name and a description")
        version = data.get("version")
        if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
            problem(path, "expected a release version such as 0.1.0")
        else:
            versions.add(version)
        if path.startswith(".cursor-plugin") and data.get("skills") != [f"./{SKILL}"]:
            problem(path, "expected the shared Skill path")
        if any(key in data for key in ("mcp", "mcpServers", "apps")):
            problem(path, "keep MCP connection configuration outside the public package")
    if len(versions) > 1:
        problem("plugin manifests", "versions differ")

    for path in MARKETPLACES:
        data = manifest(path)
        source = {"source": "local", "path": "./"} if path.startswith(".agents/") else "./"
        entries = data.get("plugins")
        if (data.get("name") != "tripo-studio" or not isinstance(entries, list)
                or len(entries) != 1 or not isinstance(entries[0], dict)
                or entries[0].get("name") != NAME or entries[0].get("source") != source):
            problem(path, "expected one marketplace entry pointing to the root plugin")

    entry = root / SKILL / "SKILL.md"
    try:
        text = entry.read_text()
        frontmatter = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
        if (not frontmatter or not re.search(rf"^name: {NAME}$", frontmatter[1], re.MULTILINE)
                or not re.search(r"^description: +\S", frontmatter[1], re.MULTILINE)):
            problem(entry.relative_to(root), "expected Skill name and description in frontmatter")
    except OSError:
        problem(entry.relative_to(root), "missing Skill entry point")

    for name in ("mcp.json", ".mcp.json", ".app.json"):
        if (root / name).exists():
            problem(name, "keep MCP connection configuration outside the public package")

    paths = [root / name for name in ("README.md", "INSTALL.md", "plugin.json", *MARKETPLACES,
             ".claude-plugin/plugin.json", ".cursor-plugin/plugin.json")]
    paths.extend(p for p in (root / SKILL).rglob("*") if p.is_file() or p.is_symlink())
    for path in paths:
        relative = path.relative_to(root)
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            problem(relative, "package files must stay inside the repository")
            continue
        try:
            text = path.read_text()
        except (OSError, UnicodeError):
            problem(relative, "expected a readable text file")
            continue
        if INTERNAL.search(unquote(text)):
            problem(relative, "contains an internal link or test environment identifier")
        for raw in URL.findall(text):
            try:
                url = urlsplit(raw)
                github_repo = url.path.lower().split("/")[1:3]
                allowed = (url.scheme == "https" and url.hostname in PUBLIC_HOSTS
                           and not (url.username or url.password or url.port)
                           and (url.hostname != "github.com" or github_repo in (
                               ["tripo-developer", "tripo-studio-mcp"],
                               ["tripo-developer", "tripo-studio-mcp.git"],
                           )))
            except ValueError:
                allowed = False
            if not allowed:
                problem(relative, "uses a URL outside the approved public destinations")
        if path.suffix != ".md":
            continue
        for raw in LINK.findall(text):
            url = urlsplit(raw)
            if url.scheme or url.netloc:
                if url.scheme not in ("https", "mailto"):
                    problem(relative, "unsupported link scheme")
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            boundary = root / SKILL if path.is_relative_to(root / SKILL) else root
            if not target.is_relative_to(boundary) or not target.exists():
                problem(relative, f"missing or out-of-package reference {raw}")
            elif url.fragment and target.is_file() and target.suffix == ".md":
                headings = re.findall(r"^#{1,6}\s+(.+)$", target.read_text(), re.MULTILINE)
                anchors = {re.sub(r"[^\w -]", "", heading.lower()).replace(" ", "-")
                           for heading in headings}
                if unquote(url.fragment) not in anchors:
                    problem(relative, f"missing heading reference {raw}")
    return errors


if __name__ == "__main__":
    root = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]).resolve()
    errors = validate(root)
    if errors:
        sys.exit("\n".join(errors))
    print("Public Skill package checks passed")
