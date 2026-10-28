# Cursor host

Use the shared photographic skill and Façade MCP tools.

## Folder gallery

For “show this folder”, “gallery” or “browse my photos”, call
`facade_gallery_open(folder=...)` once. Cursor does not render the Codex
`display` visualization token. Open the returned `standalonePath` in the system
browser: it is the complete self-contained gallery, with every source preview.
The agent browser rejects `file://`. Do not rewrite the HTML, build a contact
sheet, or take another model turn to scroll, open a frame, move with the
arrows, or return to the grid. Those actions stay inside the page.

The page shows source previews, not accepted edits or exports. Use the
displayed number with `sourceNames` or `manifestPath`. Reopen only when the
folder changed or the user asks to refresh.

There is no verified control in this host that reveals the processed export of
the selected frame in Finder. Do not draw that button, send a chat message as
a stand-in for the click, open the original, or choose the newest JPEG. If the
user asks, say the page cannot call the local backend.

## Show the picture in the chat

The person using Cursor wants to see the photograph in the transcript. A path, and a Read of that file, show the picture to the model only.

- Prefer the Façade MCP tools. An `image` block they return is attached to the chat. Do not repeat that same image as markdown.
- When the tool returns only a file path, put one markdown image in the reply, with the absolute path: `![До и после](/absolute/path.jpg)`. That is how a local JPEG appears in this Mac chat. One sheet is enough.
- For a result or a requested comparison, build one side-by-side with `facade_view(layout="comparison", revisions=[...], labels=[...])` and show that sheet. Label the columns in the user's language, and name which revision each column is. There is no before/after slider.
- Do not paste a stack of diagnostic crops into the chat. Crops stay in the review. The transcript gets the whole-frame comparison, unless the user asked to see one detail.

## Marks on a picture

Cursor does not send Codex-style notes: a pin, a comment, and coordinates for several regions. What arrives is the picture itself.

- The user can attach an image, open it, and draw on it. The ink is part of the image the model sees. Treat a circle or stroke as the area they mean, and say which object that is. In the IDE chat viewer a saved mark on a wide image can shift toward the center; a mark made in the Agents Window stays where it was drawn. If the mark and the words disagree, ask which place they meant.
- Design Mode drawing is for a browser page, not a photograph. Do not send the user there to mark a photo.
- A photo attached from Cursor on iPhone or iPad can include a point or a drawing. Use that mark the same way.
- Several separate comments on one frame are not a Cursor payload. Words, or a separate image per note, are the way those notes arrive.
