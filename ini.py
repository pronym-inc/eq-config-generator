import os
import shutil
from dataclasses import dataclass
from typing import Dict, List, Optional

from character import Character, CHARACTERS, BardConfig
from roles.eq_class import EqClass
from roles.models import HotButton, Social
from roles.models.hot_button import SocialHotButton, SkillHotButton
from roles.models.party_config import PartyConfiguration


@dataclass(frozen=True)
class VideoModes:
    width: int
    height: int
    windowed_width: int
    windowed_height: int
    reduced_quality: bool


@dataclass(frozen=True)
class Server:
    name: str
    eq_path: str
    mq_path: str
    video_modes: VideoModes

    @property
    def macro_path(self) -> str:
        return os.path.join(self.mq_path, "Macros")

    @property
    def mq_config_path(self) -> str:
        return os.path.join(self.mq_path, "config")


@dataclass(frozen=True)
class EqbcServer:
    host: str
    port: int = 2112


LOCAL_EQBC = EqbcServer("127.0.0.1")
REMOTE_EQBC = EqbcServer("127.0.0.1")


LOCAL = Server(
    "Local",
    eq_path="C:\\everquest_rof2",
    mq_path="C:\\Users\\Gregg Keithley\\AppData\\Local\\VeryVanilla\\Emu\\Release",
    video_modes=VideoModes(
        width=1820,
        height=1440,
        windowed_width=1820,
        windowed_height=1440,
        reduced_quality=False
    )
)


AWS1 = Server(
    "AWS1",
    eq_path="\\\\10.0.14.190\\everquest_rof2",
    mq_path="\\\\10.0.14.190\\Release",
    video_modes=VideoModes(
        width=800,
        height=600,
        windowed_width=800,
        windowed_height=600,
        reduced_quality=True
    )
)

AWS2 = Server(
    "AWS2",
    eq_path="\\\\10.0.1.42\\everquest_rof2",
    mq_path="\\\\10.0.1.42\\Release",
    video_modes=VideoModes(
        width=800,
        height=600,
        windowed_width=800,
        windowed_height=600,
        reduced_quality=True
    )
)


SERVERS = [LOCAL]


def compare_dicts(dict1: Dict[str, Dict[str, str]], dict2: Dict[str, Dict[str, str]]) -> bool:
    if set(dict1.keys()) != set(dict2.keys()):
        return False

    for key, sub_dict1 in dict1.items():
        sub_dict2 = dict2[key]

        if set(sub_dict1.keys()) != set(sub_dict2.keys()):
            return False

        for sub_key, value1 in sub_dict1.items():
            value2 = sub_dict2[sub_key]
            if value1 != value2:
                return False

    return True


def diff_ini_sections(section_name: str, section1: Dict[str, str], section2: Dict[str, str]) -> None:
    all_keys = set(section1.keys()).union(set(section2.keys()))
    for key in all_keys:
        value1 = section1.get(key)
        value2 = section2.get(key)
        if value1 != value2:
            print(f"[{section_name}] {key}: {value1} != {value2}")


def diff_inis(dict1: Dict[str, Dict[str, str]], dict2: Dict[str, Dict[str, str]]) -> None:
    for section_name in set(dict1.keys()).union(set(dict2.keys())):
        if section_name not in dict1:
            print(f"Missing {section_name} in dict 1")
        elif section_name not in dict2:
            print(f"Missing {section_name} in dict 1")
        else:
            diff_ini_sections(
                section_name,
                dict1[section_name],
                dict2[section_name]
            )


def render_file_to_eq(
        path: str,
        contents: Dict[str, Dict[str, str]],
        servers: List[Server]
) -> None:
    paths_to_use = [
        server.eq_path
        for server
        in servers
    ]

    for eq_path in paths_to_use:
        render_file_to_path_if_different(os.path.join(eq_path, path), contents)


def render_file_to_mq2(
    path: str,
    contents: Dict[str, Dict[str, str]],
    servers: List[Server]
) -> None:
    paths_to_use = [
        server.mq_config_path
        for server
        in servers
    ]

    for mq2_path in paths_to_use:
        render_file_to_path_if_different(os.path.join(mq2_path, path), contents)


def render_file_to_macros(
    path: str,
    contents: Dict[str, Dict[str, str]],
    servers: List[Server]
) -> None:
    paths_to_use = [
        server.macro_path
        for server
        in servers
    ]

    for mq2_path in paths_to_use:
        render_file_to_path_if_different(os.path.join(mq2_path, path), contents)


