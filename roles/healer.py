from typing import List

from roles.base import Role
from roles.models.hot_button import HotButton, ArbitrarySpellHotButton
from roles.models.social import Social
from roles.models.spell_alias import SpellAlias


class HealerRole(Role):
    def get_hotbuttons(self) -> List[HotButton]:
        return [
            ArbitrarySpellHotButton(
                5,
                1,
                SpellAlias("SmallHeal"),
                Social("Heal MA", "/mac tryheal ${BureauMainAssist}")
            ),
            ArbitrarySpellHotButton(
                5,
                10,
                SpellAlias("Heal"),
                Social("Top Up", "/mac topup")
            )
        ]
