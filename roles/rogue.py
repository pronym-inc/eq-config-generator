from typing import List

from roles.base import Role
from roles.models.hot_button import HotButton, SkillHotButton
from roles.models.skill import HIDE_SKILL, SNEAK_SKILL


class RogueRole(Role):
    def get_hotbuttons(self) -> List[HotButton]:
        return [
            SkillHotButton(1, 9, HIDE_SKILL),
            SkillHotButton(1, 10, SNEAK_SKILL)
        ]
