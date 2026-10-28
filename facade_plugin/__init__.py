#!/usr/bin/env python3
"""Generate thin local packages from one skill and one runtime path."""
import json

import os
from pathlib import Path
import shutil
import shlex

# Bump when generated package structure changes. Included in lifecycle release IDs.
# 4: Cursor mcp.json uses the absolute runtime path. Cursor 3.26 resolves a
# relative command from the workspace and does not apply cwd ${CURSOR_PLUGIN_ROOT}.
# 5: public homepage and Codex listing website metadata.
# 6: standalone thin-layer package, shared setup skill and installation docs.
# 7: carry the MIT license with every generated host package.
PACKAGE_FORMAT_VERSION = 7
PLUGIN_WEBSITE = "https://facade.pictures"
PLUGIN_ICON = "./skills/facade-photo-editor/assets/facade.png"

def asset_root() -> Path:
    """Resolve canonical checkout assets or self-contained wheel/frozen assets."""
    module = Path(__file__).resolve().parent
    checkout = module.parent
    root = checkout if (checkout / "pyproject.toml").is_file() and (checkout / "plugin.json").is_file() else module
    if not (root / "skills/facade-photo-editor/SKILL.md").is_file() or not (root / "hosts/codex.md").is_file():
        raise ValueError("Façade plugin assets are missing; initialize the submodule and reinstall the local dependency")
    return root


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def generate_plugins(executable: Path, output: Path, *, version: str, installed_executable: Path | None = None,
                     library: Path | None = None) -> Path:
    """Validate a staged runtime and optionally target its final published path."""
    executable = executable.expanduser().resolve()
    if not executable.is_file() or not os.access(executable, os.X_OK):
        raise ValueError("executable must be an existing executable")
    if installed_executable is not None:
        executable = installed_executable.expanduser().resolve()
    root = asset_root()
    skills = root / "skills"
    if not (skills / "facade-photo-editor/assets/facade.png").is_file():
        raise ValueError("Bundled Façade plugin icon is missing")
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    identity = {"name": "facade-photo-editor", "version": version,
                "description": "Persistent local photo editing with previews, masks and PSD export.",
                "author": {"name": "Façade"}, "homepage": PLUGIN_WEBSITE, "license": "MIT"}
    mcp = {"mcpServers": {"facade": {"command": str(executable), "args": ["mcp"]}}}
    environment = {"FACADE_LIBRARY": str(library.resolve())} if library is not None else {}
    if environment:
        mcp["mcpServers"]["facade"]["env"] = environment
    for host in ("codex", "claude"):
        folder = output / host
        shutil.copytree(skills, folder / "skills")
        shutil.copytree(root / "docs", folder / "docs")
        shutil.copy2(root / "LICENSE", folder / "LICENSE")
        manifest = dict(identity)
        if host == "codex":
            # Portable Agent Plugins rejects absolute command paths. Ship a
            # contained executable launcher; quote the installed runtime path
            # as shell data, including spaces/apostrophes. Compatibility .mcp
            # below retains its host-supported absolute command contract.
            launcher = folder / "bin/facade-editor"
            launcher.parent.mkdir(parents=True)
            launcher.write_text("#!/bin/sh\nexec " + shlex.quote(str(executable)) + ' "$@"\n')
            launcher.chmod(0o755)
            manifest.update(skills="./skills/", mcpServers="./.mcp.json", requires_local_executor=True,
                            interface={"displayName": "Façade Photo Editor", "shortDescription": "Edit photos with your agent",
                                       "websiteURL": PLUGIN_WEBSITE,
                                       "logo": PLUGIN_ICON, "composerIcon": PLUGIN_ICON})
            write(folder / "plugin.json", {
                "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
                **identity, "extensions": {"com.openai": {
                    "requires_local_executor": True, "interface": manifest["interface"]}}})
            write(folder / "mcp.json", {
                "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
                "mcpServers": {"facade": {"type": "stdio", "command": "./bin/facade-editor", "args": ["mcp"]}}})
            if environment:
                portable = json.loads((folder / "mcp.json").read_text())
                portable["mcpServers"]["facade"]["env"] = environment
                write(folder / "mcp.json", portable)
        else:
            # Anthropic's directory reads icon; Claude Code itself ignores it.
            manifest["icon"] = PLUGIN_ICON
        write(folder / f".{host}-plugin/plugin.json", manifest)
        write(folder / ".mcp.json", mcp)
    cursor = output / "cursor"
    shutil.copytree(output / "codex", cursor)
    # Cursor's documented logo field belongs to its native plugin format,
    # not to the portable schema or the OpenAI-specific extension.
    (cursor / "plugin.json").unlink()
    shutil.rmtree(cursor / ".codex-plugin")
    write(cursor / ".cursor-plugin/plugin.json", {
        **identity, "logo": PLUGIN_ICON, "skills": "./skills/", "mcpServers": "./mcp.json"})
    # Cursor launches mcp.json, not the compatibility .mcp.json. An absolute
    # command is required: a relative launcher is resolved in the workspace.
    write(cursor / "mcp.json", {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
        "mcpServers": {"facade": {"type": "stdio", **mcp["mcpServers"]["facade"]}}})
    if environment:
        portable = json.loads((cursor / "mcp.json").read_text())
        portable["mcpServers"]["facade"]["env"] = environment
        write(cursor / "mcp.json", portable)
    for host in ("codex", "cursor", "claude"):
        skill = output / host / "skills/facade-photo-editor"
        shutil.copy2((root / "hosts") / f"{host}.md", skill / "host.md")
        entry = skill / "SKILL.md"
        entry.write_text(entry.read_text() + "\n## Host presentation\n\nRead [host instructions](host.md) for this host’s image display and user annotations.\n")
    write(output / ".agents/plugins/marketplace.json", {
        "name": "facade-local", "interface": {"displayName": "Façade local"},
        "plugins": [{"name": identity["name"], "source": {"source": "local", "path": "./codex"},
                     "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}, "category": "Productivity"}]})
    write(output / ".claude-plugin/marketplace.json", {
        "name": "facade-local", "description": "Local Façade photo editor integration", "owner": {"name": "Façade"},
        "plugins": [{"name": identity["name"], "source": "./claude", "description": identity["description"]}]})
    return output
