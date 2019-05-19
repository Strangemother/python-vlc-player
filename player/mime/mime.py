
import json
import os

cur_dir = os.path.dirname(__file__)
with open(os.path.join(cur_dir, './mimes.json')) as stream:
    mimes = json.load(stream)

with open(os.path.join(cur_dir, './exts.json')) as stream:
    exts = json.load(stream)


def get_ext(mime):
    return mimes.get(mime, None)

def get_mime(ext):
    if ext[0] == '.':
        return exts.get(ext[1:], None)
    return exts.get(ext, None)

def extract(filepath):
    name, ext = os.path.splitext(filepath)
    mime = get_mime(ext)
    res = {
        'ext': get_ext(mime),
        'mime': mime
    }

    return res
