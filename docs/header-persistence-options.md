# Header Persistence Options

## The Problem

When navigating between pages (About, Lists, Writing, etc.), the header banner briefly flashes or changes shade. This happens because:

1. Every navigation triggers a full page reload
2. The browser must re-fetch, decode, and paint the header image each time
3. There's a brief moment where the background color shows before the image renders

The key insight: **the header is completely static** - same image, same text, same styling across all pages. We should be able to keep it stable.

---

## Option 1: Astro View Transitions (Native Solution)

Astro has built-in support for View Transitions, which can persist elements across page navigations.

### Implementation

**1. Update `astro.config.mjs`:**

```javascript
import { defineConfig } from 'astro/config';

export default defineConfig({
  // View Transitions work without config changes in Astro 4+
});
```

**2. Update `src/layouts/Layout.astro`:**

```astro
---
import { ViewTransitions } from 'astro:transitions';

interface Props {
  title: string;
}

const { title } = Astro.props;
---

<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="description" content="Tim Farrelly" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,600;1,400&display=swap"
      rel="stylesheet"
    />
    <title>{title}</title>
    <ViewTransitions />
  </head>
  <body>
    <!-- rest of layout -->
  </body>
</html>
```

**3. Add `transition:persist` to the header in each page:**

```astro
<header class="header-wrapper" transition:persist>
  <div class="header">
    <img src="/short.jpg" alt="" class="header-img" />
    <!-- ... -->
  </div>
</header>
```

### Pros
- Native Astro feature, well-supported
- Simple to implement (add a few attributes)
- Handles back/forward navigation automatically
- Can add smooth animations between pages

### Cons
- Still technically navigating (new page loads), just with persistence
- Need to add `transition:persist` to each page's header
- Scripts may need `transition:persist` or re-initialization handling

---

## Option 2: Client-Side Content Swapping (SPA-like)

Instead of navigating at all, intercept clicks and swap only the content area via JavaScript fetch.

### How It Works

```
┌─────────────────────────────────────────┐
│  HEADER (static, never touched)         │
├─────────────────────────────────────────┤
│  NAV  │  CONTENT AREA  │  ARTWORK       │
│       │  (swapped via  │                │
│       │   fetch/JS)    │                │
└─────────────────────────────────────────┘
```

1. User clicks "Lists" → JavaScript intercepts
2. Fetch `/lists` HTML → Extract just the `.col-content` portion
3. Swap the content div → Replace current with fetched
4. Update URL → `history.pushState()` changes URL to `/lists`

The header **literally never re-renders** because it's outside the swap zone.

### Implementation

**Add this script to `src/layouts/Layout.astro`:**

```astro
<script>
  function initClientRouter() {
    const contentSelector = '.col-content';
    const navSelector = '.col-menu a, .mobile-nav a';

    // Intercept navigation clicks
    document.querySelectorAll(navSelector).forEach(link => {
      link.addEventListener('click', handleNavClick);
    });

    async function handleNavClick(e) {
      const link = e.currentTarget;
      const url = link.getAttribute('href');

      // Skip external links or same page
      if (!url || url.startsWith('http') || url === window.location.pathname) {
        return;
      }

      e.preventDefault();
      await navigateTo(url);
    }

    async function navigateTo(url) {
      try {
        // Fetch the target page
        const response = await fetch(url);
        const html = await response.text();

        // Parse and extract the content
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const newContent = doc.querySelector(contentSelector);

        if (newContent) {
          // Swap content
          const currentContent = document.querySelector(contentSelector);
          currentContent.replaceWith(newContent);

          // Update URL
          history.pushState({ url }, '', url);

          // Update active nav state
          updateActiveNav(url);

          // Re-run any scripts needed for new content
          reinitializeContent();
        }
      } catch (error) {
        // Fallback to normal navigation on error
        console.error('Client navigation failed:', error);
        window.location.href = url;
      }
    }

    function updateActiveNav(url) {
      // Remove current active states
      document.querySelectorAll('.col-menu li strong').forEach(el => {
        const text = el.textContent;
        const li = el.parentElement;
        el.replaceWith(document.createTextNode(text));

        // Wrap in link if not current page
        const link = document.createElement('a');
        link.href = getHrefForPage(text);
        link.textContent = text;
        link.addEventListener('click', handleNavClick);
        li.appendChild(link);
      });

      // Set new active state
      document.querySelectorAll('.col-menu a').forEach(link => {
        if (link.getAttribute('href') === url) {
          const li = link.parentElement;
          const text = link.textContent;
          link.remove();
          const strong = document.createElement('strong');
          strong.textContent = text;
          li.appendChild(strong);
        }
      });
    }

    function getHrefForPage(pageName) {
      const routes = {
        'About': '/',
        'Lists': '/lists',
        'Writing': '/writing',
        'Art Gallery': '/art',
        'Pics:)': '/pics'
      };
      return routes[pageName] || '/';
    }

    function reinitializeContent() {
      // Re-attach event listeners or re-run scripts for dynamic content
      // This is where you'd reinitialize anything the new content needs
    }

    // Handle browser back/forward
    window.addEventListener('popstate', (e) => {
      if (e.state?.url) {
        navigateTo(e.state.url);
      } else {
        // Fallback for initial page
        navigateTo(window.location.pathname);
      }
    });

    // Set initial state
    history.replaceState({ url: window.location.pathname }, '', window.location.pathname);
  }

  // Initialize on page load
  initClientRouter();
</script>
```

