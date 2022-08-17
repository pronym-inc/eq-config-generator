from abc import ABC
from dataclasses import dataclass

from roles.models.skill import Skill
from roles.models.social import Social
from roles.models.spell_alias import SpellAlias


class HotButton(ABC):
    bank_index: int
    button_index: int


@dataclass(frozen=True)
class SkillHotButton(HotButton):
    bank_index: int
    button_index: int
    skill: Skill


class SocialHotButton(HotButton, ABC):
    social: Social


@dataclass(frozen=True)
class ArbitraryHotButton(SocialHotButton):
    bank_index: int
    button_index: int
    social: Social


class SpellHotButton(SocialHotButton, ABC):
    spell_alias: SpellAlias


@dataclass(frozen=True)
class ArbitrarySpellHotButton(SpellHotButton):
    bank_index: int
    button_index: int
    spell_alias: SpellAlias
    social: Social


@dataclass(frozen=True)
class AssistAndCastHotButton(SpellHotButton):
    bank_index: int
    button_index: int
    spell_alias: SpellAlias

    @property
    def social(self) -> Social:
        return Social(f"{self.spell_alias.alias} Target", f"/mac assistandcast {self.spell_alias.alias}Spell")


@dataclass(frozen=True)
class TargetAndCastHotButton(SpellHotButton):
    target: str
    bank_index: int
    button_index: int
    spell_alias: SpellAlias

    @property
    def social(self) -> Social:
        return Social(
            f"{self.spell_alias.alias} {self.target}",
            f"/mac targetandcast {self.target} {self.spell_alias.alias}Spell"
        )


@dataclass(frozen=True)
class DoBuffCycleHotButton(SpellHotButton):
    bank_index: int
    button_index: int
    spell_alias: SpellAlias

    @property
    def social(self) -> Social:
        return Social(f"{self.spell_alias.alias} Cycle", f"/mac dobuff {self.spell_alias.alias}")


@dataclass(frozen=True)
class CastSpellHotButton(SpellHotButton):
    bank_index: int
    button_index: int
    spell_alias: SpellAlias

    @property
    def social(self) -> Social:
        return Social(f"{self.spell_alias.alias}", f"/mac castspell {self.spell_alias.alias}Spell")
