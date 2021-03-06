#!/usr/bin/env python


import ConfigParser
import dropbox
import re
import subprocess
import os
import time
import daemon

import transapp


def main():
    while True:
        # connect to dropbox api
        access_token = config.get("dropbox", "access_token")
        magnet_link_file = config.get("dropbox", "magnet_file_path")
        client = dropbox.client.DropboxClient(access_token)
        # get magnet links and add to transmission server
        f = client.get_file(magnet_link_file)
        all_magnets = [line.strip('\n') for line in f if not re.search(r"^#", line)]
        if len(all_magnets):
            if subprocess.call(['service', 'transmission-daemon', 'status']):
                subprocess.call(['service', 'transmission-daemon', 'start'])
            for m in all_magnets:
                subprocess.call(['transmission-remote', '-a', m])
            # replace magnet maintenance file with empty one
            tmpfname = "tmpfile_for_update_magnet_link"
            subprocess.call(['touch', tmpfname])
            f = open(os.path.join(".", tmpfname), 'r')
            response = client.put_file(magnet_link_file, f, overwrite=True)
            f.close()
            os.remove(tmpfname)
        else:
            transapp.shutdownTransmission() 
            time.sleep(60*10)

def runAsDaemon():
    with daemon.DaemonContext():
        main()


if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    if not len(config.read(['config.ini'])):
        print "No config file found. Program aborted."
        exit(1)       
    runAsDaemon()
