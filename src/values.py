from __future__ import annotations

from collections.abc import Iterable, Generator
from dataclasses import dataclass
from pathlib import Path
from sqlite3 import connect, Connection as SQLiteDatabase
from typing import Optional

from misc import multiline


@dataclass(frozen=True)
class Order:
    order_id: int
    customer_id: int

    @staticmethod
    def from_csv_line(line: str) -> Order:
        [order_id, customer_id] = map(int, line.split(','))
        return Order(order_id, customer_id)


@dataclass(frozen=True)
class Barcode:
    id: str
    order_id: Optional[int]

    @staticmethod
    def from_csv_line(line: str) -> Barcode:
        [barcode, order_id] = line.split(',')
        return Barcode(barcode, int(order_id) if order_id else None)


@dataclass(frozen=True)
class CustomerOrder:
    customer_id: int
    order_id: int
    barcodes: str  # todo: having this as a string might not be ideal later, but works well with SQL query.

    def __str__(self):
        return f"{self.customer_id}, {self.order_id}, [{self.barcodes}]"


@dataclass(frozen=True)
class CustomerStatistics:
    customer_id: int
    amount_of_tickets: int

    def __str__(self):
        return f"{self.customer_id}, {self.amount_of_tickets}"

@dataclass(frozen=True)
class RejectedValue:
    value: Order | Barcode
    reason: str


@dataclass(frozen=True)
class Database:
    db: SQLiteDatabase

    def orders(self) -> Generator[Order, None, None]:
        cursor = self.db.execute("select id, customer_id from orders order by id")
        yield from [Order(id, cid) for (id, cid) in cursor]

    def barcodes(self) -> Generator[Order, None, None]:
        cursor = self.db.execute("select id, order_id from barcodes order by id")
        yield from [Barcode(id, oid) for (id, oid) in cursor]

    def customer_orders(self) -> Generator[CustomerOrder, None, None]:
        cursor = self.db.execute(multiline("""
            select
              orders.customer_id, 
              orders.id as order_id,
              group_concat(barcodes.id, ', ') as barcodes
            from 
              orders
              inner join barcodes on barcodes.order_id = orders.id
            group by 
              orders.customer_id,
              orders.id
            order by
              orders.customer_id asc,
              orders.id asc
            """))

        yield from [CustomerOrder(cid, oid, bbs) for (cid, oid, bbs) in cursor]

    def top_five_customers(self):
        cursor = self.db.execute(multiline("""
            select 
              orders.customer_id, 
              count(distinct barcodes.id) as amount_of_tickets
            from 
              orders 
              inner join barcodes on barcodes.order_id = orders.id
            group by
              orders.customer_id having amount_of_tickets > 0
            order by
              amount_of_tickets desc,
              customer_id asc
            limit 5
        """))

        yield from [CustomerStatistics() for (cid, cnt) in cursor]

    def unsold_barcodes(self):
        pass

    def to_file(self, path: Path, overwriting_existing_file: bool):
        # Connection#backup() did not work right away for some reason,
        # so in case target path existing, we are truncating it with open(w).
        if overwriting_existing_file:
            open(path, 'wb').close()  # todo maybe not the greatest `rm || true` :)

        dst = connect(path)
        with dst:
            dst.executescript("\n".join(self.db.iterdump()))

        dst.close()

    @staticmethod
    def init_db() -> SQLiteDatabase:
        db = connect(':memory:')
        with db:
            db.executescript("""
                create table orders (
                    id int primary key check (id > 0),
                    customer_id int check (customer_id > 0)
                ) strict;
                
                create table barcodes (
                    id text primary key check (length(id) > 0),
                    order_id int references orders(id) 
                ) strict;
                """)

        return db

    @classmethod
    def of(cls, orders: Iterable[Order], barcodes: Iterable[Barcode]) -> tuple[Database, list[RejectedValue]]:
        good_orders: dict[int, Order] = dict()
        good_barcodes: dict[str, Barcode] = dict()
        rejected = list()

        # todo: cleanup
        # This validation is not ok. For example, "no order without barcodes" is possible only
        # after we have seen all the data, so doing duplicate check now does not buy us much.
        # Buffering all of this in memory takes it from "annoying" to "impractical".
        for order in orders:
            if order.order_id in good_orders:
                rejected.append(RejectedValue(order, "Duplicate order"))
            else:
                good_orders[order.order_id] = order

        for barcode in barcodes:
            if barcode.id in good_barcodes:
                rejected.append(RejectedValue(barcode, "Duplicate barcode"))
            else:
                good_barcodes[barcode.id] = barcode

        # todo: batching
        db = cls.init_db()
        with db:
            db.executemany(
                "insert into orders (id, customer_id) values (?, ?)",
                [(order.order_id, order.customer_id) for order in good_orders.values()]
            )
            db.executemany(
                "insert into barcodes (id, order_id) values (?, ?)",
                [(barcode.id, barcode.order_id) for barcode in good_barcodes.values()]
            )

        return Database(db), rejected
