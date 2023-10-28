from typing import Callable, Generator, TextIO

from misc import identity, T


def lines_of(file: TextIO):
    for line in file:
        normalized = line.strip()
        if len(normalized) > 0:
            yield normalized


def read_csv(path: str,
             parse_line: Callable[[str], T] = identity,
             contains_header: bool = True
             ) -> Generator[T, None, None]:
    """Yields non-empty lines of a CSV file."""
    waiting_for_header = contains_header
    with open(path) as file:
        for line in lines_of(file):
            # todo: maybe find a way to not `if` on every line
            if waiting_for_header:
                waiting_for_header = False
                continue

            yield parse_line(line)
