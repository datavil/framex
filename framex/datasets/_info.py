from __future__ import annotations

from typing import Literal

import polars

from framex._dicts import _LOCAL_CACHES, _REMOTE_DATASETS
from framex._dicts._constants import _INFO_FILE


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
    try:
        row = df.filter(polars.col("name") == name)
    except Exception as e:
        msg = f"Dataset {name} not found in datasets_info.csv"
        raise ValueError(msg) from e

    if mode == "row":  #
        return row
    elif mode == "print":
        og_name = row.select("source").item().split("/")[-1]
        og_id = "OG NAME"
        for column in row.columns:
            print(f"{column.upper():<8}: {row.select(column).item()}")
        print(f"{og_id:<8}: {og_name}")
        return
    else:
        msg = "Invalid mode. Please use either 'print' or 'row'."
        raise ValueError(msg)
