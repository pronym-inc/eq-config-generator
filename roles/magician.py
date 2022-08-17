from typing import List

from roles.base import Role
from roles.models.hot_button import HotButton, AssistAndCastHotButton, DoBuffCycleHotButton
from roles.models.spell_alias import SpellAlias


class MagicianRole(Role):
    def get_hotbuttons(self) -> List[HotButton]:
        return [
            AssistAndCastHotButton(3, 1, SpellAlias("Mala")),
            DoBuffCycleHotButton(3, 2, SpellAlias("Burnout"))
        ]
