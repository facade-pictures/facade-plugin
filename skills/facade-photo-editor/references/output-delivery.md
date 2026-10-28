# Delivery size and output detail

Use `delivery` in `facade_view`, `facade_export` and `facade_finish` when the user
needs a specific output size. Get its schema from `facade_capabilities`. This is
an output boundary, after native edits/retouch/geometry; it does not change the
saved photographic revision.

`{"longEdge":2048,"sharpen":{"amount":35,"radius":0.7,"threshold":3}}` illustrates
the shape, not a mandatory preset. Aspect is preserved to pixel rounding.
`allowUpscale` defaults false; a larger request reports `upscaleSkipped` and
keeps native size. Enlargement is interpolation, not restoration.

Inspect the full delivered frame and relevant delivered-pixel crops. `view` with
the same delivery settings runs the export pipeline; its `long_edge` is only a
transport limit. Crops are then measured in delivered pixels, not native source
pixels. A crop no larger than the preview limit shows output detail without
downsampling. Transport is JPEG, so inspect the file for encoding artifacts.

Sharpen happens after resize; radius is in output pixels. Start without it and
add only if edge definition needs it. Grain/noise and existing halos can become
worse. It cannot recover missing focus or moving fingers. Keep a native master.
Mask overlays cannot accompany delivery. PSD/PSB rejects delivery entirely;
native layered export stays separate.

Optional `grain` runs after output sharpening and uses `grain_texture` parameters
in output pixels. Read [grain guidance](grain.md). It is global; native masks
require a stack edit. Keep it out of both stages unless accumulation is intended.
The sidecar saves output grain, while native project revisions remain unchanged.

Reuse exactly the reviewed settings in export/finish. Raster exports with delivery
write `output.ext.json` with normalized settings, pinned revision and hashes.
It is a replay aid, not a replacement for the project. Omit delivery to preserve
legacy full-size output without a sidecar. JPEG/PNG are 8-bit; TIFF stays 16-bit
sRGB. Do not promise a print-specific or Adobe-equivalent sharpening algorithm.
