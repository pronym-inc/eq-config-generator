from typing import List

from roles.base import Role
from roles.models.hot_button import HotButton, ArbitraryHotButton
from roles.models.social import Social


class CommonRole(Role):
    INIT_SOCIAL = Social("Init", "/mac init")
    FOLLOW_ME_SOCIAL = Social("Follow Me", "/mac smartfollowme")
    STOP_FOLLOWING_SOCIAL = Social("Stop Following", "/mac stopsmartfollowme")
    HEAL_ME_SOCIAL = Social("Heal Me", "/mac healme")
    COME_TO_ME_SOCIAL = Social("Come to Me", "/mac smartcometome")
    ASSIST_SOCIAL = Social("Assist", "/mac bureauassist")
    CHECK_FOR_HEALS_SOCIAL = Social("Check for Heals", "/mac checkheal")
    STATUS_CHECK_SOCIAL = Social("Status", "/bcaa //mac statuscheck")
    DISABLE_AUTOHEAL = Social("Disable Autoheal", "/varset AutoHealEnabled FALSE")
    ENABLE_AUTOHEAL = Social("Enable Autoheal", "/varset AutoHealEnabled TRUE")

    def get_hotbuttons(self) -> List[HotButton]:
        return [
            ArbitraryHotButton(1, 1, self.COME_TO_ME_SOCIAL),
            ArbitraryHotButton(1, 2, self.FOLLOW_ME_SOCIAL),
            ArbitraryHotButton(1, 3, self.STOP_FOLLOWING_SOCIAL),
            ArbitraryHotButton(1, 4, self.HEAL_ME_SOCIAL),
            ArbitraryHotButton(1, 5, self.ASSIST_SOCIAL),
            ArbitraryHotButton(1, 8, self.CHECK_FOR_HEALS_SOCIAL),
            ArbitraryHotButton(1, 12, self.INIT_SOCIAL),
            ArbitraryHotButton(4, 10, self.STATUS_CHECK_SOCIAL),
            ArbitraryHotButton(4, 8, self.ENABLE_AUTOHEAL),
            ArbitraryHotButton(4, 9, self.DISABLE_AUTOHEAL)
        ]
