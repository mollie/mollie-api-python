from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Tuple, Union  # pragma: no cover

if TYPE_CHECKING:  # pragma: no cover
    # Note: for some weird reason we can't use dict[str, str] in Python 3.7 in this file,
    # even with the annotations import.
    Amount = Dict[str, str]
    Timeout = Union[None, float, Tuple[float, float], Tuple[float, None]]
