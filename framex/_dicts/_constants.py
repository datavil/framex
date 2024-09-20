from pathlib import Path

_LOCAL_DIR = Path(__file__).parent.parent / "data"
if not _LOCAL_DIR.exists():
    _LOCAL_DIR.mkdir()

_EXTENSION = "parquet"
_REMOTE_DIR_GITHUB = f"https://github.com/datavil/datasets/raw/main/{_EXTENSION}/"
_INFO_FILE = "https://github.com/datavil/datasets/raw/main/datasets_info.csv"
