
import shutil
import subprocess
from pathlib import Path

def red(text):
    return f"\033[31m{text}\033[0m"

def green(text):
    return f"\033[32m{text}\033[0m"

def blue(text):
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
    # test get
    run_command("fx get titanic --dir ./data --format parquet")

    # test multiple get
    run_command("fx get titanic mpg --dir ./data --format csv")

    # test get with cache
    run_command("fx get iris --dir cache --format feather --overwrite")

    # test list
    run_command("fx list")

    # test about
    run_command("fx about titanic")

    # test about multiple
    run_command("fx about titanic mpg")

    # test an invalid command
    run_command("fx invalid")

    return


def main():  # noqa: D103
    # Remove 'data' directory if it exists, then recreate it
    if Path("data").exists():
        shutil.rmtree("data", ignore_errors=True)
        print("Deleted data directory")

    Path("data").mkdir(exist_ok=True)
    test_cli()
    shutil.rmtree("data", ignore_errors=True)

    return

if __name__ == "__main__":
    main()