from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from polars import read_ipc, read_parquet, scan_ipc, scan_parquet

from framex._dicts import _DATASETS, _LOCAL_CACHES
from framex._dicts._constants import _EXTENSION, _LOCAL_DIR

if TYPE_CHECKING:
    from polars import DataFrame, LazyFrame


def load(
    name: str,
    *,
    lazy: bool = False,
    check_local: bool = True,
    cache: bool = True,
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
    if _EXTENSION == "parquet":
        loader: Callable[..., DataFrame | LazyFrame] = (
            scan_parquet if lazy else read_parquet
        )
    elif _EXTENSION == "feather":
        loader: Callable[..., DataFrame | LazyFrame] = scan_ipc if lazy else read_ipc

    # check if the dataset is available
    if name not in _DATASETS:
        msg = f"Dataset {name} not found."
        raise ValueError(msg)

    # local_path = _LOCAL_CACHES.get(name)
    # load the dataset
    if check_local:
        if name in _LOCAL_CACHES:
            frame = loader(_LOCAL_CACHES.get(name), memory_map=False)
        else:
            frame = loader(_DATASETS.get(name), memory_map=False)
    else:
        frame = loader(_DATASETS.get(name), memory_map=False)

    # cache the dataset locally
    if cache and name not in _LOCAL_CACHES:
        path = _LOCAL_DIR / f"{name}.{_EXTENSION}"
        if lazy:
            if _EXTENSION == "parquet":
                frame.sink_parquet(path, compression="zstd")
            elif _EXTENSION == "feather":
                frame.collect().write_ipc(path, compression="zstd")
                # sink IPC is not yet supportted
                # polars.exceptions.InvalidOperationError:
                # sink_Ipc(IpcWriterOptions { compression: Some(ZSTD), maintain_order: true })
                # not yet supported in standard engine.
                # Use 'collect().write_parquet()'
                ## polars 1.7.1
        else:
            if _EXTENSION == "parquet":
                frame.write_parquet(path, compression="zstd")
            elif _EXTENSION == "feather":
                frame.write_ipc(path, compression="zstd")

    return frame
