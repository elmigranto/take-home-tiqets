from args import Args
from inout import parse_csv_file
from misc import pf, print_error, resolve_from_cwd
from values import Barcode, Database, Order


def main(args: Args):
    db, rejections = Database.of(
        orders=parse_csv_file(args.orders, Order.from_csv_line),
        barcodes=parse_csv_file(args.barcodes, Barcode.from_csv_line),
    )

    for r in rejections:
        print_error(f"[Rejected] {r.reason}: {pf(r.value)}")

    get_iter = {
        'orders': db.customer_orders,
        'top5': db.top_five_customers,
        'unsold': db.unsold_barcodes,
    }[args.command]

    for item in get_iter():
        print(item)

    if args.debug_output is not None:
        db.to_file(
            resolve_from_cwd(args.debug_output, False),
            True)

    db.db.close()


if __name__ == "__main__":
    main(Args.parse())
