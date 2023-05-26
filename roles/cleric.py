from typing import List, FrozenSet

from roles import Role
from roles.models import Social, HotButton
from roles.models.hot_button import DoBuffCycleHotButton, ArbitrarySpellHotButton
from roles.models.spell_alias import SpellAlias


class ClericRole(Role):
    def get_hotbuttons(self) -> List[HotButton]:
        return [
            DoBuffCycleHotButton(4, 1, SpellAlias("HpAc")),
            DoBuffCycleHotButton(4, 2, SpellAlias("Symbol")),
            DoBuffCycleHotButton(4, 3, SpellAlias("Ac")),
            ArbitrarySpellHotButton(
                5,
                2,
                SpellAlias("CompleteHeal"),
                Social("CH Main Assist", "/mac tryheal ${BureauMainAssist} complete")
            )
        ]

    def get_extra_spell_aliases(self) -> FrozenSet[SpellAlias]:
        return frozenset([
            SpellAlias("Rez"),
            SpellAlias("BigHeal"),
            SpellAlias("ResistDisease")
        ])

    def get_eqbc_channels(self) -> list[str]:
        return ['cleric']
