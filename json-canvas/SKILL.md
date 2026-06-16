---
name: json-canvas
description: Create and edit JSON Canvas files (.canvas) with nodes, edges, groups, and connections. Use when working with .canvas files, creating visual canvases, mind maps, flowcharts, or when the user mentions Canvas files in Obsidian.
---

# JSON Canvas Skill

This skill enables Claude Code to create and edit valid JSON Canvas files (`.canvas`) used in Obsidian and other applications.

## Overview

JSON Canvas is an open file format for infinite canvas data. Canvas files use the `.canvas` extension and contain valid JSON following the [JSON Canvas Spec 1.0](https://jsoncanvas.org/spec/1.0/).

## File Structure

A canvas file contains two top-level arrays:

```json
{
  "nodes": [],
  "edges": []
}
```

- `nodes` (optional): Array of node objects
- `edges` (optional): Array of edge objects connecting nodes

## Nodes

Nodes are objects placed on the canvas. There are four node types:
- `text` - Text content with Markdown
- `file` - Reference to files/attachments
- `link` - External URL
- `group` - Visual container for other nodes

### Z-Index Ordering

Nodes are ordered by z-index in the array:
- First node = bottom layer (displayed below others)
- Last node = top layer (displayed above others)

### Generic Node Attributes

All nodes share these attributes:

| Attribute | Required | Type | Description |
|-----------|----------|------|-------------|
| `id` | Yes | string | Unique identifier for the node |
| `type` | Yes | string | Node type: `text`, `file`, `link`, or `group` |
| `x` | Yes | integer | X position in pixels |
| `y` | Yes | integer | Y position in pixels |
| `width` | Yes | integer | Width in pixels |
| `height` | Yes | integer | Height in pixels |
| `color` | No | canvasColor | Node color (see Color section) |

### Text Nodes

```json
{
  "id": "6f0ad84f44ce9c17",
  "type": "text",
  "x": 0,
  "y": 0,
  "width": 400,
  "height": 200,
  "text": "# Hello World\n\nThis is **Markdown** content."
}
```

| Attribute | Required | Type | Description |
|-----------|----------|------|-------------|
| `text` | Yes | string | Plain text with Markdown syntax |

### File Nodes

```json
{
  "id": "a1b2c3d4e5f67890",
  "type": "file",
  "x": 500,
  "y": 0,
  "width": 400,
  "height": 300,
  "file": "Attachments/diagram.png"
}
```

| Attribute | Required | Type | Description |
|-----------|----------|------|-------------|
| `file` | Yes | string | Path to file within the system |
| `subpath` | No | string | Link to heading or block (starts with `#`) |

### Link Nodes

```json
{
  "id": "c3d4e5f678901234",
  "type": "link",
  "x": 1000,
  "y": 0,
  "width": 400,
  "height": 200,
  "url": "https://obsidian.md"
}
```

| Attribute | Required | Type | Description |
|-----------|----------|------|-------------|
| `url` | Yes | string | External URL |

### Group Nodes

```json
{
  "id": "d4e5f6789012345a",
  "type": "group",
  "x": -50,
  "y": -50,
  "width": 1000,
  "height": 600,
  "label": "Project Overview",
  "color": "4"
}
```

| Attribute | Required | Type | Description |
|-----------|----------|------|-------------|
| `label` | No | string | Text label for the group |
| `background` | No | string | Path to background image |
| `backgroundStyle` | No | string | Background rendering style (`cover`/`ratio`/`repeat`) |

## Edges

Edges are lines connecting nodes.

| Attribute | Required | Type | Default | Description |
|-----------|----------|------|---------|-------------|
| `id` | Yes | string | - | Unique identifier |
| `fromNode` | Yes | string | - | Node ID where connection starts |
| `fromSide` | No | string | - | Side where edge starts (`top`/`right`/`bottom`/`left`) |
| `fromEnd` | No | string | `none` | Shape at edge start (`none`/`arrow`) |
| `toNode` | Yes | string | - | Node ID where connection ends |
| `toSide` | No | string | - | Side where edge ends |
| `toEnd` | No | string | `arrow` | Shape at edge end |
| `color` | No | canvasColor | - | Line color |
| `label` | No | string | - | Text label for the edge |

## Colors

The `canvasColor` type can be specified as hex (`"#FF0000"`) or preset (`"1"`-`"6"`):

| Preset | Color |
|--------|-------|
| `"1"` | Red |
| `"2"` | Orange |
| `"3"` | Yellow |
| `"4"` | Green |
| `"5"` | Cyan |
| `"6"` | Purple |

## ID Generation

Node and edge IDs should be unique 16-character lowercase hex strings, e.g. `"6f0ad84f44ce9c17"`.

## Layout Guidelines

- Coordinates can be negative (canvas extends infinitely)
- Standard spacing: leave 20-50px padding inside groups, 50-100px between nodes
- Align nodes to grid (multiples of 10 or 20) for cleaner layouts

## Validation Rules

1. All `id` values must be unique across nodes and edges
2. `fromNode` and `toNode` must reference existing node IDs
3. `type` must be one of: `text`, `file`, `link`, `group`
4. `fromSide`, `toSide` must be one of: `top`, `right`, `bottom`, `left`
5. `fromEnd`, `toEnd` must be one of: `none`, `arrow`
6. Color presets must be `"1"` through `"6"` or valid hex color

## References

- [JSON Canvas Spec 1.0](https://jsoncanvas.org/spec/1.0/)
- [JSON Canvas GitHub](https://github.com/obsidianmd/jsoncanvas)
