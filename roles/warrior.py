from typing import List

from roles.base import Role
from roles.models.hot_button import HotButton, ArbitraryHotButton
from roles.models.social import Social


def set_heal_threshold_social(amount: int) -> Social:
    return Social(f"Heal {amount}", f"/mac sethealthreshold {amount}")


class WarriorRole(Role):

    def get_hotbuttons(self) -> List[HotButton]:
        return [
            ArbitraryHotButton(1, 7, Social("CH Me", "/mac healme complete")),
            ArbitraryHotButton(6, 1, set_heal_threshold_social(40)),
            ArbitraryHotButton(6, 2, set_heal_threshold_social(50)),
            ArbitraryHotButton(6, 3, set_heal_threshold_social(60)),
            ArbitraryHotButton(6, 4, set_heal_threshold_social(70)),
            ArbitraryHotButton(6, 5, set_heal_threshold_social(80)),
            ArbitraryHotButton(6, 6, set_heal_threshold_social(90)),
            ArbitraryHotButton(5, 1, Social("Offtank CC Target", "/mac offtank"))
        ]

    def get_eqbc_channels(self) -> list[str]:
        return ['warrior']
