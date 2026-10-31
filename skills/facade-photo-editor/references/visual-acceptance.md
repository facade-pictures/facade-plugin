# Visual acceptance checkpoint

This is a host-agent instruction, not a backend evaluator or human approval.
Run it after the first finished visual candidate, before finish/accept. Do not run
it after each slider, export-only request, archive or other service operation.

## Freeze the inputs

Before editing, record the exact project and numeric revision being worked on as
`before`, the verbatim user request and applicable constraints. Resolve `current`
once; before is the state before this request, not necessarily original/RAW.
Keep before fixed through both reviews. Record the first finished candidate's
numeric revision as `first_candidate`; never overwrite, reject or delete it during
this checkpoint. Corrections create a new revision based explicitly on that candidate.
Retain these IDs, request, review count and verdict in the handoff after compaction.
If the baseline cannot be recovered, stop as uncertain; do not substitute original.

Use existing `facade_view` comparison images and matching `crops` for local work.
Show before and candidate with the same scale, delivery and rendering settings;
no independent brightness/color normalization. Geometry changes are not registered
automatically: use comparable views and mark an unresolvable comparison uncertain.
Open returned files if necessary. Paths, operation descriptions and successful tool
responses are not visual input. Reuse already visible exact-revision images.

## Reviewer input and instruction

Use an existing clean host context with image viewing/delegation if available;
otherwise explicitly perform **self-review**, never call it independent review.
No new harness, provider integration or backend model call is required. Give a
separate reviewer only this instruction, actual before/candidate images, the
verbatim request and constraints, an actual reference only if supplied for this
request, and optionally a short useful summary of existing measurements. Do not
send the editor's rationale or claims that the candidate is good. On review 2,
also show the saved first_candidate with an unambiguous label. The reviewer must
actually view every required image; missing images or reviewer errors mean uncertain.

Judge the requested visible outcome, not a universal beautiful photograph.
For each substantial requirement distinguish met, too_weak, excessive,
wrong_direction or uncertain. A visible change is not necessarily sufficient:
respect slightly, noticeably and radically. Do not demand changes in areas that
already meet the request. Intentional grain, blur, darkness, crushed shadows or
unusual color are not defects by themselves. Check obvious unwanted consequences,
including important subject readability, faces, halos and local boundaries.
Every issue needs observable evidence identifying what and where. Invent no
mandatory improvement; accept a ready result. Measurements are supporting evidence,
not proof of artistic success. Do not use quality_score or Apple aesthetic scores.
Describe the visual problem and desired correction; the editor chooses tools and
parameters. Return at most TWO substantial issues across unmet and regressions:

```json
{"decision":"revise","unmet":[{"requirement":"Noticeably darker mood","status":"too_weak","evidence":"The bright wall on the right still dominates the frame"}],"regressions":[],"next_change":"Subdue the wall more while preserving the face and lights"}
```

`decision` is accept, revise or uncertain. `unmet[].status` is too_weak, excessive,
wrong_direction or uncertain; met requirements need no entry. Regressions contain
an issue and observable evidence. For accept use empty lists and null next_change.
For uncertain describe the missing evidence, not invented visual defects. No
confidence numbers or long critique. On review 2 identify the preferred candidate
by its supplied revision ID (first or corrected); newer is not automatically better.
An accept with unresolved issues or an invalid/missing verdict is uncertain.

## Bounded transitions

Follow this table; review count is per user request, never reset after a correction.

| Review | Verdict | Action |
| --- | --- | --- |
| 1 | accept | Stop editing; finish the reviewed first candidate. |
| 1 | revise | Make ONE targeted correction, save a new candidate, then review 2. |
| 1 | uncertain/error/missing images | Preserve candidates; stop automatic edits; disclose uncertainty; no acceptance. |
| 2 | accept | Stop editing; finish the explicitly selected reviewed candidate. |
| 2 | revise | Preserve both; stop; report the remaining gap; no acceptance. |
| 2 | uncertain/error/missing images | Preserve both; stop; disclose uncertainty; no acceptance. |

For too_weak make a clearly visible change in the identified aspect, not a symbolic
step or indiscriminate strengthening of the entire treatment. At most ONE corrective
iteration and TWO reviews. Never restart this budget under a new candidate name.
Review 2 compares before, first_candidate and corrected candidate: retain the first
if correction is worse. It may be accepted only if review now finds it meets the
request; otherwise leave it saved without declaring success. uncertain/error is
never accept. Existing saved revisions preserve incomplete work without finish.

Persist a concise verdict and IDs in the existing finish/decide comment when
accepting. When stopping without acceptance, keep the report and saved IDs in the
chat/handoff and, when persisting, an existing brief audit comment as described below; do not call reject merely to record a report. Tell the user any
remaining gap or uncertainty and which saved result is preferred. Agent acceptance
is not user approval. Existing exact-revision artifact inspection still applies;
combine it with this checkpoint rather than launching another improvement loop.

## Concrete collection through existing tools

1. `facade_state(project)` resolves acceptedRevision/version; freeze the numeric
   revision actually being edited (use the explicit candidate ID for a follow-up
   on a candidate). Keep the verbatim request in brief.goal and the handoff.
2. `facade_view(project, revisions=[before, candidate], long_edge=1536)` returns
   actual image blocks in MCP. Consume those images, not just the JSON labels.
   For review 2 use `[before, first_candidate, corrected]`. For CLI, invoke
   `facade-editor call view --images NEW_DIRECTORY` with the same request JSON,
   then OPEN every returned previewPath using the host image viewer. A path-only
   context must stop as uncertain. `layout="comparison"` is useful for adjacent
   comparison but bounds the entire sheet; separate frames retain more detail.
3. `facade_inspect(project, revisions=[before, candidate], measurements=true,
   regions=[{"id":"frame","box":[0,0,WIDTH,HEIGHT]}])` measures the same whole
   source frame. Add a relevant local box if helpful, keeping boxes/mask_revision
   fixed. WIDTH/HEIGHT are oriented-source dimensions, not preview dimensions.
   Read `images[].regions[].measurement.output.summary` for each revision:
   lightnessMean (Oklab L), tonalContrastP90P10 (L distribution spread), chromaMean
   (mean OKLCh C), nearBlackPct/nearWhitePct (all display RGB channels <=.01 or
   >=.99). Report before, candidate and their differences; no pass/fail threshold.
   These use shared bounded weighted samples; approximateColorStats reports
   sampling. `limits` separately retains native pre-display channel endpoints.
   Older runtimes without summary supply OklabMean[0], L[2]-L[0], C percentiles
   and limits; label these accurately, never invent missing near-range statistics.
4. Inspect ignores output geometry and delivery. Use `view` for their actual
   appearance and disclose that statistics are pre-geometry/pre-delivery; they
   cannot establish a crop or output-size requirement. Missing/empty measurements
   are not zero change. Never replace visual input with inspect's tiny thumbnails.
5. Record the concise JSON verdict, fixed before/first/corrected IDs and request
   in the existing decision comment on acceptance. For a stop without acceptance,
   `facade_brief` can save the unchanged brief plus a review comment in existing
   history (use its current expected_version); it does not accept/reject candidates.
   No separate review database or evaluator is involved.
