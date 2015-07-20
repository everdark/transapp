#!/usr/bin/env python



import sys
import ConfigParser
import urllib2
from bs4 import BeautifulSoup
import bencode
import hashlib
import base64
import urllib


def main():
    goodwords = config.get("movie_crawler", "good_word").split(',')
    badwords = config.get("movie_crawler", "bad_word").split(',')
    keyword = sys.argv[1].replace(' ', '+')
    pagelink = urllib2.urlopen("http://www.1337x.to/search/%s/1/" % keyword)
    
    # parse 1337x page
    soup = BeautifulSoup(pagelink)
    tlist = soup.findAll("ul", {"class": "clearfix"})
    if not len(tlist):
        print("No mathcing result.")
        return None
    title_list = tlist[1].findAll("div", {"class": "coll-1"})
    title_links = [ title.find('strong').find('a').get("href") for title in title_list ]
    titles = [ t.split('/')[3].lower() for t in title_links ]

    # filter and select
    badcnt = 0
    for t in titles:
        print t
        for bw in badwords:
            if bw in t:
                badcnt += 1
        
    print float(badcnt) / len(titles)

    # get magnet
    selected_title_link = title_links[0]
    target_link = "http://www.1337x.to" + selected_title_link
    soup_target = BeautifulSoup(urllib2.urlopen(target_link))
    magnet = soup_target.find('a', {"class": "magnet"}).get("href")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: %s keyword" % sys.argv[0])
        exit(1)
    else:
        config = ConfigParser.ConfigParser()
        if not len(config.read(['config.ini'])):
            print "No config file found. Program aborted."
            exit(1)
        main()
