from typing import List

from roles.base import Role
from roles.models.hot_button import HotButton, AssistAndCastHotButton
from roles.models.spell_alias import SpellAlias


class NukerRole(Role):
    def get_hotbuttons(self) -> List[HotButton]:
        return [
            AssistAndCastHotButton(2, 8, SpellAlias("Nuke"))
        ]
