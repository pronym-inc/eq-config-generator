from character import CHARACTER_LACUS, CHARACTER_GOBBIN, CHARACTER_JELESPIA, CHARACTER_HEEYO, CHARACTER_ZAVVO, \
    CHARACTER_KIKA, CHARACTER_QUIA, CHARACTER_XELMAR, CHARACTER_CONTOR, CHARACTER_FADRO, CHARACTER_TOMMAR, \
    CHARACTER_STABBA, CHARACTER_WAMMA, CHARACTER_KORLOV, CHARACTER_UTLIAH, CHARACTER_POXXIN, CHARACTER_BELOMB, \
    CHARACTER_DIDYA, CHARACTER_AGRAUL, CHARACTER_MAMBO, CHARACTER_ETTIA, CHARACTER_YAMMER, CHARACTER_NOKO, \
    CHARACTER_VELLOCK, CHARACTER_CHAILA, CHARACTER_OMBRO, CHARACTER_KRYSO, CHARACTER_TIRIA, CHARACTER_PORRIT, \
    CHARACTER_RASTLE
from ini import generate_configs_for_all_characters, SERVERS, REMOTE_EQBC
from roles.eq_class import ClericClass, WarriorClass
from roles.models.buff_config import BuffConfig
from roles.models.party_config import PartyConfiguration, Group
from roles.models.target import ExplicitTarget, MeleeTarget, ClassTarget, PetTarget, CasterTarget
from sync_macros import sync_macros

buff_config = frozenset([
    ('HpAc', BuffConfig(caster=CHARACTER_HEEYO, targets=frozenset([ClassTarget(WarriorClass), ExplicitTarget(CHARACTER_JELESPIA), ClassTarget(ClericClass)]))),
    ('Symbol', BuffConfig(caster=CHARACTER_HEEYO, targets=frozenset([ClassTarget(WarriorClass), ExplicitTarget(CHARACTER_JELESPIA), ClassTarget(ClericClass)]))),
    ('Ac', BuffConfig(caster=CHARACTER_XELMAR, targets=frozenset([ClassTarget(WarriorClass), ExplicitTarget(CHARACTER_JELESPIA), ClassTarget(ClericClass)]))),
    ('Sow', BuffConfig(caster=CHARACTER_GOBBIN, targets=frozenset([ExplicitTarget(CHARACTER_LACUS)]), is_group_spell=True)),
    ('StrBuff', BuffConfig(caster=CHARACTER_POXXIN, targets=frozenset([MeleeTarget()]))),
    ('StaBuff', BuffConfig(caster=CHARACTER_POXXIN, targets=frozenset([ClassTarget(WarriorClass)]))),
    ('DamageShield', BuffConfig(caster=CHARACTER_PORRIT, targets=frozenset([ExplicitTarget(CHARACTER_LACUS)]))),
    ('Clarity', BuffConfig(caster=CHARACTER_JELESPIA, targets=frozenset([CasterTarget()]))),
    ("Haste", BuffConfig(caster=CHARACTER_JELESPIA, targets=frozenset([MeleeTarget()]))),
    ("Burnout", BuffConfig(caster=CHARACTER_PORRIT, targets=frozenset([PetTarget(CHARACTER_PORRIT)]))),
    ("Burnout", BuffConfig(caster=CHARACTER_CONTOR, targets=frozenset([PetTarget(CHARACTER_CONTOR)]))),
    ("Talisman", BuffConfig(caster=CHARACTER_POXXIN, targets=frozenset([ClassTarget(WarriorClass), ExplicitTarget(CHARACTER_JELESPIA), ClassTarget(ClericClass)]))),
])


