import importlib.metadata

from framex.datasets import about, available, get_url, load

__version__ = importlib.metadata.version("framex")

__all__ = ["about", "available", "load", "get_url"]

from polars import DataFrame


def __getattr__(name: str) -> DataFrame:
    """
    Allow loading datasets importing as attributes.

    e.g. `from framex import iris`.

    This is equivalent to `framex.load("iris")`.

    Parameters
    ----------
    name : str
        The name of the dataset to load.

    Returns
    -------
    DataFrame
        The dataset as a Polars DataFrame.
    """
    if name in available()["remote"]:
        dataset = load(name=name)
    else:
        msg = f"`framex` has no attribute or dataset `{name}`"
        raise AttributeError(msg)

    return dataset
