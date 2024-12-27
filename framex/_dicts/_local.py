from pathlib import Path

from framex._dicts._constants import _EXTENSION, _LOCAL_DIR

# find locally cached files
## all files without extension
_LOCAL_CACHES = {path.stem: path for path in Path(_LOCAL_DIR).glob("*")}
## all files with THEIR extension 
_LOCAL_CACHES_EXT = {path.name: path for path in Path(_LOCAL_DIR).glob("*")}
## all files with _EXTENSION extension
_LOCAL_CACHES_MAIN_EXT = {path.stem: path for path in Path(_LOCAL_DIR).glob(f"*.{_EXTENSION}")}

