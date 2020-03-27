from typing import Dict, Union, Optional, Callable, Literal, List, Tuple
from dataclasses import dataclass, replace

Falsifiable = lambda t: Union[Literal[False], t]
WrapType = Literal['tag', 'text']
LabelText = str

''' GENERAL Settings Storage '''

@dataclass(frozen=True)
class TWSettingStorage:
    name: Optional[str]
    description: Optional[str]
    enabled: Optional[bool]
    collective_button: Optional[TWCollectiveButtonStorage]
    extra_button: Optional[TWExtraButtonStorage]
    context_menu: Optional[TWContextMenuStorage]
    wrap: Optional[TWWrapStorage]

@dataclass(frozen=True)
class TWContextMenuStorage:
    enabled: Optional[bool]
    text: Optional[str]

@dataclass(frozen=True)
class TWExtraButtonStorage:
    enabled: Optional[bool]
    text: Optional[str]
    tooltip: Optional[str]

@dataclass(frozen=True)
class TWCollectiveButtonStorage:
    enabled: Optional[bool]
    text: Optional[str]

''' GENERAL Settings Bool '''

@dataclass(frozen=True)
class TWSettingBool:
    name: bool
    description: bool
    enabled: bool
    collectiveButton: TWCollectiveButtonBool
    extraButton: TWExtraButtonBool
    contextMenu: TWContextMenuBool
    wrap: TWWrapBool

@dataclass(frozen=True)
class TWCollectiveButtonBool:
    enabled: bool
    text: bool

@dataclass(frozen=True)
class TWExtraButtonBool:
    enabled: bool
    text: bool
    tooltip: bool

@dataclass(frozen=True)
class TWContextMenuBool:
    enabled: bool
    text: bool

''' GENERAL Settings '''

@dataclass(frozen=True)
class TWSetting:
    name: str
    description: str
    enabled: bool
    collectiveButton: TWCollectiveButton
    extraButton: TWExtraButton
    contextMenu: TWContextMenu
    wrap: TWWrap

@dataclass(frozen=True)
class TWCollectiveButton:
    enabled: bool
    text: str

@dataclass(frozen=True)
class TWExtraButton:
    enabled: bool
    text: str
    tooltip: str

@dataclass(frozen=True)
class TWContextMenu:
    enabled: bool
    text: str

''' WRAPS Storage '''

@dataclass(frozen=True)
class TWTagWrapStorage:
    tagname: Optional[str]
    classname: Optional[str]
    attributes: Optional[Dict[str, str]]
    styling: Optional[Dict[str, str]]

@dataclass(frozen=True)
class TWTextWrapStorage:
    prefix: Optional[str]
    suffix: Optional[str]

TWWrapStorage = Union[
    TWTagWrapStorage,
    TWTextWrapStorage,
]

''' WRAPS Bool '''

@dataclass(frozen=True)
class TWTagWrapBool:
    tagname: bool
    classname: bool
    attributes: bool
    styling: bool

@dataclass(frozen=True)
class TWTextWrapBool:
    prefix: bool
    suffix: bool

TWWrapBool = Union[
    TWTagWrapBool,
    TWTextWrapBool
]

'''WRAPS'''

@dataclass(frozen=True)
class TWWrap:
    pass

@dataclass(frozen=True)
class TWTagWrap(TWWrap):
    tagname: str
    classname: str
    attributes: Dict[str, str]
    styling: Dict[str, str]

@dataclass(frozen=True)
class TWTextWrap(TWWrap):
    prefix: str
    suffix: str
    infix: str
    infixRegex: str

@dataclass(frozen=True)
class TWMetaWrap(TWWrap):
    tag: str
    id: str
    storage: TWWrapStorage

""" INTERFACE """

AnkiModel = str
Fields = List[Tuple(str, str)]
Tags = List[str]
WhichField = int

@dataclass(frozen=True)
class TWInterface:
    # name for the type of the interface
    tag: str
    prototype:  WrapType
    getter: Callable[[str, TWSettingStorage], TWSetting]
    # result is used for storing
    setter: Callable[[str, TWSetting], Union[bool, TWSetting]]
    wrapper: Callable[[str, TWSettingStorage, AnkiModel, Fields, WhichField, slice, Tags], Tuple[Fields, Tags]]

    label: Falsifiable(Callable[[str, TWSettingStorage], LabelText])
    reset: Falsifiable(Callable[[str, TWSettingStorage], TWSetting])
    deletable: Falsifiable(Callable[[str, TWSettingStorage], bool])

    # list of values that are readonly
    readonly: TWSettingBool
    # list of values or stored in `storage` field
    store: TWSettingBool