def render_file_to_path_if_different(
    path: str,
    contents: Dict[str, Dict[str, str]]
) -> None:
    if os.path.exists(path):
        data = load_ini(path)
        # If the files are the same, no need to do anything else.
        if compare_dicts(contents, data):
            return

    print(f"Updating {path}")

    render_ini(contents, path)


def render_ini(contents: Dict[str, Dict[str, str]], output_path: str):
    with open(output_path, 'w') as f:
        for header, data in contents.items():
            f.writelines([f"[{header}]\n"])
            for key, value in data.items():
                f.writelines([f"{key}={value}\n"])


def load_ini(path: str) -> Dict[str, Dict[str, str]]:
    with open(path) as f:
        output: Dict[str, Dict[str, str]] = {}
        current_header: Optional[str] = None
        for line in f:
            if line.strip() == "":
                continue
            if line.startswith("["):
                current_header = line.replace("[", "").replace("]", "").strip()
                output[current_header] = {}
            else:
                split_line = line.split("=")
                key = split_line[0]
                value = "=".join(split_line[1:]).strip()
                output[current_header][key] = value

        return output


def render_file_to_path_with_backup(contents: Dict[str, Dict[str, str]], path: str):
    if os.path.exists(path):
        shutil.copyfile(path, path + ".bak")

    render_ini(contents, path)


def render_config(data: Dict[str, Dict[str, str]]) -> List[str]:
    output: List[str] = []

    for header, values in data.items():
        output.append(f"[{header}]")
        for key, value in values.items():
            output.append(f"{key}={value}")

    return output


def create_spell_config_for_character(character: Character) -> Dict[str, Dict[str, str]]:
    output: Dict[str, Dict[str, str]] = {"default": {}}
    for idx, spell in enumerate(character.spellbook.get_sorted_spells()):
        output["default"][f"Gem{idx + 1}"] = spell.name
    output["default"]["RequiredSpells"] = ",".join(sorted(list(character.class_.required_spells)))
    return output


def create_client_config_for_character(character: Character, server: Server) -> Dict[str, Dict[str, str]]:
    ini = load_ini("ini_templates/eqclient.template.ini")
    ini['Defaults']['AttackOnAssist'] = "TRUE" if character.class_.is_melee() else "FALSE"
    ini['VideoMode']['Width'] = str(server.video_modes.width)
    ini['VideoMode']['Height'] = str(server.video_modes.height)
    ini['VideoMode']['WindowedWidth'] = str(server.video_modes.windowed_width)
    ini['VideoMode']['WindowedHeight'] = str(server.video_modes.windowed_height)

    if server.video_modes.reduced_quality:
        ini['Defaults'].update({
            'MultiPassLighting': '0',
            'SpellParticleDensity': '0.000000',
            'ActorParticleDensity': '0.000000',
            'PostEffects': '0',
            'EnvironmentParticleDensity': '0.000000',
            'ShowGrass': '0',
            'TerrainTextureQuality': '0'
        })
        ini['Options'].update({
            'ClipPlane': '0',
            'Sky': '0',
            'ActorClipPlane': '0',
            'FogScale': '0.100000',
            'ShadowClipPlane': '0',
            'LoD': '0'
        })
    return ini


def create_ui_config() -> Dict[str, Dict[str, str]]:
    return load_ini("ini_templates/ui.template.ini")


def get_base_character_config() -> Dict[str, Dict[str, str]]:
    return load_ini("ini_templates/character.template.ini")


def create_configs_for_class(class_: EqClass) -> Dict[str, Dict[str, str]]:
    output = get_base_character_config()

    social_entries: List[Social] = sorted(class_.get_socials(), key=lambda x: x.name)

    social_output: Dict[str, str] = {}

    social_number_by_name: Dict[str, str] = {}

    for (idx, social) in enumerate(social_entries):
        page_idx = 2 + idx // 12
        button_idx = 1 + idx % 12
        social_idx = idx + 12

        social_number_by_name[social.name] = f"E{social_idx}"

        name_base = f"Page{page_idx}Button{button_idx}"

        social_output[f"{name_base}Name"] = social.name
        social_output[f"{name_base}Color"] = str(social.color)
        social_output[f"{name_base}Line1"] = social.line1
        for i in range(2, 6):
            maybe_line = getattr(social, f"line{i}")
            if maybe_line is not None:
                social_output[f"{name_base}Line{i}"] = maybe_line

    output["Socials"] = social_output

    hot_buttons: List[HotButton] = class_.get_hot_buttons()

    hot_buttons_output: Dict[str, Dict[str, str]] = {}

    for hot_button in hot_buttons:
        section_name: str
        if hot_button.bank_index == 1:
            section_name = "HotButtons"
        else:
            section_name = f"HotButtons{hot_button.bank_index}"

        if section_name not in hot_buttons_output:
            hot_buttons_output[section_name] = {}

        key = f"Page1Button{hot_button.button_index}"

        value: str

        if isinstance(hot_button, SocialHotButton):
            key_alias = social_number_by_name[hot_button.social.name]
            value = f"{key_alias},@-1,0000000000000000,0,{hot_button.social.name or ''}"
        elif isinstance(hot_button, SkillHotButton):
            value = f"J{hot_button.skill.skill_id},@-1,0000000000000000,0,{hot_button.skill.name}"
        else:
            raise Exception(f"Unknown hot button type: {hot_button}")

        hot_buttons_output[section_name][key] = value

    output.update(hot_buttons_output)

    return output