### Pros
- Header **absolutely cannot flash** - it's never part of any update
- Instant navigation feel (faster than View Transitions)
- Full control over the experience
- No Astro-specific features required

### Cons
- More code to maintain
- Need to handle edge cases (scripts re-initialization, back button)
- Need to ensure content from fetched pages works correctly
- Forms or interactive elements in content need special handling

---

## Option 3: Quick Fixes (Partial Solutions)

If you want minimal changes, these can reduce (but not eliminate) the flash:

### 3a. Add Preload Hint

In `Layout.astro` `<head>`:

```html
<link rel="preload" as="image" href="/short.jpg" fetchpriority="high" />
```

### 3b. Optimize Image Size

Current image is 3840x860px but displays at 75px height. Resize to ~1920x430 or smaller.

### 3c. Use CSS Background Image

```css
.header {
  background-image: url('/short.jpg');
  background-size: cover;
  background-position: center;
}
```

Remove the `<img>` tag entirely.

---

## How Other Frameworks Handle This

### Plain HTML/CSS/JS (No Framework)

**The Problem**: Same as Astro - every page is a full reload.

**Solutions**:
1. **Single Page Application (SPA)**: One HTML file, JavaScript handles all "navigation" by showing/hiding content or fetching via AJAX. The header is in the single HTML file and never reloads.

2. **iframe approach** (old school): Header in parent frame, content in iframe. Navigation happens in iframe only. Terrible for SEO and accessibility but technically works.

3. **Server-Side Includes (SSI)**: Server assembles pages from fragments. Doesn't help with client-side flash though.

### React / Next.js

**Built-in SPA behavior**: React apps are SPAs by default. The header component mounts once and stays mounted. Navigation via React Router or Next.js router only re-renders components that change.

```jsx
// Layout component - header is outside the route
function Layout({ children }) {
  return (
    <>
      <Header />  {/* Never re-renders on navigation */}
      <main>{children}</main>  {/* This swaps based on route */}
    </>
  );
}
```

**Next.js App Router**: Uses React Server Components with streaming. Shared layouts persist automatically - the header in a `layout.tsx` never flashes because it's not part of what re-renders.

### Vue / Nuxt

Similar to React - Vue's reactivity system and Vue Router mean components outside `<router-view>` persist. Nuxt has `layouts/` directory where you define persistent shells.

### SvelteKit

Has a `+layout.svelte` concept where shared UI persists. Also supports View Transitions natively.

### HTMX

Modern approach to the "fetch and swap" pattern. Instead of writing JavaScript:

```html
<nav hx-boost="true">
  <a href="/lists" hx-target=".col-content" hx-select=".col-content" hx-swap="outerHTML">
    Lists
  </a>
</nav>
```

This tells HTMX to intercept the click, fetch `/lists`, extract `.col-content`, and swap it in. No custom JS needed.

---

## Recommendation

| Approach | Complexity | Effectiveness | Best For |
|----------|------------|---------------|----------|
| View Transitions | Low | High | Astro-native solution, good enough for most cases |
| Client-Side Swap | Medium | Highest | Maximum control, guaranteed no flash |
| Preload + Optimize | Very Low | Medium | Quick improvement with minimal changes |

**For your site**: Start with **View Transitions** since it's native to Astro and handles 90% of the use case with minimal code. If you still see issues or want finer control, the client-side swap approach guarantees the header never touches.

---

## Resources

- [Astro View Transitions Docs](https://docs.astro.build/en/guides/view-transitions/)
- [View Transitions API (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API)
- [HTMX - high power tools for HTML](https://htmx.org/)
