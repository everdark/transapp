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
        """get torrent title, download link, and download count"""
        tlist = self.getParsedPage()
        tinfo = [ (t.find("td", {"class": "tlistname"}).text.encode("utf-8"),
                   t.find("td", {"class": "tlistdownload"}).find('a').get("href"),
                   int(t.find("td", {"class": "tlistdn"}).text)) for t in tlist ]
        return tinfo
        




