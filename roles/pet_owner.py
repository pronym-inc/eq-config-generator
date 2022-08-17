from typing import List, FrozenSet

from roles.base import Role
from roles.models.hot_button import HotButton, ArbitraryHotButton
from roles.models.social import Social
from roles.models.spell_alias import SpellAlias


class PetOwnerRole(Role):
    def get_hotbuttons(self) -> List[HotButton]:
        return [
            ArbitraryHotButton(4, 11, Social("Pet Attack Target", "/mac petassist"))
        ]

    def get_extra_spell_aliases(self) -> FrozenSet[SpellAlias]:
        return frozenset([
            SpellAlias("Pet")
        ])
