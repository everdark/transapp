#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import urllib2
from bs4 import BeautifulSoup
import bencode
import hashlib
import base64
import urllib


# construct command line argument parser
def getCommandLineParser():
    parser = argparse.ArgumentParser(description=
            "Crawl given bango (over nyaa) and return available magnet link.")
    parser.add_argument("bango", metavar='bango', type=str, nargs=1, 
                        help="the bango wanted.")
    parser.add_argument("-a", "--auto", action="store_true", 
                        help="automatically return the magnet according to maximum dls")
    parser.add_argument("-n", "--nitem", metavar='N', type=int, action="store", default=10,
                        help="maximum number of items listed, default at 10; ignored if -a is used")
    return parser

def getUserInput(maxn=10):
    while True:
        try:
            chosen = int(raw_input("Enter the wanted number:"))
        except ValueError:
            print("Incorrect answer input!")
            continue
        else:
            if 0 <= chosen < maxn: 
                break
            else:
                print("Entering number out of range!")
                continue
    return chosen

# define main function
def main():
    parser = getCommandLineParser()
    args = parser.parse_args()
    site = "http://sukebei.nyaa.se/"
    pagelink = urllib2.urlopen("%s?page=search&cats=0_0&filter=0&term=%s" % (site, args.bango))
    
    # parse nyaa page
    soup = BeautifulSoup(pagelink, "lxml") # explicitly require lxml
    tlist = soup.findAll("tr", {"class": "tlistrow"})

    if not len(tlist):
        print("No mathcing result.")
        return None

    if args.auto:
        # take the one with maximum downloads
        dls = [ int(t.find("td", {"class": "tlistdn"}).text) for t in tlist ]
        chosen = dls.index(max(dls))
        target = tlist[chosen]
        name = target.find("td", {"class": "tlistname"}).text.encode("utf-8")
        link = target.find("td", {"class": "tlistdownload"}).find('a').get("href")
    else:
        # list top 10 and wait for user interact
        titles = []
        links = []
        for t in tlist[:args.nitem]:
            titles.append(t.find("td", {"class": "tlistname"}).text.encode("utf-8"))
            links.append(t.find("td", {"class": "tlistdownload"}).find('a').get("href"))
        for i, t in enumerate(titles):
            print i, t
        chosen = getUserInput(maxn=args.nitem)
        name = titles[chosen]
        link = links[chosen]

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
    main()
