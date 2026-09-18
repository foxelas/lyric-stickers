# Lyric Sticker Generator — Plan

## What it does

Takes song lyrics, wraps text to fill a target width (adjustable), renders them onto images with gradient backgrounds in specific aspect ratios (Instagram story, square, etc.), and exports as PNG or Signal-compatible WebP sticker packs.

## Input format

- **Table input** (webapp): each row = one lyric record. `/` within a row = forced newline.
- **TXT file upload**: each line = one record, `/` = forced newline. Auto-fills the table.
- **CLI**: `--lyrics file.txt` or `--text "line 1 / line 2"`

## Key behavior

- Text wraps to fill the target image width (minus padding). A **fill slider** (0–100%) controls how aggressively text fills the width — low = short centered lines, high = text spans edge to edge.
- One bundled font for now (Inter or similar open-source sans-serif).
- A few preset gradient backgrounds: muted pastel, dark moody, warm sunset, cool ocean.
- Each lyric record → one image/sticker.

## Project structure

```
lyric-stickers/
├── lyricimg/
│   ├── __init__.py
│   ├── engine.py        # Text layout + image rendering (Pillow)
│   ├── backgrounds.py   # Gradient presets
│   └── presets.py       # Aspect ratio definitions
├── fonts/
│   └── Inter-Regular.ttf
├── static/              # Webapp frontend files
│   ├── index.html
│   ├── style.css
│   └── app.js
├── cli.py               # CLI entry point (click)
├── app.py               # FastAPI webapp
├── requirements.txt
└── dev/
    └── plan.md
```

## Presets

| Name | Size | Ratio |
|------|------|-------|
| `instagram-story` | 1080×1920 | 9:16 |
| `square` | 1080×1080 | 1:1 |
| `instagram-post` | 1080×1350 | 4:5 |
| `signal-sticker` | 512×512 | 1:1 |

## Gradient presets

| Name | Colors (top → bottom) |
|------|----------------------|
| `pastel` | #ffecd2 → #fcb69f |
| `moody` | #1a1a2e → #16213e |
| `sunset` | #fa709a → #fee140 |
| `ocean` | #667eea → #764ba2 |
| `mint` | #a8edea → #fed6e3 |

## CLI usage

```bash
python cli.py --lyrics songs.txt --preset square --bg moody --fill 70 --output ./out/
python cli.py --text "hello world / second line" --preset instagram-story --output hello.png
```

## Webapp

- **FastAPI** backend reusing `lyricimg/` — serves API + static files
- **Frontend**: left panel = lyrics table + file upload + controls (preset dropdown, bg picker, fill slider); right panel = live preview
- **Endpoints**: `POST /api/preview`, `POST /api/render` (PNG), `POST /api/sticker-pack` (ZIP of WebP)

## Deployment (later)

Cheapest Python webapp hosting options:
- **Render.com** — free tier for web services, sleeps after 15min inactivity
- **Fly.io** — free allowance, stays warm
- **Railway** — $5/mo hobby plan
- **Hugging Face Spaces** — free, but less control over custom UI

All support Docker or direct Python deploy. Repo stays on GitHub regardless.

## Implementation order

1. `presets.py` + `backgrounds.py` — data definitions
2. `engine.py` — text layout + Pillow rendering (core of everything)
3. `cli.py` — working CLI
4. `app.py` + `static/` — webapp with live preview
5. Signal sticker pack export (ZIP of 512×512 WebP)
6. Test, tune spacing, polish
