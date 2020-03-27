import json
import os.path as path

from dataclasses import asdict
from typing import Union, Optional, List

from aqt import mw

from .utils import safenav, safenav_preset

from .config_types import (
    TWSetting,
    TWWrap,
    TWTagWrap,
    TWTextWrap,
    TWMetaWrap,
)

from .interface import (
    make_setting,
    make_html_tag_wrap,
    make_html_class_wrap,
    make_text_wrap,
    make_meta_wrap,
)

from .registrar import has_interface, get_meta_wraps, meta_wrap_is_registered

SCRIPTNAME = path.dirname(path.realpath(__file__))

with open(path.join(SCRIPTNAME, '../../config.json'), encoding='utf-8') as config:
    config_default = json.load(config)

    SETTINGS_DEFAULT = config_default['settings']['1'][0]
    deck_default = SETTINGS_DEFAULT

    safenav_setting = safenav_preset(deck_default)

def serialize_setting(setting: TWSetting) -> dict:
    return {
        'deckConfName': setting.deck_conf_name,
        'enableNotifications': setting.enable_notifications,
        'straightLength': setting.straight_length,
        'baseEase': setting.base_ease,
        'stepEase': setting.step_ease,
        'startEase': setting.start_ease,
        'stopEase': setting.stop_ease,
    }

def deserialize_setting(deck_conf_name, setting_data, access_func = safenav_setting) -> TWSetting:
    result = setting_data if type(setting_data) == TWSetting else TWSetting(
        deck_conf_name,
        access_func([setting_data], ['straightLength']),
        access_func([setting_data], ['enableNotifications']),
        access_func([setting_data], ['baseEase']),
        access_func([setting_data], ['stepEase']),
        access_func([setting_data], ['startEase']),
        access_func([setting_data], ['stopEase']),
    )

    return result



def deserialize_setting_with_default(deck_conf_name, settings) -> TWSetting:
    found = filter(
        lambda v: safenav([v], ['deckConfName'], default='') == deck_conf_name,
        settings,
    )

    try:
        deck_deserialized = deserialize_setting(deck_conf_name, next(found))

    except StopIteration as e:
        deck_deserialized = deserialize_setting(deck_conf_name, deck_default)

    return deck_deserialized

def get_default_setting(deck_conf_name) -> TWSetting:
    return deserialize_setting(deck_conf_name, deck_default)

def get_setting(col, deck_conf_name='Default') -> Optional[TWSetting]:
    all_config = mw.addonManager.getConfig(__name__)
    setting = safenav(
        [all_config],
        ['settings', str(col.crt)],
        default=[],
    )

    return deserialize_setting_with_default(
        deck_conf_name,
        setting,
    )

def get_settings(col) -> List[TWSetting]:
    all_config = mw.addonManager.getConfig(__name__)
    setting = safenav([all_config], ['settings', str(col.crt)], default=[])

    deck_settings = [
        get_setting(col, deck['name'], setting)
        for deck
        in col.decks.decks.values()
    ]

    return deck_settings

# write config data to config.json
def write_settings(col, settings: List[TWSetting]) -> None:
    serialized_settings = [
        serialize_setting(setting)
        for setting
        in settings
    ]

    all_config = mw.addonManager.getConfig(__name__)

    new_config = safenav([all_config], ['settings'], default={})
    new_config[str(col.crt)] = serialized_settings

    mw.addonManager.writeConfig(__name__, {
        'settings': new_config,
    })

def write_setting(col, setting: TWSetting) -> None:
    serialized_setting = serialize_setting(setting)

    all_config = mw.addonManager.getConfig(__name__)
    current_config = safenav(
        [all_config],
        ['settings', str(col.crt)],
        default=[],
    )

    try:
        idx = next(i for i,v in enumerate(current_config) if v['deckConfName'] == setting.deck_conf_name)
        current_config[idx] = serialized_setting

    except StopIteration:
        current_config.append(serialized_setting)

    new_config = safenav([all_config], ['settings'], default={})
    new_config[str(col.crt)] = current_config

    mw.addonManager.writeConfig(__name__, {
        'settings': new_config,
    })

def rename_setting(col, old_name: str, new_name: str) -> None:
    all_config = mw.addonManager.getConfig(__name__)

    current_config = safenav(
        [all_config],
        ['settings', str(col.crt)],
        default=[],
    )

    found = filter(
        lambda v: safenav([v], [1, 'deckConfName'], default='') == old_name,
        enumerate(current_config),
    )

    try:
        conf_for_rename = next(found)
        current_config[conf_for_rename[0]]['deckConfName'] = new_name

    except StopIteration as e:
        pass

    new_config = safenav([all_config], ['settings'], default={})
    new_config[str(col.crt)] = current_config

    mw.addonManager.writeConfig(__name__, {
        'settings': new_config,
    })

def remove_setting(col, conf_name: str) -> None:
    all_config = mw.addonManager.getConfig(__name__)

    current_config = safenav(
        [all_config],
        ['settings', str(col.crt)],
        default=[],
    )

    found = filter(
        lambda v: safenav([v], [1, 'deckConfName'], default='') == conf_name,
        enumerate(current_config),
    )

    try:
        conf_for_deletion = next(found)
        del current_config[conf_for_deletion[0]]

    except StopIteration as e:
        pass

    new_config = safenav([all_config], ['settings'], default={})
    new_config[str(col.crt)] = current_config

    mw.addonManager.writeConfig(__name__, {
        'settings': new_config,
    })
