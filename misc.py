from os import getcwd
from pathlib import Path
from pprint import pprint
from sys import stderr
from typing import TypeVar


T = TypeVar('T')


def pp(value: T, destination: type(stderr) = stderr) -> T:
    """Pretty-prints a value to a destination and returns it."""
    pprint(value, stream=destination)
    return value


def resolve_from_cwd(path: str):
    path = Path(path)
    return str(path if path.is_absolute() else Path(getcwd()).joinpath(path).resolve(True))


def identity(value: T) -> T:
    return value
