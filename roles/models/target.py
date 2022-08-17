from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import FrozenSet

from character import Character, CHARACTERS
from roles.eq_class import EqClass, MagicianClass


class Target(ABC):
    def get_targets(self) -> FrozenSet[str]:
        ...


class CharacterTarget(Target, ABC):
    def get_targets(self) -> FrozenSet[str]:
        return frozenset(map(lambda x: x.name, self.get_characters(CHARACTERS)))

    def get_characters(
            self,
            character_set: FrozenSet[Character]
    ) -> FrozenSet[Character]:
        return frozenset([
            character
            for character
            in character_set
            if self.should_match_character(character)
        ])

    @abstractmethod
    def should_match_character(self, character: Character) -> bool:
        ...


@dataclass(frozen=True)
class ExplicitTarget(CharacterTarget):
    character: Character

    def should_match_character(self, character: Character) -> bool:
        return character == self.character


class MeleeTarget(CharacterTarget):
    def should_match_character(self, character: Character) -> bool:
        return character.class_.is_melee()


class CasterTarget(CharacterTarget):
    def should_match_character(self, character: Character) -> bool:
        return character.class_.is_caster()


@dataclass(frozen=True)
class ClassTarget(CharacterTarget):
    class_: EqClass

    def should_match_character(self, character: Character) -> bool:
        return character.class_ == self.class_


class AllTarget(CharacterTarget):
    def should_match_character(self, character: Character) -> bool:
        return True


@dataclass(frozen=True)
class PetTarget(Target):
    owner: Character

    def get_targets(self) -> FrozenSet[str]:
        return frozenset([f"Pet:{self.owner.name}"])
