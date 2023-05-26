import random
from random import randint
from typing import List, Tuple, Generator

from character import CHARACTER_LACUS, CHARACTER_GOBBIN, CHARACTER_JELESPIA, CHARACTER_HEEYO, CHARACTER_ZAVVO, \
    CHARACTER_KIKA, CHARACTER_QUIA, CHARACTER_XELMAR, CHARACTER_CONTOR, CHARACTER_FADRO, CHARACTER_TOMMAR, \
    CHARACTER_STABBA, CHARACTER_WAMMA, CHARACTER_KORLOV, CHARACTER_UTLIAH, CHARACTER_POXXIN, CHARACTER_BELOMB, \
    CHARACTER_DIDYA, CHARACTER_AGRAUL, CHARACTER_MAMBO, CHARACTER_ETTIA, CHARACTER_YAMMER, CHARACTER_NOKO, \
    CHARACTER_VELLOCK, CHARACTER_CHAILA, CHARACTER_OMBRO, CHARACTER_KRYSO, CHARACTER_TIRIA, CHARACTER_PORRIT, \
    CHARACTER_RASTLE, Character, CHARACTERS
from ini import generate_configs_for_all_characters, REMOTE_EQBC
from roles.assist_healer import AssistHealerRole
from roles.battle_rezzer import BattleRezzerRole
from roles.eq_class import ClericClass, WarriorClass, RogueClass, DruidClass, MonkClass, ShadowknightClass, \
    PaladinClass, RangerClass, ShamanClass, MagicianClass, EnchanterClass, WizardClass
from roles.joust_monitor import JoustMonitorRole, JoustTrigger
from roles.joust_nuker import JoustNukerRole
from roles.jouster import JousterRole
from roles.junk_buffer import JunkBufferRole
from roles.models.buff_config import BuffConfig
from roles.models.party_config import PartyConfiguration, Group, CharacterHealingConfiguration, HealingStrategy, \
    HealingConfiguration
from roles.models.target import ExplicitTarget, ClassTarget, CasterTarget, AllTarget, MeleeTarget, ExcludeTarget
from roles.tank_rotation_monitor import TankRotationMonitorRole

buff_config = frozenset([
    ('HpAc', BuffConfig(casters=frozenset([ClassTarget(ClericClass)]), targets=frozenset([ClassTarget(WarriorClass), ExplicitTarget(CHARACTER_JELESPIA), ClassTarget(ClericClass)]))),
    ('Symbol', BuffConfig(casters=frozenset([ClassTarget(ClericClass)]), targets=frozenset([ClassTarget(WarriorClass), ExplicitTarget(CHARACTER_JELESPIA), ClassTarget(ClericClass)]))),
    ('Ac', BuffConfig(casters=frozenset([ClassTarget(ClericClass)]), targets=frozenset([ClassTarget(WarriorClass)]))),
    ('Sow', BuffConfig(casters=frozenset([ClassTarget(DruidClass)]), targets=frozenset([AllTarget()]), is_group_spell=True)),
    ('StrBuff', BuffConfig(casters=frozenset([ClassTarget(ShamanClass)]), targets=frozenset([ClassTarget(WarriorClass), ClassTarget(RogueClass)]))),
    ('StaBuff', BuffConfig(casters=frozenset([ClassTarget(ShamanClass)]), targets=frozenset([ClassTarget(WarriorClass)]))),
    ('DamageShield', BuffConfig(casters=frozenset([ClassTarget(MagicianClass)]), targets=frozenset([ClassTarget(WarriorClass)]))),
    ('Clarity', BuffConfig(casters=frozenset([ClassTarget(EnchanterClass)]), targets=frozenset([CasterTarget()]))),
    ("Haste", BuffConfig(casters=frozenset([ClassTarget(EnchanterClass)]), targets=frozenset([ClassTarget(WarriorClass), ClassTarget(RogueClass), ClassTarget(MonkClass), ClassTarget(ShadowknightClass), ClassTarget(PaladinClass), ClassTarget(RangerClass)]))),
    # ("Burnout", BuffConfig(casters=frozenset([CHARACTER_PORRIT]), targets=frozenset([PetTarget(CHARACTER_PORRIT)]))),
    # ("Burnout", BuffConfig(casters=frozenset([CHARACTER_CONTOR]), targets=frozenset([PetTarget(CHARACTER_CONTOR)]))),
    ("Talisman", BuffConfig(casters=frozenset([ClassTarget(ShamanClass)]), targets=frozenset([ClassTarget(WarriorClass)]))),
    # ("ResistDisease", BuffConfig(casters=frozenset([ClassTarget(ClericClass)]), targets=frozenset([AllTarget()])))
    ("IntWis", BuffConfig(casters=frozenset([ClassTarget(EnchanterClass)]), targets=frozenset([ClassTarget(ClericClass)])))
])


