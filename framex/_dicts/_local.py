from pathlib import Path

from framex._dicts._constants import _EXTENSION, _LOCAL_DIR

# find locally cached _EXTENSION files
_LOCAL_CACHES = {path.stem: path for path in Path(_LOCAL_DIR).glob("*")}
_LOCAL_CACHES_EXT = {path.name: path for path in Path(_LOCAL_DIR).glob("*")}
