---
name: facade-setup
description: Help install or reconnect the separate local Façade photo editor when the user asks for setup or Façade MCP tools are missing. Explains installation; use the photographic skill for edits.
---

Explain that Façade requires a separate local macOS backend. Check the tools
actually available in this chat first. If a Façade capabilities tool is present,
use its compact read-only response to confirm that the connection responds.
Do not create a project, render a photograph or launch another MCP process to
test setup. Use the installed photographic skill for subsequent editing.

If the tools are absent, read [installation](../../docs/installation.md). Direct
the user to [facade.pictures](https://facade.pictures) for official availability
and download information. Do not invent a release URL or claim a signed release
exists without checking. If no public release is available, explain that setup
must wait for an approved release.

For an existing installation, use the app's Help/support context to obtain the
exact runtime path and version. If local command execution is available, invoke
that known executable with the single `doctor` argument as a read-only check.
Do not search the whole disk, choose the newest directory by sorting version
names, run a downloader, modify PATH or rewrite host configuration. A failed
doctor or missing executable is a setup problem, not permission to rebuild the
backend from source.

Use the app's documented connection flow with the user's authorization. Honor
authorization already given; do not ask twice. Keep existing connections until
the replacement has been reviewed. Explain any required reload/new chat and
verify the responding tools afterward. A successful doctor does not prove a
live host connection or image display.

Read [compatibility](../../docs/compatibility.md) for host limits. The app generates
MCP launch configuration for its exact runtime; the source repository has no
universal launcher. Do not manufacture configuration or enable duplicate
Façade plugins. In a cloud or isolated execution environment, do not assume a
macOS application on the user's computer is accessible.

Support reports should contain explicit version/error metadata and necessary
paths only. Do not include credentials, host configuration contents, raw logs,
photographs or private project data.
