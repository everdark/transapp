#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import inspect
import textwrap

import siteparser

def getAllParserClass():
    all_parsers = [ c for c in inspect.getmembers(siteparser, inspect.isclass) 
                    if c[1].__module__ == "siteparser" ]
    return all_parsers

def getCommandLineParser():
    plist = [ '\t'.join([p[0].replace("Parser", ''), p[1].site]) for p in getAllParserClass() ]
    plist_excludeSuper = [ p for p in plist if "any" not in p ]
    src_help = '''\
           source site to parse (default at \"nyaa\")
           partial matching is allowed
           available SRC includes:
           -----------------------
           '''
    parser = argparse.ArgumentParser(
            description="Crawl given keyword and return available magnet link.",
            formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("keyword", metavar='keyword', type=str, nargs=1, 
                        help="the keyword wanted.")
    parser.add_argument("-a", "--auto", action="store_true", 
                        help="automatically return the magnet link according to maximum dls")
    parser.add_argument("-n", "--nitem", metavar='N', type=int, action="store", default=10,
                        help="maximum number of items listed (default at 10); ignored if -a is used")
    parser.add_argument("-s", "--src", metavar="SRC", type=str, action="store", default="nyaa",
                        help=''.join([textwrap.dedent(src_help), '\n'.join(plist_excludeSuper)]))
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

def main():
    # get command line arguments
    parser = getCommandLineParser()
    args = parser.parse_args()

    # determine and utilize selected site parser class
    all_parsers = dict([ (p[0].replace("Parser", ''), p[1]) for p in getAllParserClass() ])
    all_parsers.pop("any", None)
    check_src = dict([ (p, args.src in p) for p in all_parsers.keys() ])
    np = sum(check_src.values())

    if np == 0:
        print("Source type \"%s\" not found. Program aborted." % args.src)
        return None
    elif np > 1:
        print("Source type ambiguous. Please re-specify in more accuracy.")
        return None

    selected_parser = [ k for k, v in check_src.items() if v == True][0]
    parser = all_parsers[selected_parser](args.keyword)

    tlist = parser.getTorrentInfo()
    if isinstance(tlist, Exception):
        print(str(tlist))
        return None
    if not len(tlist):
        print("No matching result.")
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

    # resolve the magnet link from selected torrent
    magnet = parser.resolveLink(link)
    print magnet


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "\nCanceled."
