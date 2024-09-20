import polars as pl

import framex as fx


def assert_load():
    """Assertion."""
    assert type(fx.load("titanic")) is pl.DataFrame
    assert type(fx.load("titanic", lazy=True)) is pl.LazyFrame


if __name__ == "__main__":
    # test 1: DataFrame eager
    titanic_eager = fx.load("titanic")
    assert type(titanic_eager) is pl.DataFrame
    # test 2: LazyFrame lazy
    titanic_lazy = fx.load("titanic", lazy=True)
    assert type(titanic_lazy) is pl.LazyFrame

iris = fx.load("iris")
iris = fx.load("iris")
print(iris.head())
