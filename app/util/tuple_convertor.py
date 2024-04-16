from typing import Any, Tuple, TypeVar

TupleFirstType = TypeVar("TupleFirstType")


def tuple_first_item(tuple_item: Tuple[TupleFirstType, Any]) -> TupleFirstType:
    return tuple_item[0]
