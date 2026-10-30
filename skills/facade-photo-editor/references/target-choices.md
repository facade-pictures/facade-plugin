# Choose local targets by ID

Use when exact placement or a local comparison is uncertain and the backend
advertises `facade_capabilities(path="topics/targets")`. These are optional
shared CLI/MCP tools. They do not start an internal agent or a scene-preparation
pass. Do not load the complete catalog to use them.

`facade_targets(project, revision, kind="regions")` shows a numbered 3x3 grid.
Choose a displayed ID. Copy returned `use.refine`, replacing the example ID with
your choice, to subdivide that region; `action="inspect"` shows it without marks.
Use `within_many:[{set_id,id},...]` to refine up to three regions in one call.
For inspect/compare, `selections:[{set_id,id},...]` accepts up to six choices
across sets in one call; omit single-set selectors. Batch independent questions
when they are already known. The default 3x3 selection is unchanged.
No coordinate transcription is needed. A region is a rectangle, not a detected
object. Use only as much refinement as the actual task requires.

`kind="masks"` offers existing masks at the selected revision, frozen once as
native 16-bit coverage. It does not invent object masks. `kind="red_reflex"`
offers experimental red-component candidates, optionally inside a chosen region
via `within:{set_id,id}`. Plain context and the frozen support are shown together.
Red components can include skin, lips, clothing or other objects; they are not
verified eyes. A missing or truncated proposal list does not mean the image is
clean. Inspect support and surrounding anatomy, decline unsuitable proposals,
or refine by selecting a smaller region. Do not choose an unsafe candidate just
because it ranks first. Ranking is a heuristic, not confidence.

Target IDs are local to the returned `set_id`, which binds them to the source,
capture revision and frozen support. Copy those identifiers exactly. Paging
reuses the frozen set. Do not silently reuse targets after editing: mutation and
refinement reject stale project versions. Rediscover on the intended revision.

## Compare a selected place

`facade_targets(action="compare", project, set_id, ids, compare_revision)` shows
unmarked before/after crops. Before is the set's capture revision; after is the
explicit comparison revision. Both use the same source-space coverage, before
output crop/rotation. The small measurement result provides named before/after
values, computed `afterMinusBefore` and `lightnessDirection`; do not reverse them
or infer photographic quality from their sign. Oklab D65 L is 0..1, a/b signed;
positive b is yellower, negative b bluer. A changed median is not the median of
per-pixel changes. Sampled large regions are marked approximate.

Select relevant material rather than averaging unrelated foreground/background.
Numbers help answer a specific question; they do not determine neutral skin,
natural light, good transitions or whether the complete brief is finished.

## Apply the chosen support

`facade_target_apply(project, expected_version, set_id, ids, action, comment)`
creates an ordinary candidate from the capture revision and leaves acceptance
unchanged. `action="none"`, with no IDs, declines all without creating a revision.

- `action="mask"` saves the union of the selected coverage and returns `maskId`
  and `candidateRevision`. Continue ordinary edits from that candidate using
  the returned mask. Rectangular tiles do not become feathered object selections.
- `action="red_eye"` accepts only red-component targets and neutralizes the
  frozen support directly. It does not convert the ID back to an approximate
  center or detect again. Iris highlights outside that support stay untouched.
  The resulting `red_eye_component` retouch item has a stable correction ID;
  ordinary retouch inspection/removal can use it. This is conventional processing.

Review actual photographic pixels and completeness before finishing. Fixed
support solves coordinate transfer, not correctness of detection or taste.
Applied masks/retouch recipes persist in ordinary project history and exports;
the local discovery cache can be regenerated and is not required for rendering.
