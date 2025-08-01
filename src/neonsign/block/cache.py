from __future__ import annotations

import threading
from typing import Any, Callable, Dict, Hashable, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from neonsign.block.measurable import Measurable


class RenderCache:

    def __init__(self):
        self._cache: Dict[Hashable, Any] = {}

    def get(self, key: Hashable, compute: Callable[[], Any]) -> Any:
        if key in self._cache:
            return self._cache[key]
        value = compute()
        self._cache[key] = value
        return value


_LAYOUT_CONTAINER = threading.local()


class LayoutContainer:

    def __init__(self, root: Measurable):
        self._cache = RenderCache()
        self._root = root

    def __enter__(self) -> LayoutContainer:
        self._previous = getattr(_LAYOUT_CONTAINER, 'instance', None)
        _LAYOUT_CONTAINER.instance = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        _LAYOUT_CONTAINER.instance = self._previous
        return False

    @property
    def cache(self) -> RenderCache:
        return self._cache

    def get_cache_key(
        self,
        block: Measurable,
        width_constraint: Optional[int],
        height_constraint: Optional[int]
    ) -> Hashable:
        return id(block), width_constraint, height_constraint


def current_layout_container() -> Optional[LayoutContainer]:
    return getattr(_LAYOUT_CONTAINER, 'instance', None)
