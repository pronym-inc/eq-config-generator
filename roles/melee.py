from typing import List

from roles.base import Role
from roles.models.hot_button import HotButton, ArbitraryHotButton
from roles.models.social import Social


class MeleeRole(Role):
    def get_hotbuttons(self) -> List[HotButton]:
        return [
            ArbitraryHotButton(1, 6, Social("Mark Assist", "/mac setasmainassist ${Me.Name}"))
        ]
