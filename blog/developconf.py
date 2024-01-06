# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent))

from pelicanconf import *

RELATIVE_URLS = True
DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

# DISQUS_SITENAME = ""
# GOOGLE_ANALYTICS = ""
