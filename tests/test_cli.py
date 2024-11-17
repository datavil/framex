import shutil
import subprocess
from pathlib import Path

from framex._dicts import _LOCAL_DIR


def red(text) -> str:  # noqa: D103
    return f"\033[31m{text}\033[0m"


def green(text) -> str:  # noqa: D103
    return f"\033[32m{text}\033[0m"


def blue(text) -> str:  # noqa: D103
    return f"\033[34m{text}\033[0m"


def run_command(command):  # noqa: D103
    try:
        print(green(command))
        result = subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(red(e))
        return None

    return result


def test_cli():
    """Test the CLI components."""
    ## GET
    # test get
    run_command("fx get titanic --dir ./data --format parquet")

    # test multiple get
    run_command("fx get titanic mpg --dir ./data --format csv")

    # test with cache
    run_command("fx get titanic --format feather --cache")
    # test get with wrong dir ## ERROR
    run_command("fx get iris --dir wrong --format feather --overwrite")
    # test both dir and cache ##  WARNING
    run_command("fx get titanic --dir ./data --format feather --cache")
    # test get with invalid format ## ERROR
    run_command("fx get titanic --format batman")

    # test list
    run_command("fx list")

    # test about
    run_command("fx about titanic")

    # test about multiple
    run_command("fx about titanic mpg")

    # test version
    run_command("fx --version")

    # test show
    run_command("fx show iris")

    # test describe
    run_command("fx describe titanic")

    # INVALIDS
    # test an invalid command
    run_command("fx do")

    # test an invalid dataset
    run_command("fx show joker")
    run_command("fx about beatles")

    return


def main():  # noqa: D103
    # Remove 'data' directory if it exists, then recreate it
    if Path("data").exists():
        shutil.rmtree("data", ignore_errors=True)
        print("Deleted data directory")

    Path("data").mkdir(exist_ok=True)
    test_cli()
    shutil.rmtree("data", ignore_errors=True)

    shutil.rmtree(_LOCAL_DIR, ignore_errors=True)
    return


if __name__ == "__main__":
    main()
