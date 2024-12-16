from typing import Any, TypeVar, Union
from dataclasses_json import DataClassJsonMixin

A = TypeVar("A", bound="DataClassJsonMixin")
Json = Union[dict[Any, Any], list[Any], str, int, float, bool, None]


class DataClassJson(DataClassJsonMixin):
    """Fix the incomplete typing of DataClassJsonMixin."""

    def to_dict(self, encode_json: bool = False) -> dict[str, Json]:
        return super().to_dict(encode_json)  # type: ignore

    @classmethod
    def from_dict(cls: type[A], kvs: dict[Any, Any], *, infer_missing: bool = False) -> A:  # type: ignore
        return super().from_dict(kvs, infer_missing=infer_missing)  # type: ignore
