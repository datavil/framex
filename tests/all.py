from tests import (
    assert_available,
    assert_load,
    clean,
    test_about,
    test_cli,
    test_get_url,
)

if __name__ == "__main__":
    try:
        # clean()
        assert_available()
        assert_load()
        assert_load()
        test_about()
        test_get_url()
        test_cli()
        clean()
    except Exception as e:
        raise f"Did not pass all tests: {e}" from e
