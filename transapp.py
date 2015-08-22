
# define helper functions for transapp

def shutdownTransmission():
    """shutdown transmission daemon if all current torrents are finished downloading"""
    cur_torrents = subprocess.check_output(["transmission-remote", "-l"])
    pcts = [ t.split()[1] for t in cur_torrents[1:-2] ]
    unfinished = [ p for p in pcts if p != "100%" ]
    if not len(unfinish):
        subprocess.call(['service', 'transmission-daemon', 'stop'])
