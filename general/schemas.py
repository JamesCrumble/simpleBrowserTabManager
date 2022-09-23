from dataclasses import dataclass

from .types_ import BROWSER_TAB_UUID


@dataclass(init=True)
class Tab:

    index: int
    uuid: BROWSER_TAB_UUID
