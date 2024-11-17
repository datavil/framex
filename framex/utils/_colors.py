

def black(text) -> str:  # noqa: D103
    return f"\033[30m{text}\033[0m"


def red(text) -> str:  # noqa: D103
    return f"\033[31m{text}\033[0m"


def green(text) -> str:  # noqa: D103
    return f"\033[32m{text}\033[0m"


def yellow(text) -> str:  # noqa: D103
    return f"\033[33m{text}\033[0m"


def blue(text) -> str:  # noqa: D103
    return f"\033[34m{text}\033[0m"


def magenta(text) -> str:  # noqa: D103
    return f"\033[35m{text}\033[0m"


def cyan(text) -> str:  # noqa: D103
    return f"\033[36m{text}\033[0m"


def white(text) -> str:  # noqa: D103
    return f"\033[37m{text}\033[0m"

def bold(text: str) -> str:  # noqa: D103
    return f"\033[1m{text}\033[22m"  # Adding bold escape codes

if __name__ == "__main__":
    # print(red("red"), bold(red("bold")))
    # print(green("green"), bold(green("bold")))
    # print(yellow("yellow"), bold(yellow("bold")))
    # print(blue("blue"), bold(blue("bold")))
    # print(magenta("magenta"), bold(magenta("bold")))
    format = "csvx"
    msg = f"Invalid format: {format}. format must be one of 'feather', 'parquet', 'csv', 'json', 'ipc'"
    print(bold(red(msg)))
    msg = f"Invalid format: {bold(format)}. format must be one of 'feather', 'parquet', 'csv', 'json', 'ipc'"
    print(red(msg))
    # print(red(f"I have some bold text, {bold("I have some bold text")} but should reset here"))
    # print(red(f"I have some bold text, {bold('I have some bold text')} but should reset here"))
    name = "mpg"
    path = "C:/Users/zafi_/.cache/framex/mpg.csv"
    msg = f"Dataset `{cyan(bold(name))}` already exists at `{cyan(path)}`.\n"
    msg += magenta(f"Use {bold("--overwrite")} or {bold("-o")} to overwrite.\n")
    msg += magenta(f"Or use {bold("--dir")} or {bold("-d")} to specify a different directory.")
    print(msg)

    print(f"{yellow(bold("Overwritten:"))} {cyan(path)}")
    print(f"{green(bold("Saved:"))} {cyan(path)}")