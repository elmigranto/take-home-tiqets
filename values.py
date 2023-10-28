from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Order:
    order_id: int
    customer_id: int

    @staticmethod
    def from_csv_line(line: str) -> Order:
        # TODO: validation
        [order_id, customer_id] = map(int, line.split(','))
        return Order(order_id, customer_id)


@dataclass(frozen=True)
class Barcode:
    barcode: str
    order_id: Optional[int]

    @staticmethod
    def from_csv_line(line: str) -> Barcode:
        # TODO: validation
        [barcode, order_id] = line.split(',')
        return Barcode(barcode, int(order_id) if order_id else None)
