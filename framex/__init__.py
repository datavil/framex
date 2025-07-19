import importlib.metadata
from typing import TYPE_CHECKING

from framex.datasets import about, available, get_url, load

__version__ = importlib.metadata.version("framex")

__all__ = ["about", "available", "load", "get_url"]

if TYPE_CHECKING:
    from polars import DataFrame


def __getattr__(name: str) -> DataFrame:
    if name in available()["remote"]:
        return load(name=name)
    msg = f"`framex` has no attribute or dataset `{name}`"
    raise AttributeError(msg)
