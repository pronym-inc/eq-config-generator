from dataclasses import dataclass
from functools import reduce
from typing import FrozenSet, List, Tuple, Dict

from roles import MeleeRole, BardRole, SnarerRole, HealerRole, PetOwnerRole, MagicianRole, DoterRole, \
    NukerRole, DispellerRole, SlowerRole, EnchanterRole, ShamanRole, CasterRole, Role, CommonRole, ClericRole, \
    DruidRole, MonkRole, RogueRole, PaladinRole, RangerRole, ShadowknightRole, WizardRole, \
    NecromancerRole, WarriorRole, DamageShielderRole, BufferRole
from roles.models import HotButton, Social
from roles.models.event import Event
from roles.models.spell_alias import SpellAlias


@dataclass(frozen=True)
class EqClass:
    name: str
    roles: FrozenSet[Role]
    required_spells: FrozenSet[str] = frozenset([])

    def _get_all_roles(self) -> FrozenSet[Role]:
        return self.roles.union(frozenset([CommonRole()]))

    def get_hot_buttons(self) -> List[HotButton]:
        output: List[HotButton] = []

        for role in self._get_all_roles():
            output.extend(role.get_hotbuttons())

        return output

    def get_socials(self) -> List[Social]:
        output: List[Social] = []

        for role in self._get_all_roles():
            output.extend(role.get_socials())

        return output

    def get_spell_aliases(self) -> List[SpellAlias]:
        output: List[SpellAlias] = []

        for role in self._get_all_roles():
            output.extend(role.get_spell_aliases())

        return list(set(output))

    def is_caster(self) -> bool:
        return len([role for role in self.roles if isinstance(role, CasterRole)]) > 0

    def is_melee(self) -> bool:
        return len([role for role in self.roles if isinstance(role, MeleeRole)]) > 0

    def is_warrior(self) -> bool:
        return len([role for role in self.roles if isinstance(role, WarriorRole)]) > 0

    def validate(self) -> None:
        found_hotbutton_config: Dict[Tuple[int, int], HotButton] = {}

        for hotbutton in self.get_hot_buttons():
            if (hotbutton.bank_index, hotbutton.button_index) in found_hotbutton_config:
                raise Exception(
                    f"Hot button conflict in {self}.  {hotbutton.bank_index}, {hotbutton.button_index}"
                    f"{found_hotbutton_config[(hotbutton.bank_index, hotbutton.button_index)]} and {hotbutton}"
                )
            else:
                found_hotbutton_config[(hotbutton.bank_index, hotbutton.button_index)] = hotbutton

    def get_events(self) -> list[Event]:
        def combine_lists(x: list, y: list) -> list:
            output = []
            output.extend(x)
            output.extend(y)
            return output

        return reduce(
            combine_lists,
            [role.get_events() for role in self._get_all_roles()],
            []
        )


