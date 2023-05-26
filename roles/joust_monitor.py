from dataclasses import dataclass
from typing import Tuple

from roles import Role
from roles.models.event import Event


@dataclass(frozen=True)
class JoustTrigger:
    name: str
    resist_text: str
    landed_text: str


@dataclass(frozen=True)
class JoustMonitorRole(Role):
    _triggers: frozenset[JoustTrigger]
    _boss_name: str
    _joust_safe_xy_coordinates: Tuple[int, int]

    def get_events(self) -> list[Event]:
        output: list[Event] = []
        for idx, trigger in enumerate(self._triggers):
            joust_command = f"/mac monitorjoust {trigger.name} \"{self._boss_name}\" {self._joust_safe_xy_coordinates[0]} {self._joust_safe_xy_coordinates[1]}"
            output.extend([
                Event(f"JoustLand{idx}", trigger.landed_text, joust_command),
                Event(f"JoustResist{idx}", f"#*#You resist the {trigger.resist_text} spell#*#", joust_command),
            ])
        return output
