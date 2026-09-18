import json
import os

import click

from lyricimg.backgrounds import GRADIENTS, DEFAULT_GRADIENT
from lyricimg.engine import render_lyric
from lyricimg.presets import PRESETS, DEFAULT_PRESET


def _load_records(lyrics_path: str | None, text: str | None) -> dict[str, str]:
    if text:
        return {"output": text.replace(" / ", "\n")}

    if not lyrics_path:
        raise click.UsageError("Provide --lyrics FILE or --text TEXT")

    if lyrics_path.endswith(".json"):
        with open(lyrics_path) as f:
            data = json.load(f)
        return {k: v for k, v in data.items()}

    # TXT: each line is a record, / = newline within record
    records = {}
    with open(lyrics_path) as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if line:
                records[f"lyric_{i:03d}"] = line.replace(" / ", "\n")
    return records


@click.command()
@click.option("--lyrics", type=click.Path(exists=True), help="Input file (JSON or TXT)")
@click.option("--text", type=str, help="Inline lyrics (use ' / ' for newlines)")
@click.option("--preset", type=click.Choice(list(PRESETS.keys())), default=DEFAULT_PRESET,
              show_default=True)
@click.option("--bg", type=click.Choice(list(GRADIENTS.keys())), default=DEFAULT_GRADIENT,
              show_default=True)
@click.option("--fill", type=click.IntRange(10, 100), default=70, show_default=True,
              help="How much text fills the width (10-100%)")
@click.option("--output", "-o", type=click.Path(), default="output", show_default=True,
              help="Output directory or file path")
@click.option("--format", "fmt", type=click.Choice(["png", "webp"]), default="png",
              show_default=True)
def main(lyrics, text, preset, bg, fill, output, fmt):
    """Generate lyric images from text or file input."""
    records = _load_records(lyrics, text)

    os.makedirs(output, exist_ok=True)

    for name, lyric_text in records.items():
        img = render_lyric(lyric_text, preset_name=preset, gradient_name=bg, fill=fill)

        stem = os.path.splitext(name)[0]
        filename = f"{stem}.{fmt}"
        filepath = os.path.join(output, filename)

        save_kwargs = {}
        if fmt == "webp":
            save_kwargs["quality"] = 90

        img.save(filepath, **save_kwargs)
        click.echo(f"  {filepath}")

    click.echo(f"Done: {len(records)} image(s)")


if __name__ == "__main__":
    main()
