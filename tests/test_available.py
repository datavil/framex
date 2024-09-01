import framex as fx


def main():
    """Test `available` functions."""
    print(fx.available(option="remote"))  # remote only
    print(fx.available(option="local"))  # locally cached
    print(fx.available(option=None))  # all available
    return

def assert_available():
    """Assertion."""
    assert isinstance(fx.available(option="remote"), dict)
    assert isinstance(fx.available(option="local"), dict)
    assert isinstance(fx.available(option=None), dict)


if __name__ == "__main__":
    main()
    assert_available()
