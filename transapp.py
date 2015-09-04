
# define helper functions for transapp

import subprocess
import bencode
import hashlib
import base64
import urllib
import urllib2

def extractMagnet(fname, isLink=True):
    """
    Return magnet link as string from a torrent file via filesystem path or URL.
    """
    torrent = urllib2.urlopen(fname).read() if isLink else open(fname).read()
    meta = bencode.bdecode(torrent)
    b32hash = base64.b32encode(hashlib.sha1(bencode.bencode(meta["info"])).digest())
    params =[
        ("xt", "urn:btih:%s" % b32hash),
        ("dn", meta["info"].get("name")),
        ("tr", meta.get("announce")),
        ("xl", meta["info"].get("length"))
        ]
    magnet = "magnet:?%s" % urllib.urlencode([(k, v) for k, v in params if v is not None])
    return magnet.replace("urn%3Abtih%3A", "urn:btih:")

def shutdownTransmission():
    """
    Shutdown transmission daemon if all current torrents are finished downloading.
    """
    down = subprocess.call(["service", "transmission-daemon", "status"])
    if not down:
        cur_torrents = subprocess.check_output(["transmission-remote", "-l"])
        cur_torrents = [ t for t in cur_torrents.split('\n') if '%' in t ]
        pcts = [ t.split()[1] for t in cur_torrents ]
        unfinished = [ p for p in pcts if p != "100%" ]
        if not len(unfinished):
            subprocess.call(['service', 'transmission-daemon', 'stop'])
    else:
        pass


