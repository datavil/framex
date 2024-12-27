from framex._dicts._github import _GITHUB_DATASETS
from framex._dicts._local import _LOCAL_CACHES

# merge dictionaries
_REMOTE_DATASETS = {**_GITHUB_DATASETS}
_DATASETS = {**_LOCAL_CACHES, **_REMOTE_DATASETS}
