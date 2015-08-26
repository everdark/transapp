#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import urllib2
from bs4 import BeautifulSoup
import bencode
import hashlib
import base64

import transapp
import siteparser

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
    parser = siteparser.nyaaParser(args.bango)
    tlist = parser.getTorrentInfo()

    if not len(tlist):
        print("No mathcing result.")
        return None

    if args.auto:
        # take the one with maximum downloads
        dls = [ t[2] for t in tlist ]
        target = tlist[dls.index(max(dls))]
        name, link = target[:2] 
    else:
        # list top 10 and wait for user interact
        for i, t in enumerate(tlist[:args.nitem]):
            print i, t[0]
        chosen = getUserInput(maxn=args.nitem)
        name, link = tlist[chosen][:2]

    print("File targeted: %s" % name)

    # download the chosen torrent
    magnet = transapp.extractMagnet(link)
    print magnet


if __name__ == "__main__":
    main()
