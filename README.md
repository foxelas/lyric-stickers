# lyric-stickers

Generate styled lyric images and sticker packs from song lyrics.

## Setup

```bash
pip install -r requirements.txt
```

## CLI Usage

```bash
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

From a JSON file (each key → one image):

```bash
python3 cli.py --lyrics data/sadam.json --preset square --bg sunset --fill 80 -o output
```

Inline text (`/` splits lines):

```bash
python3 cli.py --text "first line / second line" --preset instagram-story --bg moody -o output
```

From a TXT file (each line → one image, `/` = newline within image):

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
| `square` | 1080×1080 | 1:1 |
| `instagram-story` | 1080×1920 | 9:16 |
| `instagram-post` | 1080×1350 | 4:5 |
| `signal-sticker` | 512×512 | 1:1 |

### Gradients

| Name | Style |
|------|-------|
| `pastel` | Warm peach → salmon |
| `moody` | Dark navy → dark blue |
| `sunset` | Pink → yellow |
| `ocean` | Blue → purple |
| `mint` | Teal → pink |
