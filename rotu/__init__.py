import datetime
import importlib.metadata

try:
    __version__ = importlib.metadata.version("rotu")
except importlib.metadata.PackageNotFoundError:
    __version__ = datetime.date.today().strftime("%Y.%m.%d") + "+local_repository"
