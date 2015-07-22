#!/usr/bin/env python



import sys
import urllib2
from bs4 import BeautifulSoup
import bencode
import hashlib
import base64
import urllib


def main():
    keyword = sys.argv[1]
    pagelink = urllib2.urlopen("http://sukebei.nyaa.se/?page=search&cats=0_0&filter=0&term=%s" % keyword)
    
    # parse nyaa page
    soup = BeautifulSoup(pagelink, "lxml")
    tlist = soup.findAll("tr", {"class": "tlistrow"})
    if not len(tlist):
        print("No mathcing result.")
        return None
    dls = [ int(t.find("td", {"class": "tlistdn"}).text) for t in tlist ]
    chosen = dls.index(max(dls)) # take the one with maximum downloads
    target = tlist[chosen]
    name = target.find("td", {"class": "tlistname"}).text
    link = target.find("td", {"class": "tlistdownload"}).find('a').get("href")
    print("File targeted: %s" % name)

    # download the chosen torrent
    torrent = urllib2.urlopen(link).read()
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
        print("Usage: %s keyword" % sys.argv[0])
        exit(1)
    else:
        main()
