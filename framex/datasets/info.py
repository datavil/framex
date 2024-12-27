from __future__ import annotations

from typing import Literal

import polars

from framex._dicts import _LOCAL_CACHES_MAIN_EXT, _REMOTE_DATASETS
from framex._dicts._constants import _INFO_FILE
from framex.utils._exceptions import DatasetNotFoundError


def available(
    includes: str | None = None,
    *,
    option: Literal["remote", "local"] | None = None,
) -> dict[str, list[str]]:
    """
    List available datasets.

    Parameters
    ----------
    includes : str, optional
        A string to filter the available datasets.
        Default is None

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
    remote_datasets = sorted(_REMOTE_DATASETS.keys(), key=str.lower)
    local_datasets = sorted(_LOCAL_CACHES_MAIN_EXT.keys(), key=str.lower)

    if includes is not None:
        remote_datasets = [x for x in remote_datasets if includes in x]
        local_datasets = [x for x in local_datasets if includes in x]

    if option is None:
        return {
            "remote": list(remote_datasets),
            "local": list(local_datasets),
        }
    elif option == "remote":
        return {option: list(remote_datasets)}
    elif option == "local":
        return {option: list(local_datasets)}
    else:
        msg = "Invalid option. Please use either 'remote' or 'local'."
        raise ValueError(msg)


def about(
    name: str, mode: Literal["print", "row"] = "print"
) -> None | polars.DataFrame:
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
    row = df.filter(polars.col("name") == name)
    if row.height == 0:  # no dataset found
        msg = f"Dataset `{name}` not found in datasets_info.csv"
        raise DatasetNotFoundError(msg)
    if mode == "row":
        return row
    elif mode == "print":
        og_name = row.select("source").item().split("/")[-1]
        og_id = "OG NAME"
        for column in row.columns:
            print(f"{column.upper():<8}: {row.select(column).item()}")
        print(f"{og_id:<8}: {og_name}")
        return
    else:
        msg = "Invalid mode. Please use either `print` or `row`."
        raise ValueError(msg)
