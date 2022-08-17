from typing import List

from roles.base import Role
from roles.models.hot_button import HotButton, AssistAndCastHotButton
from roles.models.spell_alias import SpellAlias


class DispellerRole(Role):
    def get_hotbuttons(self) -> List[HotButton]:
        return [
            AssistAndCastHotButton(3, 4, SpellAlias("Dispel"))
        ]
