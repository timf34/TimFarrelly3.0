"""
Convert all painting source files to optimized WebP format.

Outputs into public/paintings/:
  - {slug}.webp        — full-size, max 2000px longest edge, quality 90
  - {slug}-thumb.webp   — thumbnail, max 600px longest edge, quality 75

Run: pip install Pillow && python scripts/process_paintings.py
"""

import os
from pathlib import Path
from PIL import Image

# Project root (script lives in scripts/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOWNLOADS_DIR = PROJECT_ROOT / "public" / "paintings" / "downloads"
OUTPUT_DIR = PROJECT_ROOT / "public" / "paintings"

FULL_MAX = 2000
FULL_QUALITY = 90
THUMB_MAX = 600
THUMB_QUALITY = 75

# Mapping: slug -> source filename in downloads/
PAINTINGS = {
    "isle-of-the-dead": "isle_of_the_Dead.jpg",
    "carnation-lily-lily-rose": "John_Singer_Sargent_-_Carnation,_Lily,_Lily,_Rose_-_Google_Art_Project.jpg",
    "two-men-contemplating-the-moon": "two_men_contempating_the_moon.jpg",
    "achill-horses": "m-jellett-achill-horse-homepage.jpg",
    "vertumnus": "Vertumnus_årstidernas_gud_målad_av_Giuseppe_Arcimboldo_1591_-_Skoklosters_slott_-_91503.tiff.jpg",
    "course-of-empire-destruction": "Cole_Thomas_The_Course_of_Empire_Destruction_1836.jpg",
    "winter-landscape": "winter_landscape.png",
    "singing-horseman": "singing_horseman_jb_yeats.jpg",
    "hope": "George_Frederic_Watts,_1885,_Hope.jpg",
    "rokeby-venus": "RokebyVenus.jpg",
    "on-board-a-sailing-ship": "on-board-a-sailing-ship.jpg",
    "nighthawks": "nighthawks.jpg",
    "springtime": "spring_time_Claude_Monet-772777.jpg",
    "the-morning": "the-morning.jpg",
    "the-monk-by-the-sea": "the-monk-by-the-sea.jpg",
    "self-portrait-with-death": "self_portrait_with_death.jpg",
    "one-no-31": "no_31_pollock.jpg",
    "ulysses-deriding-polyphemus": "Joseph_Mallord_William_Turner_064.jpg",
    "ulysses-and-the-sirens": "ulysses_and_the_sirens.jpg",
    "nude-binding-her-hair": "nude_binding_her_hair.png",
    "overflow": "overflow.jpg!Large.jpg",
    "the-mountain-mists": "the-mountain-mists.jpg",
    "pieta": "pieta-jellett.jpeg",
    "new-york-movie": "new-york-movie.jpeg",
    "the-lovers": "the-lovers.jpeg",
    "fountain-of-inspiration": "fountain-of-inspiration.jpeg",
    "nude-1916": "nude-1916.jpeg",
    "satans-treasures": "satans-treasures.jpg",
    "engloutissement": "engloutissement.jpeg",
    "october": "october.jpeg",
    "experiment-bird-air-pump": "experiment-bird-air-pump.jpeg",
    "sadko": "sadko.jpeg",
    "covent-garden-brittany": "covent-garden-brittany.jpeg",
    "pandora": "pandora.jpeg",
    "morning-glazunov": "morning-glazunov.jpeg",
    "pygmalion-and-galatea": "pygmalion-and-galatea.jpeg",
    "voyage-of-life-childhood": "voyage-of-life-childhood.jpeg",
    "voyage-of-life-youth": "voyage-of-life-youth.jpeg",
    "voyage-of-life-manhood": "voyage-of-life-manhood.jpeg",
    "voyage-of-life-old-age": "voyage-of-life-old-age.jpeg",
    "bal-tabarin": "bal-tabarin.jpeg",
    "le-ballet": "le-ballet.jpeg",
    "mr-gilhooley-geneva-window": "mr-gilhooley-geneva-window.jpeg",
    "opus-217-felix-feneon": "opus-217-felix-feneon.jpg",
    "sunflowers-petrol-station": "sunflowers-petrol-station.jpeg",
    "atem-breath": "atem-breath.jpeg",
    "siesta": "siesta.jpeg",
    "the-ball": "latouche-ball300.jpg",
    "susanna-at-her-bath": "susanna_at_her_bath.jpg",
    "lament-for-icarus": "Herbert_Draper_-_The_Lament_for_Icarus_-_Google_Art_Project.jpg",
    "ariadne": "ariadne_john_lavery.jpg",
    "graceful-ascent": "graceful_ascent_kandinsky.jpg",
    "of-lilies-and-remains": "of_lillies_and_remains_richard_mosse.jpg",
    "in-morocco": "in_morocco_john_lavery.jpg",
    "catherine-and-midnight": "Catherine and Midnight.jpg",
    "the-chess-game": "John_Singer_Sargent_-_The_Chess_Game.jpg",
    "the-truth": "la_verite.jpg",
    "bernard-and-roger": "bernard-and-roger.jpeg",
    "knight-of-the-flowers": "flower_knight.jpg",
    "anguish": "anguish.jpg",
    "twins": "twins.jpg",
    "how-to-entangle-the-universe-in-a-spiderweb": "how-to-entangle-the-universe-in-a-spiderweb-toms-saraceno-oceans-of-air52557994836o_1240_0.webp",
    "alberi-libro": "giuseppe_penone_Alberi libro (Book Trees).jpg",
    "among-the-olive-trees-capri": "among_the_olive_tress_capri_sargent.jpg",
    "dove": "dove_conor_fallon.jpg",
}


def process_image(src_path: Path, slug: str) -> None:
    img = Image.open(src_path)
    img = img.convert("RGB")

    # Full size
    full = img.copy()
    full.thumbnail((FULL_MAX, FULL_MAX), Image.LANCZOS)
    full_path = OUTPUT_DIR / f"{slug}.webp"
    full.save(full_path, "WEBP", quality=FULL_QUALITY)

    # Thumbnail
    thumb = img.copy()
    thumb.thumbnail((THUMB_MAX, THUMB_MAX), Image.LANCZOS)
    thumb_path = OUTPUT_DIR / f"{slug}-thumb.webp"
    thumb.save(thumb_path, "WEBP", quality=THUMB_QUALITY)

    print(f"  OK {slug} ({img.size[0]}x{img.size[1]} -> full {full.size[0]}x{full.size[1]}, thumb {thumb.size[0]}x{thumb.size[1]})")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    missing = []
    processed = 0

    for slug, filename in PAINTINGS.items():
        src = DOWNLOADS_DIR / filename
        if not src.exists():
            missing.append((slug, filename))
            print(f"  MISSING: {filename} (for {slug})")
            continue
        process_image(src, slug)
        processed += 1

    print(f"\nDone: {processed} paintings processed, {len(missing)} missing")
    if missing:
        print("Missing files:")
        for slug, fn in missing:
            print(f"  - {fn} ({slug})")

    # Count output files
    webps = list(OUTPUT_DIR.glob("*.webp"))
    print(f"Total .webp files in output: {len(webps)}")


if __name__ == "__main__":
    main()
