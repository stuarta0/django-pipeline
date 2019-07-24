

import mimetypes
import posixpath

try:
    from urllib.parse import quote
except ImportError:
    from urllib.parse import quote

from django.utils.encoding import smart_str
from django.utils.module_loading import import_string

from pipeline.conf import settings


def to_class(class_str):
    if not class_str:
        return None
    
    return import_string(class_str)


def filepath_to_uri(path):
    if path is None:
        return path
    return quote(smart_str(path).replace("\\", "/"), safe="/~!*()'#?")


def guess_type(path, default=None):
    for type, ext in settings.PIPELINE_MIMETYPES:
        mimetypes.add_type(type, ext)
    mimetype, _ = mimetypes.guess_type(path)
    if not mimetype:
        return default
    return smart_str(mimetype)


def relpath(path, start=posixpath.curdir):
    """Return a relative version of a path"""
    if not path:
        raise ValueError("no path specified")

    start_list = posixpath.abspath(start).split(posixpath.sep)
    path_list = posixpath.abspath(path).split(posixpath.sep)

    # Work out how much of the filepath is shared by start and path.
    i = len(posixpath.commonprefix([start_list, path_list]))

    rel_list = [posixpath.pardir] * (len(start_list) - i) + path_list[i:]
    if not rel_list:
        return posixpath.curdir
    return posixpath.join(*rel_list)
