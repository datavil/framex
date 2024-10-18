import argparse
import importlib.metadata

from framex.cli._cli import get
from framex.datasets import about, available


def main():
    parser = argparse.ArgumentParser(description="Framex CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand: get
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
    info_parser = subparsers.add_parser("about", help="info about a dataset")
    info_parser.add_argument("datasets", nargs="+", help="info about a dataset(s)")

    # Subcommand: list
    subparsers.add_parser("list", help="List available datasets")  # noqa: F841
    subparsers.add_parser("version", help="Show version")  # noqa: F841
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()  # Show help if no command is provided
        return

    elif args.command == "get":
        for dataset in args.datasets:
            get(
                name=dataset,
                dir=args.dir,
                format=args.format,
                overwrite=args.overwrite,
            )
    elif args.command == "list":
        print(available()["remote"])

    elif args.command == "version":
        print(importlib.metadata.version("framex"))

    elif args.command == "about":
        for dataset in args.datasets:
            about(name=dataset, mode="print")
            print()
    else:
        msg = f"Invalid command: {args.command}"
        raise ValueError(msg)

    return


if __name__ == "__main__":
    main()
