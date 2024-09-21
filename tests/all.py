from tests import assert_about, assert_available, assert_load, clean, test_get_url

if __name__ == "__main__":
    try:
        # clean()
        assert_available()
        assert_load()
        assert_load()
        assert_about()
        test_get_url()
        clean()
    except Exception as e:
        raise f"Did not pass all tests: {e}" from e
