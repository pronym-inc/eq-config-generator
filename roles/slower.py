from typing import List

from roles.base import Role
from roles.models.hot_button import HotButton, ArbitraryHotButton, AssistAndCastHotButton
from roles.models.social import Social
from roles.models.spell_alias import SpellAlias


class SlowerRole(Role):
    def get_hotbuttons(self) -> List[HotButton]:
        return [
            AssistAndCastHotButton(3, 1, SpellAlias("Slow")),
            ArbitraryHotButton(3, 2, Social("Slow CC Target", "/mac assistandcast SlowSpell ${CCAssist}"))
        ]
