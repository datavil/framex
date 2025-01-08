from time import time

"""
framex has only two direct dependencies: 
polars and requests
"""

start = time()
import polars as pl # 0.53 to 0.43 seconds
print(f"Imported polars in {time() - start:.2f} seconds")

start = time()
import requests # 0.95 to 0.82 seconds
print(f"Imported requests in {time() - start:.2f} seconds")
