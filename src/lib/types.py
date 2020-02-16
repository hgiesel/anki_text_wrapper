from typing import Dict, Union, Optional, Callable, Literal, List, Tuple
from dataclasses import dataclass, replace

Falsifiable = lambda t: Union[Literal[False], t]
WrapType = Literal['htmlTag', 'htmlClass', 'text']
LabelText = str

''' General Settings Storage '''

@dataclass(frozen=True)
class TWSettingStorage:
    name: Optional[str]
    description: Optional[str]
    enabled: Optional[bool]
    collectiveButton: Optional[TWCollectiveButtonStorage]
    extraButton: Optional[TWExtraButtonStorage]
    contextMenu: Optional[TWContextMenuStorage]
    wrap: Optional[TWWrapStorage]

@dataclass(frozen=True)
class TWCollectiveButtonStorage:
    text: Optional[str]

@dataclass(frozen=True)
class TWExtraButtonStorage:
    text: Optional[str]
    tooltip: Optional[str]

@dataclass(frozen=True)
class TWContextMenuStorage:
    text: Optional[str]

''' General Settings Bool '''

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
    text: str

@dataclass(frozen=True)
class TWExtraButtonBool:
    text: str
    tooltip: str

@dataclass(frozen=True)
class TWContextMenuBool:
    text: str

''' General Settings '''

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
    text: str

@dataclass(frozen=True)
class TWExtraButton:
    text: str
    tooltip: str

@dataclass(frozen=True)
class TWContextMenu:
    text: str

''' Wraps Storage '''

@dataclass(frozen=True)
class TWHTMLTagWrapStorage:
    tagname: Optional[str]
    attributes: Optional[Dict[str, str]]

@dataclass(frozen=True)
class TWHTMLClassWrapStorage:
    tagname: Optional[str]
    classname: Optional[str]
    writeToGlobal: Optional[bool]
    styling: Optional[Dict[str, str]]

@dataclass(frozen=True)
class TWTextWrapStorage:
    prefix: Optional[str]
    suffix: Optional[str]

TWWrapStorage = Union[
    TWHTMLTagWrapStorage,
    TWHTMLClassWrapStorage,
    TWTextWrapStorage,
]

''' Wraps Bool '''

@dataclass(frozen=True)
class TWHTMLTagWrapBool:
    tagname: bool
    attributes: bool

@dataclass(frozen=True)
class TWHTMLClassWrapBool:
    tagname: bool
    classname: bool
    writeToGlobal: bool
    styling: bool

@dataclass(frozen=True)
class TWTextWrapBool:
    prefix: bool
    suffix: bool

TWWrapBool = Union[
    TWHTMLTagWrapBool,
    TWHTMLClassWrapBool,
    TWTextWrapBool
]

'''Wraps'''

@dataclass(frozen=True)
class TWWrap:
    pass

@dataclass(frozen=True)
class TWHTMLTagWrap(TWWrap):
    tagname: str
    attributes: Dict[str, str]

@dataclass(frozen=True)
class TWHTMLClassWrap(TWWrap):
    classname: str
    styling: Dict[str, str]

@dataclass(frozen=True)
class TWTextWrap(TWWrap):
    prefix: str
    suffix: str

@dataclass(frozen=True)
class TWMetaWrap(TWWrap):
    tag: str
    id: str
    storage: TWWrapStorage

""" Interface """

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
