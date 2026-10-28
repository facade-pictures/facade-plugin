# Artifact review

Use `facade_diagnose(project, revision)` before finishing a candidate. It reads saved revisions and returns lossless PNG images without changing acceptance or recipes. By default the reference is the candidate's parent; `current` means the accepted revision, so pass the candidate number explicitly. For accumulated damage, also compare against `base_revision="original"` or the last visually trusted revision.

Set `review_artifacts=true` on `facade_edit` to receive the same automatic review inline. If `diagnostics.status="unavailable"`, the edit is already saved: retry `diagnose` on its candidate number, not the mutation. Variants use standalone `diagnose` on the chosen candidate.

## What to inspect

1. Judge the ordinary whole frame against the user's intended look. A technically quiet image can still be weak, muddy or unfinished.
2. Inspect the returned ordinary native before/after crops. When subtle structure remains uncertain, copy that region's `detailRequests[].next` into `facade_diagnose`, or request `modes=["shadows"]` or `["highpass"]` for its box. These rows use identical settings on both sides. Confirm a suspected problem in the ordinary crop; filtered ugliness alone is not damage. All three modes remain available together explicitly, but are not a mandatory pass.
3. Inspect an additional relevant smooth field and a strong edge if the nominated crops miss them: sky, walls, skin, shadow gradients, lights, silhouettes or mask transitions. Look for blocks/banding, halos, unnatural texture and seams. Mask overlays show coverage, not the photograph's quality.
4. If a defect is visible, try a small reversible change that tests its cause. A signal locates a symptom; it does not identify the guilty operation. Compare with the same reference and crop, retaining the intended contrast, texture and mood.

`blockiness_growth`, `detail_growth`, `edge_neighborhood_change` and `mask_boundary` nominate locations, not confirmed defects. Real texture, grids, stronger edges and deliberate grain can trigger them. Scores are not confidence or quality; no leads is not a pass. Do not automatically denoise, reduce contrast or revert a strong treatment just to reduce scores.

## Exact recheck

Use a returned region's `box` with the repaired revision:

```json
{"project":"/absolute/project/path","revision":4,"base_revision":2,"crops":[[32,0,288,256]],"modes":["ordinary"],"overview":false}
```

Up to six integer `[left,top,right,bottom]` boxes, each at most 320 pixels per side. Coordinates are output pixels, or delivered pixels when `delivery` is supplied. Both frames are rendered through the target revision's final geometry and identical delivery. If framing changes during repair, choose the equivalent subject location again. Use identical `delivery` settings when inspecting output sharpening and exporting.

Explicit crops skip automatic whole-frame nomination; `checks` reports
`not_run_explicit_crops`, not a clean result. `overview=false` requires crops.
For a new automatic search, omit crops and keep the overview. The returned next
calls pin both revisions and delivery; update the target revision after a repair.
Recover only missing regions/modes after context loss, while retaining a
whole-frame review of the final result. An interrupted edit may have committed;
read state before repeating the mutation.

The native block scan checks only 4/8/16-pixel periodic structure; detail/edge analysis uses an overview. It can miss defects already present in the reference, other block sizes, color-only problems and semantic retouch errors. Diagnostic views precede export compression and do not inspect a CMYK proof. Review the actual exported file if compression is a concern; use `facade_proof` for print.

If the connected runtime lacks `facade_diagnose`, inspect the same whole-frame and native risk regions with `facade_view`, disclose the missing automatic nomination, and do not claim that diagnostics ran. A skill on disk does not update an already-connected MCP server.
