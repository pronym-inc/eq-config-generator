from typing import Callable, Any


def flatten(x: list[list]) -> list:
    output: list = []
    for item in x:
        output.extend(item)
    return output


def flatmap(fn: Callable[[Any], list], x: list) -> list:
    return flatten(list(map(fn, x)))
