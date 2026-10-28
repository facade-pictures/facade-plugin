# Installation

This repository is for local development and review. Public installation instructions will be
published after the backend distribution and each host workflow are accepted.

The intended sequence is:

1. Install the Façade agent plugin through a supported host.
2. Ask the agent to check whether Façade tools are available.
3. If the backend is missing, visit [facade.pictures](https://facade.pictures).
   Use only an available official release for the stated macOS and architecture.
   A website link does not establish that a signed download is already available.
4. Install the signed and notarized macOS application when that release exists.
5. Use the application's documented connection flow for the chosen host.
6. Start a new chat or reload the host as instructed, then verify a read-only
   Façade capabilities response before editing a photograph.

Downloads, installation and connection changes need the user's authorization.
This plugin contains no downloader, installer, background service or lifecycle
hook. It must not bypass macOS security checks or overwrite working host settings.

If an exact installed executable is known from the application's support
information, its existing `doctor` command reports the version and dependency
health without downloads. Run that executable directly, with `doctor` as an
argument. Do not assume that a command named `facade` on PATH is the same CLI.

Successful `doctor` output proves neither a host connection nor that previews
are visible to the user. A plugin on disk, a runtime on disk and an active MCP
connection are three separate states. If tools remain unavailable, use the
application's Help/support context and [compatibility](compatibility.md).
