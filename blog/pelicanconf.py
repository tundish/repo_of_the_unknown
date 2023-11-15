# ~/py3.11-blog/bin/pelican -t pelican-stirring content/

AUTHOR = "JunkDLC"
SITENAME = "Incremental Authorship"
SITEURL = ""

PATH = "content"

TIMEZONE = "Europe/London"

DEFAULT_LANG = "en"

# SEE
# https://github.com/hansliu/pelican-stirring#settings

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Pelican", "https://getpelican.com/"),
    ("Python.org", "https://www.python.org/"),
    ("Jinja2", "https://palletsprojects.com/p/jinja/"),
    ("You can modify those links in your config file", "#"),
)

# Social widget
SOCIAL = (
    ("You can add links in your config file", "#"),
    ("Another social link", "#"),
)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

DEFAULT_METADATA = {
"status": "draft",
}

GOOGLE_CUSTOM_SEARCH = 'your google custom search Id'
SITEAUTHORS = {
    'the author name': {
        'image': 'the author image',
        'description': 'the author profile'
    }
}
SITECATEGORIES = {
    'the category name': {
        'image': 'the category image',
    }
}
SITEFAVICON = 'your favicon.ico path'
SITECOVER = 'your background cover image path'
# Replace MENUITEMS, the tuple list support font awesome icon
THEME_MENUITEMS = (
    ('Home', '#', 'fas fa-home'),
    ('You can modify those links in your config file', '#', 'font awesome icon')
)
# Replace SOCIAL, the tuple list support font awesome icon
THEME_SOCIAL = (
    ('Github', 'https://github.com/hansliu', 'fab fa-github-square fa-2x'),
    ('You can modify those links in your config file', '#', 'font awesome icon')
)
# The INTERNAL LINKS open the linked in current window
INTERNAL_LINKS = (
    ('Terms', 'pages/tos.html'),
    ('Privacy', 'pages/privacy.html'),
    ('You can modify those links in your config file', '#')
)
# Like DISPLAY_PAGES_ON_MENU, you could control DISPLAY_FEEDS_ON_MENU by yourself
DISPLAY_FEEDS_ON_MENU = True
