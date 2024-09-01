# FRAMEX

Getting __test datasets__ made easy.   
Built on top of [polars](https://pola.rs/).

## Installation

To get started, install the library with:

```shell
pip install framex
```

## Usage

### CLI

Get a single dataset:

```shell
fx get iris
```

or get multiple datasets:

```shell
fx get iris mpg titanic
```

which will download dataset(s) to the current directory.

```shell
fx list
```

this will list all available datasets on the remote server.

### Python

```python
import framex as fx
```

#### Loading datasets

```python
iris = fx.load("iris")
```

which returns a polars [__DataFrame__](https://docs.pola.rs/api/python/stable/reference/dataframe/index.html)  
Therefore, you can use all the __polars__ functions and methods on the returned __DataFrame__.


```python
iris.head()
```

```text
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

```python
iris = fx.load("iris", lazy=True)
```

which returns a polars [__LazyFrame__](https://docs.pola.rs/api/python/stable/reference/lazyframe/index.html)

Both these operations create local copies of the datasets
by default ```cache=True```.

#### Available datasets

To see the list of available datasets, run:

```python
fx.available()
```

```python
{'remote': ['iris', 'mpg', 'netflix', 'starbucks', 'titanic'], 'local': ['titanic']}
```

which returns a dictionary of both __locally__ and __remotely__ available datasets.

To see only __local__ or __remote__ datasets, run:

```python
fx.available("local")
fx.available("remote")
```

```python
{'local': ['titanic']}
{'remote': ['iris', 'mpg', 'netflix', 'starbucks', 'titanic']}
```