def make_healer_configuration(
        main_healers: list[Character],
        offtank_healers: list[Character],
        spot_healers: list[Character],
        spot_clerics: list[Character],
        topup_healers: list[Character]
) -> HealingConfiguration:
    def round_robin(characters: list[Character]) -> Generator[Character, None, None]:
        while True:
            for character in characters:
                yield character

    def round_robin_cleric(characters: list[Character]) -> Generator[Character, None, None]:
        while True:
            for character in characters:
                yield character

    spot_healer_gen = round_robin(spot_healers)
    spot_cleric_gen = round_robin_cleric(spot_clerics)

    output: List[Tuple[Character, CharacterHealingConfiguration]] = []

    for character in CHARACTERS:
        healers: list[Character] = []

        if character.class_ == WarriorClass:
            random.shuffle(spot_clerics)
            healers.extend(spot_clerics[:2])
        else:
            healers_ = spot_clerics + spot_healers
            random.shuffle(healers_)
            healers.extend(healers_[:2])

        config = CharacterHealingConfiguration(
            frozenset(healers),
            HealingStrategy.NORMAL
        )

        output.append((character, config))

    return HealingConfiguration(
        frozenset(output),
        frozenset(main_healers),
        frozenset(offtank_healers),
        frozenset(topup_healers)
    )


