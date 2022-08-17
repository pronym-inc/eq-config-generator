from typing import List

from roles.base import Role
from roles.models.hot_button import HotButton, SkillHotButton
from roles.models.skill import FEIGN_DEATH_SKILL, MEND_SKILL


class MonkRole(Role):
    def get_hotbuttons(self) -> List[HotButton]:
        return [
            SkillHotButton(1, 9, FEIGN_DEATH_SKILL),
            SkillHotButton(1, 10, MEND_SKILL)
        ]
