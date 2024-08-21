from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from polars import read_ipc, scan_ipc

from frames._dicts import _DATASETS, _LOCAL_CACHES, _REMOTE_DATASETS
from frames._dicts._constants import _LOCAL_DIR

if TYPE_CHECKING:
    from polars import DataFrame, LazyFrame


def load(
    name: str, *, lazy: bool = False, check_local: bool = True, cache: bool = True
) -> DataFrame | LazyFrame:
    """
    Loads dataset by with the given name if available.

    Parameters
    ----------
    name : str
        Name of the dataset to load.
    lazy : bool, optional
        Lazy loading,
        Default is  False

    check_local : bool, optional
        Whether to check if the dataset is available locally
        Default is True

    cache : bool, optional
        Whether to cache the dataset locally.
        Default is True

    Returns
    -------
    polars.DataFrame or polars.LazyFrame
    """
    # select the function to load the dataset
    loader = scan_ipc if lazy else read_ipc
    # check if the dataset is available
    if name not in _DATASETS:
        msg = f"Dataset {name} not found."
        raise ValueError(msg)

    local_path = _LOCAL_CACHES.get(name)
    # load the dataset
    if check_local:
        if Path(local_path).exists():
            frame = loader(local_path)
        else:
            frame = loader(_DATASETS.get(name))
    else:
        frame = loader(_DATASETS.get(name))

    # cache the dataset locally
    if cache and not Path(local_path).exists():
        if lazy:
            frame.sink_ipc(local_path, compression="zstd")
        else:
            frame.write_ipc(local_path, compression="zstd")

    return frame


def available(option: str | None = None) -> list[str]:
    """
    List available datasets.

    Parameters
    ----------
    option : str, optional {"remote", "local"}
        The option to list available datasets.
        Default is None

    Returns
    -------
    list of available datasets

    Raises
    ------
    ValueError
        If the option is not 'remote' or 'local'.

    """
    if option is None:
        return {
            "remote": list(_REMOTE_DATASETS.keys()),
            "local": list(_LOCAL_CACHES.keys()),
        }
    elif option == "remote":
        return {option: list(_REMOTE_DATASETS.keys())}
    elif option == "local":
        return {option: list(_LOCAL_CACHES.keys())}
    else:
        msg = "Invalid option. Please use either 'remote' or 'local'."
        raise ValueError(msg)
