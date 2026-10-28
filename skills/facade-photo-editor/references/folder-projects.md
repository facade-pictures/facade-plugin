# A photo folder as a Façade project

Use this when the user wants editing state alongside a shoot or a folder of RAWs.
The host workspace can be larger: Codex/Cursor might open `Photos/`, while the
Façade folder is `Photos/Trip/`. No companion app or host-specific project format
is required.

1. Initialize the chosen existing folder with
   `facade_folder(action="init", folder="/absolute/Photos/Trip")`.
   Optional `name` labels it. Use `source_scope="root"` when only root-level
   images are sources and subfolders are existing exports; default `tree` permits
   sources in subfolders. The saved rule is enforced by create, not just advice. This imports no photos and preserves existing host
   instructions. Repeating init returns the existing identity/name.
2. Resume a saved photo with `facade_projects(folder="/absolute/Photos/Trip")`
   and the usual state/view calls. This lists edited photo documents, not every
   untouched source on disk. The agent can list source files with its normal tools.
3. Start a selected photo with
   `facade_create(folder="/absolute/Photos/Trip", source="day-1/IMG_1234.RAF", brief=...)`.
   Relative sources resolve from that folder, including its subfolders. Absolute
   sources must also be inside it. Do not provide both `folder` and `project`.
4. Use the returned `project` path with existing edit/view/decide/export tools.
   Default image and single-photo archive exports go into the shoot's `facade.exports/`.
   An explicitly requested output location still takes precedence.

```text
Trip/
  day-1/IMG_1234.RAF
  day-2/...
  .facade/
    project.json             folder ID and name
    README.md                short agent guide
    IMG_1234.processing/
      project.json           recipe, revisions and decisions
      original.raf           relative symlink to ../../day-1/IMG_1234.RAF
      assets/                masks and other edit assets
  facade.exports/                   rendered images or single-photo archives
```

Only photos explicitly selected for editing get a `.processing` directory.
The original stays in place: `original.*` is a relative symlink, not a copy.
Same-named photos get a short suffix when needed to keep documents distinct.
Use existing documents for follow-ups instead of creating another for each edit.
Keep the source file at its relative location; changing its bytes is detected by
its saved hash, and deleting or renaming it breaks the link. Masks and other edit
assets remain regular files inside the document.

Copy the entire folder, including hidden `.facade/`, to transfer it. Then list
projects using the new folder path and use the returned paths. The folder ID,
photo history and relative links survive when the folder layout is preserved;
chat history and installed runtimes are separate. For an independent photo,
project_export materializes the linked original as a regular asset in its ZIP.
project_import restores a self-contained document with the same revisions.
Existing projects with copied originals keep working; no automatic migration.

The selected folder is explicit on each create/list call. There is no shared
current-folder setting, photo crawl, folder registry or batch processing in this
first slice. A folder groups independent photo documents; ordinary editing
permissions and the agreed series workflow still apply.

## Open the whole gallery

Call `facade_gallery_open(folder=...)` once for a complete interactive source
browser. It respects the saved source scope and returns ready `display`,
`fragmentPath`, `standalonePath`, `manifestPath` and the photo count. Optional
`output_directory` chooses an absolute artifact directory outside the shoot;
the default is `<FACADE_LIBRARY>/galleries` (normally `~/Pictures/Facade/galleries`).
Follow the host instructions to display it. Do not generate or rewrite the UI.

All previews are embedded. Scrolling, click-to-enlarge, previous/next and returning
to the grid are local interactions: no model, tool, daemon, HTTP server or network
call is involved. The explicit discussion button sends the selected source to
chat when the host supplies that bridge. Otherwise browse the standalone HTML and
refer to its displayed number. `sourceNames` is the exact 1-based filename mapping
for up to 200 photos; larger folders keep the full mapping in `manifestPath`.

This is a snapshot of originals, not a rendered edited collection. Reopen to
refresh changed files. Browse previews are not a photographic-quality review;
inspect the selected source/current revision before editing. Sources, projects
and existing exports are unchanged. Each opening creates private presentation
files outside the shoot; they survive process restarts and are not a photo index.

The inline fragment stays below 1 MB by reducing preview resolution when needed.
The standalone file retains 720px thumbnails plus separate 2560px (or source-size if smaller) quality-90 detail images, with a 100% zoom button. Inline detail still uses the budget-limited thumbnail; use the standalone gallery for detailed browsing. If even the minimum inline size cannot
hold every file, `inlineAvailable=false` and the complete standalone gallery is
returned; no photos are dropped. Corrupt files remain numbered error slots.

## Show a static contact-sheet page

Call `facade_gallery(folder=...)`: one numbered contact sheet is returned directly
as a native image plus a ready temporary local file (`previewPaths`) and
`displayMarkdown`. If native images are not visible in this host, include that
Markdown directly in the reply; no extra tool calls, base64 copying or file
writing are needed. The file lives outside the photo folder, survives MCP
restart, and may eventually be removed by OS temp cleanup. On a remote MCP
server the path may not be accessible to the host; use the native image there.
Default 18 source photos in six
columns; `limit` is 1..24, `columns` is 2..6. This respects `source_scope`; existing
edits are not rendered by this source browser. For “next”, pass the returned `next`
object to the same tool; null means the end. Keep the latest result's mapping from
number to `items[].source` and use that exact source when the user selects a frame.
Do not import the whole gallery or write an ad hoc contact-sheet script.

The cursor works across chats/processes when preserved. Names are scanned cheaply,
only a page of names is retained, and only that page's photos are decoded, one at a
time. There is no thumbnail cache on disk or hidden full-library image indexing.
Ordering is live by relative filename: deletions before the cursor do not shift the
page; new files before it appear after restarting without cursor. Numbers belong
to the displayed browsing sequence, not permanent photo IDs. Corrupt/unsupported
previews remain numbered slots with errors. For large RAWs/TIFFs the selected-page
decodes can still be costly. CLI returns metadata unless `--images` is explicitly
requested; MCP sends the image inline and saves the same encoded bytes once for
local display. This temporary page artifact is not a per-photo thumbnail cache.
