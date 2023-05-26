from typing import Dict

from roles import Role
from roles.models.event import Event


class JousterRole(Role):
    def get_events(self) -> list[Event]:
        return [
            Event(
                "Joust",
                "#*#Bureau Joust Attack #1# now#*#",
                "/mac joust \"${EventArg1}\""
            ),
            Event(
                "Retreat",
                "#*#Bureau Joust Retreat #1# #2# now#*#",
                "/mac joustretreat ${EventArg1} ${EventArg2}"
            )
        ]