def create_bureauconfig_for_character(
        character: Character,
        party_config: PartyConfiguration
) -> Dict[str, Dict[str, str]]:
    output: Dict[str, str] = {
        'IsMelee': "1" if character.class_.is_melee() else "0",
        'Healer': ",".join(map(
            lambda x: x.name,
            party_config.get_healers_by_character().get(character, [])
        )),
        'HealThreshold': str(65 if character.class_.is_warrior() else 90)
    }

    for spell_alias in character.get_spell_aliases():
        maybe_spell = spell_alias.get_from_spellbook(character.spellbook)
        if maybe_spell:
            output[f"{spell_alias.alias}Spell"] = maybe_spell.name

    return {"Default": output}


def create_mq2_config_for_character() -> Dict[str, Dict[str, str]]:
    return {
        "MQ2Rez": {
            "Accept": "On",
            "RezPct": "0",
            "SafeMode": "Off",
            "VoiceNotify": "Off",
            "ReleaseToBind": "Off",
            "SilentMode": "On",
            "Command Line": "/mac lootcorpse",
            "Delay": "1000"
        }
    }


def create_event_config_for_character(character: Character) -> Dict[str, Dict[str, str]]:
    return {
        event.name: {
            "trigger": event.trigger,
            "command": event.command
        }
        for event
        in character.get_events()
    }


def generate_eqls_for_character(character: Character) -> Dict[str, Dict[str, str]]:
    contents = load_ini("ini_templates/eqlsPlayerData.template.ini")

    contents['PLAYER']['Username'] = character.name.lower()

    return contents


def generate_config_for_character(
    character: Character,
    party_config: PartyConfiguration,
    servers: List[Server]
) -> None:
    character.class_.validate()

    render_file_to_eq(
        f"{character.name}_GreggServer.ini",
        create_configs_for_class(character.class_),
        servers
    )
    for server in servers:
        render_file_to_eq(
            f"eqclient-{character.name}.ini",
            create_client_config_for_character(character, server),
            [server]
        )
    render_file_to_eq(
        f"UI_{character.name}_GreggServer.ini",
        create_ui_config(),
        servers
    )
    render_file_to_eq(
        f"eqlsPlayerData-{character.name}.ini",
        generate_eqls_for_character(character),
        servers
    )
    render_file_to_macros(
        f"BureauSpells_{character.name}.ini",
        create_spell_config_for_character(character),
        servers
    )
    render_file_to_macros(
        f"BureauConfig_{character.name}.ini",
        create_bureauconfig_for_character(character, party_config),
        servers
    )
    render_file_to_mq2(
        f"MQ2Events_{character.name}.ini",
        create_event_config_for_character(character),
        servers
    )
    render_file_to_mq2(
        f"GreggServer_{character.name}.ini",
        create_mq2_config_for_character(),
        servers
    )

    if character.bard_config is not None:
        generate_bard_config(character, character.bard_config, servers)


def generate_auto_accept_config(
    characters: List[Character],
    servers: List[Server]
) -> None:
    output: Dict[str, Dict[str, str]] = {}

    for character in characters:
        character_entries: Dict[str, Dict[str, str]] = {
            f"{character.name}_Settings": {
                "Enabled": "1",
                "Translocate": "1",
                "Anchor": "0",
                "SelfAnchor": "0",
                "Trade": "1",
                "TradeAlways": "1",
                "TradeReject": "0",
                "Group": "1",
                "Fellowship": "1",
                "Raid": "1"
            },
            f"{character.name}_Names": {
                other_character.name: "1"
                for other_character
                in characters
                if other_character != character
            },
            f"{character.name}_Anchors": {}
        }
        output.update(character_entries)

    render_file_to_mq2(
        "MQ2AutoAccept.ini",
        output,
        servers
    )


