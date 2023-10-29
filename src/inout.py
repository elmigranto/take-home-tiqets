from collections.abc import Callable, Generator, Iterable
from itertools import islice, filterfalse

from src.misc import identity, T


def csv_nonvalue(s: str) -> bool:
    """
    Returns `True` for non-value CSV rows, namely:
      - empty lines;
      - whitespace-only lines;
      - lines starting with `#`.
    """
    return not s or s.isspace() or s.startswith('#')


def normalized_lines(raw_lines: Iterable[str]) -> Generator[str, None, None]:
    """ Yields value-only lines from iterable of CSV rows. """
    yield from filterfalse(csv_nonvalue, raw_lines)


def parse_csv_lines(lines: Iterable[str],
                    parse_line: Callable[[str], T] = identity,
                    contains_header: bool = True,
                    ) -> Generator[T, None, None]:
    """
    Yields values parsed from CSV rows with `parse_line()`.

    Unless `contains_header` is `False`, first row is skipped.
    Only non-empty, non-comment lines are considered (see `csv_nonvalue()`).
    """
    seq = normalized_lines(lines)
    headerless_seq = islice(seq, 1, None) if contains_header else seq
    yield from map(parse_line, headerless_seq)


def parse_csv_string(csv: str,
                    parse_line: Callable[[str], T] = identity,
                    contains_header: bool = False
                    ) -> Generator[T, None, None]:
    """Parses a string with CSV file using `parse_csv_lines()`."""
    return parse_csv_lines(csv.splitlines(), parse_line, contains_header)


def parse_csv_file(path: str,
                   parse_line: Callable[[str], T] = identity,
                   contains_header: bool = True
                   ) -> Generator[T, None, None]:
    """Parses text file's lines using `parse_csv_lines()`."""
    with open(path) as file:
        yield from parse_csv_lines(file, parse_line, contains_header)
