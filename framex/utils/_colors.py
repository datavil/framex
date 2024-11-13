"""
Black: 30
Red: 31
Green: 32
Yellow: 33
Blue: 34
Magenta: 35
Cyan: 36
White: 37
"""


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
