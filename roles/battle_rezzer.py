from typing import Dict

from character import Character
from roles import Role
from roles.models.event import Event


class BattleRezzerRole(Role):
    _battle_rez_targets: list[Character]

    def __init__(self, battle_rez_targets: list[Character]):
        self._battle_rez_targets = battle_rez_targets

    def get_events(self) -> list[Event]:
        return [
            Event("BattleRez", "#1# has been slain by #*#", "/mac checkbattlerez ${EventArg1}")
        ]

    def get_bureau_config(self) -> Dict[str, str]:
        return {
            'BattleRezTargets': ",".join(list(map(lambda x: x.name,  self._battle_rez_targets)))
        }
