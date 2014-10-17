import os
import shutil
import json
import dateutil.parser as dparser
#from xml.sax.saxutils import unescape
from importers.importer import Importer
from point.core.user import AnonymousUser
from point.core.post import Post, Comment

import settings

def unescape(s):
    return s.replace("&quot;", '"')

class Juick(Importer):
    def __init__(self, user, path):
        self.user = user
        self.path = path

    def posts(self):
        with open(os.path.join(self.path, "posts.json")) as fd:
            plist = json.load(fd)

        for post in plist:
            p = self._post(post[0])
            yield post[0]["mid"], p, self._comments(p, post[1:])

    def _post(self, p):
        if "photo" in p and p["photo"]:
            img = os.path.basename(p["photo"]["medium"])
            try:
                shutil.copy(os.path.join(self.path, "juick-images", img),
                            settings.media_path)
                imgurl = os.path.join(settings.media_root, img)
                text = "%s\n\nhttp%s" % (unescape(p["body"]), imgurl)
            except IOError:
                text = unescape(p["body"])
        else:
            text = unescape(p["body"])

        try:
            private = bool(str(p["friends"]) == "1")
        except KeyError:
            private = False

        tags = p["tags"] if "tags" in p else []

        return Post.from_data(None, author=self.user, text=text, tags=tags,
                              created=dparser.parse(p["timestamp"]),
                              type='post', archive=True, private=private)

    def _comments(self, post, clist):
        comments = []
        for c in clist:
            if "photo" in c and c["photo"]:
                img = os.path.basename(c["photo"]["medium"])
                try:
                    shutil.copy(os.path.join(self.path, "juick-images", img),
                                settings.media_path)
                    imgurl = os.path.join(settings.media_root, img)
                    text = "%s\n\n%s" % (unescape(c["body"]), imgurl)
                except IOError:
                    text = unescape(c["body"])
            else:
                text = unescape(c["body"])

            try:
                to = c["replyto"]
            except KeyError:
                to = None

            comments.append(
                Comment.from_data(post=post, id=c["rid"], to_comment_id=to,
                    author=AnonymousUser(c["user"]["uname"]),
                    created=dparser.parse(c["timestamp"]),
                    text=text, archive=True)
            )

        return comments

