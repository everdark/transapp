# transapp
Remote management for torrents via dropbox api. On your server which running transmission daemon, run the `torrent.monitor.py` (as daemon). On your client side you simply sync new magnet link by using `upload-magnet.py`. This can be further simplified if you have Alfred on Mac OS X so that a workflow to trigger the python script can be easily constructed. :)


Use format for config.ini:
```
[dropbox]
access_token = your_dropbox_app_token
magnet_file_path = path_for_the_magnet_maintenance_file

[transmission_server]
incomplete_path = path_of_your_incomplete_folder
```
