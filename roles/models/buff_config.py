from dataclasses import dataclass
from typing import FrozenSet

from character import Character
from roles.models.target import Target


@dataclass(frozen=True)
class BuffConfig:
    caster: Character
    targets: FrozenSet[Target]
    is_group_spell: bool = False
    enabled: bool = True
