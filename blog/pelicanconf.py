# ~/py3.11-blog/bin/pelican -t pelican-stirring content/




DEFAULT_LANG = "en"

# SEE
# https://github.com/hansliu/pelican-stirring#settings
# https://github.com/aleylara/Peli-Kiera
THEME = "Peli-Kiera"
#THEME = "pelican-stirring"

AUTHOR = "JunkDLC"
SITENAME = "Incremental Authorship"
SITEURL = ""
COPYRIGHT = "2019"
SITESUBTITLE = "Site Subtitle"
PATH = "content"
TIMEZONE = "Europe/London"
DEFAULT_LANG = "en"

#PLUGIN_PATHS = ["pelican-plugins"]
PLUGINS = ["readtime", "neighbors"]
STATIC_PATHS = ["images"]
# Article summary length on main index page
SUMMARY_MAX_LENGTH = 100
DEFAULT_PAGINATION = 10
GITHUB_URL = "https://github.com/"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
RSS_FEED_SUMMARY_ONLY = True

# Social widget
SOCIAL = (
    ("tumblr", "https://tumblr.com/"),
    ("twitter", "https://twitter.com/"),
    ("linkedin", "https://www.linkedin.com"),
    ("github", "https://github.com/"),
    ("gitlab", "https://gitlab.com/"),
    ("facebook", "https://facebook.com"),
    ("instagram", "https://instagram.com"),
)
