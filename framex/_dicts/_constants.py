from pathlib import Path

_LOCAL_DIR = Path.home() / ".cache" / "framex" / "datasets"
if not _LOCAL_DIR.exists():
    _LOCAL_DIR.mkdir(parents=True)

# feather: almost as effective compression as parquet, much faster to loading times
_EXTENSION = "feather"
_REMOTE_DIR_GITHUB = f"https://github.com/datavil/datasets/raw/main/{_EXTENSION}/"
_INFO_FILE = "https://github.com/datavil/datasets/raw/main/datasets_info.csv"
