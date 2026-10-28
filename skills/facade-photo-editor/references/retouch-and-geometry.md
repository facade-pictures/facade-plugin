# Local retouch, texture and framing

Use this for requested cleanup, tonal/texture defects, noise or geometry.
Decide what counts as a defect in this photograph before selecting a tool.
A request for a clean product, a natural portrait, beauty finishing or an aged
print can justify different treatment of the same mark. Genre alone does not
authorize smoothing skin, removing freckles/wrinkles, suppressing grain or
erasing wear. Clarify only uncertainty that materially changes the requested
content; leaving an intentional feature alone is a valid result.

## Distinguish the problem before repairing it

| Evidence and intent | Candidate action | Check |
|---|---|---|
| Unwanted small texture defect inside a continuous surface | `heal` with a compatible donor and clean boundary | Material, grain and surrounding gradients |
| A line, seam or pattern needs exact continuation | `clone`, aligned to structure | Repeated pattern, seams, light/color mismatch |
| Texture is intact; a light/dark patch disrupts the desired tone | Soft masked exposure/curves (dodge & burn) | Preserve form and natural large light transitions |
| Tone/texture are intact; local color is unwanted | Local color correction | Read [light and materials](photographic-finish.md); avoid replacing good texture |
| Red flash reflex in a pupil | `red_eye` | Iris, catchlight, eyelid and glasses |
| Objectionable distributed sensor noise | Consider `neural_denoise` | Fine texture, grain and missed-focus limits |
| A mark, grain or unevenness serves the brief | No repair | Do not manufacture work to complete a routine |

For tonal repair, [local light](local-light.md) and [local edits](local-edits.md)
describe existing curves/exposure and soft coverage. Large transitions can
describe a face's shape or a fabric fold; micro transitions may be distracting
in one brief and valuable texture in another. Match the scale of the correction
to the chosen defect. Do not compensate for flattened volume by adding sharpening.
Broad blur or negative texture is not equivalent to frequency separation or
targeted cleanup.

## Choose donors and boundaries

Match material, texture scale/direction, sharpness, grain, structure and local
illumination. The nearest clean point is not necessarily a good donor. A cheek,
forehead and neck can have different texture; rotating/scaling a donor is useful
only if the transformed texture still belongs. Avoid conspicuous repeated
motifs and donors containing another defect.

`heal` preserves donor gradients and adapts surrounding tone; `clone` transfers
the sampled appearance with feather/opacity. Heal needs the defect wholly
inside coverage and a clean outer boundary. A nearby high-contrast seam or
different material can contaminate the repair; choose coverage/donor that
respects it, use aligned clone when appropriate, or retain/report the gap.
Feather cannot fix the wrong texture or illumination.

Examples are conditional:

- Dust in a smooth sky: a nearby compatible donor may work; preserve sky
  gradients and do not mistake stars/birds for sensor dirt.
- Lint beside a fabric seam: inspect weave and seam direction; a large circular
  heal can damage both. An ellipse or smaller compatible repair may help.
- Temporary skin blemish: repair if the brief calls for it, preserving nearby
  texture and contour. Freckles or age lines need not receive the same treatment.
- Scratched product or old print: distinguish unwanted damage from requested
  patina/history. Large missing structure is not guaranteed recoverable by
  tiling small patches.

## Inspect once, apply a batch, review together

Read `facade_capabilities(path="topics/retouch")` or `facade_capabilities(path="topics/geometry")` when you need that stage's exact schema. These are document stages in `patch`, not IDs in `upsertEdits`. Reuse a schema already available in context.

`facade_inspect(project, revisions, regions)` accepts 1..12 regions `{id, box:[left,top,right,bottom]}` in native oriented-source pixels. It returns one contact sheet per revision and a `frame` for each region. These views show the photographic grade and retouch **before geometry**. Labels identify each crop; points are normalized within that crop, never relative to the contact sheet.

Copy the returned frame into every relevant retouch item. The backend maps its local `target`, `source`, `stroke` points and radii into source coordinates and validates project/base revision. A follow-up using old frames must inspect its new base or use the persisted canonical coordinates from `state(revision=...)`.

