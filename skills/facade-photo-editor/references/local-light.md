# Shape existing light with curves and masks

Use this for a stronger screen/window glow, a quieter room or a more dimensional
portrait. First identify the existing source direction and the surfaces it lights.
Changing their relative brightness can be enough; don't automatically brighten
the subject or add clarity. A bright face against a quieter room can look more
luminous even when its exposure stays unchanged.

Start with the smallest useful combination:

- A broad radial/linear gradient or soft brush describes light falloff.
- `curves` or `exposure` controls its amount. Use `blendMode: "luminosity"` when
  changing tone without deliberately shifting hue; still judge saturation/skin.
- Intersect coverage with `luminance_range` when the change must spare bright
  skin or deep shadows. Ranges are evaluated from the decoded/developed source
  after input optics, **not after the preceding edits**. Inspect coverage after
  changing RAW development/optics; don't compensate for a stale assumption by
  adding more exposure.
- `refinement.smoothness` with `edgeSensitivity` refines an existing boundary.
  It does not identify a person or invent a hair mask. Use it only when a visible
  edge problem warrants it; wide, smooth light transitions often need no refinement.

Example patch, intended for a chosen subject in the central area. Coordinates
and strengths are illustrative, not reusable face positions:

```json
{
  "upsertMasks": [
    {"id":"light-area","type":"radial_gradient",
     "parameters":{"center":[0.52,0.445],"radiusX":0.21,"radiusY":0.31,"feather":1,"rotation":-12}},
    {"id":"light-tones","type":"luminance_range",
     "parameters":{"low":0.18,"high":0.50,"lowFeather":0.12,"highFeather":0.14,"space":"srgb"}},
    {"id":"light-midtones","type":"intersection",
     "parameters":{"inputs":["light-area","light-tones"]}}
  ],
  "upsertEdits": [
    {"id":"screen-light","operation":"curves","maskId":"light-midtones","blendMode":"luminosity",
     "parameters":{"channels":{"rgb":[[0,0],[40,42],[90,100],[150,158],[210,210],[255,255]]}}}
  ]
}
```

Submit the relevant zones together. Compare against the same color-corrected
base to see what the light work actually adds. Inspect face highlights, nearby
hair/wall boundaries and the full frame together. If skin gets flatter or whiter,
reduce the lift or narrow the tonal coverage before adding texture/sharpening.
Feather cannot make an implausible light pattern physically consistent.

This reshapes existing photographic information. It does not move a lamp in 3D,
create reliable new cast shadows or recover clipped features. A new relight
operation is warranted only by a demonstrated control gap, not by this label.
