# Optics and aperture blur

## Saved bokeh

`lens_blur` is an ordinary persisted edit. Read its capability schema. Select
the background with `maskId`: white pixels participate in source sampling and
receive blur; black pixels remain protected and cannot bleed their color into
the background. Without a mask it blurs the entire frame. Inspect the overlay
before applying a strong effect, including whole people, hair, frames and gaps.

`radius` is the aperture circumradius, not Gaussian sigma or an f-number.
Default units scale with a 2048px long edge; `radiusUnits:pixels` fixes native
pixels. `blades` includes 5 and 10; `rounding:0` makes polygonal highlights,
`rounding:1` a disk. `rotation` turns the shape clockwise. Opacity mixes with
the original; reduce radius to reduce actual defocus.

This version treats one selected background plane. A feathered mask is an
application/source-eligibility transition, not a depth gradient. Separate
stacked edits are not a physical multilayer depth renderer. Existing bokeh is
blurred again, not replaced with a new diaphragm shape. There is no automatic
depth inference, calibrated lens profile or added highlight energy.

Normalized sampling avoids direct foreground color spill, but cannot recover
hidden background or separate an old background color already mixed into hair.
If a person is half blurred or a window strip remains sharp, correct coverage
before adjusting radius. Review the actual native composite, not only the mask.
The recipe reopens in Façade; ordinary PSD export bakes the effect and does not
promise a Photoshop-native Lens Blur filter.

## Generic lens controls

Use `facade_capabilities(path="topics/optics")` for the exact `optics` schema. This is
`patch.optics`, a whole-object replacement; omission inherits and `{}` resets.
Read current/selected optics before changing one control so others survive.

- `distortion`: poly3 k, -0.1…0.3, negative barrel / positive pincushion model.
  `distortionMode:correct` removes that model; `simulate` adds it by solving the
  inverse. Start small and judge straight architectural lines and edge subjects.
- `redScalePercent` / `blueScalePercent`: -1…1%, radial input sampling relative
  to green. Positive samples outward. Compare multiple native edges across the
  frame in one inspect; opposite signs are not exactly inverse scales. The narrow
  newly exposed channel border extends nearest pixels; crop it if visible.
- `vignetteEV`: -2…2 stops at the farthest corner, positive brightens and negative
  darkens, applied in linear light with quadratic radial falloff. Lifting noise
  or blowing out corners is a reason to reduce it. For a directional light change,
  use the existing masked photographic operations instead.
- `center`: normalized source optical center, default `[.5,.5]`. Profiles are not
  loaded; do not claim camera-calibrated correction or apply guessed EXIF matches.

TCA/vignette precede grading. Radial distortion shares final output geometry;
`geometry.autoCrop` trims exposed borders or, if false, rejects them. Inspect
returns SOURCE-coordinate frames before radial/output geometry, with input optics
visible. View/export show the warped result. Masks and patches move with the
image, so use inspect frames rather than coordinates from a warped preview.

Check full-frame composition and multiple native edges together. This radial
scale is not a defringe control, longitudinal CA restoration, fisheye conversion,
or an exact simulation of a lens. Old input may already be corrected. Zero is
appropriate when no optical defect or requested effect is visible. Effects are
baked in PSD; recipes remain editable in the Façade project.

## Narrow colored fringes

`defringe` is a normal edit in `upsertEdits`, with masks/opacity, separate from
`patch.optics`. Retrieve its operation schema. Use it for a narrow unwanted
color peak beside a luminance edge; use TCA for actual radial misalignment of
channels. Apply TCA first, then defringe before strong grading/sharpening.

Select suspect **OKLCh** hues (not HSL degrees), using color probes if uncertain.
One to six ranges support arbitrary hues, including blue/yellow. `radius` is
1–12 native pixels; start near the observed fringe width. `amount` controls
suppression; `edgeThreshold` and `chromaThreshold` reject weak contrast/color
peaks. Common masks limit correction but not neighbor sampling.

Compare the same native edges and nearby genuine colored material. A two-sided
peak test protects broad uniform color, but real thin threads, reflections and
colored lights can also qualify. Mask these out or leave ambiguous edges alone;
do not equate selected pixels with proven optical defects. No suitable nearby
color reference can mean little/no correction. This does not restore focus.

`facade_view(revisions=[candidate], effect_mask_id="edit-id", crops=[...])`
overlays effective correction coverage in magenta. It accounts for strength,
opacity and mask at the edit's stack position, then follows final geometry.
Use a revision containing that defringe edit. This diagnostic cannot combine
with `mask_id` or delivery sizing. Inspect unmarked full frames and details too;
overlay coverage is not a quality score. Ordinary PSD export bakes this edit;
native Photoshop adjustment translation is unsupported.
