# lyric-stickers

Generate styled lyric images and sticker packs from song lyrics.

## Web App

The web app runs entirely in the browser (Canvas API) — no backend needed.
Open `docs/index.html` locally or deploy it as a static site.

### Local preview

```bash
# Option A: just open the file
open docs/index.html

# Option B: run a local server (needed for file upload to work in some browsers)
python3 -m http.server 8000 --directory docs
```

## CLI Usage

The CLI uses Python + Pillow for batch image generation.

```bash
pip install -r requirements.txt
python3 cli.py [OPTIONS]
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--lyrics PATH` | Input file (JSON or TXT) | — |
| `--text TEXT` | Inline lyrics (`/` = newline) | — |
| `--preset` | `square`, `instagram-story`, `instagram-post`, `signal-sticker` | `square` |
| `--bg` | `pastel`, `moody`, `sunset`, `ocean`, `mint` | `moody` |
| `--fill N` | How much text fills the width (10–100%) | `70` |
| `-o, --output PATH` | Output directory | `output` |
| `--format` | `png` or `webp` | `png` |
| `--help` | Show help | — |

### Examples

From a JSON file (each key -> one image):

```bash
python3 cli.py --lyrics data/sadam.json --preset square --bg sunset --fill 80 -o output
```

Inline text (`/` splits lines):

```bash
python3 cli.py --text "first line / second line" --preset instagram-story --bg moody -o output
```

From a TXT file (each line -> one image, `/` = newline within image):

```bash
python3 cli.py --lyrics songs.txt --preset instagram-post --bg mint --format webp -o stickers
```

### Input formats

- **JSON**: `{"image_name": "line 1\nline 2", ...}` — each key becomes the output filename
- **TXT**: one record per line, ` / ` within a line becomes a newline in the image
- **Inline**: `--text "line 1 / line 2"`

### Presets

| Name | Size | Ratio |
|------|------|-------|
| `square` | 1080x1080 | 1:1 |
| `instagram-story` | 1080x1920 | 9:16 |
| `instagram-post` | 1080x1350 | 4:5 |
| `signal-sticker` | 512x512 | 1:1 |

### Gradients

| Name | Style |
|------|-------|
| `pastel` | Warm peach -> salmon |
| `moody` | Dark navy -> dark blue |
| `sunset` | Pink -> yellow |
| `ocean` | Blue -> purple |
| `mint` | Teal -> pink |

## Deployment

### GitHub Pages (static site, free)

The web app is fully client-side — deploy `docs/` to GitHub Pages:

1. Go to repo **Settings > Pages**
2. Set source to **Deploy from a branch**
3. Set branch to `main` and folder to `/docs`
4. Your app is live at `https://<username>.github.io/lyric-stickers/`

### Docker (self-hosted)

A Dockerfile is included for running the full Python backend version (FastAPI + Pillow):

```bash
docker build -t lyric-stickers .
docker run -p 8000:8000 lyric-stickers
```

This runs the FastAPI server at `http://localhost:8000`.

Deploy the container to any host that runs Docker:

| Platform | Cost | Notes |
|----------|------|-------|
| **Render.com** | Free tier | Sleeps after 15min inactivity |
| **Fly.io** | Free allowance | Stays warm, good free tier |
| **Railway** | ~$5/mo | Simple deploy from GitHub |
| **PikaPods** | ~$1/mo | One-click open-source app hosting |

### Local dev server (FastAPI)

```bash
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

## Credits

Made by foxelas.
