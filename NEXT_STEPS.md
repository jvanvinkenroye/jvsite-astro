# Next Steps: Multi-Page Structure Implementation

## Overview
Converting the single-page academic site to a multi-page structure similar to vene.ro with separate sections for better navigation and content organization.

## Current Status
- ✅ Pelican static site generator configured
- ✅ BibTeX integration working with pelican-bibtex plugin
- ✅ Minimal theme created with clean academic design
- ✅ All content consolidated in single index.md file
- 🔄 **IN PROGRESS**: Creating separate pages structure

## Required Steps

### 1. Content Separation (IN PROGRESS)
Split the current `content/index.md` into separate page files:
- `content/index.md` - Brief homepage with introduction
- `content/pages/research.md` - Publications and research interests
- `content/pages/teaching.md` - Teaching experience and courses
- `content/pages/cv.md` - Professional experience and qualifications

### 2. Navigation Implementation (PENDING)
Update the minimal theme templates to include:
- Navigation menu in `base.html` template
- Active page highlighting
- Consistent header/footer across all pages
- Mobile-responsive navigation

### 3. Template Updates (PENDING)
Modify theme templates for multi-page support:
- Update `themes/minimal/templates/base.html` with navigation
- Create `themes/minimal/templates/page.html` for individual pages
- Ensure proper styling for different content types

### 4. Pelican Configuration
Update `pelicanconf.py` settings:
- Configure page generation
- Set up proper URL structure
- Maintain BibTeX integration for publications page

## File Structure After Implementation
```
content/
├── index.md                 # Homepage
└── pages/
    ├── research.md          # Publications & research
    ├── teaching.md          # Teaching experience
    └── cv.md               # Professional background

themes/minimal/
├── templates/
│   ├── base.html           # Navigation & layout
│   ├── index.html          # Homepage template
│   └── page.html           # Individual pages
└── static/css/
    └── main.css            # Updated styles
```

## Expected Outcome
A professional academic website with:
- Clean navigation between sections
- Organized content presentation
- Maintained BibTeX functionality for publications
- Responsive design across all pages
- Similar structure to vene.ro for better user experience

## Commands to Test After Implementation
```bash
# Build and serve locally
pelican content -o output -s pelicanconf.py
pelican --listen --bind 127.0.0.1 --port 8000
```