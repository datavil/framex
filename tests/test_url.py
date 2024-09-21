import requests

import framex as fx


def check_url(url):
    """Check if the URL is valid."""
    try:
        response = requests.head(url, allow_redirects=True)
    except requests.RequestException:
        return False
    return response.status_code == 200


def test_get_url():
    """Test `get_url` function."""
    for format in ["csv", "parquet", "feather"]:
        url = fx.get_url("mpg", format=format)
        assert check_url(url)

    return


if __name__ == "__main__":
    test_get_url()
