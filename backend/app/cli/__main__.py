"""Command-line entry point for Andiny Atlas operations."""

import argparse
import sys
from collections.abc import Sequence

from app.cli.seed import seed_development_users


def build_parser() -> argparse.ArgumentParser:
    """Build the Andiny Atlas operations command parser."""

    parser = argparse.ArgumentParser(
        prog="python -m app.cli",
        description="Andiny Atlas operational commands.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    subparsers.add_parser(
        "seed-users",
        help="Create the standard development user accounts.",
        description=(
            "Create development accounts for the Super Admin, Admin, "
            "Supervisor, and Agent roles."
        ),
    )

    return parser


def main(
    arguments: Sequence[str] | None = None,
) -> int:
    """Execute an Andiny Atlas operational command."""

    parser = build_parser()
    parsed_arguments = parser.parse_args(arguments)

    if parsed_arguments.command == "seed-users":
        return seed_development_users()

    parser.error(
        f"Unsupported command: {parsed_arguments.command}",
    )

    return 2


if __name__ == "__main__":
    sys.exit(main())
