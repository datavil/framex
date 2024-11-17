import argparse
import importlib.metadata

from framex.cli._cli import get
from framex.datasets import about, available, load
from framex.utils._colors import blue, bold, cyan, red
from framex.utils._exceptions import DatasetNotFoundError, InvalidFormatError


def main():  # noqa: D103
    parser = argparse.ArgumentParser(description=cyan("Framex CLI"))
    # --version
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"framex {blue(importlib.metadata.version('framex'))}",
        help="Show version",
    )
    # init subparsers
    subparsers = parser.add_subparsers(dest="command")

    # ------------------------------"get" subparsers------------------------------
    get_parser = subparsers.add_parser("get", help="Get dataset(s)")
    get_parser.add_argument(
        "datasets", nargs="+", help="Dataset name(s), accepts multiple names"
    )
    get_parser.add_argument(
        "--dir",
        "-d",
        help="Directory to save the dataset to. Defaults to current directory.",
        default=None,
        metavar="",
    )
    get_parser.add_argument(
        "--format",
        "-f",
        help="Format to save the dataset in. Defaults to csv.",
        default="csv",
        metavar="",
    )
    get_parser.add_argument(
        "--overwrite",
        "-o",
        action="store_true",
        help="Whether to overwrite the dataset if it already exists.",
    )
    get_parser.add_argument(
        "--cache",
        "-c",
        action="store_true",
        help="Whether to save to the local cache directory.",
    )
    # ------------------------------"about" subparsers------------------------------
    info_parser = subparsers.add_parser("about", help="Info about dataset(s)")
    info_parser.add_argument("datasets", nargs="+", help="Info about dataset(s)")
    # "list" subparsers
    subparsers.add_parser("list", help="List available datasets")
    # ------------------------------"show" subparsers------------------------------
    show_parser = subparsers.add_parser(
        "show", help="Show a preview of a single dataset"
    )
    show_parser.add_argument("dataset", help="Dataset name")
    # ------------------------------"describe" subparsers------------------------------
    describe_parser = subparsers.add_parser(
        "describe", help="Describe (or summarize) a dataset"
    )
    describe_parser.add_argument("dataset", help="Dataset name")

    # PARSE ALL ARGS ------------------------------
    args = parser.parse_args()

    # EVALUATE ARGS ------------------------------
    # Subcommand: list
    if args.command is None:
        parser.print_help()  # Show help if no command is provided
        return
    # ------------------------------ get ------------------------------
    elif args.command == "get":
        for dataset in args.datasets:
            try:
                get(
                    name=dataset,
                    dir=args.dir,
                    format=args.format,
                    overwrite=args.overwrite,
                    cache=args.cache,
                )
            except InvalidFormatError as err:
                print(err)
            except FileNotFoundError as err:
                print(err)
                return
            except DatasetNotFoundError as err:
                print(err)

    # ------------------------------ list ------------------------------
    elif args.command == "list":
        print(available()["remote"])

    # ------------------------------ about ------------------------------
    elif args.command == "about":
        for dataset in args.datasets:
            try:
                about(name=dataset, mode="print")
                print()
            except DatasetNotFoundError:
                print(red(f"Dataset `{bold(dataset)}` not found."))
            except ValueError as err:
                print(red(err))

    # ------------------------------ show ------------------------------
    elif args.command == "show":
        try:
            frame = load(name=args.dataset)
            print(frame)

        except DatasetNotFoundError: # err not colored
            print(red(f"Dataset `{bold(args.dataset)}` not found."))
    # ------------------------------ describe ------------------------------
    elif args.command == "describe":
        try:
            frame = load(name=args.dataset)
            print(frame.describe())
        except DatasetNotFoundError: # err not colored
            print(red(f"Dataset `{bold(args.dataset)}` not found."))

    else:  # argparse handles this part...
        msg = red(f"Invalid command: `{bold(args.command)}`")
        raise ValueError(msg)

    return


if __name__ == "__main__":
    pass
