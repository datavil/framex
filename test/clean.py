import shutil
from pathlib import Path

if __name__ == "__main__":
    root = Path("../").resolve()

    for pycache in root.rglob("__pycache__"):
        if pycache.is_dir() and ".venv" not in pycache.parts:
            print(f"Removing {pycache}")
            shutil.rmtree(pycache)
