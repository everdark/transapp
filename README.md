# transapp
Remote management for torrents via dropbox api. On your server which running transmission daemon, run the `torrent-monitor.py` as daemon (or schedule `torrent-monitor-cron.py` as cron job in case the daemon doesn't work as expected). On your client side you simply sync new magnet link by using `upload-magnet.py`. This can be further simplified if you have Alfred on Mac OS X so that a workflow to trigger the python script can be easily constructed. :)

### Usage of `keyword2magnet.py`
This is a small script tool that conveniently converts a "bango" into one available magnet link string, by crawling of course.

[![asciicast](https://asciinema.org/a/7gkwp3doab8eh4kxhh59ms2r7.png)](https://asciinema.org/a/7gkwp3doab8eh4kxhh59ms2r7)

### Use format for config.ini:
```
[dropbox]
access_token = your_dropbox_app_token
magnet_file_path = path_for_the_magnet_maintenance_file

[movie_crawler]
# this is experimental!
bad_word = cam,ts
good_word = 1080
```
