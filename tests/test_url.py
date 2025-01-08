import framex as fx


def test_get_url():
    """Test `get_url` function."""
    for format in ["csv", "parquet", "feather"]:
        url = fx.get_url("mpg", format=format)
        assert url

    return


if __name__ == "__main__":
    test_get_url()
