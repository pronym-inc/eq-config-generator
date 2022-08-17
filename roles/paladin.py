from typing import List

from roles.base import Role
from roles.models.hot_button import HotButton


class PaladinRole(Role):
    def get_hotbuttons(self) -> List[HotButton]:
        return []
