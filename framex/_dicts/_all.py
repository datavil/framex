# from framex._dicts._github import _GITHUB_DATASETS
from framex._dicts._local import _LOCAL_CACHES

# more will be added later

for i in range(200):
    if i % 20 == 0:
        print(i)
    from framex._dicts._github import _GITHUB_DATASETS
# merge dictionaries
_REMOTE_DATASETS = {**_GITHUB_DATASETS}
_DATASETS = {**_LOCAL_CACHES, **_REMOTE_DATASETS}
