from os import getcwd
from pathlib import Path
from pprint import pformat
from sys import stderr
from typing import TypeVar

T = TypeVar('T')


def pp(value: T, destination: type(stderr) = stderr) -> T:
    """Pretty-prints a value to a destination and returns it."""
    print(pf(value), file=destination)
    return value


def pf(value: object) -> str:
    """Formats a value into a string using pformat() with defaults"""
    return pformat(value)


def print_error(*values: object):
    print(*values, file=stderr)


def resolve_from_cwd(path: str, throw_if_missing: bool = True):
    path = Path(path)
    resolved = path if path.is_absolute() else Path(getcwd()).joinpath(path).resolve(throw_if_missing)

    if path.is_dir():
        raise Exception(f"Directory input: {path}")

    if throw_if_missing and not path.exists():
        raise Exception(f"File not found: {path}")

    return str(resolved)


def identity(value: T) -> T:
    return value
