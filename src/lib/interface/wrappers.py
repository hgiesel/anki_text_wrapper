from typing import Optional, Dict

from ..config_types import (
    TWWrap,
    TWTagWrap, TWTextWrap, TWMetaWrap,

    TWWrapBool,
    TWTagWrapBool, TWTextWrapBool, TWMetaWrapBool,

    TWWrapStorage,
    TWTagWrapStorage, TWTextWrapStorage, TWMetaWrapStorage,
)

''' Wrappers Bool '''

def make_tag_wrap_bool(
    tagname: Optional[bool] = None,
    classname: Optional[bool] = None,
    attributes: Optional[bool] = None,
    stylings: Optional[bool] = None,
) -> TWTagWrapBool:
    return TWTagWrapBool(
        classname if classname is not None else False,
        tagname if tagname is not None else False,
        attributes if attributes is not None else False,
        stylings if stylings is not None else False,
    )

def make_text_wrap_bool(
    prefix: Optional[bool] = None,
    suffix: Optional[bool] = None,
) -> TWTextWrapBool:
    return TWTextWrapBool(
        prefix,
        suffix,
    )

''' Wrappers Storage '''

def make_tag_wrap_storage(
    tagname: Optional[str] = None,
    classname: Optional[str] = None,
    attributes: Optional[Dict[str, str]] = None,
    stylings: Optional[Dict[str, str]] = None,
) -> TWTagWrapStorage:
    return TWTagWrapStorage(
        tagname,
        classname,
        attributes,
        stylings,
    )

def make_text_wrap_storage(
    prefix: Optional[str],
    suffix: Optional[str],
    infix: Optional[str],
    infixRegex: Optional[str],
) -> TWTextWrapStorage:
    return TWTextWrapStorage(
        prefix,
        suffix,
        infix,
        infixRegex,
    )

''' Wrappers '''

def make_tag_wrap(
    tagname: str,
    classname: str,
    attributes: Dict[str, str],
    stylings: Dict[str, str],
) -> TWTagWrap:
    return TWTagWrap(
        tagname,
        classname,
        attributes,
        stylings,
    )

def make_text_wrap(
    prefix: str,
    suffix: str,
    infix: str,
    infixRegex: str,
) -> TWTextWrap:
    return TWTextWrap(
        prefix,
        suffix,
        infix,
        infixRegex,
    )

def make_meta_wrap(
    tag: str,
    id: str,
    storage: Optional[TWWrapStorage],
) -> TWMetaWrap:
    return TWMetaWrap(
        tag,
        id,
        storage,
    )
