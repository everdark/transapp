#!/usr/bin/env python



import ConfigParser
import sys, os
import dropbox


def main():
    # connect to the dropbox account
    access_token = config.get("dropbox", "access_token")
    client = dropbox.client.DropboxClient(access_token)

    # setup variables and check file existence
    magnet_link = sys.argv[1]
    magnet_link_file = config.get("dropbox", "magnet_file_path")
    tmpfname = "tmpfile_for_update_magnet_link"
    if tmpfname in os.listdir('.'):
        sys.stdout.write("Tmpfile already exists?")
        exit(1)

    # download and update the magnet-link maintenance file
    f = client.get_file(magnet_link_file)
    out = open(os.path.join('.', tmpfname), 'w')
    out.write(f.read())
    out.write(magnet_link + '\n')
    out.close()

    # upload the magnet-link maintenance file back to dropbox
    f = open(os.path.join(".", tmpfname), 'r')
    response = client.put_file(magnet_link_file, f, overwrite=True)
    f.close()

    # delete tmp file
    os.remove(tmpfname)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stdout.write("Usage: %s \"magnet-link\"\n" % sys.argv[0])
        exit(1)
    else:
        config = ConfigParser.ConfigParser()
        if not len(config.read(['config.ini'])):
            print "No config file found. Program aborted."
            exit(1)
        main()
