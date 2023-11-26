import pelican
from pelican.plugins import neighbors
import readtime

# SEE
# https://github.com/aleylara/Peli-Kiera
THEME = "Peli-Kiera"

AUTHOR = "D. E. Haynes"
SITENAME = "Repo of the Unknown"
SITEURL = "https://tundish.github.io/repo_of_the_unknown"
COPYRIGHT = "2023"
SITESUBTITLE = "Interactive Fiction step-by-step in Python"
PATH = "content"
TIMEZONE = "Europe/London"
DEFAULT_LANG = "en"

# PLUGINS = ["pelican.plugins.neighbors", "readtime"]
PLUGINS = [pelican.plugins.neighbors, readtime]
STATIC_PATHS = ["images"]

ARTICLE_ORDER_BY = "date"
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

READTIME_WPM = {
    "default": {
        "wpm": 200,
        "min_singular": "minute",
        "min_plural": "minutes",
        "sec_singular": "second",
        "sec_plural": "seconds"
    },
    "en": {
        "wpm": 220,
        "min_singular": "minute",
        "min_plural": "minutes",
        "sec_singular": "second",
        "sec_plural": "seconds"
    }
}
