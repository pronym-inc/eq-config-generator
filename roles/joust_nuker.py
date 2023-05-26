from roles import Role
from roles.models.event import Event


class JoustNukerRole(Role):
    def get_events(self) -> list[Event]:
        return [
            Event(
                "Joust",
                "#*#Bureau Joust Attack #1# now#*#",
                "/mac joustnuke \"${EventArg1}\""
            )
        ]