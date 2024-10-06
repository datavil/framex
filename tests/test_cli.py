
import shutil
import subprocess
from pathlib import Path


def run_command(command):  # noqa: D103
    result = subprocess.run(command, shell=True, check=True)
    return result


def test_cli():
    """Test the CLI components."""
    # test get
    Path("data").mkdir()
    run_command("fx get titanic --dir ./data --format parquet")

    # test multiple get
    run_command("fx get titanic mpg --dir ./data --format csv")

    # test list
    run_command("fx list")

    # test about
    run_command("fx about titanic")

    # test about multiple
    run_command("fx about titanic mpg")
    return


def main():  # noqa: D103
    if Path("data").exists():
        shutil.rmtree("data", ignore_errors=True)
        Path ("data").mkdir()
    else:
        Path ("data").mkdir()

    test_cli()

    return


if __name__ == "__main__":
    main()
