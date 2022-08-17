from typing import List

from roles.base import Role
from roles.models.hot_button import HotButton, ArbitraryHotButton
from roles.models.social import Social


class CasterRole(Role):
    def get_hotbuttons(self) -> List[HotButton]:
        return [ArbitraryHotButton(2, 10, Social("Meditate", "/if (${Me.Standing}) /sit"))]
