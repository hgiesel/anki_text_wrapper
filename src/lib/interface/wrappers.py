from typing import Optional, Dict

from ..types import (
    TWWrap,
    TWHTMLTagWrap, TWHTMLClassWrap, TWTextWrap, TWMetaWrap,

    TWWrapBool,
    TWHTMLTagWrapBool, TWHTMLClassWrapBool, TWTextWrapBool, TWMetaWrapBool,

    TWWrapStorage,
    TWHTMLTagWrapStorage, TWHTMLClassWrapStorage, TWTextWrapStorage, TWMetaWrapStorage,
)

''' Wrappers Bool '''

def make_html_tag_wrap_bool(
    tagname: Optional[bool] = None,
    attributes: Optional[bool] = None,
) -> TWHTMLTagWrapBool:
    return TWHTMLTagWrapBool(
        tagname if tagname is not None else False,
        attributes if attributes is not None else False,
    )

def make_html_class_wrap_bool(
    classname: Optional[bool] = None,
    styling: Optional[bool] = None,
) -> TWHTMLClassWrapBool:
    return TWHTMLClassWrapBool(
        classname,
        styling,
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

def make_html_tag_wrap_storage(
    tagname: Optional[str] = None,
    attributes: Optional[Dict[str, str]] = None,
) -> TWHTMLTagWrapStorage:
    return TWHTMLTagWrapStorage(
        tagname,
        attributes
    )

def make_html_class_wrap_storage(
    classname: Optional[str],
    styling: Optional[Dict[str, str]],
) -> TWHTMLClassWrapStorage:
    return TWHTMLClassWrapStorage(
        classname,
        styling,
    )

def make_text_wrap_storage(
    prefix: Optional[str],
    suffix: Optional[str],
) -> TWTextWrapStorage:
    return TWTextWrapStorage(
        prefix,
        suffix,
    )

''' Wrappers '''

def make_html_tag_wrap(
    tagname: str,
    attributes: Dict[str, str],
) -> TWHTMLTagWrap:
    return TWHTMLTagWrap(
        tagname,
        attributes
    )

def make_html_class_wrap(
    classname: str,
    styling: Dict[str, str]
) -> TWHTMLClassWrap:
    return TWHTMLClassWrap(
        classname,
        styling,
    )

def make_text_wrap(
    prefix: str,
    suffix: str,
) -> TWTextWrap:
    return TWTextWrap(
        prefix,
        suffix,
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
