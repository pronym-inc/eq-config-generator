from dataclasses import dataclass
from typing import List, Optional, FrozenSet, Dict

from misc import flatten
from roles import Role
from roles.eq_class import DruidClass, RogueClass, WarriorClass, PaladinClass, ClericClass, EnchanterClass, BardClass, \
    MagicianClass, MonkClass, ShamanClass, ShadowknightClass, NecromancerClass, RangerClass, WizardClass, EqClass
from roles.models.event import Event
from roles.models.spell import Spell
from roles.models.spell_alias import SpellAlias
from roles.models.spellbook import Spellbook, DruidSpellbook, NullSpellbook, ClericSpellbook, EnchanterSpellbook, \
    BardSpellbook, MagicianSpellbook, ShamanSpellbook, ShadowknightSpellbook, NecromancerSpellbook, RangerSpellbook, \
    WizardSpellbook


@dataclass(frozen=True)
class BardConfig:
    weapon_name: str
    lute_name: str
    horn_name: str
    wind_name: str
    drum_name: str


@dataclass(frozen=True)
class Character:
    name: str
    class_: EqClass
    spellbook: Spellbook = NullSpellbook()
    bard_config: Optional[BardConfig] = None
    extra_roles: FrozenSet[Role] = frozenset([])

    def get_bureau_config(self) -> Dict[str, str]:
        output: Dict[str, str] = {
            'IsMelee': "1" if self.class_.is_melee() else "0",
            'Leader': 'Wamma',
            'CCAssist': 'Jelespia',
            'HealThreshold': str(self.get_heal_threshold()),
            'BattleStarted': "FALSE"
        }

        for spell_alias in self.get_spell_aliases():
            maybe_spell = spell_alias.get_from_spellbook(self.spellbook)
            if maybe_spell:
                output[f"{spell_alias.alias}Spell"] = maybe_spell.name

        for role in self.extra_roles:
            output.update(role.get_bureau_config())

        return output

    def get_heal_threshold(self) -> int:
        if self.class_.is_warrior():
            return 65
        else:
            return 90

    def get_events(self) -> List[Event]:
        return [
            Event(
                "CheckHeal",
                "#*#YOU for #*# damage#*#",
                "/if (!${Bool[${JustCheckedHeal}]} && ${Me.PctHPs}<${Ini[BureauConfig_${Me.Name}.ini,Default,HealThreshold]}) /mac checkheal"
            )
        ] + self.class_.get_events() + flatten(list(map(lambda x: x.get_events(), self.extra_roles)))

    def get_spell_aliases(self) -> List[SpellAlias]:
        return self.class_.get_spell_aliases()

    def with_extra_role(self, role: Role) -> 'Character':
        return Character(
            self.name,
            self.class_,
            self.spellbook,
            self.bard_config,
            frozenset(list(self.extra_roles) + [role])
        )

    def get_eqbc_channels(self) -> list[str]:
        output: list[str] = self.class_.get_eqbc_channels()

        for role in self.extra_roles:
            output.extend(role.get_eqbc_channels())

        return output



druid_spellbook = DruidSpellbook(
    snare=Spell("Ensnare"),
    nuke=Spell("Starfire"),
    dot=Spell("Drifting Death"),
    heal=Spell("Greater Healing"),
    sow=Spell("Pack Spirit"),
    dispel=Spell("Nullify Magic"),
    regen=Spell("Pack Chloroplast"),
    junk=Spell("Endure Cold")
)

cleric_spellbook = ClericSpellbook(
    hp_ac=Spell("Resolution"),
    symbol=Spell("Symbol of Naltron"),
    ac=Spell("Shield of Words"),
    small_heal=Spell("Greater Healing"),
    big_heal=Spell("Superior Healing"),
    complete_heal=Spell("Complete Heal"),
    rez=Spell("Resurrection"),
    resist_disease=Spell("Resist Disease")
)

enchanter_spellbook = EnchanterSpellbook(
    int_wis=Spell("Brilliance"),
    mesmerize=Spell("Dazzle"),
    tash=Spell("Tashania"),
    clarity=Spell("Clarity"),
    haste=Spell("Swift Like the Wind"),
    mana_drain=Spell("Mana Sieve"),
    ae_stun=Spell("Color Skew"),
    dispel=Spell("Pillage Enchantment")
)

bard_spellbook = BardSpellbook(
    hp_mana_regen=Spell("Cantata of Soothing"),
    int_wis=Spell("Cassindra's Elegy"),
    levitation=Spell("Agilmente's Aria of Eagles"),
    mana_regen=Spell("Cassindra's Chorus of Clarity"),
    movement_speed=Spell("Selo's Accelerando"),
    resist_1=Spell("Elemental Rhythms"),
    resist_2=Spell("Purifying Rhythms"),
    resist_3=Spell("Psalm of Mystic Shielding")
)

magician_spellbook = MagicianSpellbook(
    mala=Spell("Malaise"),
    nuke=Spell("Lava Bolt"),
    pet=Spell("Greater Conjuration: Water"),
    burnout=Spell("Burnout III"),
    damage_shield=Spell("Shield of Lava")
)

shaman_spellbook = ShamanSpellbook(
    dispel=Spell("Nullify Magic"),
    talisman=Spell("Talisman of Altuna"),
    sta_buff=Spell("Stamina"),
    str_buff=Spell("Strength"),
    slow=Spell("Togor's Insects"),
    heal=Spell("Greater Healing"),
    dot=Spell("Envenomed Bolt"),
    junk=Spell("Dexterous Aura")
)

