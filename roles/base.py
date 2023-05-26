from abc import ABC
from typing import List, FrozenSet, Dict

from roles.models.event import Event
from roles.models.hot_button import HotButton, SpellHotButton, SocialHotButton
from roles.models.social import Social
from roles.models.spell_alias import SpellAlias


class Role(ABC):
    def get_hotbuttons(self) -> List[HotButton]:
        ...

    def get_socials(self) -> List[Social]:
        return [
            hot_button.social
            for hot_button
            in self.get_hotbuttons()
            if isinstance(hot_button, SocialHotButton)
        ]

    def get_spell_aliases(self) -> FrozenSet[SpellAlias]:
        return frozenset([
            hot_button.spell_alias
            for hot_button
            in self.get_hotbuttons()
            if isinstance(hot_button, SpellHotButton)
        ] + list(self.get_extra_spell_aliases()))

    def get_extra_spell_aliases(self) -> FrozenSet[SpellAlias]:
        return frozenset([])

    def get_events(self) -> list[Event]:
        return []

    def get_bureau_config(self) -> Dict[str, str]:
        return {}
