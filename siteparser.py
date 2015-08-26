"""
Every site parser, as a class, must implement the getTorrentInfo method.
It shall return information about all available torrents from the site, in tuple.
The tuple is designed and has to be (file name, download link, download counts).
The download link could be either an URL to the corresponding torrent file, 
    or the magnet link itself.
"""

import urllib
import urllib2
from bs4 import BeautifulSoup

class nyaaParser:
    """Specific parser for Nyaa"""
    
    site = "http://sukebei.nyaa.se/"

    def __init__(self, bango):
        self.bango = bango

    def getParsedPage(self):
        query_link = "%s?page=search&cats=0_0&filter=0&term=%s" % (self.site, self.bango)
        soup = BeautifulSoup(urllib2.urlopen(query_link), "lxml")
        tlist = soup.findAll("tr", {"class": "tlistrow"})
        return tlist

    def getTorrentInfo(self):
        tlist = self.getParsedPage()
        tinfo = [ (t.find("td", {"class": "tlistname"}).text.encode("utf-8"),
                   t.find("td", {"class": "tlistdownload"}).find('a').get("href"),
                   int(t.find("td", {"class": "tlistdn"}).text)) for t in tlist ]
        return tinfo

class dmhyParser:
    """"Specific parser for DMHY"""

    site = "https://share.dmhy.org/"

    def __init__(self, searchw):
        self.searchw = str(searchw)

    def getParsedPage(self):
        query_link = "%stopics/list?keyword=%s" % (self.site, urllib.quote(self.searchw))
        soup = BeautifulSoup(urllib2.urlopen(query_link), "lxml")
        tlist = soup.findAll("td", {"class": "title"})
        mlist = soup.findAll('a', {"class": "download-arrow arrow-magnet"})
        stat = soup.findAll("td", {"nowrap": "nowrap"}, {"align": "center"})
        return tlist, mlist, stat[4::5]

    def getTorrentInfo(self):
        tlist, mlist, stat = self.getParsedPage()
        tlist = [ t.findAll('a')[-1] for t in tlist]
        tinfo = [ (t.text.encode("utf-8").strip(),
                   m.get("href"),
                   int(s.text)) for t, m, s in zip(tlist, mlist, stat) ]
        return tinfo





