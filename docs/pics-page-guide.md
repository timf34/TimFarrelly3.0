# Pics:) Page - How It Works

This document explains how the Pics:) visual timeline page works and how to update it with new Instagram photos.

## Overview

The Pics:) page (`/pics`) displays your monthly Instagram photo posts as a visual timeline. It shows posts grouped by year, with each month's photos displayed in a grid (desktop) or horizontal carousel (mobile).

## How It Works

### Data Flow

1. **Instagram Data Export** → You download your data from Instagram
2. **Python Script** → `scripts/process_instagram_pics.py` parses the JSON and copies/converts images
3. **Manifest JSON** → Script generates `src/data/pics-manifest.json` with post metadata
4. **Astro Page** → `src/pages/pics.astro` reads the manifest and renders the gallery

### What the Script Does

The Python script (`scripts/process_instagram_pics.py`):

1. Reads `posts_1.json` from your Instagram data export
2. Filters for posts with titles like "May" or "May, art" (monthly posts only)
3. For each matching post:
   - Extracts the year from the folder structure (e.g., `202512` = December 2025)
   - Gets the month from the post title (e.g., "May" = month 5)
   - Copies images to `public/pics/` with standardized names like `2025_05_may_0.jpg`
   - Converts HEIC files to JPG (using ImageMagick)
4. Generates `src/data/pics-manifest.json` with all post data

### File Structure

```
TimFarrelly3.0/
├── public/pics/                    # All processed images
│   ├── 2025_05_may_0.jpg
│   ├── 2025_05_may_1.jpg
│   └── ...
├── scripts/
│   └── process_instagram_pics.py   # Image processing script
├── src/
│   ├── data/
│   │   └── pics-manifest.json      # Generated manifest
│   └── pages/
│       └── pics.astro              # The page itself
└── temp/                           # (gitignored)
    └── instagram-data/             # Your Instagram export goes here
```

---

## How to Update with New Photos

### Step 1: Download Your Instagram Data

1. Go to Instagram → Settings → Your Activity → Download Your Information
2. Request a download of your data (JSON format)
3. Wait for Instagram to email you the download link
4. Download and extract the ZIP file

### Step 2: Place the Data in the Project

1. Create the folder if it doesn't exist:
   ```
   temp/instagram-data/
   ```

2. Copy these folders from your Instagram export:
   ```
   temp/instagram-data/
   ├── media/
   │   └── posts/           # Contains folders like 202512, 202501, etc.
   └── your_instagram_activity/
       └── media/
           └── posts_1.json # The JSON with post metadata
   ```

### Step 3: Run the Processing Script

```bash
python scripts/process_instagram_pics.py
```

The script will:
- Show you how many posts it found
- Process each monthly post (May, April, etc.)
- Convert HEIC files to JPG
- Skip files that already exist (safe to re-run)
- Generate a new `pics-manifest.json`

### Step 4: Verify and Commit

1. Run the dev server to check it looks right:
   ```bash
   npm run dev
   ```

2. Visit http://localhost:4321/pics and verify new posts appear

3. Commit the changes:
   ```bash
   git add public/pics/ src/data/pics-manifest.json
   git commit -m "Add new monthly photos"
   ```

---

## Troubleshooting

### HEIC files not converting

The script uses ImageMagick to convert HEIC files. If conversion fails:

1. Install ImageMagick: https://imagemagick.org/script/download.php
2. Or install pillow-heif: `pip install pillow-heif`

### Wrong year detected

The script infers the year from the Instagram folder structure (e.g., `202512`). If a post shows the wrong year, it's likely because the export folder date doesn't match the post date. The month is always taken from the post title, which should be correct.

### Missing posts

The script only includes posts with titles that are exactly:
- A month name: "January", "February", ..., "December"
- A month name with ", art": "January, art", "February, art", etc.

If your Instagram post has a different title format, it won't be included.

### Images not showing

1. Check that images exist in `public/pics/`
2. Check `src/data/pics-manifest.json` for the correct paths
3. Run `npm run build` to see any errors

---

## Technical Details

### Manifest Format

Each entry in `pics-manifest.json`:

```json
{
  "id": "2025_05_may",
  "title": "May",
  "year": 2025,
  "month": 5,
  "sort_key": 202505,
  "images": [
    "2025_05_may_0.jpg",
    "2025_05_may_1.jpg",
    ...
  ]
}
```

### Supported Image Formats

- **Input**: HEIC, JPG, JPEG, PNG, WEBP, MP4 (videos are copied but not displayed)
- **Output**: JPG (for HEIC), original format for others

### Page Features

- **Desktop**: Responsive grid layout with hover effects
- **Mobile**: Horizontal carousel with swipe/scroll
- **Modal**: Click any image to view fullscreen, navigate with arrows or keyboard
- **Lazy loading**: Images load as you scroll
