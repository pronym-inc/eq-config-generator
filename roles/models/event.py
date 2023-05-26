from dataclasses import dataclass


@dataclass(frozen=True)
class Event:
    name: str
    trigger: str
    command: str
