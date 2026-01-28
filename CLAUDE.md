# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an academic website for Jan Vanvinkenroye built with **Astro** static site generator. The site features academic publications managed via BibTeX, with a custom TypeScript parser for bibliography rendering.

## Build and Development Commands

```bash
# Install dependencies
npm install

# Development server with hot reload
npm run dev
# Then visit http://localhost:4321

# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Architecture

```
src/
├── components/         # Astro components
│   ├── BaseLayout.astro    # Main layout with SEO meta tags
│   ├── Navigation.astro    # Nav with mobile hamburger menu
│   ├── Footer.astro
│   └── CVEntry.astro       # Reusable CV entry component
├── pages/              # Route pages (file-based routing)
│   ├── index.astro         # Homepage
│   ├── publications.astro  # Publications (from BibTeX)
│   ├── cv.astro            # Curriculum Vitae
│   ├── teaching.astro      # Teaching positions
│   ├── projekte.astro      # Projects
│   ├── engagement.astro    # Memberships
│   ├── impressum.astro     # Legal notice
│   └── 404.astro           # Error page
├── lib/
│   └── bibtex.ts       # Custom BibTeX parser
├── data/
│   └── publications.bib    # BibTeX bibliography
└── styles/
    └── main.css        # Global styles

public/                 # Static assets (copied as-is)
├── images/
├── files/
├── robots.txt
└── favicon.svg

dist/                   # Build output (git-ignored)
```

## BibTeX Integration

### Custom Parser
The custom BibTeX parser in `src/lib/bibtex.ts`:
- Parses `src/data/publications.bib` at build time
- Filters entries with `keywords={selected}`
- Sorts by year (newest first)
- Cleans LaTeX formatting

### Adding New Publications
1. Edit `src/data/publications.bib`
2. Add BibTeX entry with standard fields
3. Include `keywords={selected}` to display on website
4. Rebuild: `npm run build`

### BibTeX Entry Requirements
- Use standard types: `@article`, `@inproceedings`, `@incollection`, `@book`
- Always include: `author`, `title`, `year`
- Optional: `doi`, `url`, `journal`, `booktitle`, `pages`, `publisher`
- Add `keywords={selected}` to include in publication list

## Configuration

### astro.config.mjs
- `site`: Production URL (https://vanvinkenroye.de)
- `trailingSlash: 'always'`: Consistent URL format
- `i18n`: German as default locale
- Integrations: `@astrojs/sitemap` for SEO

### SEO Features
- Open Graph meta tags for social sharing
- Twitter Card support
- Canonical URLs
- Sitemap generation
- robots.txt

## Component Usage

### BaseLayout
```astro
<BaseLayout title="Page Title" description="Optional description">
  <h1>Content</h1>
</BaseLayout>
```

### CVEntry
```astro
<CVEntry
  title="Position Title"
  dateStart="01.2020"
  dateEnd="heute"
  organization="Organization Name"
  url="https://example.com"
  description="Description text"
/>
```

## Content Editing Guidelines

### Language
- Default language is German
- Use `lang="en"` attribute for English content sections

### Icons
- FontAwesome 5: `<i class="fas fa-icon"></i>`
- Academicons: `<i class="ai ai-orcid"></i>`

### Styling
- Vollkorn serif font
- Link color: #0066cc
- Mobile-responsive with hamburger menu
- Print styles included

## Deployment

Build output is in `dist/` directory:
```bash
npm run build
# Upload dist/ contents to web server
```

Supports: Netlify, Vercel, GitHub Pages, any static hosting.
