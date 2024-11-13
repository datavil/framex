![Banner](https://github.com/datavil/framex/blob/master/.github/framex_banner_narrower.png?raw=true)
A [DataVil](https://github.com/datavil) project.

# FrameX

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/Zaf4/framex) [![PyPI](https://img.shields.io/pypi/v/framex?color=blue)](https://pypi.org/project/framex/)

**FrameX** is a light-weight, dataset fetching library for fast **prototyping**, **tutorial creation**, and **experimenting**.

Built on top of [Polars](https://pola.rs/).

## Installation

To get started, install the library with:

``` shell
pip install framex
```

## Usage

### Python

``` python
import framex as fx
```

#### Loading datasets

``` python
iris = fx.load("iris")
```

which returns a [**polars DataFrame**](https://docs.pola.rs/api/python/stable/reference/dataframe/index.html)\
Therefore, you can use all the **polars** functions and methods on the returned **DataFrame**.

``` python
iris.head()
```

``` text
shape: (5, 5)
┌──────────────┬─────────────┬──────────────┬─────────────┬─────────┐
│ sepal_length ┆ sepal_width ┆ petal_length ┆ petal_width ┆ species │
│ ---          ┆ ---         ┆ ---          ┆ ---         ┆ ---     │
│ f32          ┆ f32         ┆ f32          ┆ f32         ┆ str     │
╞══════════════╪═════════════╪══════════════╪═════════════╪═════════╡
│ 5.1          ┆ 3.5         ┆ 1.4          ┆ 0.2         ┆ setosa  │
│ 4.9          ┆ 3.0         ┆ 1.4          ┆ 0.2         ┆ setosa  │
│ 4.7          ┆ 3.2         ┆ 1.3          ┆ 0.2         ┆ setosa  │
│ 4.6          ┆ 3.1         ┆ 1.5          ┆ 0.2         ┆ setosa  │
│ 5.0          ┆ 3.6         ┆ 1.4          ┆ 0.2         ┆ setosa  │
└──────────────┴─────────────┴──────────────┴─────────────┴─────────┘
```

``` python
iris = fx.load("iris", lazy=True)
```

which returns a [**polars LazyFrame**](https://docs.pola.rs/api/python/stable/reference/lazyframe/index.html)

Both these operations create local copies of the datasets by default `cache=True`.

#### Available datasets

To see the list of available datasets, run:

``` python
fx.available()
```

``` python
{'remote': ['iris', 'mpg', 'netflix', 'starbucks', 'titanic'], 'local': ['titanic']}
```

which returns a dictionary of both **locally** and **remotely** available datasets.

To see only **local** or **remote** datasets, run:

``` python
fx.available("local")
fx.available("remote")
```

``` python
{'local': ['titanic']}
{'remote': ['iris', 'mpg', 'netflix', 'starbucks', 'titanic']}
```

#### Getting information on Datasets

To get information on a dataset, run:

``` python
fx.about("mpg") # basically the same as `fx.about("mpg", mode="print")`
```

which will print the information on the dataset as the following:

``` text
NAME    : mpg
SOURCE  : https://www.kaggle.com/datasets/uciml/autompg-dataset
LICENSE : CC0: Public Domain
ORIGIN  : Kaggle
OG NAME : autompg-dataset
```

Or you can get the information as a single row polars.DataFrame by running:

``` python
row = fx.about("mpg", mode="row")
print(row)
```

which will print the information on the dataset **ASCII art** as the following:

``` text
shape: (1, 4)
┌──────┬─────────────────────────────────┬────────────────────┬────────┐       
│ name ┆ source                          ┆ license            ┆ origin │       
│ ---  ┆ ---                             ┆ ---                ┆ ---    │       
│ str  ┆ str                             ┆ str                ┆ str    │       
╞══════╪═════════════════════════════════╪════════════════════╪════════╡       
│ mpg  ┆ https://www.kaggle.com/dataset… ┆ CC0: Public Domain ┆ Kaggle │       
└──────┴─────────────────────────────────┴────────────────────┴────────┘ 
```

or you can simply treat `row` as a polars DataFrame in your code.

#### Getting Dataset URLs

In case you need the file links.

``` python
url_pokemon = fx.get_url("pokemon")
```

by default, the format is " feather".

Optionally, you can specify the format of the dataset.

``` python
url_pokemon_csv = fx.get_url("pokemon", format="csv")
```

### CLI

Get a single dataset:

``` shell
fx get iris
```

or get multiple datasets:

``` shell
fx get iris mpg titanic
```

which will download dataset(s) to the current directory.

For more parameters

``` shell
fx get --help
```

To get the name of the available datasets on the **remote server**.

``` shell
fx list
```

this will list all available datasets on the remote server.
