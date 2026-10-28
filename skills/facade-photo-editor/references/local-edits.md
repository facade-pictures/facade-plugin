# Local edits with fewer commands

Coordinates are normalized to the oriented original: [0,0] top left, [1,1] bottom right. Brush radius is a fraction of the image short edge. A single point paints a soft circle; a short list paints a stroke. It does not identify an object. Use existing procedural/raster masks for boundaries that cannot be represented honestly by soft coverage.

For an object boundary, `facade_segment` is another optional mask producer. Discover
`facade_capabilities(path="requests/segment")`; supply a stable `mask_id`, include/
exclude points and an optional box in oriented **uncropped source** coordinates,
plus `expected_version`, `base_revision` and a comment. Use an original view for
placement, not a cropped/warped output. SAM runs locally only when configured; it
never downloads during editing and never silently substitutes a rough contour.
If unavailable, use an appropriate existing mask method and state its limits.

Inspect the returned overlay (green include/red exclude clicks) and grayscale
coverage. Continue with the returned candidate as `base_revision` to refine the
same mask or apply an edit referencing its ID. The candidate is not automatically
accepted. Saved raster masks render without SAM. Use points for visible separate
parts; do not assume fine hair, glass or a narrow edge is alpha-matted. Native
overlays and ordinary raster refinement remain available through view/edit.

Create coverage and use it in the same `facade_edit.patch`:

```json
{
  "selections": [{
    "id": "cheek-light",
    "strokes": [{"points": [[0.48, 0.35], [0.52, 0.39]], "radius": 0.04, "hardness": 0.2}],
    "within": "existing-face-mask",
    "exclude": ["existing-hair-mask"]
  }],
  "upsertEdits": [{
    "id": "cheek-color",
    "operation": "white_balance",
    "maskId": "cheek-light",
    "parameters": {"temperature": 5, "tint": 2}
  }]
}
```

Omit `within`/`exclude` when unnecessary. Those IDs must exist; example names above are not provided masks. Add a stroke with `mode: "subtract"` to remove painted coverage. Reusing the selection ID replaces its coverage, while references to it survive. The backend stores ordinary portable brush/composite masks. Do not edit the generated `--brush`/`--area` helper IDs independently.

For a follow-up, send only the meaningful parameter changes:

```json
{"adjustEdits": [{"id": "cheek-color", "parameters": {"temperature": 3}, "opacity": 0.8}]}
```

Unmentioned top-level parameters stay unchanged; nested objects are replaced as units. Use full `upsertEdits` to change operation, mask or blend mode. Each variant patch applies independently to `base_revision`, not to the previous variant. Inspect the returned full-frame image and relevant crop before acceptance; inspect an overlay when you cannot tell whether the region covers the intended surface.
