---
title: Backlog — ideas not scheduled
type: index
status: current
updated: 2026-09-02
tags: [backlog, ideas, tooling]
---

# Backlog

Ideas worth keeping but **not scheduled**. Nothing here blocks the doc work in
[NEXT-SESSION.md](NEXT-SESSION.md); nothing here has an owner or a date. An item leaves this file
by becoming a batch in the manifest, an ADR, or a deleted line.

| Item | Kind | Why it is here |
|---|---|---|
| [Editable AI diagrams — Excalidraw + Mermaid](#editable-ai-diagrams--excalidraw--mermaid) | Tooling | This vault has 70+ Mermaid diagrams; making them editable on a canvas is a weekend project, not a platform build |

---

## Editable AI diagrams — Excalidraw + Mermaid

**The idea:** generate a diagram from a prompt, then *edit it by hand* — the thing eraser.io sells.
It is three open-source packages wired together, no proprietary piece.

The component that closes the loop is **`@excalidraw/mermaid-to-excalidraw`** — Excalidraw's own
official parser. Feed it a Mermaid string and it returns **native, editable Excalidraw elements**,
not a static image.

```javascript
import { parseMermaidToExcalidraw } from "@excalidraw/mermaid-to-excalidraw";
import { convertToExcalidrawElements, Excalidraw } from "@excalidraw/excalidraw";

// 1. Ask Claude to output only valid Mermaid syntax
const mermaidCode = await callClaude(userPrompt, {
  system: "Output only valid Mermaid syntax. No prose, no markdown fences."
});

// 2. Parse it into Excalidraw's skeleton format
const { elements, files } = await parseMermaidToExcalidraw(mermaidCode);

// 3. Convert skeleton → fully-qualified Excalidraw elements
const excalidrawElements = convertToExcalidrawElements(elements);

// 4. Drop them on the canvas — now the user can drag, recolor,
//    add hand-drawn annotations, delete a box, whatever
<Excalidraw initialData={{ elements: excalidrawElements, files }} />
```

### The trade-off to know before choosing a diagram language

The converter **exists only for Mermaid**. There is no D2 equivalent. So:

| | Mermaid | D2 |
|---|---|---|
| On the Excalidraw canvas | **Native editable elements** — grab a box, drag it | A static SVG/image element — move and resize only |
| Auto-layout on tangled architecture diagrams | Weaker | Nicer |
| Verdict | **Default to this** | Reach for it only when Mermaid's layout engine gives up |

This matters for the vault specifically: everything in `interview-prep/` is already Mermaid (see
[../interview-prep/diagrams/components.md](../interview-prep/diagrams/components.md)), so every
existing diagram would drop onto the canvas as editable elements with no conversion work.

### Self-hosting the collaboration piece

Real-time collab is not something to build either — it is
**`excalidraw/excalidraw-room`**, the same Socket.IO server behind excalidraw.com's live
collaboration, and it is open source. Two community bundles package frontend + room server +
storage into one Docker Compose file and are the more actively maintained ones:

- `alswl/excalidraw-collaboration`
- `BetterAndBetterII/excalidraw-full`

Clone, `docker compose up`, done — this would sit on the Rocky Linux box alongside everything else.

### Minimal project shape

```
/app
  /api/generate-diagram   # POST → calls Claude, returns a Mermaid string
  /components/Canvas.tsx  # Excalidraw + parseMermaidToExcalidraw glue
docker-compose.yml        # excalidraw-room + storage backend, if collab is wanted
```

The hard parts — canvas rendering, hand-drawn styling, Mermaid parsing — are already solved by the
libraries. This is wiring, not construction.

### If it is ever picked up

Two questions to answer first, because they decide whether it is worth doing at all:

1. **What does it give this vault that GitHub's native Mermaid rendering does not?** The honest
   answer is *editing and annotation*, not display — so the use case is "sketch on top of a diagram
   while drilling", not "read the docs".
2. **Where does the edited version live?** If an edited diagram cannot round-trip back to Mermaid
   in the repo, it becomes a second, diverging copy — the exact failure mode
   [../interview-prep/patterns/materialized-views-and-derived-data.md](../interview-prep/patterns/materialized-views-and-derived-data.md)
   warns about. Either it round-trips, or it is explicitly a scratch surface with no source of
   truth claim.

## See also

- [NEXT-SESSION.md](NEXT-SESSION.md) — what *is* scheduled
- [../STATUS.md](../STATUS.md) — where work stopped
- [../interview-prep/diagrams/components.md](../interview-prep/diagrams/components.md) — the Mermaid vocabulary this would consume

## Referenced by

- [Docs index](README.md)
- [STATUS](../STATUS.md)

## Sources

- [`@excalidraw/mermaid-to-excalidraw`](https://github.com/excalidraw/mermaid-to-excalidraw)
- [`@excalidraw/excalidraw`](https://github.com/excalidraw/excalidraw)
- [`excalidraw/excalidraw-room`](https://github.com/excalidraw/excalidraw-room)