shadowknight_spellbook = ShadowknightSpellbook(
    snare=Spell("Cascade of Darkness")
)

necromancer_spellbook = NecromancerSpellbook(
    dot=Spell("Envenomed Bolt"),
    nuke=Spell("Ignite Bones"),
    summon_pet=Spell("Servant of Darkness")
)

ranger_spellbook = RangerSpellbook(
    snare=Spell("Ensnare")
)

wizard_spellbook = WizardSpellbook(
    nuke=Spell("Conflagration"),
    dispel=Spell("Nullify Magic")
)


CHARACTER_GOBBIN = Character("Gobbin", DruidClass, druid_spellbook)
CHARACTER_ZAVVO = Character("Zavvo", RogueClass)
CHARACTER_LACUS = Character("Lacus", WarriorClass)
CHARACTER_FADRO = Character("Fadro", PaladinClass)
CHARACTER_HEEYO = Character(
    "Heeyo",
    ClericClass,
    cleric_spellbook
)
CHARACTER_STABBA = Character("Stabba", RogueClass)
CHARACTER_JELESPIA = Character("Jelespia", EnchanterClass, enchanter_spellbook)
CHARACTER_TOMMAR = Character("Tommar", WarriorClass)
CHARACTER_QUIA = Character(
    "Quia",
    BardClass,
    bard_spellbook,
    BardConfig(
        weapon_name="Enameled Black Mace",
        lute_name="Mandolin",
        horn_name="Horn",
        wind_name="Wooden Flute",
        drum_name="Hand Drum"
    )
)
CHARACTER_CONTOR = Character("Contor", MagicianClass, magician_spellbook)
CHARACTER_KIKA = Character("Kika", MonkClass)
CHARACTER_XELMAR = Character("Xelmar", ClericClass, cleric_spellbook)
CHARACTER_WAMMA = Character("Wamma", WarriorClass)
CHARACTER_KORLOV = Character(
    "Korlov",
    BardClass,
    bard_spellbook,
    BardConfig(
        weapon_name="Combine Long Sword",
        lute_name="Mandolin",
        horn_name="Horn",
        wind_name="Wooden Flute",
        drum_name="Hand Drum"
    )
)
CHARACTER_UTLIAH = Character("Utliah", ClericClass, cleric_spellbook)
CHARACTER_POXXIN = Character("Poxxin", ShamanClass, shaman_spellbook)
CHARACTER_BELOMB = Character("Belomb", ShadowknightClass, shadowknight_spellbook)
CHARACTER_VELLOCK = Character("Vellock", NecromancerClass, necromancer_spellbook)
CHARACTER_AGRAUL = Character("Agraul", ClericClass, cleric_spellbook)
CHARACTER_MAMBO = Character("Mambo", RangerClass, ranger_spellbook)
CHARACTER_ETTIA = Character(
    "Ettia",
    BardClass,
    bard_spellbook,
    BardConfig(
        weapon_name="Enameled Black Mace",
        lute_name="Mandolin",
        horn_name="Horn",
        wind_name="Wooden Flute",
        drum_name="Selo`s Drums of the March"
    )
)
CHARACTER_NOKO = Character("Noko", WizardClass, wizard_spellbook)
CHARACTER_YAMMER = Character("Yammer", MonkClass)
CHARACTER_DIDYA = Character("Didya", RogueClass)
CHARACTER_CHAILA = Character("Chaila", ClericClass, cleric_spellbook)
CHARACTER_OMBRO = Character("Ombro", WarriorClass)
CHARACTER_TIRIA = Character(
    "Tiria",
    BardClass,
    bard_spellbook,
    BardConfig(
        weapon_name="Enameled Black Mace",
        lute_name="Mandolin",
        horn_name="Horn",
        wind_name="Wooden Flute",
        drum_name="Hand Drum"
    )
)
CHARACTER_KRYSO = Character("Kryso", WizardClass, wizard_spellbook)
CHARACTER_PORRIT = Character("Porrit", MagicianClass, magician_spellbook)
CHARACTER_RASTLE = Character("Rastle", RogueClass)


CHARACTERS = [
    CHARACTER_GOBBIN,
    CHARACTER_GOBBIN,
    CHARACTER_ZAVVO,
    CHARACTER_LACUS,
    CHARACTER_FADRO,
    CHARACTER_HEEYO,
    CHARACTER_STABBA,
    CHARACTER_JELESPIA,
    CHARACTER_TOMMAR,
    CHARACTER_QUIA,
    CHARACTER_CONTOR,
    CHARACTER_KIKA,
    CHARACTER_XELMAR,
    CHARACTER_WAMMA,
    CHARACTER_KORLOV,
    CHARACTER_DIDYA,
    CHARACTER_UTLIAH,
    CHARACTER_POXXIN,
    CHARACTER_BELOMB,
    CHARACTER_VELLOCK,
    CHARACTER_AGRAUL,
    CHARACTER_MAMBO,
    CHARACTER_ETTIA,
    CHARACTER_NOKO,
    CHARACTER_YAMMER,
    CHARACTER_CHAILA,
    CHARACTER_OMBRO,
    CHARACTER_TIRIA,
    CHARACTER_KRYSO,
    CHARACTER_PORRIT,
    CHARACTER_RASTLE
]
