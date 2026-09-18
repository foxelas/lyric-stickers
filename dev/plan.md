# Lyric Image & Sticker Pack Generator — Implementation Plan

## Context

Build a tool that takes song lyrics, lays them out line-by-line (quote-card style), and renders them as images in specific aspect ratios (Instagram story 9:16, square 1:1, etc.) with subtle gradient backgrounds. Also generates Signal-compatible sticker packs (512×512 WebP). Two phases: Python CLI first, then a browser-based app.

---

## Phase 1: Python CLI Tool

### 1.1 Project Structure

```
lyric-sticker/
├── lyricimg/
│   ├── __init__.py
│   ├── core.py          # Text layout engine
│   ├── renderer.py      # Image rendering (Pillow)
│   ├── backgrounds.py   # Gradient/subtle background generators
│   ├── fonts.py         # Font loading & management
│   ├── stickers.py      # Signal sticker pack export
│   └── presets.py       # Aspect ratio presets
├── fonts/                # Bundled open-source fonts
├── cli.py               # CLI entry point
├── requirements.txt
└── README.md
```

### 1.2 Core Modules

**`presets.py` — Aspect ratio definitions**
- `INSTAGRAM_STORY`: 1080×1920 (9:16)
- `INSTAGRAM_SQUARE`: 1080×1080 (1:1)
- `INSTAGRAM_POST`: 1080×1350 (4:5)
- `SIGNAL_STICKER`: 512×512 (1:1)
- Custom ratio support via CLI args

**`core.py` — Text layout engine**
- Parse lyrics text (split by newlines, handle blank lines as section breaks)
- Auto-size font to fit the canvas with padding
- Center-align text vertically and horizontally
- Handle long lines: shrink font or soft-wrap
- Return a layout spec: list of `(text, x, y, font_size)` tuples

**`backgrounds.py` — Gradient generators**
- Linear gradient (top-to-bottom, configurable two colors)
- Radial gradient (center-out)
- Preset palettes: muted pastels, dark moody, warm sunset, cool ocean
- User-specified hex colors

**`renderer.py` — Image rendering with Pillow**
- Takes layout spec + background + font → renders final PIL Image
- Text rendering with anti-aliasing
- Optional subtle text shadow for readability
- Export as PNG (full-size images) or WebP (stickers)

**`stickers.py` — Signal sticker export**
- Split lyrics into chunks (one sticker per line or per couplet)
- Render each chunk at 512×512 WebP
- Package into a directory ready for upload via [Signal sticker tools](https://github.com/nickoala/nicko-sticker-packs) or signalstickers.com
- Generate a manifest/metadata file

**`fonts.py` — Font management**
- Bundle 3-4 open-source fonts (e.g., Inter, Playfair Display, Caveat, JetBrains Mono)
- Load custom .ttf/.otf from a path
- Font selection via CLI flag

### 1.3 CLI Interface

```bash
# Basic usage — generates PNG
python cli.py --lyrics "lyrics.txt" --preset instagram-story --output out.png

# With styling
python cli.py --lyrics "lyrics.txt" --preset square \
  --font playfair --bg-style gradient \
  --bg-colors "#1a1a2e,#16213e" --text-color "#eee" \
  --output out.png

# Generate sticker pack
python cli.py --lyrics "lyrics.txt" --sticker-pack \
  --output ./stickers/
```

### 1.4 Dependencies

- **Pillow** — image rendering
- **click** — CLI framework
- **numpy** — gradient math (optional, Pillow can do basic gradients)

---

## Phase 2: Browser-Based App

### 2.1 Architecture

**Recommended: FastAPI backend + vanilla HTML/JS/CSS frontend**

Why this approach:
- Reuses all Phase 1 Python code (core, renderer, backgrounds) without rewriting
- FastAPI serves the API and static frontend files — single deployment
- No React/build tooling overhead for what is essentially a form + preview
- Server-side rendering means consistent output across browsers
- Easy sticker pack ZIP generation server-side

### 2.2 Backend (FastAPI)

**Endpoints:**
- `POST /api/preview` — accepts lyrics + settings, returns a preview image (lower res)
- `POST /api/render` — accepts lyrics + settings, returns full-res PNG
- `POST /api/sticker-pack` — accepts lyrics + settings, returns ZIP of WebP stickers
- `GET /api/presets` — returns available presets, fonts, palettes
- `GET /` — serves the frontend

### 2.3 Frontend (vanilla HTML/JS/CSS)

Simple single-page app:
- **Left panel**: textarea for lyrics, dropdowns for preset/font/palette, color pickers for custom colors
- **Right panel**: live preview of the rendered image (updates on change with debounce)
- **Export buttons**: "Download PNG", "Download Sticker Pack (ZIP)"
- Responsive layout (works on mobile too)
- No build step — plain files served by FastAPI

### 2.4 Frontend Dependencies

- None required (vanilla JS + CSS)
- Optional: a lightweight CSS framework like Pico CSS for clean defaults

---

## Implementation Order

| Step | What | Deliverable |
|------|------|-------------|
| 1 | Set up project, `presets.py`, `fonts.py` | Project scaffold, font loading |
| 2 | `core.py` — text layout engine | Auto-sizing, centering, wrapping |
| 3 | `backgrounds.py` — gradient generators | Gradient background images |
| 4 | `renderer.py` — Pillow rendering | End-to-end PNG output |
| 5 | `cli.py` — CLI with click | Working CLI tool |
| 6 | `stickers.py` — Signal sticker export | Sticker pack directory + WebP |
| 7 | Test with real lyrics, tune spacing/sizing | Polished output |
| 8 | FastAPI backend + API endpoints | Server-side rendering API |
| 9 | Frontend HTML/JS/CSS | Browser UI with live preview |
| 10 | Sticker pack ZIP download in browser | Full browser feature parity |

---

## Verification

- **Phase 1**: Run CLI with sample lyrics, visually inspect output PNGs at each preset ratio. Verify sticker pack WebP files are 512×512 and under 300KB (Signal limit).
- **Phase 2**: Start FastAPI server, open browser, enter lyrics, verify live preview updates. Download PNG and sticker ZIP, inspect outputs.
