from dataclasses import dataclass
from typing import Optional

from roles.models.spell import Spell
from roles.models.spellbook import Spellbook


def camel2snake(inp: str) -> str:
    output = f"{inp[0].lower()}"
    for character in inp[1:]:
        if character.capitalize() == character:
            output += f"_{character.lower()}"
        else:
            output += character
    return output


@dataclass(frozen=True)
class SpellAlias:
    alias: str

    def get_from_spellbook(self, spellbook: Spellbook) -> Optional[Spell]:
        attr_name = camel2snake(self.alias)
        if hasattr(spellbook, attr_name):
            return getattr(spellbook, attr_name)
        return None


SNARE_SPELL = SpellAlias("Snare")
HP_AC_BUFF_SPELL = SpellAlias("HpAc")
SYMBOL_SPELL = SpellAlias("Symbol")
AC_BUFF_SPELL = SpellAlias("Ac")
DOT_SPELL = SpellAlias("Dot")
SLOW_SPELL = SpellAlias("Slow")
CANNIBALIZE_SPELL = SpellAlias("Cannibalize")
TALISMAN_SPELL = SpellAlias("Talisman")
STA_BUFF_SPELL = SpellAlias("StaBuff")
DISPEL_SPELL = SpellAlias("Dispel")
