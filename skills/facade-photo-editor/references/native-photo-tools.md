# Experimental native photo tools (backend 0.3.16+)

Discover `operations=["shadows_highlights","match_color","edge_decontaminate"]`
for exact schemas before use. These are optional experiments, not replacements
for existing tonal/curves/masks, SAM or defringe. Inspect actual photographs and
native boundaries; execution and a plausible mask do not establish quality.
All three operate through an encoded-sRGB 0..1 boundary, at most 8MP. No automatic
black/white clipping or RAW highlight recovery. Old operations retain their behavior.

- `shadows_highlights`: separate amount/tone/native-pixel radius for each side,
  plus color and midtone controls. Compare to curves/masks when halos or loss of
  light hierarchy appear. Defaults have no effect; start with moderate amounts.
- `match_color`: Reinhard-style Lab-D50 mean/std transfer. Use `inspect` with
  `regions`, `measurements=true` on the chosen source project/revision; the response
  gives `measurement.colorStats.output` for regions up to 8MP. Copy its `mean`/`std`
  into `parameters.sourceStats`, and record the exact source/revision in `sourceLabel`
  or the edit comment. Saved numbers replay without the source file. `fade=100`
  disables the effect; higher fade weakens it. A mask also selects target statistics.
  This is color-distribution transfer, not recognition of a reference's composition,
  lighting or aesthetic intent. Do not accept a damaged result merely because the
  statistics match. Without useful measured coverage request another region.
- `edge_decontaminate`: requires a soft `maskId`. Cleans mixed fringe RGB from
  nearby confident foreground; does not change alpha. `radiusPx=3..32`, amount
  0..100. Existing shared destination mask/opacity is applied once afterward.
  Check hair/branches against both light and dark backgrounds; colors can smear.

Quick Selection is a **mask type**, not an edit operation. Use
`capabilities(path="topics/masks")` → `quickSelectionSchema` for exact parameters.
`patch.upsertMasks` type `quick_selection` takes add/subtract strokes with normalized
points and `sizePx` in native source pixels. First stroke adds. The explicit working
long edge defaults to 768 (max 1024), with upsampled coverage; it is not a native
hair mask or learned semantic detector. Use an edit referencing that mask, then
`view(mask_id=...)` to inspect the actual overlay. Refine via strokes rather than
blindly trusting a click. No weights or separate SAM environment are needed.

Any mask's `refinement.colorGuidedRadiusPx=1..32` enables RGB-guided edge refinement
independently of existing scalar smoothness. It estimates coverage, not foreground
color. Keep alpha refinement and RGB decontamination separate when investigating
an edge. PatchMatch remains disabled and is not part of this capability set.
