import importlib
from typing import Any, Type


def get_class_from_dotted_path(dotted_path: str) -> Type[Any]:
    module_path, class_name = dotted_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    class_ = getattr(module, class_name)
    return class_
