import argparse

from framex.datasets import available
from framex.datasets._cli import get


def main():
    parser = argparse.ArgumentParser(description="Framex CLI")
    parser.add_argument("command", choices=["get", "list"], help="Command to run")
    parser.add_argument("datasets", nargs="+", help="Dataset name(s), accepts multiple names")
    parser.add_argument("--dir", help="Directory to save the dataset to",default=".", required=False)
    parser.add_argument("--format", help="Format to save the dataset in", default="csv")
    parser.add_argument("overwrite", action="store_false", help="Overwrite the dataset if it already exists")
    if args.command == "get":
        for dataset in args.datasets:
            get(
                name=dataset,
                dir=args.dir,
                format=args.format,
                overwrite=args.overwrite,
            )
    elif args.command == "list":
        available("remote")
    else:
        msg = f"Invalid command: {args.command}"
        raise ValueError(msg)

    return


if __name__ == "__main__":
    main()
