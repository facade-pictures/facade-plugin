# Optional local generated repairs

The user controls **Allow generative patches** in the app's Overview. It defaults
to off and applies across hosts. Query `facade_capabilities(path="topics/generative_patches")`
immediately before generation; missing/error/false means no generation. Never change
the policy through the CLI, files or another tool on your own initiative. Do not
repeatedly ask to enable it. Existing saved patches remain visible when disabled.

When allowed, first identify why ordinary clone/heal cannot solve the local problem.
Use an actually available host image tool; Façade does not supply or call a generator.
If no suitable tool exists, explain that limitation and continue ordinary editing.
Supply only the relevant image context, following the host tool's instructions.
Preserve full-frame composition and identity. This permission is for local repairs,
not whole-image regeneration. Do not claim a provider/model you cannot identify.

Use the oriented source coordinate space **before output geometry**. Inspect the
current revision and obtain a context crop. Ask the generator for a matching local
repair, preserving perspective, illumination, grain and texture. Save an RGB/RGBA
8-bit PNG. The pixel box must be inside the source, <=1 million pixels; the sum of
active generated boxes must be <=25% of the source area (overlaps count twice).

Apply with `facade_edit`, including current `expected_version` and explicit base:

```json
{"patch":{"retouch":{"roundId":"local-repair","upsert":[{
  "id":"repair-1","kind":"generated","box":[100,200,300,400],
  "path":"/absolute/path/to/repair.png",
  "model":"actual model identifier supplied by host",
  "prompt":"actual generation instruction",
  "reason":"why conventional retouching was insufficient",
  "feather":16,"matchBoundary":true,"resize":false,"opacity":1
}]}}}
```

By default PNG dimensions must match the box. `resize:true` explicitly permits
resizing with matching aspect ratio (within 1%). Feather is measured in source
pixels. Alpha holes remain unchanged; feather and opacity blend in linear light.
Boundary matching adjusts a mean color offset; it does not guarantee a seamless
texture or correct generated content. Façade imports an immutable checksummed copy;
the original photo and previous revisions remain intact. Model/prompt provenance
is an agent declaration, not independent provider verification.

Inspect the whole frame and the patch boundary at native detail. Check structure,
texture, repeated patterns, halos and color, then accept only the reviewed result.
Backend success is not photographic approval. Remove with the ordinary retouch
`remove:["repair-1"]` field, even while permission is off. Turning permission off
also blocks accepting/restoring a candidate that introduces a different active
generated patch; it does not erase history or prevent viewing/exporting saved work.