Example patch, using a frame returned by inspect:

```json
{"retouch":{"roundId":"eyes","upsert":[
  {"id":"left-pupil","kind":"red_eye","target":[0.32,0.45],"radius":0.025,"frame":{"projectId":"FROM_INSPECT","revision":1,"box":[100,100,500,500]}},
  {"id":"right-pupil","kind":"red_eye","target":[0.66,0.44],"radius":0.025,"frame":{"projectId":"FROM_INSPECT","revision":1,"box":[100,100,500,500]}}
]}}
```

Batch the chosen related repairs, rather than looping over individual pupils or spots. `review_retouch:true` on `facade_edit` or `facade_variants` returns 128px base/candidate thumbnails for 1..40 changed IDs alongside full frames, including old positions and removals. Variants share one base and pool their changed IDs. For a short piece use `review_retouch:"native"`: 1..4 changed IDs plus full-context 1:1 PNG crops, without downsampling. On edit, `review_regions` is the alternative for manual context boxes; it cannot be combined with either retouch review mode. Larger patches still support 4096 items; review them with paginated inspect. If retouch review is unavailable but candidates were saved, retry inspect, not edit/variants.

`facade_inspect` can take `retouch` **instead of** `regions`:

```json
{"project":"/path/to/project","revisions":[0,2],
 "retouch":{"ids":["left-pupil","right-pupil"],"include_sources":true,"native_detail":true}}
```

Omit `ids` to page through all saved repairs; optional `round_id`, `offset` and
`limit` (1..40) select a bounded group. `nextOffset` is null at the end. The pool
is the union of requested revisions, with the last requested occurrence supplying
the recipe; this makes removed items reviewable. `context` (1..8, default 3)
multiplies ellipse extents with a minimum 32px box. For strokes it adds a margin
of `max(16px, radius*context)` around the whole path; it does not multiply path
length. Each numbered group has the
requested revisions side by side; the image caption maps those numbers to IDs.
Optional donor crops show the **actual immutable input of that item's batch**,
including prior batches, at `donor.revision`. They are unrotated source crops,
not a preview of the transformed/healed replacement. A disabled item still shows
the input it would sample. After round consolidation, use surviving IDs or the
current round IDs from state.

The overview has 128px tiles, up to 4x nearest-neighbor zoom. With
`native_detail:true`, select at most four IDs: overlapping contexts merge, then
at most six native crops cover the whole selection. Each crop is at most 320px
per side, with at least 32px overlap when split, and is transported as lossless
PNG. Metadata reports source boxes, exact sheet cell bounds and `scale:1`.
Oversized requests fail explicitly; select fewer IDs or reduce `context`, or
inspect specific named regions. Thumbnails, successful execution and status
`applied` do not establish repair quality. Check the full frame too.

Each entry returns `item` in canonical whole-source coordinates and a `frame`
for the **last requested revision**. For parameter/donor changes, copy the
canonical item and change only the intended fields; do not attach that crop
frame to an unchanged canonical item. Use the frame only when replacing target,
source and radii with crop-local coordinates. Set `base_revision` to that same
revision and use the returned project `version` for the next patch. For a donor
outside the target crop, use canonical coordinates or inspect a larger region.
Color measurements remain in the `regions` mode; retouch review omits them.

Red-eye searches for a red-dominant connected component near the point. It preserves non-red catchlights and reports `no_red_reflex` when nothing suitable is found. It is not face detection or proof of correct targeting. Inspect eyes at useful scale, including adjacent iris/eyelid/glasses.

Clone items use `kind:clone`, `target`, `source`, `radius`, optional `sourceRadius`, `rotation`, `feather` and `opacity`. With no frame, points are normalized to the oriented original and radius is a fraction of its short edge. With a frame, both points refer to the same crop and radius to that crop's short edge. Use a larger crop or canonical coordinates when the donor is elsewhere. Optional `radiusY` makes an ellipse (same units as `radius`); `angle` rotates that ellipse clockwise. `rotation` separately rotates donor texture; `sourceRadius/radius` is an isotropic donor scale, not an independent donor Y radius. Both heal radii must be <=128 native pixels. Red-eye retains its circular search area. Feather softens coverage, not donor texture. Clone does not harmonize mismatched light/color; choose a suitable donor. Donor support outside the image fails before saving.

