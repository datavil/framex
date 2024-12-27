from __future__ import annotations

import shutil
from pathlib import Path
from typing import TYPE_CHECKING, Callable, Literal

from polars import read_ipc, read_parquet

from framex._dicts import _LOCAL_CACHES, _LOCAL_CACHES_EXT, _REMOTE_DATASETS
from framex._dicts._constants import _EXTENSION, _LOCAL_DIR
from framex.utils._colors import (
    blue,
    bold,
    cyan,
    green,
    magenta,
    red,
    yellow,
)
from framex.utils._exceptions import (
    DatasetExistsError,
    DatasetNotFoundError,
    InvalidFormatError,
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
        raise InvalidFormatError(msg)
    return


def _get(
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
        Default is False

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
            msg = yellow(
                f"Both `{bold('--dir')}` and `{bold('--cache')}` used, ignoring {bold('--dir')}."
            )
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
        raise DatasetNotFoundError(msg)
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
            msg += magenta(f"Use {bold('--overwrite')} or {bold('-o')} to overwrite ")
            msg += magenta(
                f"or use {bold('-dir')} or {bold('-d')} to specify a different directory."
            )
            raise DatasetExistsError(msg)
        else:
            _save(frame=frame, path=path, format=format)
            print(f"{yellow(bold('Overwritten:'))} {cyan(path)}")
    elif path not in cached:
        _save(frame=frame, path=path, format=format)
        print(f"{green(bold('Saved:'))} {cyan(path)}")

    return


def _bring(
    name: str,
    *,
    dir: str | Path | None = None,
    format: str | Literal["feather", "parquet", "csv", "json", "ipc"] = "csv",
    overwrite: bool = False,
) -> None:
    """
    Bring a dataset from the cache to the current working directory or to a specified directory.

    Parameters
    ----------
    name : str
        Name of the dataset to bring from the cache.

    dir : str, optional
        Directory to save the dataset to.

    format : str or Literal["feather", "parquet", "csv", "json", "ipc"], optional
        The format to save the dataset in.
        Default is "feather"

    overwrite : bool, optional
        Whether to overwrite an existing dataset with the same name.
        Default is False

    Returns
    -------
    None

    """
    cache_dir = _LOCAL_DIR
    cached = list(cache_dir.glob(f"{name}.*"))
    formats = ["csv", "feather", "parquet", "ipc", "json"]

    # resolve dir
    if dir is None:
        new_dir = Path().resolve()
    else:
        new_dir = Path(dir).resolve()

    # handle `does not exist locally`
    if cached == []:
        msg = red(f"Dataset `{bold(name)}` not found in the cache directory.")
        raise DatasetNotFoundError(msg)

    # handle `format`
    if format not in formats:
        msg = red(
            f"Format `{bold(format)}` not supported. Please choose from {bold(formats)}"
        )
        raise InvalidFormatError(msg)

    # handle `already existing dataset` here
    if not overwrite:
        destination = new_dir / f"{name}.{format}"
        if destination.exists():
            msg = f"Dataset `{cyan(bold(name))}` already exists in `{cyan(destination)}`.\n"
            msg += magenta(f"Use {bold('--overwrite')} or {bold('-o')} to overwrite ")
            raise DatasetExistsError(msg)
        elif new_dir.glob(f"{name}.*") != []:
            msg = f"Dataset `{cyan(bold(name))}` already exists at `{cyan(new_dir)}`.\n"

    # prioritize the same format
    eq_fmt_path = cache_dir / f"{name}.{format}"
    if eq_fmt_path.exists():
        destination = new_dir / f"{name}.{format}"
        shutil.copy(eq_fmt_path, destination)
        print(f"{green(bold('Brought:'))} {cyan(destination)}")
    else:  # bring whichever format available, in order
        for fmt in formats:
            cache_file = cache_dir / f"{name}.{fmt}"
            if cache_file.exists():
                destination = new_dir / f"{name}.{fmt}"
                if not destination.exists():
                    shutil.copy(cache_file, destination)
                    print(
                        yellow(
                            f"Format `{bold(format)}` not found, using `{bold(fmt)}` cache"
                        )
                    )
                    print(f"{green(bold('Brought:'))} {cyan(destination)}")
                    break
                elif overwrite and destination.exists():
                    wrn = yellow(
                        f"Format `{bold(format)}` not found, using `{bold(fmt)}` cache\n"
                    )
                    shutil.copy(cache_file, destination)
                    print(wrn, end="")
                    print(f"{yellow(bold('Brought:'))} {cyan(destination)}")
                    break
                else:
                    wrn = yellow(
                        f"Format `{bold(format)}` not found, using `{bold(fmt)}` cache\n"
                    )
                    msg = f"Dataset `{cyan(bold(name))}` already exists in `{cyan(destination)}`.\n"
                    msg += magenta(
                        f"Use {bold('--overwrite')} or {bold('-o')} to overwrite "
                    )
                    raise DatasetExistsError(wrn + msg)

    return


def _print_avail(which: Literal["all", "remote", "local"] = "all", includes: str | None = None) -> None:
    remote_datasets = sorted(_REMOTE_DATASETS.keys(), key=str.lower)
    local_datasets_ext = sorted(_LOCAL_CACHES_EXT.keys(), key=str.lower)
    local_datasets = sorted(_LOCAL_CACHES.keys(), key=str.lower)


    if includes is not None:
        remote_datasets = [x for x in remote_datasets if includes in x]
        local_datasets = [x for x in local_datasets if includes in x]
        local_datasets_ext = [x for x in local_datasets_ext if includes in x]

    spacer = "\t"
    if which == "local":
        print(
            bold("Locally available datasets:"),
            f"({red('feather')}, {blue('parquet')}, {green('csv')}, {yellow('other')})",
        )
        for name in local_datasets_ext:
            no_ext = name.split(".")[0]
            if ".feather" in name:
                print(f"{red(no_ext)}", end=spacer)
            elif ".parquet" in name:
                print(f"{blue(no_ext)}", end=spacer)
            elif ".csv" in name:
                print(f"{green(no_ext)}", end=spacer)
            else:
                print(f"{yellow(no_ext)}", end=spacer)
        print()

    elif which == "remote":
        print(bold("Remote datasets:"))
        for name in remote_datasets:
            print(f"{cyan(name)}", end=spacer)
        print()

    elif which == "all":
        print(
            bold("Locally available datasets:"),
            f"({red('feather')}, {blue('parquet')}, {green('csv')}, {yellow('other')})",
        )
        for name in local_datasets_ext:
            no_ext = name.split(".")[0]
            if ".feather" in name:
                print(f"{red(no_ext)}", end=spacer)
            elif ".parquet" in name:
                print(f"{blue(no_ext)}", end=spacer)
            elif ".csv" in name:
                print(f"{green(no_ext)}", end=spacer)
            else:
                print(f"{yellow(no_ext)}", end=spacer)
        print()
        print(bold("Remote datasets:"))
        for name in remote_datasets:
            print(f"{cyan(name)}", end=spacer)
        print()
    else:
        msg = red(f"Invalid key `{bold(which)}` for available datasets.")
        raise KeyError(msg)

    return


if __name__ == "__main__":
    new_dir = Path("../..").resolve()
    for p in new_dir.glob("iris.*"):
        print(type(new_dir.glob("irgdgdis.*")))
        print(p.name)
