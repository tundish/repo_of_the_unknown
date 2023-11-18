# ~/py3.11-blog/bin/pelican -t pelican-stirring content/




DEFAULT_LANG = "en"

# SEE
# https://github.com/aleylara/Peli-Kiera
THEME = "Peli-Kiera"
#THEME = "pelican-stirring"

AUTHOR = "D. E. Haynes"
SITENAME = "Repo of the Unknown"
SITEURL = "https://tundish.github.io/repo_of_the_unknown"
COPYRIGHT = "2023"
SITESUBTITLE = "Interactive Fiction step-by-step in Python"
PATH = "content"
TIMEZONE = "Europe/London"
DEFAULT_LANG = "en"

#PLUGIN_PATHS = ["pelican-plugins"]
PLUGINS = ["readtime", "neighbors"]
STATIC_PATHS = ["images"]
# Article summary length on main index page
SUMMARY_MAX_LENGTH = 100
DEFAULT_PAGINATION = 10
GITHUB_URL = "https://github.com/tundish/repo_of_the_unknown"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
RSS_FEED_SUMMARY_ONLY = True

# Social widget
SOCIAL = (
    ("tumblr", "https://junkdlc.tumblr.com/"),
    ("github", "https://github.com/tundish"),
    ("youtube", "https://youtube.com"),
)
