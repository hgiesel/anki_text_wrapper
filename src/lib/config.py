import json
import os.path as path

from dataclasses import asdict
from typing import Union, Optional, List

from aqt import mw

from .utils import safenav, safenav_preset

from .config_types import (
    TWSetting,

    TWWrap, TWTagWrap, TWTextWrap, TWMetaWrap,

    TWCollectiveButton, TWExtraButton, TWContextMenu,
)

from .interface_settings import (
    make_setting,
)

from .interface_wrappers import (
    make_tag_wrap,
    make_text_wrap,
    make_meta_wrap,
)

from .registrar import has_interface, get_meta_wraps, meta_wrap_is_registered

SCRIPTNAME = path.dirname(path.realpath(__file__))

with open(path.join(SCRIPTNAME, '../../config.json'), encoding='utf-8') as config:
    config_default = json.load(config)

    SETTINGS_DEFAULT = config_default['settings']['1']
    default = SETTINGS_DEFAULT

    safenav_setting = safenav_preset(default[0])
    safenav_extra_button = safenav_preset(default[0]['extra_button'])
    safenav_collective_button = safenav_preset(default[0]['collective_button'])
    safenav_context_menu = safenav_preset(default[0]['context_menu'])
    safenav_tag_wrap = safenav_preset(default[0]['wrap'])
    safenav_text_wrap = safenav_preset(default[1]['wrap'])
    safenav_meta_wrap = safenav_preset(default[2]['wrap'])

############################################################
# SERIALIZATION

def serialize_setting(setting: TWSetting) -> dict:
    return {
        'name': setting.name,
        'description': setting.description,
        'enabled': setting.enabled,
        'collective_button': serialize_collective_button(setting.collectiveButton),
        'extra_button': serialize_extra_button(setting.extraButton),
        'context_menu': serialize_extra_button(setting.contextMenu),
        'wrap': serialize_wrap(setting.wrap),
    }

def serialize_collective_button(cbutton: TWCollectiveButton) -> dict:
    return {
        'enabled': cbutton.enabled,
        'text': cbutton.text,
    }

def serialize_extra_button(ebutton: TWExtraButton) -> dict:
    return {
        'enabled': ebutton.enabled,
        'text': ebutton.text,
        'tooltip': ebutton.tooltip,
    }

def serialize_context_menu(cmenu: TWContextMenu) -> dict:
    return {
        'enabled': cmenu.enabled,
        'text': cmenu.text,
    }

def serialize_wrap(wrap: TWWrap) -> dict:
    if type(wrap) == TWTagWrap:
        return serialize_tag_wrap(wrap)
    elif type(wrap) == TWTextWrap:
        return serialize_text_wrap(wrap)
    elif type(wrap) == TWMetaWrap:
        return serialize_meta_wrap(wrap)

def serialize_tag_wrap(wrap: TWTagWrap) -> dict:
    return {
        'tagname': wrap.tagname,
        'classname': wrap.classname,
        'attributes': wrap.attributes,
        'stylings': wrap.stylings,
    }

def serialize_text_wrap(wrap: TWTextWrap) -> dict:
    return {
        'prefix': wrap.prefix,
        'suffix': wrap.suffix,
        'infix': wrap.infix,
        'infix_regex': wrap.infixRegex,
    }

def serialize_meta_wrap(wrap: TWMetaWrap) -> dict:
    return {
        'tag': wrap.tag,
        'id': wrap.id,
        'storage': wrap.storage,
    }

############################################################
# DESERIALIZATION

def deserialize_setting(setting_data, access_func = safenav_setting) -> TWSetting:
    return setting_data if type(setting_data) == TWSetting else TWSetting(
        access_func([setting_data], ['name']),
        access_func([setting_data], ['description']),
        access_func([setting_data], ['enabled']),
        deserialize_collective_button(access_func([setting_data], ['collective_button'])),
        deserialize_extra_button(access_func([setting_data], ['extra_button'])),
        deserialize_context_menu(access_func([setting_data], ['context_menu'])),
        deserialize_wrap(access_func([setting_data], ['wrap'])),
    )

def deserialize_collective_button(cbutton: dict, access_func = safenav_collective_button) -> TWCollectiveButton:
    return cbutton if type(cbutton) == TWCollectiveButton else TWCollectiveButton(
        access_func([cbutton], ['enabled']),
        access_func([cbutton], ['text']),
    )

def deserialize_extra_button(ebutton: dict, access_func = safenav_extra_button) -> TWExtraButton:
    return ebutton if type(ebutton) == TWExtraButton else TWExtraButton(
        access_func([ebutton], ['enabled']),
        access_func([ebutton], ['text']),
        access_func([ebutton], ['tooltip']),
    )

def deserialize_context_menu(cmenu: dict, access_func = safenav_context_menu) -> TWContextMenu:
    return cmenu if type(cmenu) == TWContextMenu else TWContextMenu(
        access_func([cmenu], ['enabled']),
        access_func([cmenu], ['text']),
    )

def deserialize_wrap(wrap: dict) -> TWWrap:
    if type(wrap) in [TWTextWrap, TWTagWrap, TWMetaWrap]:
        return wrap

    if 'tagname' in wrap:
        return deserialize_tag_wrap(wrap)
    elif 'prefix' in wrap:
        return deserialize_text_wrap(wrap)
    elif 'id' in wrap:
        return deserialize_meta_wrap(wrap)
    else:
        return # TODO

def deserialize_tag_wrap(wrap: dict, access_func = safenav_tag_wrap) -> TWTagWrap:
    return wrap if type(wrap) == TWTagWrap else TWTagWrap(
        access_func([wrap], ['tagname']),
        access_func([wrap], ['classname']),
        access_func([wrap], ['attributes']),
        access_func([wrap], ['stylings']),
    )

def deserialize_text_wrap(wrap: dict, access_func = safenav_text_wrap) -> TWTextWrap:
    return wrap if type(wrap) == TWTextWrap else TWTextWrap(
        access_func([wrap], ['prefix']),
        access_func([wrap], ['suffix']),
        access_func([wrap], ['infix']),
        access_func([wrap], ['infix_regex']),
    )

def deserialize_meta_wrap(wrap: dict, access_func = safenav_meta_wrap) -> TWMetaWrap:
    return wrap if type(wrap) == TWTextWrap else TWTextWrap(
        access_func([wrap], ['tag']),
        access_func([wrap], ['id']),
        access_func([wrap], ['storage']),
    )

def get_setting(col) -> Optional[TWSetting]:
    all_config = mw.addonManager.getConfig(__name__)
    setting = safenav(
        [all_config],
        ['settings', str(col.crt)],
        default=[],
    )

    return deserialize_setting(
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