if __name__ == '__main__':
    party_config = PartyConfiguration(
        groups=frozenset([
            Group(
                CHARACTER_KIKA,
                frozenset([
                    CHARACTER_WAMMA,
                    CHARACTER_TOMMAR,
                    CHARACTER_LACUS,
                    CHARACTER_STABBA,
                    CHARACTER_DIDYA
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
                    CHARACTER_OMBRO,
                    CHARACTER_KRYSO,
                    CHARACTER_CHAILA,
                    CHARACTER_PORRIT,
                    CHARACTER_RASTLE
                ])
            )
        ]),
        healers=[
            (CHARACTER_LACUS, [CHARACTER_HEEYO, CHARACTER_AGRAUL, CHARACTER_XELMAR, CHARACTER_UTLIAH]),
            (CHARACTER_JELESPIA, [CHARACTER_XELMAR, CHARACTER_HEEYO, CHARACTER_AGRAUL, CHARACTER_GOBBIN]),
            (CHARACTER_GOBBIN, [CHARACTER_XELMAR, CHARACTER_HEEYO, CHARACTER_UTLIAH]),
            (CHARACTER_ZAVVO, [CHARACTER_XELMAR, CHARACTER_AGRAUL, CHARACTER_UTLIAH]),
            (CHARACTER_KIKA, [CHARACTER_HEEYO, CHARACTER_UTLIAH, CHARACTER_HEEYO]),
            (CHARACTER_HEEYO, [CHARACTER_XELMAR, CHARACTER_UTLIAH, CHARACTER_AGRAUL]),
            (CHARACTER_TOMMAR, [CHARACTER_AGRAUL, CHARACTER_XELMAR, CHARACTER_UTLIAH, CHARACTER_HEEYO]),
            (CHARACTER_CONTOR, [CHARACTER_GOBBIN, CHARACTER_XELMAR, CHARACTER_HEEYO, CHARACTER_AGRAUL]),
            (CHARACTER_XELMAR, [CHARACTER_HEEYO, CHARACTER_UTLIAH, CHARACTER_AGRAUL, CHARACTER_GOBBIN]),
            (CHARACTER_QUIA, [CHARACTER_GOBBIN, CHARACTER_XELMAR, CHARACTER_HEEYO, CHARACTER_AGRAUL]),
            (CHARACTER_FADRO, [CHARACTER_XELMAR, CHARACTER_AGRAUL, CHARACTER_UTLIAH, CHARACTER_HEEYO]),
            (CHARACTER_STABBA, [CHARACTER_XELMAR, CHARACTER_HEEYO, CHARACTER_AGRAUL, CHARACTER_UTLIAH]),
            (CHARACTER_WAMMA, [CHARACTER_UTLIAH, CHARACTER_XELMAR, CHARACTER_AGRAUL, CHARACTER_HEEYO]),
            (CHARACTER_KORLOV, [CHARACTER_AGRAUL, CHARACTER_UTLIAH, CHARACTER_AGRAUL, CHARACTER_HEEYO]),
            (CHARACTER_UTLIAH, [CHARACTER_AGRAUL, CHARACTER_HEEYO, CHARACTER_XELMAR, CHARACTER_GOBBIN]),
            (CHARACTER_POXXIN, [CHARACTER_AGRAUL, CHARACTER_UTLIAH, CHARACTER_HEEYO, CHARACTER_XELMAR]),
            (CHARACTER_BELOMB, [CHARACTER_AGRAUL, CHARACTER_XELMAR, CHARACTER_AGRAUL, CHARACTER_HEEYO]),
            (CHARACTER_DIDYA, [CHARACTER_AGRAUL, CHARACTER_HEEYO, CHARACTER_UTLIAH, CHARACTER_XELMAR]),
            (CHARACTER_VELLOCK, [CHARACTER_AGRAUL, CHARACTER_UTLIAH, CHARACTER_XELMAR, CHARACTER_HEEYO]),
            (CHARACTER_NOKO, [CHARACTER_UTLIAH, CHARACTER_HEEYO, CHARACTER_XELMAR, CHARACTER_AGRAUL]),
            (CHARACTER_MAMBO, [CHARACTER_UTLIAH, CHARACTER_AGRAUL, CHARACTER_XELMAR, CHARACTER_HEEYO]),
            (CHARACTER_ETTIA, [CHARACTER_UTLIAH, CHARACTER_XELMAR, CHARACTER_HEEYO, CHARACTER_AGRAUL]),
            (CHARACTER_YAMMER, [CHARACTER_UTLIAH, CHARACTER_AGRAUL, CHARACTER_HEEYO, CHARACTER_XELMAR]),
            (CHARACTER_AGRAUL, [CHARACTER_UTLIAH, CHARACTER_HEEYO, CHARACTER_XELMAR, CHARACTER_AGRAUL]),
            (CHARACTER_TIRIA, [CHARACTER_CHAILA, CHARACTER_AGRAUL, CHARACTER_HEEYO, CHARACTER_UTLIAH]),
            (CHARACTER_OMBRO, [CHARACTER_CHAILA, CHARACTER_AGRAUL, CHARACTER_HEEYO, CHARACTER_UTLIAH]),
            (CHARACTER_CHAILA, [CHARACTER_AGRAUL, CHARACTER_HEEYO, CHARACTER_UTLIAH]),
            (CHARACTER_RASTLE, [CHARACTER_CHAILA, CHARACTER_AGRAUL, CHARACTER_HEEYO, CHARACTER_UTLIAH]),
            (CHARACTER_KRYSO, [CHARACTER_CHAILA, CHARACTER_AGRAUL, CHARACTER_HEEYO, CHARACTER_UTLIAH]),
            (CHARACTER_PORRIT, [CHARACTER_CHAILA, CHARACTER_AGRAUL, CHARACTER_HEEYO, CHARACTER_UTLIAH])
        ],
        buff_config=buff_config
    )

    generate_configs_for_all_characters(
        party_config,
        eqbc_server=REMOTE_EQBC,
        local_only=False)

    sync_macros(SERVERS[1:])
