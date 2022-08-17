from typing import List

from roles.base import Role
from roles.models.hot_button import HotButton, CastSpellHotButton, DoBuffCycleHotButton
from roles.models.spell_alias import SpellAlias


class ShamanRole(Role):
    def get_hotbuttons(self) -> List[HotButton]:
        return [
            CastSpellHotButton(3, 5, SpellAlias("Cannibalize")),
            DoBuffCycleHotButton(4, 1, SpellAlias("Talisman")),
            DoBuffCycleHotButton(4, 2, SpellAlias("StaBuff")),
            DoBuffCycleHotButton(4, 3, SpellAlias("StrBuff")),
            DoBuffCycleHotButton(4, 4, SpellAlias("DexBuff"))
        ]
