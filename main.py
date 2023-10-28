#!/usr/bin/env python3
from args import Args
from inout import read_csv
from misc import pp, pf, print_error, resolve_from_cwd
from values import Barcode, Database, Order


def main(args: Args):
    db, rejected = Database.of(
        orders=read_csv(args.orders, Order.from_csv_line),
        barcodes=read_csv(args.barcodes, Barcode.from_csv_line),
    )

    for malformed in rejected:
        print_error(f"[Rejected]: {pf(malformed)}")

    for order in db.orders():
        pp(order)

    for barcode in db.barcodes():
        pp(barcode)

    if args.debug_output is not None:
        db.to_file(
            resolve_from_cwd(args.debug_output, False),
            True)

    db.db.close()


if __name__ == "__main__":
    main(Args.parse())
