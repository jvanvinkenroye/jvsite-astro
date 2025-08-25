# Jan Vanvinkenroye - Pelican Static Site

This project uses [Pelican](https://getpelican.com/) to generate a static website from Markdown content.

## 🚀 Quick Start

### Option 1: Using the Build Script
```bash
chmod +x build.sh
./build.sh
```

### Option 2: Using Make
```bash
make setup
make html
make serve
```

### Option 3: Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate site
pelican content -o output -s pelicanconf.py

# Serve locally
cd output && python3 -m http.server 8000
```

## 📁 Project Structure

```
jvsite/
├── content/           # Markdown content files
│   └── index.md      # Main page content
├── themes/           # Custom theme
│   └── academic/     # Academic theme
│       ├── templates/
│       └── static/
├── output/           # Generated HTML (created after build)
├── pelicanconf.py    # Pelican configuration
├── requirements.txt  # Python dependencies
├── build.sh         # Build script
├── serve.sh         # Development server script
└── Makefile         # Make commands
```

## ✏️ Editing Content

### Main Page
Edit `content/index.md` to modify the homepage content. The file uses:
- **Markdown syntax** for formatting
- **HTML** for complex layouts (like the CV entries)
- **FontAwesome icons** using `<i class="fas fa-icon-name"></i>`
- **Academicons** using `<i class="ai ai-icon-name"></i>`

### Adding New Pages
Create new `.md` files in the `content/` directory:

```markdown
Title: New Page
Date: 2024-08-24
Status: published

# Content here
Your markdown content...
```

### CV Entry Format
Use this HTML structure for consistent CV entries:

```html
<div class="entry">
    <div class="date">2024</div>
    <div class="content">
        <h3>Position Title</h3>
        <p><strong>Institution</strong> - Department</p>
        <p>Description of role and responsibilities</p>
    </div>
</div>
```

## 🎨 Customizing Appearance

### CSS Styling
Edit `themes/academic/static/css/main.css` to modify styles.

### Templates
Modify templates in `themes/academic/templates/`:
- `base.html` - Main page structure
- `index.html` - Homepage template
- `page.html` - Individual page template

### Icons
The site uses:
- **FontAwesome 5.0.13**: `<i class="fas fa-icon-name"></i>`
- **Academicons**: `<i class="ai ai-icon-name"></i>`

Popular icons:
- 💼 `fas fa-briefcase` (work)
- 🎓 `fas fa-graduation-cap` (education) 
- 👥 `fas fa-users` (groups)
- 🔗 `fas fa-link` (links)
- 📚 `ai ai-google-scholar` (publications)
- 📧 `fas fa-envelope` (email)

## 🛠️ Development Commands

### Build site once
```bash
make html
# or
pelican content -o output -s pelicanconf.py
```

### Development server with auto-reload
```bash
make devserver
# or
./serve.sh
```

### Clean generated files
```bash
make clean
```

## 🌐 Deployment

### GitHub Pages
1. Build the site: `make html`
2. Commit the `output/` directory
3. Configure GitHub Pages to serve from that folder

### Netlify
1. Connect your repository
2. Set build command: `make html`
3. Set publish directory: `output`

### Manual Upload
1. Build: `make html` 
2. Upload contents of `output/` directory to your web server

## 📝 Content Writing Tips

### Markdown Basics
```markdown
# Heading 1
## Heading 2
### Heading 3

**Bold text**
*Italic text*
[Link text](https://example.com)

- Bullet point
- Another point

1. Numbered list
2. Second item
```

### Mixing HTML and Markdown
You can use HTML within Markdown for complex layouts:

```markdown
## Section Title

Regular markdown paragraph here.

<div class="special-layout">
    <p>HTML content for precise control</p>
</div>

Back to markdown.
```

### Adding Publications
Use this format for consistent publication entries:

```html
<div class="entry">
    <div class="date">2024</div>
    <div class="content">
        <p>Author, A., <strong>Your Name</strong>, & Author, C. (2024). Paper Title. <em>Journal Name</em>. <a href="https://doi.org/..." target="_blank">DOI</a></p>
    </div>
</div>
```

## 🔧 Advanced Configuration

Edit `pelicanconf.py` to customize:
- Site metadata
- URL structure  
- Plugin integration
- Theme settings
- Social links

## 📚 Resources

- [Pelican Documentation](https://docs.getpelican.com/)
- [Markdown Guide](https://www.markdownguide.org/)
- [FontAwesome Icons](https://fontawesome.com/v5/search)
- [Academicons](https://jpswalsh.github.io/academicons/)

---

Happy blogging! 🎉