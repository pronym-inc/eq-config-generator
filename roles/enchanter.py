from typing import List

from roles.base import Role
from roles.models.hot_button import HotButton, ArbitraryHotButton, CastSpellHotButton, AssistAndCastHotButton, \
    DoBuffCycleHotButton
from roles.models.social import Social
from roles.models.spell_alias import SpellAlias


class EnchanterRole(Role):
    def get_hotbuttons(self) -> List[HotButton]:
        def xtar_social(n: int) -> Social:
            return Social(f"X Target {n}", f"/xtar {n}")

        return [
            ArbitraryHotButton(6, 1, xtar_social(1)),
            ArbitraryHotButton(6, 2, xtar_social(2)),
            ArbitraryHotButton(6, 3, xtar_social(3)),
            ArbitraryHotButton(6, 4, xtar_social(4)),
            ArbitraryHotButton(6, 5, xtar_social(5)),
            ArbitraryHotButton(6, 6, Social("Assist Main Assist", "/mac bureauassist")),
            CastSpellHotButton(6, 7, SpellAlias("MemoryBlur")),
            CastSpellHotButton(6, 8, SpellAlias("Mesmerize")),
            CastSpellHotButton(6, 9, SpellAlias("Slow")),
            CastSpellHotButton(6, 10, SpellAlias("Tash")),
            CastSpellHotButton(6, 11, SpellAlias("AeStun")),
            AssistAndCastHotButton(5, 1, SpellAlias("Tash")),
            DoBuffCycleHotButton(4, 1, SpellAlias("Clarity")),
            DoBuffCycleHotButton(4, 2, SpellAlias("Haste")),
            AssistAndCastHotButton(5, 3, SpellAlias("ManaDrain")),
            DoBuffCycleHotButton(5, 4, SpellAlias("IntWisBuff"))
        ]
