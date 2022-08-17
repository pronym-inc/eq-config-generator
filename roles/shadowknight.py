from typing import List

from roles.base import Role
from roles.models.hot_button import HotButton


class ShadowknightRole(Role):
    def get_hotbuttons(self) -> List[HotButton]:
        return []
