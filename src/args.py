from __future__ import annotations

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Optional

from misc import resolve_from_cwd, multiline


@dataclass(frozen=True)
class Args:
    """App"s arguments."""
    command: str
    orders: str
    barcodes: str
    debug_output: Optional[str]

    def __post_init__(self):
        if self.orders == self.barcodes:
            raise Exception(f"Got same file for orders and barcodes: {self.orders}")

    @staticmethod
    def parse(command_line: Sequence[str] | None = None) -> Args:
        parser = ArgumentParser(
            prog="TiqetsTakeHome",
            description="Tiqets take-home assignment by Aleksei Zabrodskii",
            formatter_class=ArgumentDefaultsHelpFormatter,
            epilog="""
                Unless specified, `orders` command is chosen and prints `customer id, order id, [barcodes]`.
                Use `top5` to print customer IDs of those with most orders,
                or `unsold` to list barcodes still available to be sold (without order ID attached).
            """,
        )

        parser.add_argument(
            'command',
            type=str,
            nargs='?',
            choices=['orders', 'top5', 'unsold'],
            default='orders',
            # help='Command to executed: customer-orders, '
        )

        parser.add_argument(
            "-o", "--orders",
            type=str,
            default="data/orders.csv",
            help="Location of orders.csv file, relative to CWD"
        )

        parser.add_argument(
            "-b", "--barcodes",
            type=str,
            default="data/barcodes.csv",
            help="Location of barcodes.csv file, relative to CWD"
        )

        parser.add_argument(
            '-d', '--debug-output',
            type=str,
            help='If provided, app will write out in-memory SQLite database from this run to a given file'
        )

        ns = parser.parse_args(command_line)

        return Args(
            command=ns.command,
            orders=resolve_from_cwd(ns.orders),
            barcodes=resolve_from_cwd(ns.barcodes),
            debug_output=resolve_from_cwd(ns.debug_output, False) if ns.debug_output is not None else None,
        )
