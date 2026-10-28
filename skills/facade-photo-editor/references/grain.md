# Grain and noise

Use grain when the requested appearance benefits from it; preserve deliberate
source grain. Read `grain_texture` capabilities. Legacy `grain` retains its old
rendering, so do not silently substitute a new renderer in an existing edit.

`kind` chooses Gaussian, bounded uniform innovations or sparse film-like grains.
`size` is sigma in current pixels. `sizeVariation` mixes smaller/larger grains;
`clumping` varies local strength. Both zero gives a stationary single scale.
Film is an artistic approximation without measured stock or ISO profiles.
Gaussian/uniform may look similar on a photograph; shape and spatial structure
often matter more than the distribution name.

`color:0` adds mono grain to a color image, not monochrome conversion.
`shadows/midtones/highlights` control strength at encoded luminance 0/.5/1;
all 100 is flat. `protectExtremes` fades near black/white. Strong coarse/clumped
noise can look like blotches or damaged skin. Judge at the requested output
size and use weaker/local application when that is not the intended look.

For global grain at a final size, prefer `delivery.grain`: it runs after resize
and output sharpening, with size in output pixels. Reuse identical delivery in
view/diagnose/export/finish. Settings live in the export sidecar; reopening the
native project alone does not apply output grain. Use the saved sidecar's
revision and delivery settings to reproduce a delivered file.

For masks or grain that subsequent edits should process, use a native
`grain_texture` edit. It persists in revisions and follows the common mask and
opacity contracts. Native and output grain accumulate; avoid adding both by
accident. Existing noise remains unless deliberately reduced beforehand.

Inspect clean versus grain-on exports at matching size, including a smooth
field and skin/edge at 1:1. Small previews/JPEG can hide or reshape grain.
`diagnose` applies identical delivery to both frames and cannot isolate a
delivery-only grain change; supplement it with this clean/on comparison.
Native grain revisions can be diagnosed against their parent. Deliberate noise
may trigger artifact candidates; scores are not automatic reasons to denoise.
