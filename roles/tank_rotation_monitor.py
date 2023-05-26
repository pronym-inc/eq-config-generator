from typing import Dict

from character import Character
from roles import Role
from roles.models.event import Event


class TankRotationMonitorRole(Role):
    _tank_rotation: list[Character]

    def __init__(self, tank_rotation: list[Character]):
        self._tank_rotation = tank_rotation

    def get_events(self) -> list[Event]:
        return [
            Event(
                "CheckTankRotation",
                "#*# has been slain by #*#",
                "/mac checktankrotation"
            )
        ]

    def get_bureau_config(self) -> Dict[str, str]:
        return {
            "TankRotation": ",".join(list(map(lambda x: x.name, self._tank_rotation)))
        }
