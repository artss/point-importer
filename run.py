#!/usr/bin/env python

import settings

import sys
try:
    sys.path.extend(settings.libs)
except AttributeError:
    pass

from point.core.user import User
from importers.juick import Juick
from point.util import cache_get, cache_store

importer_types = {
    "juick": Juick
}

try:
    login, itype, path = sys.argv[1:4]
except (IndexError, ValueError):
    sys.stderr.write("Usage: %s <login> <type> <path>\n" % sys.argv[0])
    exit(1)

try:
    imp = importer_types[itype](User("login", login), path)
except KeyError:
    sys.stderr.write("%s: invalid source type\n" % itype)
    exit(1)

for ext_id, post, comments in imp.posts():
    post.archive, post.author, post.text, post.tags
    key = "imported:%s:%s:%s" % (itype, login.lower(), ext_id)
    print key
    if cache_get(key):
        continue
    post.save()
    for comment in comments:
        comment.save()
    cache_store(key, 1, settings.ids_cache_expire)

