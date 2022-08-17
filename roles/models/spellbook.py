from abc import ABC
from dataclasses import dataclass
from typing import List

from roles.models.spell import Spell


class Spellbook(ABC):
    def get_sorted_spells(self) -> List[Spell]:
        return sorted(
            self.get_spells(),
            key=lambda x: x.name
        )

    def get_spells(self) -> List[Spell]:
        return [
            attribute_value
            for attribute_value
            in self.__dict__.values()
            if isinstance(attribute_value, Spell)
        ]

    def validate(self) -> None:
        if len(self.get_spells()) > 8:
            raise Exception("Too many spells in spellbook.")


@dataclass(frozen=True)
class NullSpellbook(Spellbook):
    ...


@dataclass(frozen=True)
class BardSpellbook(Spellbook):
    movement_speed: Spell
    levitation: Spell
    resist_1: Spell
    resist_2: Spell
    resist_3: Spell
    hp_mana_regen: Spell
    mana_regen: Spell
    int_wis: Spell


@dataclass(frozen=True)
class ClericSpellbook(Spellbook):
    hp_ac: Spell
    symbol: Spell
    ac: Spell
    small_heal: Spell
    big_heal: Spell
    complete_heal: Spell
    rez: Spell


@dataclass(frozen=True)
class DruidSpellbook(Spellbook):
    snare: Spell
    nuke: Spell
    dot: Spell
    heal: Spell
    sow: Spell
    dispel: Spell
    regen: Spell


@dataclass(frozen=True)
class EnchanterSpellbook(Spellbook):
    memory_blur: Spell
    mesmerize: Spell
    tash: Spell
    clarity: Spell
    haste: Spell
    mana_drain: Spell
    ae_stun: Spell
    dispel: Spell


@dataclass(frozen=True)
class MagicianSpellbook(Spellbook):
    mala: Spell
    nuke: Spell
    pet: Spell
    burnout: Spell
    damage_shield: Spell


@dataclass(frozen=True)
class NecromancerSpellbook(Spellbook):
    dot: Spell
    nuke: Spell
    summon_pet: Spell


@dataclass(frozen=True)
class PaladinSpellbook(Spellbook):
    ...


@dataclass(frozen=True)
class RangerSpellbook(Spellbook):
    snare: Spell


@dataclass(frozen=True)
class ShadowknightSpellbook(Spellbook):
    snare: Spell


@dataclass(frozen=True)
class ShamanSpellbook(Spellbook):
    dispel: Spell
    talisman: Spell
    sta_buff: Spell
    str_buff: Spell
    dex_buff: Spell
    slow: Spell
    heal: Spell
    dot: Spell


@dataclass(frozen=True)
class WizardSpellbook(Spellbook):
    nuke: Spell
    dispel: Spell
