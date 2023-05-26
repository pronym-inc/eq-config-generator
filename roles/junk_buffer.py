from roles import Role
from roles.models.event import Event


class JunkBufferRole(Role):
    _buff_name: str
    _target: str

    def __init__(self, buff_name, target):
        self._buff_name = buff_name
        self._target = target

    def get_events(self) -> list[Event]:
        return []
