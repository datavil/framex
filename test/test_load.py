import polars as pl

import framex as fx

if __name__ == "__main__":
    # test 1: DataFrame eager
    titanic_eager = fx.load("titanic")
    assert type(titanic_eager) is pl.DataFrame
    titanic_lazy = fx.load("titanic", lazy=True)
    assert type(titanic_lazy) is pl.LazyFrame