Heal uses the same donor controls with `kind:heal`. It preserves donor texture gradients and matches the target's surrounding tone/color with a boundary-based solve. `healSpace` defaults to `"linear"`, preserving existing recipes. Optional `"srgb"` solves encoded-sRGB gradients and boundary correction before blending in linear light; compare it when tone/grain matching is poor, without assuming it is better. Feather blends coverage once. Maximum radius on either axis is 128 native pixels. Circular/elliptical target coverage needs a one-pixel boundary inside the source; stroke edge behavior is described below. Invalid donors or oversized repairs fail explicitly. Use smaller patches only when each has a suitable donor/boundary, or choose clone when its behavior is appropriate; the size limit is not a reason to tile an unsuitable repair.

## Repair a wire or scratch one short piece at a time

Use normal Façade requests for this loop; do not create photo-specific Python
scripts or raster masks for a path that `stroke` can express. Clone/heal accept
`stroke` with 2..64 normalized points and a round-ended brush of `radius` width
on either side. Points use the same source/crop coordinate frame as `target` and
`source`. Those two points are donor transform anchors; `target` is not an extra
stroke point. Donor rotation/scaling applies to the entire path. Stroke coverage
cannot combine with `radiusY` or nonzero ellipse `angle`.

Stroke heal can reach a real image edge if each repaired component has clean,
known boundary elsewhere. Donor support must remain inside the image. Limits
are 4 million pixels in the stroke bounding rectangle and 100,000 covered pixels
for heal; the 128px radius limit still applies. The tool requires an explicit
donor and does not choose one or certify continuity.

Inspect a short piece and nearby clean structure, then compare two donors from
the same base. Example request to `facade_variants` (replace project, version and
coordinates from inspection; the two `source` points are the only donor change):

```json
{
  "project":"/path/to/project", "expected_version":0, "base_revision":"current",
  "preview":"candidate", "review_retouch":"native",
  "variants":[
    {"comment":"Compare donor above", "patch":{"retouch":{"roundId":"wire-piece-1","upsert":[
      {"id":"wire-piece-1","kind":"heal","target":[0.5,0.4],"source":[0.5,0.3],
       "stroke":[[0.45,0.4],[0.5,0.405],[0.55,0.41]],"radius":0.004,"feather":0.3,"healSpace":"srgb"}
    ]}}},
    {"comment":"Compare donor below", "patch":{"retouch":{"roundId":"wire-piece-1","upsert":[
      {"id":"wire-piece-1","kind":"heal","target":[0.5,0.4],"source":[0.5,0.5],
       "stroke":[[0.45,0.4],[0.5,0.405],[0.55,0.41]],"radius":0.004,"feather":0.3,"healSpace":"srgb"}
    ]}}}
  ]
}
```

Review each native crop and its context for residual lines, tonal strips,
broken cloud/edge continuation, repeated motifs and grain mismatch. To heal
a residual artifact, call `facade_edit` with the selected candidate as
`base_revision`, the returned project version, a **new item ID** such as
`wire-piece-1-cleanup`, and `review_retouch:"native"`. This adds a later batch
which samples the already repaired result. Reusing `wire-piece-1` instead
changes the first pass in its original batch. Review the same piece again before
starting the neighboring piece with a small overlap. Preserve good areas and
stop expanding patches when the donor or missing structure is unsuitable.

## Batch and revision semantics

Items in one submitted batch sample the same immutable batch input, after photographic corrections and earlier batches. One item cannot accidentally sample another item's newly painted pixels. Later batches may sample earlier repairs. Changing an upstream grade recomputes retouch from that grade; this is deterministic sampling, not a frozen JPEG donor.

