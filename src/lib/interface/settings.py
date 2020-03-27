from typing import Dict, Optional

from ..config_types import (
    TWWrap,
    TWSetting, TWCollectiveButton, TWExtraButton, TWContextMenu,

    TWWrapStorage,
    TWSettingStorage, TWCollectiveButtonStorage, TWExtraButtonStorage, TWContextMenuStorage,

    TWWrapBool,
    TWSettingBool, TWCollectiveButtonBool, TWExtraButtonBool, TWContextMenuBool,
)

''' General Settings '''

def make_setting(
    name: str,
    description: str,
    enabled: bool,
    collective_button: TWCollectiveButton,
    extra_button: TWExtraButton,
    context_menu: TWContextMenu,
    wrap: TWWrap,
) -> TWSetting:
    return TWSetting(
        name,
        description,
        enabled,
        collective_button,
        extra_button,
        context_menu,
        wrap,
    )

def make_collective_button(
    text: str,
) -> TWCollectiveButton:
    return TWCollectiveButton(
        text,
    )

def make_extra_button(
    text: str,
    tooltip: str,
) -> TWExtraButton:
    return TWExtraButton(
        text,
        tooltip,
    )

def make_context_menu(
    text: str,
) -> TWExtraButton:
    return TWExtraButton(
        text,
    )

''' General Settings Storage '''

def make_setting_storage(
    name: Optional[str],
    description: Optional[str],
    enabled: Optional[bool],
    collective_button: Optional[TWCollectiveButtonStorage],
    extra_button: Optional[TWExtraButtonStorage],
    context_menu: Optional[TWContextMenuStorage],
    wrap: TWWrapStorage,
) -> TWSettingStorage:
    return TWSetting(
        name,
        description,
        enabled,
        collective_button,
        extra_button,
        context_menu,
        wrap,
    )

def make_collective_button_storage(
    text: Optional[str],
) -> TWCollectiveButton:
    return TWCollectiveButton(
        text,
    )

def make_extra_button_storage(
    text: Optional[str],
    tooltip: Optional[str],
) -> TWExtraButton:
    return TWExtraButton(
        text,
        tooltip,
    )

def make_context_menu_storage(
    text: Optional[str],
) -> TWExtraButton:
    return TWExtraButton(
        text,
    )

''' General Settings Bool '''

def make_setting_bool(
    name: bool = None,
    description: bool = None,
    enabled: bool = None,
    collective_button: Optional[TWCollectiveButtonBool] = None,
    extra_button: Optional[TWExtraButtonBool] = None,
    context_menu: Optional[TWContextMenuBool] = None,
    wrap: TWWrapBool = None,
) -> TWSettingBool:
    return TWSetting(
        name if name is not None else False,
        description if description is not None else False,
        enabled if enabled is not None else False,
        collective_button if collective_button is not None else make_collective_button_bool(),
        extra_button if extra_button is not None else make_extra_button_bool(),
        context_menu if context_menu is not None else make_context_menu_bool(),
        wrap if wrap is not None else False,
    )

def make_collective_button_bool(
    text: bool = None,
) -> TWCollectiveButtonBool:
    return TWCollectiveButton(
        text if text is not None else False,
    )

def make_extra_button_bool(
    text: bool = None,
    tooltip: bool = None,
) -> TWExtraButtonBool:
    return TWExtraButtonBool(
        text if text is not None else False,
        tooltip if tooltip is not None else False,
    )

def make_context_menu_bool(
    text: bool = None,
) -> TWExtraButtonBool:
    return TWExtraButtonBool(
        text if text is not None else False,
    )
