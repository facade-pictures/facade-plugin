# Light, material color and photographic finish

Use this when choosing a color/tonal treatment, resolving mixed light, shaping a
palette or interpreting a mood/reference. Correction and finish are judged
against the requested photograph. Technical neutrality, uniform skin, recovered
shadows and saturated colors are not universal goals; a second pass is useful
only when the picture warrants it.

## Establish the intended relationships

Identify the requested change and preserved relationships: light direction,
material identity, skin variation, atmosphere, texture, composition or accurate
product color. Keep explicit constraints distinct from inferred preferences.
A narrow cast correction does not imply restyling; an artistic request may
require coordinated tonal, chromatic and spatial changes. Subtle appearance
can require large control changes, so judge the render rather than slider size.

The same source supports different decisions:

| Intent | Possible treatment | Preserve/check |
|---|---|---|
| Neutral catalog rendering | Reduce unwanted illumination bias using applicable anchors | Product color, texture and diffuse whites; a pleasing match is not calibrated accuracy |
| Warm evening atmosphere | Shape amber/rose warmth and cool/warm separation | Light character; white objects need not become paper white |
| Keep club lighting expressive | Refine palette and light masses, retaining colored skin/reflections | Person and room still share illumination |
| More natural skin within colored surroundings | Local correction of unwanted midtone contamination | Colored rim, other exposed skin and transitions into clothes |
| Graphic monochrome | Channel mix, tonal placement and local separation | Requested silhouette, black masses and purposeful lost detail |

These are hypotheses, not genre presets. Different skin tones, high/low-key
images, fog, deliberate grain and already successful photographs need different
choices, including no correction. A reference can supply relationships without
supplying transferable RGB targets or settings. For a series, carry the intent
forward but reassess each frame's light, exposure, colors and coverage.

## Diagnose the source of color

Distinguish an unwanted global cast, separate illuminants, reflected color,
intrinsic material color, makeup and an existing grade. Use relationships
between surfaces as evidence; do not claim to recover a material's true color
from an ambiguous photograph. If the cause changes the treatment, consult
[measurements and probes](color-and-measurements.md).

| Evidence and desired change | Façade candidates | Main check |
|---|---|---|
| Foundational RAW WB/exposure error | `patch.develop`; read [RAW development](raw-development.md) | Complete rerender, highlights and affected masks |
| Coherent unwanted cast in rendered RGB | `white_balance` | Other materials and light sources still work |
| Different treatment under separate lights | Masked WB/color controls; gradient or brush for soft falloff | Lighting transition and adjacent surfaces |
| A material/color family needs a different hue/chroma/lightness | `oklch`, `hsl` or `selective_color` | Other objects sharing the hue and material texture |
| Desired shadow/midtone/highlight color relationship | `color_balance`, `color_grading` or channel curves | Tonal depth, hue transitions and protected areas |
| Dullness or separation is primarily tonal | `curves`, `exposure`, appropriate local contrast | Light hierarchy, texture and color side effects |

Fetch the needed operation schemas; these candidates are not a fixed sequence.
Use the simplest sufficient coverage. Hue selection does not identify objects.
For directional falloff or screen/window glow, read [local light](local-light.md);
for mask/patch mechanics, read [local edits](local-edits.md). Luminance/color
masks use source information: reassess coverage after development/input-optics
changes. Stronger corrections cannot repair unsuitable coverage.

## Artistic mood and light hierarchy

A mood or style reference can imply coupled changes to hue, tonal density, lighting and material contrast. Identify which relationships produce the requested impression before choosing operations. For example, dark blue neon may need dense blue surfaces, isolated cyan highlights, violet reflections and luminous colored skin. These are options supported by that scene, not a universal blue-to-purple recipe.

Judge the large light masses at full-frame size. A broad bright wall can compete with a person even when the person is correctly exposed. Darkening middle tones while retaining selected reflections may create more drama than increasing saturation. Preserve differences between metal glints, fabric, skin and deep space instead of giving every surface the same color treatment. A reference's exact settings or palette need not transfer, but its visual relationships should inform the result.

## Mixed light and neon

Treat color as a relationship, not a target skin RGB. A white material can retain reflected light and shaded color while reading as white. A warm factory can stay warm while its saturation or hue changes slightly to connect to the foreground. Preserving a region's role is not freezing all its pixels.

On skin, distinguish a colored rim/reflection from the dominant color of the midtones. Preserve enough environmental tint and light direction that the subject remains in the room. Removing blue through desaturation alone can leave gray/lilac skin; a global complementary tint can produce green/yellow, waxy skin or a face pasted onto the scene. Inspect face, neck and hands together, in context with nearby clothes. They need not have equal values when lit differently. Assess hue, chroma and luminance separately. Do not force every face toward an orange “healthy skin” preset or a common target lightness.

“Keep skin light” constrains luminance, not color neutrality. In stylized lighting, luminous cyan and pink skin may be the intended result. Preserve or shape those color relationships when supported by the request; do not silently convert a lighting constraint into a natural-skin-color requirement.

