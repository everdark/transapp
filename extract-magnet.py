#!/usr/bin/env python


import sys
import bencode
import hashlib
import base64
import urllib

def main():
    torrent = open(sys.argv[1]).read()
    meta = bencode.bdecode(torrent)
    b32hash = base64.b32encode(hashlib.sha1(bencode.bencode(meta["info"])).digest())
    params =[
        ("xt", "urn:btih:%s" % b32hash),
        ("dn", meta["info"].get("name")),
        ("tr", meta.get("announce")),
        ("xl", meta["info"].get("length"))
        ]
    magnet = "magnet:?%s" % urllib.urlencode([(k, v) for k, v in params if v is not None])
    print magnet.replace("urn%3Abtih%3A", "urn:btih:")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: python %s torrent-file" % sys.argv[0]
        sys.exit(1)
    else:
        main()
