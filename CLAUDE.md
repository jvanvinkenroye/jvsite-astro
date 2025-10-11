# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an academic website for Jan Vanvinkenroye built with Pelican static site generator. The site features academic publications managed via BibTeX, with custom plugins for bibliography rendering.

## Build and Development Commands

### Virtual Environment
**IMPORTANT**: All Python commands must be run with the virtual environment activated:
```bash
source venv/bin/activate
```

### Common Development Workflow
```bash
# Build the site
./build.sh
# or
make html

# Development server with auto-reload
./serve.sh
# or
make devserver
# Then visit http://localhost:8000

# Clean build artifacts
make clean
```

### Build Components
- **Build script**: `build.sh` - Creates venv if needed, installs dependencies, generates site
- **Serve script**: `serve.sh` - Starts development server with auto-reload at port 8000
- **Makefile**: Provides targets for setup, html, clean, serve, devserver

## Project Architecture

### Content Management
- **Content source**: `content/` directory contains all Markdown files and pages
- **Main page**: `content/index.md` - Homepage content
- **Additional pages**: `content/pages/` - Additional site pages
- **Publications**: `content/publications.bib` - BibTeX bibliography database

### BibTeX Integration
- **Custom plugin**: `plugins/pelican_bibtex.py` - Custom Pelican plugin for bibliography rendering
- The plugin parses `publications.bib` and makes publications available in templates
- Publications are rendered using pybtex with HTML backend
- Each publication includes: key, year, formatted text, bibtex source, and optional PDF/slides/poster links
- Insert publications in Markdown with `[@bibliography]` syntax
- Configuration in `pelicanconf.py`:
  - `PUBLICATIONS_SRC`: Path to .bib file
  - `BIBLIOGRAPHY_START/END`: HTML wrapper tags

### Theme System
- **Active theme**: `themes/minimal/` (set in `pelicanconf.py` as `THEME = 'themes/minimal'`)
- **Inactive theme**: `themes/academic/` - Available but not currently used
- Theme structure:
  - `templates/` - Jinja2 templates (base.html, index.html, page.html)
  - `static/` - CSS, JavaScript, images

### Configuration
- **Main config**: `pelicanconf.py`
  - Site metadata (AUTHOR, SITENAME, TIMEZONE='Europe/Berlin', DEFAULT_LANG='de')
  - Plugin configuration (loads from `plugins/` directory)
  - Theme selection
  - URL structure (pages use `{slug}.html` format)
  - Social media links
  - Static paths and extra file mappings
  - Disables article/tag/category features (using pages-only approach)

### Output
- **Generated site**: `output/` directory (git-ignored)
- Contains the complete static HTML site ready for deployment

## Publication Management

### Adding New Publications
1. Edit `content/publications.bib`
2. Add BibTeX entry with standard fields (author, title, year, journal/booktitle, doi, etc.)
3. Include `keywords={selected}` to display in main list
4. Rebuild: `make html` or `./build.sh`

### BibTeX Entry Requirements
- Use standard BibTeX types: `@article`, `@inproceedings`, `@incollection`, `@book`, etc.
- Always include: `author`, `title`, `year`
- Optional but recommended: `doi`, `url`, `keywords`
- Special fields supported: `pdf`, `slides`, `poster` (for additional resources)

## Dependencies

Managed in `requirements.txt`:
- `pelican[markdown]` - Core static site generator
- `markdown` - Markdown processing
- `typogrify` - Typography improvements
- `pybtex` - BibTeX parsing and formatting
- `pybtex-docutils` - Additional BibTeX utilities

## Content Editing Guidelines

### Page Format
Markdown files should include metadata header:
```markdown
Title: Page Title
Date: YYYY-MM-DD
Status: published

Content here...
```

### Mixed HTML/Markdown
The content uses both Markdown and HTML for layout control:
- Use Markdown for text formatting
- Use HTML `<div>` structures for complex layouts (e.g., CV entries)
- Icons use FontAwesome and Academicons classes

### Language
- Default language is German (`DEFAULT_LANG = 'de'`)
- Timezone is Europe/Berlin

## Deployment Notes

The generated `output/` directory contains the complete static site. Deploy by:
1. Building: `make html`
2. Uploading `output/` contents to web server
3. Optionally using GitHub Pages, Netlify, or similar static hosting

## Plugin Architecture

The custom `pelican_bibtex.py` plugin:
- Hooks into Pelican's `generator_init` signal
- Parses BibTeX file using pybtex Parser
- Formats entries with plain style and HTML backend
- Populates `generator.context['publications']` with formatted data
- Each publication is a tuple: `(key, year, text, bibtex, pdf, slides, poster)`
