# RAW development and photographic edits

Use the same create/edit/variants/view/finish workflow. A RAW project retains the immutable original, decoder version and development settings per revision. `original` is the initial development, not the camera's embedded JPEG. `state(revision=...)` returns `selectedDevelop` beside `selectedPlan`.

Use `patch.develop` for a foundational white-balance error, exposure before decoder output, or highlight recovery. Use ordinary edits for mood, local illumination, palette, curves and material contrast. RAW exposure and RGB exposure can overlap; do not apply both automatically. Changing development rerenders all subsequent edits and source-dependent masks. Review the complete photo and relevant native details after the change.

Example patch, applied together with any ordinary edit changes:

```json
{"develop":{"whiteBalance":{"mode":"camera","warmth":-8,"tint":2},"exposure":-0.3,"highlightRecovery":"blend"}}
```

- `whiteBalance.mode`: `camera` or `daylight`. `warmth` and `tint` are relative sensor-channel shifts from -100 to 100, not calibrated Kelvin. Positive warmth increases red relative to blue; positive tint reduces green. The whole whiteBalance object is replaced, so carry forward values you want to keep. Default is camera with zero shifts.
- `exposure`: -2 to +3 EV. Default 0. Unspecified top-level develop fields survive; set default values explicitly to reset. Rendered inputs reject these controls.
- `preserveHighlights`: 0 to 1, default 0. Protects bright tones when raising RAW exposure. This is separate from reconstructing clipped sensor channels; compare clouds/white fabric and watch for dull highlights.
- `highlightRecovery`: `blend` (default), `clip`, or `reconstruct`. Reconstruction estimates missing color information and can create false color; inspect the result. It cannot guarantee recovery where all sensor channels were saturated.

The first adapter uses LibRaw's bounded 16-bit linear sRGB output, then Façade float processing. It is not an unlimited scene-linear pipeline; float conversion does not restore already clipped color or highlights. Retaining the RAW allows redevelopment. A bright preview alone does not establish sensor clipping. Do not promise camera JPEG/Lightroom color parity or infer camera coverage from a filename extension.

The tool reports decoder versions and any missing-camera-WB fallback in renderStats.sourceInfo. Decoder mismatch fails explicitly to protect old revisions. Never silently change versions or substitute the embedded JPEG. Algorithm, orientation and camera crop are backend responsibilities, not aesthetic controls.

Use `facade_raw(project)` when RAW layout/clipping diagnostics would change the next decision. It reports mosaic versus decoded stack; mRAW/sRAW/linear stacks cannot provide original photosite clipping. Mosaic clipping is an estimate against declared levels, not proof of recoverability. `sourceInfo.rgbClipping` measures the decoder's separate RGB output boundary.

For uncertain WB/exposure choices, `facade_raw(project, revision="current", previews=[{"exposure":1}, {"exposure":1,"preserveHighlights":0.8}])` returns base plus independent, approximate **development-only** previews. Existing photographic edits and masks are excluded; this is not the accepted finished photo. Safe Bayer geometry uses half-size decoding; stacks and other layouts use native decoding then resizing. These probes save no candidates and cannot be accepted or exported. Apply chosen fields through `facade_edit(patch={"develop":...}, base_revision=...)` using the same base and returned project version, inspect the native result with its photographic edits, then finish normally. Never use a reduced preview to certify fine detail, mask boundaries or highlight recovery.
