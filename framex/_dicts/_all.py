from framex._dicts._github import _GITHUB_DATASETS
from framex._dicts._local import _LOCAL_CACHES_MAIN_EXT

# merge dictionaries
_REMOTE_DATASETS = {**_GITHUB_DATASETS}
_DATASETS = {**_LOCAL_CACHES_MAIN_EXT,**_REMOTE_DATASETS}
