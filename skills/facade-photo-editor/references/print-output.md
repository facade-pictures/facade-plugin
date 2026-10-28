# Print output and CMYK

Use this workflow when the user requests CMYK or a provider-specific print file.
Use the ICC supplied for the actual printer/paper/process; do not substitute an
arbitrary generic profile. If no target profile is available, finish independent
RGB edits and clarify the missing print condition before converting.

Register it with `facade_print_profile(project, expected_version, profile_path,
comment)`. The returned `printProfile.id` identifies immutable copied bytes.
Registration increments project version only for a new profile. State lists
registered profiles. No RGB edits or acceptance are changed.

Call `facade_proof` with `print_output` containing `profile_id`, intent
(`relative-colorimetric` or `perceptual`), `black_point_compensation`, `bit_depth`
(8 or 16), and `dpi`. Optional `ink_limit_percent` is a reporting threshold,
never an automatic clamp. The profile governs separation and black generation.

Inspect paired RGB/proof images, using `simulate_paper=true` when paper-white
simulation is useful. Full-frame overview is approximate because it is resized
before separation. Request up to two native delivered-pixel crops (4 MP each)
for important shadows, skin, gradients or fine texture. Ink metrics cover only
those inspected pixels; export reports all delivered pixels. Screen proof is
limited by display gamut/calibration and cannot certify a physical print.

If useful, make ordinary RGB edits as a candidate and proof that revision again.
Avoid lifting every shadow merely because paper has less contrast. Preserve the
user's intent. Dust removal still needs visually verified targets and donors;
profile conversion performs no defect detection. Leave a good proof unchanged.

Reuse identical `print_output` and `delivery` in `facade_export` or
`facade_finish`. CMYK is TIFF-only; omission of output/format selects TIFF.
`dpi` is resolution metadata, not a pixel resize. `delivery.longEdge` resizes;
`patch.geometry` controls framing. Report physical size from the export, the
profile used and any exceeded ink limit. The source and RGB project remain
editable. 16-bit CMYK acceptance depends on the print provider; use requested
8-bit output when necessary. Do not re-import the CMYK TIFF for further edits.
