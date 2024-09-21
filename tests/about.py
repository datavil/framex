import framex as fx


def assert_about():
    """Test `about` functions."""
    fx.about("mpg", mode="print")
    print(fx.about("mpg", mode="row"))
    return


if __name__ == "__main__":
    assert_about()
