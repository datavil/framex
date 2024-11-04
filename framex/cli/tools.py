import argparse
import importlib.metadata

from framex.cli._cli import get
from framex.datasets import about, available, load


def main(): # noqa: D103
    parser = argparse.ArgumentParser(description="Framex CLI")
    subparsers = parser.add_subparsers(dest="command")

    # get subparsers
    get_parser = subparsers.add_parser("get", help="Get dataset(s)")
    get_parser.add_argument(
        "datasets", nargs="+", help="Dataset name(s), accepts multiple names"
    )
    get_parser.add_argument(
        "--dir",
        "-d",
        help="Directory to save the dataset to. Defaults to current directory.",
        default=".",
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
    # about subparsers
    info_parser = subparsers.add_parser("about", help="Info about dataset(s)")
    info_parser.add_argument("datasets", nargs="+", help="Info about dataset(s)")
    # list subparsers
    subparsers.add_parser("list", help="List available datasets")
    subparsers.add_parser("version", help="Show version")
    # show subparsers
    show_parser = subparsers.add_parser("show", help="Show a single dataset")
    show_parser.add_argument("dataset", help="Dataset name")
    # describe subparsers
    describe_parser = subparsers.add_parser("describe", help="Describe a dataset")
    describe_parser.add_argument("dataset", help="Dataset name")

    # PARSE ALL ARGS
    args = parser.parse_args()

    # EVALUATE ARGS
    # Subcommand: list
    if args.command is None:
        parser.print_help()  # Show help if no command is provided
        return

    elif args.command == "get":
        for dataset in args.datasets:
            try:
                get(
                    name=dataset,
                    dir=args.dir,
                    format=args.format,
                    overwrite=args.overwrite,
                )
            except ValueError:
                print(f"Dataset `{dataset}` not found.")

    elif args.command == "list":
        print(available()["remote"])

    # Subcommand: version
    elif args.command == "version":
        print(importlib.metadata.version("framex"))

    # Subcommand: about
    elif args.command == "about":
        for dataset in args.datasets:
            try:
                about(name=dataset, mode="print")
                print()
            except ValueError:
                print(f"Dataset `{dataset}` not found.")
    # Subcommand: show
    elif args.command == "show":
        try:
            frame = load(name=args.dataset)
            print(frame)

        except ValueError:
            print(f"Dataset `{args.dataset}` not found.")
    # Subcommand: describe
    elif args.command == "describe":
        try:
            frame = load(name=args.dataset)
            print(frame.describe())
        except ValueError:
            print(f"Dataset `{args.dataset}` not found.")


    else:
        msg = f"Invalid command: {args.command}"
        raise ValueError(msg)

    return


if __name__ == "__main__":
    main()
