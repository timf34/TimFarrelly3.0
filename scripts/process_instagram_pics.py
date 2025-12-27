"""
Process Instagram data export to extract monthly photo posts for the Pics:) page.

This script:
1. Reads posts_1.json to find posts titled with month names (e.g., "May", "May, art")
2. Copies and converts images to the public/pics folder
3. Generates a JSON manifest for the Astro page to consume
"""

import json
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
INSTAGRAM_DATA = PROJECT_ROOT / "temp" / "instagram-data"
POSTS_JSON = INSTAGRAM_DATA / "your_instagram_activity" / "media" / "posts_1.json"
MEDIA_SOURCE = INSTAGRAM_DATA / "media" / "posts"
OUTPUT_DIR = PROJECT_ROOT / "public" / "pics"
MANIFEST_PATH = PROJECT_ROOT / "src" / "data" / "pics-manifest.json"

# Month names to filter for (in order)
MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Map month name to number
MONTH_TO_NUM = {name: i + 1 for i, name in enumerate(MONTH_NAMES)}

def is_monthly_post(title: str) -> bool:
    """Check if a post title matches our monthly post pattern."""
    if not title:
        return False
    # Match "Month" or "Month, art"
    for month in MONTH_NAMES:
        if title == month or title == f"{month}, art":
            return True
    return False

def get_month_from_title(title: str) -> int:
    """Extract month number from title like 'May' or 'May, art'."""
    for month in MONTH_NAMES:
        if title.startswith(month):
            return MONTH_TO_NUM[month]
    return 1

def get_year_from_timestamp(timestamp: int) -> int:
    """Extract year from Unix timestamp."""
    return datetime.fromtimestamp(timestamp).year

def get_year_month_from_uri(uri: str) -> tuple[int, int] | None:
    """Extract year and month from URI like 'media/posts/202512/...'."""
    import re
    match = re.search(r'/(\d{6})/', uri)
    if match:
        yyyymm = match.group(1)
        year = int(yyyymm[:4])
        month = int(yyyymm[4:6])
        return (year, month)
    return None

def convert_heic_to_jpg(source: Path, dest: Path) -> bool:
    """Convert HEIC to JPG using ImageMagick if available, otherwise try pillow-heif."""
    try:
        # Try ImageMagick first
        result = subprocess.run(
            ["magick", str(source), str(dest)],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return True
    except FileNotFoundError:
        pass

    try:
        # Try pillow-heif
        from PIL import Image
        import pillow_heif
        pillow_heif.register_heif_opener()

        img = Image.open(source)
        img.save(dest, "JPEG", quality=85)
        return True
    except ImportError:
        print(f"  Warning: Cannot convert HEIC. Install pillow-heif: pip install pillow-heif")
        return False
    except Exception as e:
        print(f"  Error converting {source}: {e}")
        return False

def process_image(uri: str, post_id: str, img_index: int) -> str | None:
    """Copy/convert an image to the output directory. Returns the output filename."""
    source_path = INSTAGRAM_DATA / uri

    if not source_path.exists():
        print(f"  Warning: Image not found: {source_path}")
        return None

    # Determine output filename
    ext = source_path.suffix.lower()
    if ext == ".heic":
        out_filename = f"{post_id}_{img_index}.jpg"
        out_path = OUTPUT_DIR / out_filename

        if out_path.exists():
            print(f"  Skipping (exists): {out_filename}")
            return out_filename

        print(f"  Converting: {source_path.name} -> {out_filename}")
        if convert_heic_to_jpg(source_path, out_path):
            return out_filename
        return None
    else:
        out_filename = f"{post_id}_{img_index}{ext}"
        out_path = OUTPUT_DIR / out_filename

        if out_path.exists():
            print(f"  Skipping (exists): {out_filename}")
            return out_filename

        print(f"  Copying: {source_path.name} -> {out_filename}")
        shutil.copy2(source_path, out_path)
        return out_filename

def main():
    print("Processing Instagram data for Pics:) page...")

    # Create output directories
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Read posts JSON
    print(f"Reading: {POSTS_JSON}")
    with open(POSTS_JSON, "r", encoding="utf-8") as f:
        posts = json.load(f)

    print(f"Found {len(posts)} total posts")

    # Filter for monthly posts
    monthly_posts = []
    for post in posts:
        title = post.get("title", "")
        if is_monthly_post(title):
            monthly_posts.append(post)

    print(f"Found {len(monthly_posts)} monthly posts")

    # Process each monthly post
    manifest = []
    for post in monthly_posts:
        title = post["title"]
        month_num = get_month_from_title(title)

        # Try to get year from the first media URI (folder structure like 202512)
        first_media = post.get("media", [{}])[0]
        uri = first_media.get("uri", "")
        year_month = get_year_month_from_uri(uri)

        if year_month:
            folder_year, folder_month = year_month
            # The folder month is when Instagram exported, but we need the actual post month
            # If folder_month >= title month, same year. If folder_month < title month, previous year.
            if folder_month >= month_num:
                year = folder_year
            else:
                year = folder_year - 1
        else:
            # Fallback to timestamp
            year = get_year_from_timestamp(post["creation_timestamp"])

        # Create a unique post ID
        post_id = f"{year}_{month_num:02d}_{title.replace(', ', '_').replace(' ', '_').lower()}"

        print(f"\nProcessing: {title} ({year})")

        # Process images
        images = []
        for i, media_item in enumerate(post.get("media", [])):
            uri = media_item.get("uri", "")
            if uri:
                filename = process_image(uri, post_id, i)
                if filename:
                    images.append(filename)

        if images:
            # Create a synthetic timestamp for sorting (year + month)
            sort_key = year * 100 + month_num
            manifest.append({
                "id": post_id,
                "title": title,
                "year": year,
                "month": month_num,
                "sort_key": sort_key,
                "images": images
            })

    # Sort by sort_key (newest first)
    manifest.sort(key=lambda x: x["sort_key"], reverse=True)

    # Write manifest
    print(f"\nWriting manifest: {MANIFEST_PATH}")
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nDone! Processed {len(manifest)} posts with {sum(len(p['images']) for p in manifest)} images")

if __name__ == "__main__":
    main()
