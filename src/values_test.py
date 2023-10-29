from unittest import main, TestCase

from src.inout import parse_csv_string
from src.misc import multiline
from src.values import Barcode, Database, RejectedValue, Order, CustomerOrder


class DatabaseCustomerOrders(TestCase):
    def test_it_works(self):
        db = self.make_db(
            multiline("""
            1,1
            2,2
            3,3
            """),
            multiline("""
            bar1,1
            bar2,1
            bar3,2
            bar4,3
            """)
        )

        self.assertEqual(list(db.customer_orders()), [
            CustomerOrder(1, 1, "bar1, bar2"),
            CustomerOrder(2, 2, "bar3"),
            CustomerOrder(3, 3, "bar4"),
        ])

    def make_db(self, csv_orders: str, csv_barcodes: str) -> Database:
        db, rejected = Database.of(
            orders=parse_csv_string(csv_orders, Order.from_csv_line, False),
            barcodes=parse_csv_string(csv_barcodes, Barcode.from_csv_line, False),
        )

        self.assertEqual(len(rejected), 0)
        return db


class DatabaseOf(TestCase):
    def test_it_rejects_duplicate_barcodes(self):
        csv = multiline("""
            B1,1
            B2,1
            B1,
            B3,
            B5,
            B3,1
        """)

        db, rejected = Database.of(
            barcodes=[Barcode.from_csv_line(line) for line in csv.splitlines()],
            orders=[]
        )

        self.assertEqual(rejected, [
            RejectedValue(Barcode('B1', None), 'Duplicate barcode'),
            RejectedValue(Barcode('B3', 1), 'Duplicate barcode'),
        ])

    def test_it_rejects_duplicate_orders(self):
        csv = multiline("""
            1,1
            2,2
            2,1
        """)

        db, rejected = Database.of(
            barcodes=[],
            orders=[Order.from_csv_line(line) for line in csv.splitlines()]
        )

        self.assertEqual(rejected, [
            RejectedValue(Order(2, 1), 'Duplicate order'),
        ])


if __name__ == '__main__':
    main()
