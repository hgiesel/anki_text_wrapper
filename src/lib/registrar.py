from typing import Optional, List, Tuple

from .config_types import TWInterface, TWMetaWrap
from .interface import make_meta_wrap

_meta_interfaces: List[TWInterface] = []
_meta_wraps: List[Tuple[str, TWMetaWrap]] = []

class TWInterfaceIsNotRegistered(Exception):
    pass

def register_interface(iface: TWInterface) -> None:
    _meta_interfaces.append(iface)

def get_interface(tag: str) -> Optional[TWInterface]:
    try:
        return next(filter(lambda v: v.tag == tag, _meta_interfaces))
    except StopIteration:
        return None

def has_interface(tag: str) -> bool:
    return True if get_interface(tag) else False

##############

def register_meta_wrap(meta_wrap: TWMetaWrap) -> None:
    if has_interface(meta_wrap.tag):
        _meta_wraps.append(meta_wrap)
    else:
        raise TWInterfaceIsNotRegistered(
            'You tried to register a meta wrap for a non existing interface. '
            'Make sure to register the interface first.'
        )

def deregister_meta_wrap(meta_wrap: TWMetaWrap) -> bool:
    if has_interface(meta_wrap.tag):
        try:
            found = next(filter(lambda v: (
                v[1].tag == meta_wrap.tag
                and v[1].id == meta_wrap.id
            ), enumerate(_meta_wraps)))

            _meta_wraps.pop(found[0])
            return True

        except StopIteration:
            return False

    else:
        raise TWInterfaceIsNotRegistered(
            'You tried to register a meta wrap for a non existing interface. '
            'Make sure to register the interface first.'
        )

def get_meta_wraps() -> List[TWMetaWrap]:
    return [ms[1] for ms in _meta_wraps]

def meta_wrap_is_registered(tag: str, id: str) -> bool:
    try:
        return next(filter(lambda v: v[1].tag == tag and v[1].id == id, _meta_wraps))
    except StopIteration:
        return False
