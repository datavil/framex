import importlib.metadata

from framex.datasets import about, available, get_url, load

__version__ = importlib.metadata.version("framex")

__all__ = ["about", "available", "load", "get_url", "__version__"]
