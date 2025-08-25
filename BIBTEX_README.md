# BibTeX Integration with Pelican

This project now includes **pelican-bibtex** for professional publication management.

## 📚 How BibTeX Works

### The BibTeX File
All publications are stored in `content/publications.bib`:

```bibtex
@article{doe2024example,
  title={Example Paper Title},
  author={Doe, John and Vanvinkenroye, Jan},
  journal={Journal Name},
  year={2024},
  doi={10.1000/example},
  url={https://doi.org/10.1000/example},
  keywords={selected}
}
```

### Inserting Publications
In any Markdown file, use:
```markdown
[@bibliography]
```

This will automatically:
- Format all publications professionally
- Sort by year (newest first)
- Include DOI links
- Highlight author names
- Apply consistent styling

## 🎯 Benefits

### Professional Academic Format
- Standard citation styles
- Automatic formatting
- Consistent appearance
- Academic credibility

### Easy Maintenance
- Single source of truth (`.bib` file)
- Easy to add new publications
- No manual HTML formatting
- Version control friendly

### Rich Metadata
- DOI links automatically converted
- URL support
- Keywords for categorization
- Full author information

## 📝 Adding New Publications

### Step 1: Add to BibTeX file
Edit `content/publications.bib`:

```bibtex
@inproceedings{vanvinkenroye2024new,
  title={New Research Paper},
  author={Vanvinkenroye, Jan and Collaborator, A.},
  booktitle={Conference Proceedings},
  year={2024},
  doi={10.1000/newpaper},
  keywords={selected}
}
```

### Step 2: Rebuild site
```bash
make html
```

The publication will automatically appear in the correct chronological order!

## 🎨 Custom Styling

Publications use these CSS classes:
- `.publications-list` - Container
- `.publication` - Individual entry
- `.publication-year` - Year badge
- `.publication-content` - Main content

Customize in `themes/academic/static/css/main.css`.

## 🔧 Configuration

BibTeX settings in `pelicanconf.py`:
```python
PLUGINS = ['pelican_bibtex']
PUBLICATIONS_SRC = 'content/publications.bib'
BIBLIOGRAPHY_START = '<div class="publications-list">'
BIBLIOGRAPHY_END = '</div>'
```

## 📖 Supported Entry Types

- `@article` - Journal articles
- `@inproceedings` - Conference papers  
- `@incollection` - Book chapters
- `@book` - Books
- `@phdthesis` - PhD dissertations
- `@misc` - Other publications

## 🚀 Advanced Features

### Filtering by Keywords
Add `keywords={selected}` to only show certain publications.

### Author Highlighting
The plugin automatically highlights your name in author lists.

### Multiple Bibliographies
Create separate bibliography sections by keyword or year.

---

This makes managing academic publications much more professional and maintainable! 🎓