# A guide to Lists and Writing pages 

## Adding Content

### Lists

Add markdown files to `src/content/lists/`:

```md
---
title: "My List Title"
description: "Optional description shown on index"  # optional
order: 1                                            # optional: lower = appears first
published: true                                     # optional: set false to hide from site
---

Your content here...
```

- Files appear at `/lists/[filename]`
- Published lists auto-appear on `/lists` index
- Set `published: false` to keep file locally but hide from website

### Writing (Blog)

Add markdown files to `src/content/writing/`:

```md
---
title: "Post Title"
date: 2024-12-28        # optional
description: "Optional"  # optional
---

Your content here...
```