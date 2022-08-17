from dataclasses import dataclass
from typing import FrozenSet, List, Tuple, Dict

from character import Character
from roles.models.buff_config import BuffConfig


@dataclass(frozen=True)
class Group:
    leader: Character
    followers: FrozenSet[Character]

    @property
    def members(self) -> List[Character]:
        return [self.leader] + list(self.followers)

    def validate(self) -> None:
        if len(self.followers) > 5:
            raise Exception("Too many members in group.")
        if self.leader in self.followers:
            raise Exception("Leader can't also be a follower.")


@dataclass(frozen=True)
class PartyConfiguration:
    groups: FrozenSet[Group]
    healers: List[Tuple[Character, List[Character]]]
    buff_config: FrozenSet[Tuple[str, BuffConfig]]

    def get_healers_by_character(self) -> Dict[Character, List[Character]]:
        return {
            character: healers
            for character, healers
            in self.healers
        }

    def validate(self) -> None:
        for group in self.groups:
            group.validate()
        healer_by_character = self.get_healers_by_character()

        for character in self.all_characters:
            if character not in healer_by_character:
                raise Exception(f"{character.name} has no healer assigned.")

    @property
    def all_characters(self) -> FrozenSet[Character]:
        output: FrozenSet[Character] = frozenset([])
        for group in self.groups:
            output = output.union(group.members)
        return output