For a sweater or wall, decide what is material color and what is reflected light. Avoid neutralizing the face while leaving the entire torso under an unrelated blue wash. Look at the transition and the neighboring light, not only the mask edge. An edge can be perfectly feathered yet the lighting still look incoherent.

Uniformity is appropriate only when unevenness conflicts with the brief.
Preserve meaningful variation from lips, makeup, freckles, complexion and
lighting. A beauty request can support selectively evening out skin tone; a
documentary request may favor retaining variation. Preserve differences between people instead of applying
one skin reference to the whole group. Under difficult/narrow-spectrum light,
do not promise exact color recovery through WB or selective color.

## Eyes after tonal or color changes

If eyes look unusually bright, glassy or detached after a correction, compare
with the source at the same scale before deciding what changed. Check the
relationship between the sclera, iris, pupil, catchlight and surrounding skin.
A colored reflection may be part of the original lighting. When an edit has
made it distracting, a small local tone or chroma adjustment may suffice;
preserve the gaze, eye shape and meaningful catchlights. Do not automatically
whiten eyes or alter their anatomy to compensate for exposure or color work.
Judge the result in the whole face as well as at native detail.

## Selective color with OKLCh

Use `oklch` when separate hue, chroma and lightness controls help; another
operation may already suffice. Fetch its schema. One edit accepts up to 12
ranges; sample actual colors before choosing them.

Illustrative syntax only, not a reusable palette or recommended strength:

```json
{"id":"palette","operation":"oklch","parameters":{"ranges":[
  {"hueCenter":25,"hueRadius":25,"hueFeather":20,
   "hueShift":5,"chroma":20,"lightness":0.025}
]}}
```

- Hue angles differ from HSL. `chroma` is relative percent; `lightness` is
  absolute ΔL. Hue/chroma retain nominal Oklab L, not linear Y or guaranteed
  perceived brightness. A dark berry may need a tonal change instead.
- `hueConvergence` draws hues toward the selected center. Use it only for
  unwanted variation, such as inconsistent makeup or a deliberately simplified
  background palette; inspect lips, fabric, reflections and material variation.
- `lightnessRange` limits coverage by L; `chromaByLightness` weights C changes
  toward shadows/midtones/highlights. These are controls, not scene semantics.
- Near-neutrals are protected by default; hue rotation and multiplicative
  chroma cannot reliably restore color already removed from a gray surface.
  Revisit the preceding desaturation/WB or consider an appropriate local color
  correction instead of repeatedly increasing strength.
- Ranges select from the operation's original input colors. Overlap averages
  deltas when total weight exceeds one; range order is irrelevant. Default gamut
  handling reduces C at fixed L/h, and signed/HDR residual is retained beyond
  the nominal RGB component. Saturation has finite headroom in sRGB.
- Common masks, opacity and blend apply afterward. `color` blend preserves
  linear Y rather than Oklab L. Protect same-hued objects with spatial coverage,
  not an assumed universal skin hue.

Inspect full frame and relevant details for gray/waxy skin, dirty yellows,
flattened stone or implausibly luminous surfaces. Numerical validity does not
rule these out. Raster PSD preserves the appearance; native Photoshop
adjustment translation of `oklch` is unsupported.

## Warmth

“Warmer” is not always more yellow. Warm light can be amber, orange or rose; muddy yellow-green shadows and uniform yellow saturation can look unpleasant even after the technical goal is met. If the direction is ambiguous, compare small changes in hue/chroma with similar luminance. Do not use maximum temperature to repair every aesthetic problem. Preserve meaningful warm/cool separation and neutral anchors without making isolated paper-white cutouts.

## Fashion black-and-white

Establish the main light, the shape of the silhouette and large black/gray/white masses before lifting details. A compelling face need not be the brightest area. Flare, rim light and bright props can be intentional compositional accents; do not automatically suppress them. Deep shadows may simplify a fashion image more effectively than recovering every fold or background object. Conversely, do not crush facial structure or texture merely to imitate “editorial contrast”.

Use channel mix, tonal curve and local contrast according to what they do to the actual image. Compare the full frame at small size for graphic structure, then inspect skin and transitions. A smooth, visible, evenly lit portrait can satisfy generic “good exposure” rules while missing the requested strong visual character.

For neutral black-and-white, verify that unintended residual color is gone.
Toned monochrome may deliberately retain a hue; interpret that distinction
from the brief rather than enforcing zero chroma for every monochrome request.

## Decision comments

Record observable evidence and remaining uncertainty: “skin no longer gray-lilac; blue rim retained; hand matches neck; sweater less saturated, neon still dominant.” Avoid “beautiful”, “satisfied” or a pixel-delta score as the entire justification. A user preference is evidence for that project, not a universal rule for future people or photographs.

If a correction improves an isolated crop but breaks the requested atmosphere
or its surroundings, keep the issue open. Compare the next candidate at the
same scale; a completed polish pass is not proof of resolution.

## Optional background reading

For an unresolved question, see [photographic resources](photographic-resources.md):
portrait lighting, restrained retouching and mixed-light color calibration,
with scope and limitations for each source. These are optional references;
the user's intent and visual comparison decide the treatment.