def generate_bard_config(
    character: Character,
    bard_config: BardConfig,
    servers: List[Server]
) -> None:
    config: Dict[str, Dict[str, str]] = {
        "Settings":  {
            "Horn": f'/exchange "{bard_config.horn_name}" offhand',
            "Drum": f'/exchange "{bard_config.drum_name}" offhand',
            "Wind": f'/exchange "{bard_config.wind_name}" offhand',
            "Lute": f'/exchange "{bard_config.lute_name}" offhand',
            "Singing": "DISABLED",
            "Weapons": f'/exchange "{bard_config.weapon_name}" offhand',
            "Delay": "21"
        }
    }

    render_file_to_mq2(
        f'MQ2BardSwap_{character.name}_GreggServer.ini',
        config,
        servers
    )


def generate_macroquest_config(servers: List[Server]) -> None:
    contents = load_ini("ini_templates/MacroQuest.template.ini")

    render_file_to_mq2("MacroQuest.ini", contents, servers)


def generate_group_config(
    party_config: PartyConfiguration,
    servers: List[Server]
) -> None:
    config = {
        'GroupLeaders': ",".join(sorted(map(lambda x: x.leader.name, party_config.groups)))
    }

    for idx, group in enumerate(sorted(party_config.groups, key=lambda x: x.leader.name)):
        config[f'Group{idx + 1}Members'] = ",".join(sorted(map(lambda x: x.name, group.members)))

    contents = {"Default": config}

    render_file_to_macros(
        "bureaugroup.ini",
        contents,
        servers
    )


def generate_buff_config(
    party_config: PartyConfiguration,
    servers: List[Server]
) -> None:
    contents: Dict[str, Dict[str, str]] = {}

    for spell_alias, buff_config in party_config.buff_config:
        targets: List[str] = []
        for target in buff_config.targets:
            targets.extend(list(target.get_targets()))

        entry = {
            'SpellAlias': f'{spell_alias}Spell',
            'Targets': ",".join(sorted(targets)),
            'IsGroupSpell': '1' if buff_config.is_group_spell else '0',
            'Casters': buff_config.caster.name,
            'Enabled': '1'
        }
        contents[spell_alias] = entry

    render_file_to_macros(
        'bureaubuff_main.ini',
        contents,
        servers
    )


def generate_autologin_config(
        servers: List[Server]
) -> None:
    contents: Dict[str, Dict[str, str]] = {
        'Settings': {
            'KickActiveCharacter': '1',
            'UseStationNamesInsteadOfSessions': '1',
            'UseMQ2Login': '0',
            'NotifyOnServerUP': '0'
        },
        'Servers': {
            'gregg': 'Gregg'
        }
    }

    for character in CHARACTERS:
        contents[character.name.lower()] = {
            'Password': 'darwin',
            'Server': 'gregg',
            'Character': character.name
        }

    render_file_to_mq2('mq2autologin.ini', contents, servers)


def generate_eqbc_config(
    servers: List[Server],
    eqbc_server: EqbcServer
) -> None:
    contents: Dict[str, Dict[str, str]] = {
        'Settings': {
            'AllowControl': '1',
            'AutoConnect': '1',
            'SaveByCharacter': '0',
            'LocalEcho': '0',
            'UseWindow': '1'
        }
    }

    for character in CHARACTERS:
        contents[f'GreggServer.{character.name}'] = {
            'Server': eqbc_server.host,
            'Port': str(eqbc_server.port)
        }

    render_file_to_mq2('MQ2EQBC.ini', contents, servers)


def generate_eqhost(servers: List[Server]):
    contents: Dict[str, Dict[str, str]] = {
        'LoginServer': {
            'Host': 'eq.pronym.com:5999'
        }
    }

    render_file_to_eq('eqhost.txt', contents, servers)


def generate_configs_for_all_characters(
    party_config: PartyConfiguration,
    eqbc_server: EqbcServer,
    local_only: bool = False
) -> None:
    servers = [LOCAL] if local_only else SERVERS

    for character in CHARACTERS:
        generate_config_for_character(character, party_config, servers)

    generate_autologin_config(servers)
    generate_auto_accept_config(CHARACTERS, servers)
    generate_buff_config(party_config, servers)
    generate_group_config(party_config, servers)
    generate_macroquest_config(servers)
    generate_eqbc_config(servers,eqbc_server)
    generate_eqhost(servers)


__all__ = ['generate_configs_for_all_characters', 'Server', 'SERVERS', 'REMOTE_EQBC']
