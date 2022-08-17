from dataclasses import dataclass


@dataclass(frozen=True)
class Skill:
    name: str
    skill_id: int


HIDE_SKILL = Skill("Hide", 29)
SNEAK_SKILL = Skill("Sneak", 42)
FEIGN_DEATH_SKILL = Skill("Feign Death", 25)
MEND_SKILL = Skill("Mend", 32)
TAUNT_SKILL = Skill("Taunt", 73)
