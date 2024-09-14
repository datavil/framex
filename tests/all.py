from tests import assert_available, assert_load, clean

if __name__ == "__main__":
    try:
        assert_available()
        assert_load()
        clean()
    except Exception as e:
        raise f"Did not pass all tests: {e}" from e
