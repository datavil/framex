from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Callable, Literal

from polars import read_ipc, read_parquet

from framex._dicts import _REMOTE_DATASETS
from framex._dicts._constants import _EXTENSION, _LOCAL_DIR
from framex.utils._colors import (
    bold,
    cyan,
    green,
    magenta,
    red,
    yellow,
)

# from framex._dicts._constants import _EXTENSION, _LOCAL_DIR

""" 
cyan: path to the dataset
green: saved
yellow: overwritten
magenta: warning (use --overwrite or -o to overwrite)
red: errors
"""

if TYPE_CHECKING:
    from polars import DataFrame


def _save(
    frame: DataFrame,
    path: Path,
    format: str | Literal["feather", "parquet", "csv", "json", "ipc"] = _EXTENSION,
) -> None:
    """
    Saves a LazyFrame to the desired format.

    Parameters
    ----------
    frame : polars.LazyFrame
        The frame to save.
    name : str
        The name of the dataset.
    path : Path[str]
        The path to save the dataset to.
    format : str or Literal["feather", "parquet", "csv", "json", "ipc"], optional
        The format to save the dataset in.
        Default is "feather"
    """
    if format in ("feather", "ipc"):
        frame.write_ipc(path, compression="zstd")
    elif format == "parquet":
        frame.write_parquet(path, compression="zstd")
    elif format == "csv":
        frame.write_csv(path)
    elif format == "json":
        frame.write_ndjson(path)
    else:
        msg = red(
            f"Invalid format: {bold(format)} format must be one of 'feather', 'parquet', 'csv', 'json', 'ipc'"
        )
        raise ValueError(msg)
    return


def get(
    name: str,
    *,
    dir: str | Path | None = None,
    overwrite: bool = False,
    format: str | Literal["feather", "parquet", "csv", "json", "ipc"] = _EXTENSION,
    cache: bool = False,
) -> None:
    """
    Loads dataset by with the given name if available.

    Parameters
    ----------
    name : str
        Name of the dataset to load.

    dir : str, optional
        Directory to save the dataset to.

    overwrite : bool, optional
        Whether to overwrite the dataset if it already exists.
        Default is True

    format : str or Literal["feather", "parquet", "csv", "json", "ipc"], optional
        The format to save the dataset in.
        Default is "feather"

    cache : bool, optional
        Whether to save to the local cache directory.
        Default is False

    Returns
    -------
    None
    """
    if dir is None and not cache:
        dir = Path().resolve()  # current working directory
    elif cache:
        if dir is not None:
            msg = yellow(f"Both `{bold('--dir')}` and `{bold('--cache')}` used, ignoring {bold('--dir')}.")
            print(msg)

        dir = _LOCAL_DIR  # local cache directory
    else:
        dir = Path(dir).resolve()  # the directory provided by the user

    # select the function to load the dataset
    if _EXTENSION == "parquet":
        loader: Callable[..., DataFrame] = read_parquet
    elif _EXTENSION == "feather":
        loader: Callable[..., DataFrame] = read_ipc

    # check if the dataset is available
    if name not in _REMOTE_DATASETS:
        msg = red(f"Dataset `{bold(name)}` not found.")
        raise ValueError(msg)
    else:
        frame = loader(_REMOTE_DATASETS.get(name))

    # list of all files in the directory
    dir = Path(dir).resolve()
    if not dir.exists():
        msg = red(f"Directory `{bold(dir)}` does not exist.")
        raise FileNotFoundError(msg)

    cached = list(dir.glob(f"*{format}"))
    path = dir / f"{name}.{format}"

    if path in cached:
        if not overwrite:
            msg = f"Dataset `{cyan(bold(name))}` already exists at `{cyan(path)}`.\n"
            msg += magenta(f"Use {bold('--overwrite')} or {bold('-o')} to overwrite.\n")
            msg += magenta(f"Or use {bold('-dir')} or {bold('-d')} to specify a different directory.")
            print(msg)
            return
        else:
            _save(frame=frame, path=path, format=format)
            print(f"{yellow(bold('Overwritten:'))} {cyan(path)}")
    elif path not in cached:
        _save(frame=frame, path=path, format=format)
        print(f"{green(bold('Saved:'))} {cyan(path)}")

    return
