import json
from pprint import pprint

with open('posts.json') as fd:
    posts = json.load(fd)

#print json.dumps(posts, indent=4)

pk = {}
ck = {}

for post in posts:
    p = post[0]
    pk.update(p)
    for c in post[1:]:
        ck.update(c)

print 'pk'
pprint(pk)
print 'ck'
pprint(ck)
