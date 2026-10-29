# Compatibility — local development, 28 October 2026

The shared skills and host-package generator serve Codex, Cursor and Claude
Code. Real-host acceptance is separate from package generation. Cowork's access
to an executable on the macOS host is not established.

The source manifests use Agent Plugins 1.0 and a Claude compatibility overlay.
The root source has no `mcp.json`: portable discovery of an independently
installed backend is still pending. Generated packages contain host-specific
MCP configuration for the exact runtime supplied by the application.

Generated Codex packages use a contained launcher and a portable root manifest;
Cursor packages retain the verified absolute-command workaround and native
manifest. Claude Code packages use their native manifest and `.mcp.json`.
They contain the same editing and setup skills plus the matching host notes.
No code or assets are fetched while generating a package.

Thin-layer version 0.1.3 is separate from the backend version. Generated plugin
versions follow the supplied backend release. A matching generated package does
not prove a live connection or user-visible previews. Future standalone public
plugin releases require explicit backend compatibility and clean-install tests.

OpenAI local MCP submission eligibility and the acceptance of a separate
proprietary backend still need confirmation. This is not a marketplace release.

Sources: [OpenAI packaging](https://developers.openai.com/plugins/build/plugins),
[desktop submissions](https://developers.openai.com/plugins/deploy/desktop-only),
[Cursor reference](https://cursor.com/docs/reference/plugins),
[Claude manifest](https://code.claude.com/docs/en/plugins-reference).
