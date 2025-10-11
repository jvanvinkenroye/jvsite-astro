AUTHOR = 'Jan Vanvinkenroye'
SITENAME = 'Jan Vanvinkenroye'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Berlin'
DEFAULT_LANG = 'de'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Menu and navigation
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False

# Theme and appearance
THEME = 'themes/minimal'

# Static files
STATIC_PATHS = ['images', 'extra', 'files']
EXTRA_PATH_METADATA = {
    'extra/favicon.ico': {'path': 'favicon.ico'},
}

# Plugins
PLUGIN_PATHS = ['plugins']
PLUGINS = ['pelican_bibtex']

# BibTeX settings
PUBLICATIONS_SRC = 'content/publications.bib'
BIBLIOGRAPHY_START = '<div class="publications-list">'
BIBLIOGRAPHY_END = '</div>'

# Custom bibliography formatting
DEFAULT_CATEGORY = 'misc'

# BibTeX style customization
PYBTEX_STYLE_COMPACT = True
PYBTEX_ADD_ENTRY_FIELDS = ['doi', 'url']

# URL settings
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'
INDEX_SAVE_AS = 'index.html'

# Disable tag and category pages
DIRECT_TEMPLATES = ['index']
PAGINATED_TEMPLATES = {}

# Article settings - we'll use pages instead
ARTICLE_URL = 'posts/{slug}.html'
ARTICLE_SAVE_AS = 'posts/{slug}.html'

# Profile photo
PROFILE_PHOTO = '/images/profile.jpg'

# Social widget
SOCIAL = (
    ('GitHub', 'https://github.com/jvanvinkenroye'),
    ('LinkedIn', 'https://www.linkedin.com/in/jvanvinkenroye/'),
    ('Mastodon', 'https://higher-edu.social/@jvanvinkenroye'),
    ('WhatsApp', 'http://wa.me/+491711854655'),
)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
