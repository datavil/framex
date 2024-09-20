from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Literal

import polars
from polars import read_ipc, read_parquet, scan_ipc, scan_parquet

from framex._dicts import _DATASETS, _LOCAL_CACHES, _REMOTE_DATASETS
from framex._dicts._constants import _EXTENSION, _INFO_FILE, _LOCAL_DIR

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
        loader: Callable[..., DataFrame | LazyFrame] = scan_parquet if lazy else read_parquet
    # elif _EXTENSION == "feather":
    #     loader: Callable[..., DataFrame | LazyFrame] = scan_ipc if lazy else read_ipc

    # check if the dataset is available
    if name not in _DATASETS:
        msg = f"Dataset {name} not found."
        raise ValueError(msg)

    # local_path = _LOCAL_CACHES.get(name)
    # load the dataset
    if check_local:
        if name in _LOCAL_CACHES:
            frame = loader(_LOCAL_CACHES.get(name))
        else:
            frame = loader(_DATASETS.get(name))
    else:
        frame = loader(_DATASETS.get(name))

    # cache the dataset locally
    if cache and name not in _LOCAL_CACHES:
        if lazy:
            # sink IPC is not yet supportted
            # polars.exceptions.InvalidOperationError:
            # sink_Ipc(IpcWriterOptions { compression: Some(ZSTD), maintain_order: true })
            # not yet supported in standard engine.
            # Use 'collect().write_parquet()'
            frame.sink_parquet(_LOCAL_DIR / f"{name}.{_EXTENSION}", compression="zstd")
        else:
            frame.write_parquet(_LOCAL_DIR / f"{name}.{_EXTENSION}", compression="zstd")

    return frame


def available(option: str | None = None) -> dict[str, list[str]]:
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

def about(name: str, mode: Literal["print", "row"] = "print") -> None | polars.DataFrame:
    """
    Print or return information about a dataset.

    Parameters
    ----------
    name : str
        Name of the dataset.
    mode : Literal["print", "row"]
        The mode to print information.
        Default is "print"
            print: prints the information
            row: returns the information as a single row polars.DataFrame

    Returns
    -------
    None
    """
    df = polars.read_csv(_INFO_FILE)
    try:
        row = df.filter(polars.col("name")==name)
    except Exception as e:
        msg = f"Dataset {name} not found in datasets_info.csv"
        raise ValueError(msg) from e

    if mode == "row":#
        return row
    elif mode == "print":
        og_name = row.select("source").item().split('/')[-1]
        og_id = "OG NAME"
        for column in row.columns:
            print(f"{column.upper():<8}: {row.select(column).item()}")
        print(f"{og_id:<8}: {og_name}")
        return
    else:
        msg = "Invalid mode. Please use either 'print' or 'row'."
        raise ValueError(msg)

