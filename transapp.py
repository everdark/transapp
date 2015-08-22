
# define helper functions for transapp
import subprocess

def shutdownTransmission():
    """shutdown transmission daemon if all current torrents are finished downloading"""
    cur_torrents = subprocess.check_output(["transmission-remote", "-l"])
    cur_torrents = [ t for t in cur_torrents.split('\n') if '%' in t ]
    pcts = [ t.split()[1] for t in cur_torrents ]
    unfinished = [ p for p in pcts if p != "100%" ]
    if not len(unfinished):
        subprocess.call(['service', 'transmission-daemon', 'stop'])
