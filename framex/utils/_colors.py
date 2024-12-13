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
    pass
