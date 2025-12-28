# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

| Command           | Action                              |
| :---------------- | :---------------------------------- |
| `npm install`     | Install dependencies                |
| `npm run dev`     | Start dev server at localhost:4321  |
| `npm run build`   | Build production site to `./dist/`  |
| `npm run preview` | Preview built site locally          |

## Architecture

This is a personal website built with Astro 5. The site uses Astro Content Collections for markdown-based content.

### Layouts

- `src/layouts/Layout.astro` - Base HTML layout with global styles and dev grid (toggle with 'g' key)
- `src/layouts/ContentLayout.astro` - Layout for individual content pages (lists, writing) with left menu and centered content

### Pages

The site has a 3-column grid layout on desktop (10% menu | 40% content | 50% artwork):
- `src/pages/index.astro` - Homepage with bio and generative artwork
- `src/pages/lists/` - Lists section using Content Collections
- `src/pages/writing/` - Writing/blog section using Content Collections
- `src/pages/art.astro` - Art gallery with masonry grid and modal viewer
- `src/pages/pics.astro` - Photo dumps with carousel on mobile

### Content Collections

Defined in `src/content/config.ts`:

**Lists** (`src/content/lists/*.md`):
- `title` (required)
- `order` (optional) - Lower numbers appear first
- `published` (default: true) - Set to false to hide from site

**Writing** (`src/content/writing/*.md`):
- `title` (required)
- `date` (optional)
- `description` (optional)

### Other Key Directories

- `src/artworks/` - Generative art scripts for homepage canvas
- `src/data/pics-manifest.json` - Manifest for photos page
- `public/pics/` - Photo images served statically
