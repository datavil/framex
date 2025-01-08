from __future__ import annotations

import json
import time
from pathlib import Path
from urllib.request import urlopen
from urllib.error import HTTPError

from framex._dicts._constants import _API_URL, _EXTENSION, _LOCAL_DIR


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
    response = urlopen(api_url)

    # Check if the request was successful
    if response.status != 200:
        msg = f"Error: Received status code {response.status_code}"
        raise HTTPError(msg)
    try:
        # Parse the response as JSON
        content = response.read().decode("utf-8")
        files = json.loads(content)
    except json.JSONDecodeError as err:
        msg = "Error: Failed to decode JSON response"
        raise json.JSONDecodeError(msg) from err

    # Check if the response is a list (expected format)
    if not isinstance(files, list):
        msg = f"Error: Expected a list, but got {type(files).__name__}"
        raise TypeError(msg)

    # Extract .feather files
    datasets = {
        file["name"][: -len(f".{_EXTENSION}")]: file["download_url"]
        for file in files
        if isinstance(file, dict) and file.get("name", "").endswith(f".{_EXTENSION}")
    }

    return datasets


def _save_json(datasets: dict[str, str]) -> None:
    local_json = _LOCAL_DIR.parent / "datasets.json"
    with Path.open(local_json, "w") as file_json:
        json.dump(datasets, file_json, indent=4)

    return


def _read_json(local_json: Path) -> dict[str, str]:
    local_json = _LOCAL_DIR.parent / "datasets.json"
    with Path.open(local_json, "r") as file_json:
        _datasets_dict = json.load(file_json)
    return _datasets_dict


def _cache_or_remote(url: str) -> dict[str, str]:
    """
    Decides whether to use the local cache or the remote datasets.

    Above one hour uses remote API
    Less than one hour uses local cache

    Parameters
    ----------
    url : str
        The URL of the GitHub API.

    Returns
    -------
    dict
        The names of the datasets mapped to their download URLs.

    """
    now = time.time()

    local_json = _LOCAL_DIR.parent / "datasets.json"
    if local_json.exists():
        modified = local_json.stat().st_mtime
        if now - modified < 3600:
            _datasets_dict = _read_json(local_json=local_json)
            # print(f"Using cached datasets from {local_json}")
        elif now - modified >= 3600:
            _datasets_dict = _get_names(url)
            _save_json(datasets=_datasets_dict)
            # print(f"Updated cached datasets at {local_json}")
    else:
        _datasets_dict = _get_names(url)
        _save_json(datasets=_datasets_dict)
        # print(f"Created cached datasets at {local_json}")
    return _datasets_dict


_GITHUB_DATASETS = _cache_or_remote(url=_API_URL)
