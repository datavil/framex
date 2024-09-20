from pathlib import Path

_LOCAL_DIR = Path(__file__).parent.parent / "data"
if not _LOCAL_DIR.exists():
    _LOCAL_DIR.mkdir()
_REMOTE_DIR_GITHUB = "https://github.com/datavil/datasets/raw/main/feather/"
_EXTENSION = ".feather"
_INFO_FILE = "https://github.com/datavil/datasets/raw/main/datasets_info.csv"
