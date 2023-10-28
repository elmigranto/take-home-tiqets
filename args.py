from __future__ import annotations

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from dataclasses import dataclass
from typing import Optional

from misc import resolve_from_cwd


@dataclass(frozen=True)
class Args:
    """App"s arguments."""
    orders: str
    barcodes: str
    debug_output: Optional[str]

    def __post_init__(self):
        if self.orders == self.barcodes:
            raise Exception(f"Got same file for orders and barcodes: {self.orders}")

    @staticmethod
    def parse() -> Args:
        parser = ArgumentParser(
            prog="TiqetsTakeHome",
            description="Tiqets take-home assignment by Aleksei Zabrodskii",
            formatter_class=ArgumentDefaultsHelpFormatter
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

        ns = parser.parse_args()

        return Args(
            orders=resolve_from_cwd(ns.orders),
            barcodes=resolve_from_cwd(ns.barcodes),
            debug_output=resolve_from_cwd(ns.debug_output, False) if ns.debug_output is not None else None,
        )
