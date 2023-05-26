from typing import List

from roles import Role
from roles.models import HotButton, Social
from roles.models.hot_button import ArbitraryHotButton


class RaidLeaderRole(Role):
    def get_hotbuttons(self) -> List[HotButton]:
        return [
            ArbitraryHotButton(
                5, 1, Social("Start Battle", "/mac startbattle")
            ),
            ArbitraryHotButton(
                5, 2, Social("End Battle", "/mac endbattle")
            )
        ]