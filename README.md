# FRAMES

Getting __testing datasets__ made easy.
Built on top of polars.

## Installation

to get started, install the library with:

```shell
pip install framex
```

## Usage

```python
import framex as fx
```

### Loading datasets

```python
iris = fx.load("iris")
```

which returns a polars __DataFrame__

```python
iris = fx.load("iris", lazy=True)
```

which returns a polars __LazyFrame__

Both these operations create local copies of the datasets
as by default ```cahce=True```.

### Available datasets

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