if __name__ == '__main__':
    all_clerics = [CHARACTER_HEEYO, CHARACTER_XELMAR, CHARACTER_UTLIAH, CHARACTER_AGRAUL, CHARACTER_CHAILA]

    maintank_healer_config = make_healer_configuration(
        [CHARACTER_HEEYO,  CHARACTER_XELMAR, CHARACTER_UTLIAH, CHARACTER_CHAILA],
        [],
        [CHARACTER_POXXIN, CHARACTER_GOBBIN],
        [CHARACTER_AGRAUL, CHARACTER_GOBBIN, CHARACTER_POXXIN],
        all_clerics
    )

    offtank_healer_config = make_healer_configuration(
        [CHARACTER_HEEYO,  CHARACTER_XELMAR],
        [CHARACTER_UTLIAH, CHARACTER_CHAILA],
        [CHARACTER_POXXIN, CHARACTER_GOBBIN],
        [CHARACTER_AGRAUL, CHARACTER_GOBBIN, CHARACTER_POXXIN],
        all_clerics
    )
    keeper_of_souls_healer_config = make_healer_configuration(
        [CHARACTER_HEEYO, CHARACTER_UTLIAH, CHARACTER_CHAILA],
        [],
        [CHARACTER_GOBBIN, CHARACTER_POXXIN],
        [CHARACTER_XELMAR],
        all_clerics
    )
    group_config = frozenset([
            Group(
                CHARACTER_KIKA,
                frozenset([
                    CHARACTER_WAMMA,
                    CHARACTER_TOMMAR,
                    CHARACTER_LACUS,
                    CHARACTER_DIDYA,
                    CHARACTER_OMBRO
                ])
            ),
            Group(
                CHARACTER_QUIA,
                frozenset([
                    CHARACTER_XELMAR,
                    CHARACTER_HEEYO,
                    CHARACTER_AGRAUL,
                    CHARACTER_UTLIAH,
                    CHARACTER_JELESPIA
                ])
            ),
            Group(
                CHARACTER_KORLOV,
                frozenset([
                    CHARACTER_NOKO,
                    CHARACTER_CONTOR,
                    CHARACTER_VELLOCK,
                    CHARACTER_POXXIN,
                    CHARACTER_MAMBO
                ])
            ),
            Group(
                CHARACTER_ETTIA,
                frozenset([
                    CHARACTER_GOBBIN,
                    CHARACTER_YAMMER,
                    CHARACTER_ZAVVO,
                    CHARACTER_BELOMB,
                    CHARACTER_FADRO
                ])
            ),
            Group(
                CHARACTER_TIRIA,
                frozenset([
                    CHARACTER_STABBA,
                    CHARACTER_KRYSO,
                    CHARACTER_CHAILA,
                    CHARACTER_PORRIT,
                    CHARACTER_RASTLE
                ])
            )
        ])

    offtank_party_config = PartyConfiguration(
        groups=group_config,
        healing_config=offtank_healer_config,
        buff_config=buff_config
    )
    keeper_party_config = PartyConfiguration(
        groups=group_config,
        healing_config=keeper_of_souls_healer_config,
        buff_config=buff_config,
        extra_roles=frozenset([
            (CHARACTER_XELMAR, BattleRezzerRole([CHARACTER_WAMMA, CHARACTER_OMBRO, CHARACTER_YAMMER, CHARACTER_STABBA, CHARACTER_ZAVVO])),
            (CHARACTER_AGRAUL, BattleRezzerRole([CHARACTER_LACUS, CHARACTER_TOMMAR, CHARACTER_DIDYA, CHARACTER_RASTLE, CHARACTER_KIKA])),
            (CHARACTER_QUIA, TankRotationMonitorRole([CHARACTER_WAMMA, CHARACTER_OMBRO, CHARACTER_LACUS, CHARACTER_TOMMAR]))
        ])
    )

    fright_healer_config = make_healer_configuration(
        [],
        [],
        [],
        [],
        all_clerics
    )

    fright_party_config = PartyConfiguration(
        groups=group_config,
        healing_config=fright_healer_config,
        buff_config=buff_config,
        extra_roles=frozenset([
            (CHARACTER_XELMAR, BattleRezzerRole([CHARACTER_WAMMA, CHARACTER_OMBRO, CHARACTER_YAMMER, CHARACTER_STABBA, CHARACTER_ZAVVO])),
            (CHARACTER_AGRAUL, BattleRezzerRole([CHARACTER_LACUS, CHARACTER_TOMMAR, CHARACTER_DIDYA, CHARACTER_RASTLE, CHARACTER_KIKA])),
            (CHARACTER_HEEYO, AssistHealerRole()),
            (CHARACTER_GOBBIN, AssistHealerRole()),
            (CHARACTER_UTLIAH, AssistHealerRole()),
            (CHARACTER_CHAILA, AssistHealerRole()),
        ])
    )

    nagafen_healing_config = fright_healer_config

    nagafen_party_config = PartyConfiguration(
        groups=group_config,
        healing_config=nagafen_healing_config,
        buff_config=buff_config,
        extra_roles=frozenset([
            (CHARACTER_GOBBIN, JunkBufferRole("Endure Cold", CHARACTER_WAMMA.name)),
            (CHARACTER_POXXIN, JunkBufferRole("Dexterous Aura", CHARACTER_WAMMA.name)),
            (CHARACTER_WAMMA, JoustMonitorRole(
                frozenset([
                    JoustTrigger("Fear", "Dragon Roar", "#*#You flee in terror.#*#"),
                    JoustTrigger("AE", "Lava Breath", "#*#Your body combusts as the lava hits you#*#")
                 ]),
                "Lord Nagafen",
                (-859, -1192)
            )),
            (frozenset([MeleeTarget(), ExcludeTarget(frozenset([CHARACTER_WAMMA, CHARACTER_QUIA, CHARACTER_ETTIA]))]), JousterRole()),
            (ClassTarget(WizardClass), JoustNukerRole()),
        ])
    )

    maintank_party_config = PartyConfiguration(
        groups=group_config,
        healing_config=maintank_healer_config,
        buff_config=buff_config
    )

    generate_configs_for_all_characters(
        maintank_party_config,
        eqbc_server=REMOTE_EQBC,
        local_only=False)
