from dataclasses import dataclass
from typing import Optional, List


@dataclass(frozen=True)
class Social:
    name: str
    line1: str
    line2: Optional[str] = None
    line3: Optional[str] = None
    line4: Optional[str] = None
    line5: Optional[str] = None
    color: int = 0

    def lines(self) -> List[str]:
        all_lines = [self.line1, self.line2, self.line3, self.line4, self.line5]
        return [
            line
            for line
            in all_lines
            if line is not None
        ]
