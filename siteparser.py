"""
Every site parser, as a class extending anyParser, must implement the following methods:
    getTorrentInfo
    resolveLink

Method getTorrentInfo shall return information about all available torrents from the site, in tuple. 
The tuple is designed and has to be (file name, download link, download counts). 
The download link could be either an URL to the corresponding torrent file, 
the magnet link itself, or another URL link to page containing either of the above two.

Method resolveLink will resolve the final magnet link given any one link produced by getTorrentInfo. 
The mechanism to resolve the final magnet link is class-dependent.
"""

import urllib
import urllib2
from bs4 import BeautifulSoup
import operator

import transapp

class anyParser:
    """Super class for any parser"""

    site = ''

    def __init__(self, searchw): self.searchw = str(searchw)
    def getTorrentInfo(): pass
    def resolveLink(): pass

class nyaaParser(anyParser):
    """Specific parser for Nyaa"""
    
    site = "http://sukebei.nyaa.se/"

    def getParsedPage(self):
        query_link = "%s?page=search&cats=0_0&filter=0&term=%s" % (self.site, self.searchw)
        soup = BeautifulSoup(urllib2.urlopen(query_link), "lxml")
        tlist = soup.findAll("tr", {"class": "tlistrow"})
        return tlist

    def getTorrentInfo(self):
        try:
            tlist = self.getParsedPage()
        except urllib2.HTTPError as e:
            return e
        else:
            tinfo = [ parserResult(t.find("td", {"class": "tlistname"}).text.encode("utf-8"),
                       t.find("td", {"class": "tlistdownload"}).find('a').get("href"),
                       int(t.find("td", {"class": "tlistdn"}).text)) for t in tlist ]
            return tinfo

    def resolveLink(self, link):
        return transapp.extractMagnet(link)

class dmhyParser(anyParser):
    """Specific parser for DMHY"""

    site = "https://share.dmhy.org/"

    def getParsedPage(self):
        query_link = "%stopics/list?keyword=%s" % (self.site, urllib.quote(self.searchw))
        soup = BeautifulSoup(urllib2.urlopen(query_link), "lxml")
        tlist = soup.findAll("td", {"class": "title"})
        mlist = soup.findAll('a', {"class": "download-arrow arrow-magnet"})
        stat = soup.findAll("td", {"nowrap": "nowrap"}, {"align": "center"})[4::5]
        return tlist, mlist, stat

    def getTorrentInfo(self):
        try:
            tlist, mlist, stat = self.getParsedPage()
        except urllib2.HTTPError as e:
            return e
        else:
            tlist = [ t.findAll('a')[-1] for t in tlist]
            tinfo = [ parserResult(t.text.encode("utf-8").strip(),
                       m.get("href"),
                       0 if s.text == '-' else int(s.text)) 
                       for t, m, s in zip(tlist, mlist, stat) ]
            return tinfo

    def resolveLink(self, link):
        return link

class _1337xParser(anyParser):
    """Specific parser for 1337x"""

    site = "http://1337x.to/"

    def getParsedPage(self):
        query_link = "%ssearch/%s/1/" % (self.site, urllib.quote(self.searchw))
        soup = BeautifulSoup(urllib2.urlopen(query_link), "lxml")
        tlist = soup.findAll("div", {"class": "tab-detail"})
        return tlist

    def getTorrentInfo(self):
        try:
            tlist = self.getParsedPage()
        except urllib2.HTTPError as e:
            return e
        else: 
            if not len(tlist):
                return []
            else:
                result_sec = tlist[0]
                titles_and_links  = [ (res.find("strong").find('a').text,
                                       urllib.basejoin(self.site, res.find("strong").find('a').get("href")))
                                     for res in result_sec.findAll("div", {"class": "coll-1"}) ]
                se = [ int(res.text) 
                        for res in result_sec.findAll("div", {"class": "coll-2"}) ]
                le = [ int(res.text) 
                        for res in result_sec.findAll("div", {"class": "coll-3"}) ]
                cnt = map(sum, zip(se, le))
                tinfo = [ parserResult(tl[0], tl[1], c) for tl, c in zip(titles_and_links, cnt)]
                return tinfo

    def resolveLink(self, link):
        soup = BeautifulSoup(urllib2.urlopen(link), "lxml")
        try:
            magnet = soup.find('a', {"class": "magnet"}).get("href")
        except AttributeError:
            magnet = "Link not available."
        return magnet

class parserResult(tuple):
    def __new__(self, fname, magnet, cnt):
        return tuple.__new__(parserResult, (fname, magnet, cnt))

    fname = property(operator.itemgetter(0))
    magnet = property(operator.itemgetter(1))
    cnt = property(operator.itemgetter(2))


