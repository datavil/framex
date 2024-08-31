import argparse

from framex import available
from framex.datasets._cli import get


def main():
    parser = argparse.ArgumentParser(description="Framex CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand: get
    get_parser = subparsers.add_parser("get", help="Get dataset(s)")
    get_parser.add_argument("datasets", nargs="+", help="Dataset name(s), accepts multiple names")
    get_parser.add_argument("--dir", help="Directory to save the dataset to", default=".")
    get_parser.add_argument("--format", help="Format to save the dataset in", default="csv")
    get_parser.add_argument("--overwrite", action="store_true", help="Overwrite the dataset if it already exists")

    # Subcommand: list
    list_parser = subparsers.add_parser("list", help="List available datasets")
    # No additional arguments needed for 'list'

    args = parser.parse_args()

    if args.command == "get":
        for dataset in args.datasets:
            get(
                name=dataset,
                dir=args.dir,
                format=args.format,
                overwrite=args.overwrite,
            )
    elif args.command == "list":
        print(available(option="remote")['remote'])
    else:
        msg = f"Invalid command: {args.command}"
        raise ValueError(msg)

if __name__ == "__main__":
    main()
