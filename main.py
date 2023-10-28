from args import Args
from inout import read_csv
from misc import pp
from values import Barcode, Order


def main(args: Args):
    for order in read_csv(args.orders, Order.from_csv_line):
        pp(order)

    for barcode in read_csv(args.barcodes, Barcode.from_csv_line):
        pp(barcode)


if __name__ == "__main__":
    main(Args.parse())
