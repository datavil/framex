from __future__ import annotations

from typing import Literal

from framex._dicts import _DATASETS
from framex._dicts._constants import _EXTENSION
from framex.utils._colors import red


def get_url(
    name: str, format: Literal["csv", "parquet", "feather"] = _EXTENSION
) -> str:
    """
    Returns the URL of the dataset.

    Parameters
    ----------
    name : str
        Name of the dataset.

    format : {'csv', 'parquet', 'feather'}, optional
        Format of the dataset.
        Default is 'parquet'

    Returns
    -------
    str
        URL of the dataset.

    Examples
    --------
    .. jupyter-execute ::
    
        import framex as fx

        fx.get_url('diamonds')
    """
    if name not in _DATASETS:
        msg = red(f"Dataset {name} not found.")
        raise ValueError(msg)

    url = _DATASETS.get(name)
    url = url.replace(_EXTENSION, format)

    return url
