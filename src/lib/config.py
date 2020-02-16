import json
import os.path as path

from dataclasses import asdict
from typing import Union, Optional, List

from aqt import mw

from .utils import safenav, safenav_preset

from .types import (
    TWSetting,
    TWWrap,
    TWHTMLTagWrap,
    TWHTMLClassWrap,
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

# initialize default type
SCRIPTNAME = path.dirname(path.realpath(__file__))

with open(path.join(SCRIPTNAME, '../../config.json'), encoding='utf-8') as config:
    config_default = json.load(config)

    SETTINGS_DEFAULT = config_default['settings'][0]
    model_default = SETTINGS_DEFAULT

    safenav_setting = safenav_preset(model_default)
    safenav_concr_script = safenav_preset(model_default['scripts'][0])
    safenav_meta_script = safenav_preset(model_default['scripts'][1])

def deserialize_setting(model_setting, access_func = safenav_setting) -> TWSetting:
    return model_setting if isinstance(model_setting, TWSetting) else make_setting(
        access_func([model_setting], ['name']),
        access_func([model_setting], ['description']),
        access_func([model_setting], ['enabled']),
        deserialize_collective_button(access_func([model_setting], ['collectiveButton'])),
        deserialize_extra_button(access_func([model_setting], ['collectiveButton'])),
        deserialize_context_menu(access_func([model_setting], ['contextMenu'])),
        deserialize_wrap(access_func([model_setting], ['wrap'])),
    )

def add_other_metas(model_name, scripts: List[SMScript]) -> List[SMScript]:
    meta_scripts = get_meta_wraps(model_name)

    for ms in meta_scripts:
        try:
            found = next(filter(lambda v: isinstance(v, SMMetaScript) and v.tag == ms.tag and v.id == ms.id, scripts))
        except StopIteration:
            scripts.append(make_meta_script(
                ms.tag,
                ms.id,
            ))

    return scripts

def deserialize_wrap(
    model_name,
    script_data,
) -> Union[TWHTMLTagWrap, TWHTMLClassWrap, TWTextWrap, TWMetaWrap]:
    return script_data if isinstance(script_data, SMScript) else (
        deserialize_concr_script(script_data)
        if 'name' in script_data
        else deserialize_meta_script(model_name, script_data)
    )

def deserialize_html_tag_wrap(
    wrap_data,
    access_func = safenav_concr_script,
) -> TWHTMLTagWrap:
    result = wrap_data if isinstance(wrap_data, TWHTMLTagWrap) else make_html_tag_wrap(
        access_func([wrap_data], ['tagname']),
        access_func([wrap_data], ['attributes']),
    )

    return result

def deserialize_html_class_wrap(
    wrap_data,
    access_func = safenav_concr_script,
) -> TWHTMLClassWrap:
    result = wrap_data if isinstance(wrap_data, TWHTMLClassWrap) else make_html_class_wrap(
        access_func([wrap_data], ['classname']),
        access_func([wrap_data], ['stylings']),
    )
    return result

def deserialize_text_wrap(
    wrap_data,
    access_func = safenav_concr_script,
) -> TWTextWrap:
    result = wrap_data if isinstance(wrap_data, TWTextWrap) else make_text_wrap(
        access_func([wrap_data], ['prefix']),
        access_func([wrap_data], ['suffix']),
    )
    return result

def deserialize_meta_wrap(
    wrap_data,
    access_func = safenav_concr_script,
) -> TWMetaWrap:
    result = wrap_data if isinstance(wrap_data, TWMetaWrap) else make_meta_wrap(
        access_func([wrap_data], ['tag']),
        access_func([wrap_data], ['id']),
        make_wrap_storage(**access_func([wrap_data], ['storage'], default = {})),
    )

    return result if has_interface(result.tag) and meta_wrap_is_registered(
        result.tag,
        result.id,
    ) else None

def serialize_setting(setting: TWSetting) -> dict:
    return {
        'name': 'f',
        'enabled': setting.enabled,
        'insertStub': setting.insert_stub,
        'indentSize': setting.indent_size,
        'scripts': [serialize_script(script) for script in setting.scripts],
    }

def serialize_script(script: Union[SMConcrScript, SMMetaScript]) -> dict:
    if isinstance(script, SMConcrScript):
        return asdict(script)
    else:
        preresult = asdict(script)

        return {
            'tag': preresult['tag'],
            'id': preresult['id'],
            'storage': {
                k: v for k, v in preresult['storage'].items() if v is not None
            }
        }

def deserialize_setting_with_default(model_name, settings):
    found = filter(lambda v: v['modelName'] == model_name, settings)

    try:
        model_deserialized = deserialize_setting(model_name, next(found))

    except StopIteration:
        model_deserialized = deserialize_setting(model_name, model_default)

    return model_deserialized

def get_settings():
    config = mw.addonManager.getConfig(__name__)

    def get_setting(model_name):
        return filter(lambda v: v['modelName'] == model_name, safenav([config], ['settings'], default=None))

    model_settings = []

    for model in mw.col.models.models.values():
        model_name = model['name']
        model_deserialized = deserialize_setting_with_default(model_name, get_setting(model_name))

        model_settings.append(model_deserialized)

    return model_settings

def write_settings(serializedSettings):
    mw.addonManager.writeConfig(__name__, {
        'settings': serializedSettings,
    })
