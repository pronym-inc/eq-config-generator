from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import FrozenSet, List, Tuple, Dict

from character import Character, CHARACTERS
from roles import Role
from roles.models.buff_config import BuffConfig
from roles.models.target import Target, CharacterTarget


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


class HealingStrategy(Enum):
    NORMAL = auto()
    ROUND_ROBIN = auto()


@dataclass(frozen=True)
class CharacterHealingConfiguration:
    healers: FrozenSet[Character]
    strategy: HealingStrategy


@dataclass(frozen=True)
class HealingConfiguration:
    character_configs: FrozenSet[Tuple[Character, CharacterHealingConfiguration]]
    main_tank_healers: FrozenSet[Character]
    offtank_healers: FrozenSet[Character]
    topup_healers: FrozenSet[Character]


@dataclass(frozen=True)
class PartyConfiguration:
    groups: FrozenSet[Group]
    healing_config: HealingConfiguration
    buff_config: FrozenSet[Tuple[str, BuffConfig]]
    extra_roles: FrozenSet[Tuple[Character, Role]] = frozenset([])

    def get_final_characters(self) -> list[Character]:
        extra_roles_dict = {}
        for character_or_target, role in self.extra_roles:
            if isinstance(character_or_target, Character):
                character: Character = character_or_target
                extra_roles_dict.setdefault(character, [])
                extra_roles_dict[character].append(role)
            elif isinstance(character_or_target, CharacterTarget):
                target: CharacterTarget = character_or_target
                for character in target.get_characters():
                    extra_roles_dict.setdefault(character, [])
                    extra_roles_dict[character].append(role)
            elif isinstance(character_or_target, frozenset):
                target: CharacterTarget
                running_set = CHARACTERS
                for target in character_or_target:
                    running_set = target.get_characters(running_set)
                print(running_set)
                for character in running_set:
                    extra_roles_dict.setdefault(character, [])
                    extra_roles_dict[character].append(role)
                    print(character, role)

        output = []

        for character in CHARACTERS:
            final_character = character
            for role in extra_roles_dict.get(character, []):
                final_character = final_character.with_extra_role(role)
            output.append(final_character)

        return output

    def get_healers_by_character(self) -> Dict[Character, List[Character]]:
        return {
            character: healing_config.healers
            for character, healing_config
            in self.healing_config.character_configs
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

    def get_strategy_for_character(self, character: Character) -> HealingStrategy:
        return [
            config.strategy
            for character_, config
            in self.healing_config.character_configs
            if character_ == character
        ][0]
