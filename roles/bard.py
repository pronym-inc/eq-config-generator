from typing import List, FrozenSet

from roles.base import Role
from roles.models import Social
from roles.models.hot_button import HotButton, ArbitraryHotButton
from roles.models.spell_alias import SpellAlias


class BardRole(Role):
    def get_hotbuttons(self) -> List[HotButton]:
        return [
            ArbitraryHotButton(
                5,
                1,
                Social(
                    "Regen Twist",
                    "/twist ${Me.Gem[${HpManaRegenSpell}]} ${Me.Gem[${ManaRegenSpell}]}"
                )
            ),
            ArbitraryHotButton(
                5,
                2,
                Social(
                    "Resist Twist",
                    "/twist ${Me.Gem[${Resist3Spell}]}"
                )
            ),
            ArbitraryHotButton(
                5,
                3,
                Social(
                    "Stop Songs",
                    "/twist off"
                )
            )
        ]

    def get_extra_spell_aliases(self) -> FrozenSet[SpellAlias]:
        return frozenset([
            SpellAlias("MovementSpeed"),
            SpellAlias("Levitation"),
            SpellAlias("Resist1"),
            SpellAlias("Resist2"),
            SpellAlias("Resist3"),
            SpellAlias("HpManaRegen"),
            SpellAlias("ManaRegen"),
            SpellAlias("IntWis")
        ])

    def get_eqbc_channels(self) -> list[str]:
        return ["bard"]
