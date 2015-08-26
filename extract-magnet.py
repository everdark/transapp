#!/usr/bin/env python

import sys

import transapp

def main():
    magnet = transapp.extractMagnet(sys.argv[1], isLink=False)
    print magnet

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: python %s torrent-file" % sys.argv[0]
        sys.exit(1)
    else:
        main()
