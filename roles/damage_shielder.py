from typing import List

from roles import Role
from roles.models import HotButton
from roles.models.hot_button import DoBuffCycleHotButton
from roles.models.spell_alias import SpellAlias


class DamageShielderRole(Role):
    def get_hotbuttons(self) -> List[HotButton]:
        return [
            DoBuffCycleHotButton(3, 10, SpellAlias("DamageShield"))
        ]
