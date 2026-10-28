# Façade agent plugin

Development source for the thin Façade integration. This repository owns
shared photographic skills, host presentation instructions and the package
builder. The separate Façade application, renderer, project implementation,
models and MCP server are not included.

## Layout

- `skills/facade-photo-editor/`: the shared photographic workflow and references.
- `skills/facade-setup/`: setup guidance that can be read without a running MCP server.
- `hosts/`: small Codex, Cursor and Claude presentation adapters.
- `facade_plugin/`: a standard-library Python package that generates host packages
  for a supplied exact runtime executable and backend version.
- `plugin.json` and `.claude-plugin/plugin.json`: source-level plugin metadata.

This is the single maintained source. A containing private checkout can include
it as a Git submodule and install it as a local Python dependency. A wheel carries
its skills, hosts and documentation; the application can freeze that dependency
without access to this checkout at runtime.

The Python package version describes the thin layer. Generated host manifests
use the supplied backend version so cached instructions stay paired with that
runtime. Building packages does not install, connect or publish them.

The root source package has no universal MCP launcher: installation-independent
runtime discovery is still pending. The app-generated packages already target
a verified local executable. Do not register the root source as a second
Façade plugin alongside an installed app-generated package.

See [installation](docs/installation.md), [compatibility](docs/compatibility.md)
and [license status](LICENSE-STATUS.md). This source repository is public;
an open-source license has not yet been granted. Official product information:
[facade.pictures](https://facade.pictures).

## Development

Requires Python 3.12+. The Python package has no runtime dependencies. Install
this directory as an editable dependency for development; build its wheel for
self-contained distribution. Run its tests with:

```sh
python -m unittest discover -s tests
```

Changes to skills and adapters belong here. Runtime installation, host-profile
mutations, project storage and photo processing remain outside this package.
