from typing import List

from roles import Role
from roles.models import HotButton
from roles.models.hot_button import DoBuffCycleHotButton
from roles.models.spell_alias import SpellAlias


class DruidRole(Role):
    def get_hotbuttons(self) -> List[HotButton]:
        return [
            DoBuffCycleHotButton(4, 1, SpellAlias("Regen")),
            DoBuffCycleHotButton(4, 2, SpellAlias("Sow")),
            DoBuffCycleHotButton(4, 3, SpellAlias("StrBuff"))
        ]