Stable item IDs are global within a revision: `upsert` replaces an existing item in its original batch, `remove` deletes named items. Unmentioned items survive. A new `roundId` starts a visible round; adding a sixth consolidates the oldest two, keeping their internal batches and IDs. State gives compact counts; `state(revision=...)` returns item recipes when needed. The five-round limit does not cap undo history or flatten originals. There is no automatic dust detector or liquify in this release.

## Judge detail and context

At useful native detail, compare the original/base and result for repeated
texture, seams, color bleeding, blur, catchlights and shifted structural edges.
At whole-frame and intended viewing scale, check volume, material character and
the requested degree of cleanup. Tiny pores invisible at delivery size need
not become individual repair targets.

Region contact sheets can also downsample. Use sufficiently small source
regions or `facade_view` detail crops to judge native texture, observing the
reported preview size and coordinate space. View crops use output coordinates
after geometry; inspect frames use source coordinates before geometry. Never
reuse one as the other after a transform.

If a defect remains, review the affected IDs together and revise donor,
coverage or method rather than just increasing opacity. Recheck that named
defect at the same scale; leave good repairs intact. Input optics and the grade
precede retouch, and final geometry follows it. Upstream changes recompute
repairs, so reassess their seams/texture after a significant grade change.

## Noise when it conflicts with the brief

Consider `neural_denoise` (bundled offline SCUNet) for objectionable sensor
noise, placing it before strong contrast/sharpening when those would amplify
the problem. Choose strength from the actual tradeoff in smooth areas and
fine-detail/material crops; there is no universal amount or required denoise
pass. Preserve intentional grain. Cleanup can erase fine texture and cannot
repair missed focus.

Reuse the edit ID: changing amount reuses cached tiles; enlarging a mask
computes newly covered tiles. Preceding pixel changes invalidate the cache.
Masks blend after filtering with full-image context. The first full-resolution
CPU render can take minutes. Missing weights/runtime are an installation error,
not permission for a hidden download or substitution. The old `denoise` is a
different Wiener filter; do not routinely stack both.

## Geometry

For lens distortion, corner brightness or channel misalignment, read
[optics](optics.md): `patch.optics` is a separate whole-object replacement,
with explicit generic parameters and no automatic profile selection. Distinguish
optical defects from intentional camera angle, perspective and light falloff.

`patch.geometry` replaces the complete geometry object. `{}` resets it. Defaults preserve the source exactly. `perspective` is four source points in TL/TR/BR/BL order; it rectifies that quadrilateral, followed by clockwise `rotation` in degrees and normalized rectangular `crop`. `autoCrop` trims empty borders; disabling it rejects transformations that expose empty pixels. Inspect `view.renderStats.geometry` for effective output size/crop scale.

Example of a crop that preserves the source aspect ratio: `{"geometry":{"crop":[0.02,0.02,0.98,0.98]}}`. After rotation, perspective or automatic trimming, verify the output ratio against the constraint in `SKILL.md` as well.

All photographic masks and retouch stay anchored to the oriented source, and the final transform moves them together. `facade_view` shows output geometry; its legacy `crop`/`crops` are output-pixel inspection windows, not document cropping. Use `facade_inspect` for source-anchored editing coordinates, especially after perspective/crop. Do not infer source coordinates from a transformed preview.

Judge perspective against intentional camera angle and composition; keep the user's crop intent. Check the whole frame for stretched people, lost edges and excessive automatic cropping. Original pixels outside the crop remain in the project.

PSD exports bake geometry into the canvas and color corrections into Processed. Retouch rounds export as at most five independently masked pixel layers; their feather/opacity is already baked into patch pixels, so do not apply it again. Photoshop does not receive native clone history. Original uncropped pixels, donors and operation recipes remain in Façade.

## Background

Technique principles, not identical tool behavior:
[Retouching Academy on healing boundaries](https://retouchingacademy.com/working-with-the-healing-brush-tool/),
[micro transitions and dodge & burn](https://retouchingacademy.com/dodge-burn-working-with-micro-transitions/),
[Adobe Healing Brush](https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/healing-brush-tool.html).
