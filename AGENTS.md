# Instructions for coding agents

This public repository is the MIT-licensed thin integration for Façade. Maintain
shared photographic workflows in `skills/`, host presentation notes in `hosts/`,
setup/compatibility guidance in `docs/`, and the standard-library package builder
in `facade_plugin/`. These are the canonical sources; do not edit generated or
installed packages and do not introduce per-host copies of the shared workflow.

The separate application owns photo processing, MCP server implementation,
project storage, reference databases, runtime installation/lifecycle, models and
the macOS UI. Do not copy those implementations, private documents, credentials,
user photographs or private Git history into this repository. Do not add an
internal agent loop or a host-specific editing engine. MIT applies to this
repository; it does not license the separate application or model weights.

The public prototype currently supports Codex and Cursor on macOS. Other hosts
are planned; the presence of a Claude adapter does not establish public support.
Keep README short: WIP, supported platforms/hosts, no public download yet, and
the project/demo website. Keep technical details in this file and `docs/`.

When checked out as `plugins/facade-plugin` in the private application, commit
changes here, then update the parent's gitlink with related integration changes.
Push this commit before a parent commit that references it. The parent freezes
this package and its resources into the app; maintain checkout, wheel and frozen
asset layouts. Preserve LICENSE in wheels, source archives and every generated
host package. No live host installation is required to test package generation.

Run `python -m unittest discover -s tests` from this repository with Python 3.12+
and this package installed (editable is fine). For packaging changes, also build
and inspect the wheel; in the containing application use its focused packaging
tests. By owner decision (29 October 2026), the thin package, source manifests
and application share one release version. Bump them together even when only
one repository changes; coordinate the matching application dependency/lockfile.
Generated host plugin versions come from that same backend version. Bump PACKAGE_FORMAT_VERSION
when generated package structure changes and coordinate the parent's dependency.

Before publishing any new photographs or third-party assets, establish permission
for that use; a local file or reference entry alone is not publication permission.
