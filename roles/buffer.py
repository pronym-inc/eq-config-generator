from typing import List

from roles.base import Role
from roles.models.hot_button import HotButton, ArbitraryHotButton
from roles.models.social import Social


class BufferRole(Role):
    def get_hotbuttons(self) -> List[HotButton]:
        return [ArbitraryHotButton(2, 11, Social("Do All Buffs", "/mac prep"))]
