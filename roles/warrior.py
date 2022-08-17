from typing import List

from roles.base import Role
from roles.models.hot_button import HotButton, ArbitraryHotButton
from roles.models.social import Social


class WarriorRole(Role):
    def get_hotbuttons(self) -> List[HotButton]:
        return [
            ArbitraryHotButton(1, 7, Social("CH Me", "/mac healme complete"))
        ]
