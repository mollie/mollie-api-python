import sys
from typing import TYPE_CHECKING, Dict, Tuple, Union  # pragma: no cover

if TYPE_CHECKING:  # pragma: no cover
    # Note: for some weird reason we can't use dict[str, str] in Python 3.7 in this file,
    # even with the annotations import.
    Amount = Dict[str, str]
    Timeout = Union[None, float, Tuple[float, float], Tuple[float, None]]

    # Final is available from different places, depending on the Python version
    if sys.version_info < (3, 8):
        from typing_extensions import Final  # noqa: F401
    else:
        from typing import Final  # noqa: F401
