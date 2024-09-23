import time

import polars as pl

import framex as fx


def timer(func, *args, **kwargs):
    def inner(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"function {func.__name__} took {end - start:.2f} seconds")
        return result

    return inner


@timer
def load_parquet(url):  # noqa: D103
    for _ in range(10):
        pl.scan_parquet(url).sink_parquet("f.parquet")
    return


@timer
def load_feather(url):  # noqa: D103
    for _ in range(10):
        pl.scan_ipc(url).collect().write_ipc("f.feather")
    return


def main():
    for name in fx.available()["remote"]:
        print(name.upper())
        url = fx.get_url(name, format="parquet")
        load_parquet(url)
        url = fx.get_url(name, format="feather")
        load_feather(url)
        print()
    return


if __name__ == "__main__":
    main()

"""
conclusion feather loading is 1.5x-2.5x faster than parquet

....
DEFECTS
function load_parquet took 5.71 seconds
function load_feather took 3.44 seconds
_EXTENSION will be reverted to feather
IRIS
function load_parquet took 5.93 seconds
function load_feather took 3.34 seconds

MPG
function load_parquet took 5.64 seconds
function load_feather took 3.31 seconds

NETFLIX
function load_parquet took 9.38 seconds
function load_feather took 4.27 seconds

PARIS2024
function load_parquet took 7.53 seconds
function load_feather took 3.72 seconds

POKEMON
function load_parquet took 7.12 seconds
function load_feather took 3.64 seconds

STARBUCKS
function load_parquet took 5.77 seconds
function load_feather took 3.43 seconds

TITANIC
function load_parquet took 5.92 seconds
function load_feather took 3.39 seconds
"""
