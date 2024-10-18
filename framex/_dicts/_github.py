from __future__ import annotations

import json

import requests

from framex._dicts._constants import _EXTENSION

# GitHub API URL for the directory contents
_API_URL = f"https://api.github.com/repos/datavil/datasets/contents/{_EXTENSION}"


def _get_names(api_url: str) -> dict[str, str]:
    """
    Get the names of the datasets from the GitHub API.

    Parameters
    ----------
    api_url : str
        The URL of the GitHub API.

    Returns
    -------
    dict
        The names of the datasets mapped to their download URLs.
    """
    response = requests.get(api_url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return {}

    try:
        # Parse the response as JSON
        files = response.json()
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON response")
        return {}

    # Check if the response is a list (expected format)
    if not isinstance(files, list):
        print(f"Error: Expected a list, but got {type(files).__name__}")
        return {}

    # Extract .feather files
    datasets = {
        file["name"][:-len(f".{_EXTENSION}")]: file["download_url"]
        for file in files
        if isinstance(file, dict) and file.get("name", "").endswith(f".{_EXTENSION}")
    }

    return datasets


_GITHUB_DATASETS = _get_names(_API_URL)
