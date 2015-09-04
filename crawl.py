#!/usr/bin/env python

import sqlite3
import inspect
import re

import transapp
import siteparser

def main():
    # get all parser classes
    all_parsers = dict([ c for c in inspect.getmembers(siteparser, inspect.isclass) 
                    if re.match("^.*Parser$", c[0]) and c[1].__module__ == "siteparser" ])
    all_parsers.pop("anyParser", None)

    # scan watchlist and do possible update
    dbname = "watchlist.db"
    conn = sqlite3.connect(dbname)
    cursor = conn.execute("select * from watchlist;")
    for row in cursor:
        kw, p, ts, d, magnet, submitted = row
        p = p + "Parser"
        parser = all_parsers[p](kw)
        res = transapp.autoSelectMagnet(parser.getTorrentInfo())
        if res is not None:
            magnet = parser.resolveLink(res[1])
            conn.execute("""update watchlist set magnet = "%s" where keyword = "%s";""" % (magnet, kw))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
