from pprint import pprint as pp

# Accepted list of mime types extracted from the VLC source
known = set()

with open('assets/mime.txt') as stream:
    for line in stream:
        known.add(line.strip())

# A big list of mime/ext sourced from the interweb
# https://gist.github.com/mahizsas/5999837
# https://gist.github.com/electerious/3d5a31a73cfd6423f835c074ab25fc06
# https://www.sitepoint.com/mime-types-complete-list/
# https://www.freeformatter.com/mime-types-list.html
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Complete_list_of_MIME_types
# https://github.com/ranger/ranger/blob/master/ranger/data/mime.types
# https://wiki.xiph.org/index.php?title=MIME_Types_and_File_Extensions&mobileaction=toggle_view_desktop#Codec_MIME_types
assoc = set()
with open('assets/ext-assoc.txt') as stream:
    for line in stream:
        assoc.add(line.strip())

# Cross reference of the known mime/ext and the VLC accepted list.
found = set()

for ext_item in assoc:
    kept = False

    for accepted in known:
        if ext_item.startswith(accepted):
            exts_str = ext_item[len(accepted):]
            exts = tuple(ext.strip() for ext in exts_str.split())

            found.add((accepted, exts, ))
            kept = True

# a clean list of all accepted mimes
kept = set([x[0] for x in found])

# all dropped mime types.
lost = known - kept

mimes = {}

for key, exts in found:
    loc = mimes.get(key, set())
    loc = set(loc).union(set(exts))
    mimes[key] = tuple(loc)

exts = {}

for mtype, items in mimes.items():
    for ext in items:
        exts[ext] = mtype

import json

with open('exts.json', 'w') as stream:
    json.dump(exts, stream, indent=4)

with open('mimes.json', 'w') as stream:
    json.dump(mimes, stream, indent=4)

print('known:', len(known))
print('found:', len(found))
print('lost:', len(lost))
print('assoc:', len(assoc))
print('exts:', len(exts))
print('mimes:', len(mimes))

print(lost)
