
# define helper functions for transapp

import os, subprocess
import datetime, time
import sqlite3
import bencode, hashlib, base64
import urllib, urllib2

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
        cur_torrents = [ t for t in cur_torrents.split('\n') if '%' in t or "n/a" in t]
        pcts = [ t.split()[1] for t in cur_torrents ]
        unfinished = [ p for p in pcts if p != "100%" ]
        if not len(unfinished):
            subprocess.call(['service', 'transmission-daemon', 'stop'])
    else:
        pass

def initDBifNotExist(dbname=None):
    """
    Create watchlist database if not already existant.
    """
    if dbname is None:
        dbname = "watchlist.db"
    ts = int(time.time())
    dt = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
    if not os.path.isfile(dbname):
        print "%s not found. Initiate one." % dbname
        conn = sqlite3.connect(dbname)
        conn.execute("""
                    create table watchlist(
                    keyword TEXT,
                    parser TEXT,
                    ts INTEGER,
                    d TEXT,
                    magnet TEXT,
                    submitted BOOLEAN default 0)
                    """)
        conn.execute("""insert into watchlist values("test", "nyaa", %s, "%s", '', 0)""" % (ts, dt))
        conn.commit()
        conn.close()
    else:
        print "%s found." % dbname
        pass

def autoSelectMagnet(tlist):
    if len(tlist):
        counts = [ t.cnt for t in tlist ]
        target = tlist[counts.index(max(counts))]
        return target.fname, target.magnet
    else:
        return None