WarriorClass = EqClass(
    "Warrior",
    frozenset([MeleeRole(), WarriorRole()])
)
MonkClass = EqClass("Monk", frozenset([MeleeRole(), MonkRole()]))
RogueClass = EqClass("Rogue", frozenset([MeleeRole(), RogueRole()]))
PaladinClass = EqClass(
    "Paladin", frozenset([MeleeRole(), PaladinRole(), BufferRole()]),
    required_spells=frozenset([
        "Resist Disease",
        "Renewal",
        "Greater Healing",
        "Counteract Poison",
        "Holy Might"
    ])
)
BardClass = EqClass(
    "Bard",
    frozenset([MeleeRole(), BardRole()]),
    required_spells=frozenset([
        "Verses of Victory",
        "Niv's Melody of Preservation",
        "Cassindra's Elegy",
        "McVaxius' Berserker Crescendo",
        "Psalm of Mystic Shielding",
        "Syvelian's Anti-Magic Aria",
        "Solon's Bewitching Bravura",
        "Psalm of Purity",
        "Denon's Dissension",
        "Psalm of Cooling",
        "Cassindra's Chorus of Clarity",
        "Agilmente's Aria of Eagles",
        "Psalm of Vitality",
        "Crission's Pixie Strike",
        "Psalm of Warmth",
        "Selo's Consonant Chain",
        "Alenia's Disenchanting Melody",
        "Shauri's Sonorous Clouding",
        "Guardian Rhythms",
        "Tarew's Aquatic Ayre",
        "Purifying Rhythms",
        "Cinda's Charismatic Carillon",
        "Elemental Rhythms",
        "Hymn of Restoration",
        "Selo's Accelerando"
    ])
)
RangerClass = EqClass(
    "Ranger",
    frozenset([MeleeRole(), SnarerRole(), RangerRole()]),
    required_spells=frozenset([
        "Wolf Form",
        "Superior Camouflage",
        "Ensnaring Roots",
        "Healing",
        "Resist Fire",
        "Levitate",
        "Spirit of Wolf",
        "Enduring Breath",
        "Snare"
    ])
)
ShadowknightClass = EqClass(
    "Shadowknight",
    frozenset([MeleeRole(), SnarerRole(), ShadowknightRole()]),
    required_spells=frozenset([
        "Harmshield",
        "Dismiss Undead",
        "Life Leech",
        "Summon Dead",
        "Breath of the Dead",
        "Dooming Darkness",
        "Resist Cold",
        "Gather Shadows",
        "Feign Death"
    ])
)
ClericClass = EqClass(
    "Cleric",
    frozenset([CasterRole(), HealerRole(), ClericRole(), BufferRole()]),
    required_spells=frozenset([
        "Abolish Poison",
        "Expel Summoned",
        "Resurrection",
        "Immobilize",
        "Shield of Words",
        "Word of Healing",
        "Resist Magic",
        "Banish Undead",
        "Resolution",
        "Symbol of Naltron",
        "Complete Heal",
        "Resist Cold",
        "Nullify Magic",
        "Resist Disease",
        "Pacify",
        "Resist Fire",
        "Resist Poison",
        "Superior Healing",
        "Divine Barrier",
        "Counteract Disease",
        "Greater Healing",
        "Invisibility Versus Undead",
        "Bind Affinity",
        "Gate",
        "Divine Aura"
    ])
)
ShamanClass = EqClass(
    "Shaman",
    frozenset([CasterRole(), HealerRole(), DoterRole(), SlowerRole(), ShamanRole(), BufferRole(), DispellerRole()]),
    required_spells=frozenset([
        "Envenomed Bolt",
        "Plague",
        "Abolish Disease",
        "Dexterity",
        "Malosi",
        "Charisma",
        "Strength",
        "Nullify Magic",
        "Resist Magic",
        "Stamina",
        "Alacrity",
        "Incapacitate",
        "Agility",
        "Talisman of Altuna",
        "Chloroplast",
        "Togor's Insects",
        "Resist Poison",
        "Resist Disease",
        "Greater Healing",
        "Invisibility",
        "Counteract Poison",
        "Cannibalize II",
        "Counteract Disease",
        "Spirit of Wolf",
        "Shrink",
        "Bind Affinity",
        "Gate"
    ])
)
DruidClass = EqClass(
    "Druid",
    frozenset([CasterRole(), HealerRole(), DoterRole(), NukerRole(), SnarerRole(), DispellerRole(), DruidRole(),
               DamageShielderRole(), BufferRole()]),
    required_spells=frozenset([
        "Ensnare",
        "Starfire",
        "Drifting Death",
        "Greater Healing",
        "Spirit of Wolf",
        "Pack Spirit",
        "Pack Chloroplast",
        "Shield of Thorns",
        "Bind Affinity",
        "Gate",
        "Nullify Magic",
        "Resist Magic",
        "Resist Disease",
        "Resist Poison",
        "Resist Fire",
        "Resist Cold",
        "Allure of the Wild",
        "Earthquake",
        "Counteract Disease",
        "Counteract Poison",
        "Levitate",
        "Circle of Commons",
        "Circle of Feerrott",
        "Circle of Knowledge",
        "Circle of Lavastorm",
        "Circle of Misty",
        "Circle of Ro",
        "Circle of Steamfont",
        "Circle of Surefall Glade",
        "Circle of Karana",
        "Circle of Butcher",
        "Circle of Toxxulia",
        "Superior Camouflage",
        "Harmony",
        "Ring of Butcher",
        "Ring of Commons",
        "Ring of Feerrott",
        "Ring of Karana",
        "Ring of Knowledge",
        "Ring of Lavastorm",
        "Ring of Misty",
        "Ring of Ro",
        "Ring of Steamfont",
        "Ring of Surefall Glade",
        "Ring of Toxxulia",
        "Enduring Breath",
        "Expel Summoned"
    ])
)
EnchanterClass = EqClass(
    "Enchanter",
    frozenset([CasterRole(), DispellerRole(), SlowerRole(), PetOwnerRole(), EnchanterRole(), BufferRole()]),
    required_spells=frozenset([
        "Group Resist Magic",
        "Dazzle",
        "Swift Like the Wind",
        "Adorning Grace",
        "Allure",
        "Reoccurring Amnesia",
        "Paralyzing Earth",
        "Color Skew",
        "Pillage Enchantment",
        "Tashania",
        "Brilliance",
        "Shiftless Deeds",
        "Rune IV",
        "Incapacitate",
        "Resist Magic",
        "Mana Sieve",
        "Clarity",
        "Greater Mass Enchant Platinum",
        "Enchant Platinum",
        "Greater Mass Enchant Gold",
        "Enchant Gold",
        "Color Shift",
        "Benevolence",
        "Greater Mass Enchant Electrum",
        "Enchant Electrum",
        "Pacify",
        "Levitate",
        "Enduring Breath",
        "Illusion: Dark Elf",
        "Illusion: Gnome",
        "Greater Mass Enchant Silver",
        "Bind Affinity",
        "Enchant Silver",
        "Gate",
        "Enchant Silver",
        "Enchant Clay",
        "Invisibility"
    ])
)
WizardClass = EqClass(
    "Wizard",
    frozenset([CasterRole(), NukerRole(), WizardRole(), DispellerRole()]),
    required_spells=frozenset([
        "Ice Comet",
        "Wrath of Al'Kabor",
        "Paralyzing Earth",
        "Rend",
        "Markar's Clash",
        "Alter Plane: Sky",
        "Alter Plane: Hate",
        "Supernova",
        "Translocate: Cazic",
        "Conflagration",
        "Translocate: Ro",
        "Translocate: West",
        "Translocate: Nek",
        "Translocate: Common",
        "West Portal",
        "Translocate: Tox",
        "Ro Portal",
        "Translocate: Fay",
        "Common Portal",
        "Translocate: North",
        "Nullify Magic",
        "Cazic Portal",
        "Nek Portal",
        "Tox Portal",
        "Fay Portal",
        "North Portal",
        "West Gate",
        "Cazic Gate",
        "Ro Gate",
        "Nek Gate",
        "Levitate",
        "Common Gate",
        "Fay Gate",
        "Tox Gate",
        "North Gate",
        "Lesser Evacuate",
        "Invisibility",
        "Gate",
        "Bind Affinity",
        "Translocate",
        "Harvest",
        "Concussion"
    ])
)
NecromancerClass = EqClass(
    "Necromancer",
    frozenset([CasterRole(), NukerRole(), DoterRole(), PetOwnerRole(), SnarerRole(), NecromancerRole()]),
    required_spells=frozenset([
        "Envenomed Bolt",
        "Bond of Death",
        "Lich",
        "Drain Soul",
        "Invoke Death",
        "Ignite Blood",
        "Cascading Darkness",
        "Paralyzing Earth",
        "Banish Undead",
        "Pact of Shadow",
        "Ignite Bones",
        "Dead Man Floating",
        "Nullify Magic",
        "Counteract Disease",
        "Augment Death",
        "Harmshield",
        "Feign Death",
        "Summon Corpse",
        "Gate",
        "Bind Affinity",
        "Invisibility Versus Undead",
        "Gather Shadows"
    ])
)
MagicianClass = EqClass(
    "Magician",
    frozenset([CasterRole(), NukerRole(), PetOwnerRole(), DamageShielderRole(), MagicianRole(), BufferRole()]),
    required_spells=frozenset([
        "Greater Conjuration: Water",
        "Greater Conjuration: Earth",
        "Greater Conjuration: Air",
        "Greater Conjuration: Fire",
        "Burnout III",
        "Shield of Lava",
        "Malaisement",
        "Lava Bolt",
        "Shock of Swords",
        "Nullify Magic",
        "Sword of Runes",
        "Summon Arrows",
        "Summon Throwing Dagger",
        "Bind Affinity",
        "Gate",
        "Cornucopia",
        "Everfount"
    ])
)
