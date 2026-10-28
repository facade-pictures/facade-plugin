# Color and tonal measurements: questions, probes, interpretation

Use this when a measurement or comparison can change the next decision:
uncertain casts, material separation, muddy colors or highlight detail. A clear
small edit may need only visual review. Choose the intended result and what
must survive before choosing samples; neutral, brighter or more saturated is
not an automatic improvement.

## Ask a discriminating question

Separate observation, possible cause and desired change. "The berry looks
dull" could mean insufficient chroma, excessive lightness, weak surrounding
contrast or unsuitable lighting. "The dress is bright" does not establish lost
detail. State what evidence would favor one explanation and what would make
the proposed correction unnecessary.

Select a target, a relevant neighbor and a protected comparison area when
useful. Compare the same material under different light, or different materials
under similar light. These relationships are evidence, not proof of an
illuminant. Snow, walls, fabric and skin are not automatic neutral anchors.
Use a known reference only when its material and lighting make it applicable.

Choose small representative areas inside a surface; separate diffuse material,
specular reflection, shadow, makeup and edges. A larger area reduces pixel noise
but may mix unrelated colors. A bright reflection is not a reliable diffuse
white point. Exact pixels are useful for a specific boundary or suspected
clipping, not as the default description of an entire material.

## Sample comparable regions

`facade_inspect` batches 1–12 named regions across 1–3 revisions. Supply `box`
in native oriented-source pixels, `maskId`, or both. It returns images plus
compact source/output sRGB and Oklab means, L/C p10/p50/p90 and channel/gamut
diagnostics. `detail_ids` adds histograms only for those region IDs. For exact
samples add `points: [[x,y], ...]`: absolute integer source pixels, up to 8 per
region and 24 total. These differ from normalized retouch coordinates.

Repeat the same regions after the edit. Coverage comes from `mask_revision`,
default the last requested revision, and is fixed across all compared revisions,
including original.
Use `measurements:false` for crops only. Empty masks are reported explicitly.
Geometry is omitted. Frames remain tied to their base revision.

## Interpret the returned values

| Evidence | Useful interpretation | Limit |
|---|---|---|
| `sRGBMean`, `OklabMean` | Direction of a region's change | A mean can hide opposing casts or multiple materials |
| `L` p10/p50/p90 | Changes to darker, middle and lighter parts of the distribution | No universal exposure target; these are percentiles, not anatomical or lighting zones |
| `C` p10/p50/p90 | How chroma and its spread change | More chroma is not necessarily richer or more believable |
| Point `OKLCh` | Color at a chosen pixel | Hue is unstable near neutral and null at the neutral threshold |
| `limits` | Channel endpoint occupancy and out-of-gamut working values | Neither endpoint occupancy nor out-of-gamut values prove lost RAW detail |
| Opt-in L/C histograms | Distribution hidden by a summary | They do not show which object caused it; inspect or split regions |

sRGB is 0..1; Oklab L is 0..1, a/b are signed; OKLCh C is absolute and h is
degrees. Do not transfer CIELAB, HSL or CMYK target numbers from a tutorial into
these fields. Two strongly colored areas can average toward neutral while
neither is neutral: inspect the crop and split meaningful regions before
"correcting" an average.

Color stats describe D65 display-mapped float colors before 8-bit quantization.
Explicit linear RGB and range diagnostics describe pre-display working values.
Large regions use bounded sampled color statistics; channel/gamut counts use
native pixels, weighted by coverage. Empty coverage provides no color evidence.

`source` is decoded/developed RGB for each revision before photographic edits,
not RAW photosites or a fixed original across different developments. Input
optics also precedes grading. Compare revision outputs to assess a whole
change; check develop/optics when the input baseline changes. For sensor
clipping/layout questions use `facade_raw` and read [RAW development](raw-development.md).
Its read-only probes are approximate development-only images, excluding the
grade and masks; apply chosen settings and inspect the complete native render.

For high-depth rendered inputs, uint16 RGB/gray TIFF with a matching ICC profile
imports directly into float32 linear sRGB. State exposes `colorImport`; untagged
TIFF assumes sRGB and malformed profiles fail. TIFF export is 16-bit sRGB;
16-bit PNG is unsupported. Measurements do not establish lossless wide-gamut
preservation or camera/Lightroom color parity.

## Probe a cause, then judge the photograph

Use `facade_variants` only when alternatives resolve a meaningful uncertainty.
Both patches start from the same explicit base; keep relevant coverage and
framing fixed. For diagnosis, contrast explanations (e.g. lightness versus
chroma) or vary one relevant dimension. A finished look can combine several
operations; diagnostic isolation is not a restriction on creative treatment.

| Conditional question | Probe and interpretation |
|---|---|
| A dress should read as neutral in the main light | Compare diffuse fabric, its shaded part and nearby materials. If global WB helps one but harms the others, investigate mixed light/local treatment; do not force every fold to equal RGB |
| Food or flowers should feel denser | Compare a tonal and a chroma hypothesis. Check texture, neighboring colors and gamut; increasing C alone may make a reflective surface look emissive |
| Metal looks too bright | Separate reflection from textured material. Test recovery only where detail matters to the request; do not flatten the sparkle to reduce endpoint counts |
| A monochrome subject should separate from its background | Compare tonal relationships and channel-mix options. Skip skin-hue targets and do not recover every shadow by default |

Use [light, materials and finish](photographic-finish.md) to choose corrective
operations after diagnosis. A test supports a useful editing direction, not
necessarily a unique physical explanation. If neither variant serves the brief,
retain the base and revisit the hypothesis instead of increasing strength.

Record what changed, what survived and what remains uncertain: "red fabric is
denser; folds remain distinct; face unchanged; strongest reflection still needs
review." Measurements verify changes, not photographic quality. Recheck a named
problem at matching framing/scale before calling it resolved.

## Background

Adapted principles, not transferable settings:
[Adobe color sampling](https://helpx.adobe.com/photoshop/desktop/adjust-color/selective-color-adjustments/view-pixel-color-values-in-an-image.html),
[Adobe reference points](https://helpx.adobe.com/photoshop/desktop/adjust-color/color-corrections/adjust-color-tone-levels-curves-eyedroppers.html),
[darktable sampling spaces](https://docs.darktable.org/usermanual/4.6/en/module-reference/utility-modules/darkroom/global-color-picker/).
