import qbittorrentapi
from datetime import datetime

from config import QBITTORRENT_USERNAME, QBITTORRENT_PASSWORD, QBITTORRENT_LOCALHOST, QBITTORRENT_PORT

class TorrentItem(object):

    def __init__(self, name, status, added_on):
        self.name = name
        self.status = status
        self.added_on = datetime.fromtimestamp(added_on)

def get_client():
    client = qbittorrentapi.Client(
        host=QBITTORRENT_LOCALHOST,
        port=QBITTORRENT_PORT,
        username=QBITTORRENT_USERNAME,
        password=QBITTORRENT_PASSWORD,
        VERIFY_WEBUI_CERTIFICATE=False,
    )

    # the Client will automatically acquire/maintain a logged-in state
    # in line with any request. therefore, this is not strictly necessary;
    # however, you may want to test the provided login credentials.
    try:
        client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

    for k,v in client.app.build_info.items(): print(f'{k}: {v}')

    return client


def get_torrents():
    client = get_client()
    # https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-(qBittorrent-4.1)#get-torrent-list
    torrents = []
    for torrent in client.torrents_info():
        torrents.append(
            TorrentItem(
                name=torrent.name,
                status=torrent.state,
                added_on=torrent.added_on
            )
        )
        # print(f'{torrent.name} - ({torrent.state}) ')
        # print(f'{torrent.completed} / {torrent.size} ({torrent.progress}) - {torrent.eta}')
        # print(f'{torrent.dlspeed}')
    
    torrents = sorted(torrents, key=lambda torrent: torrent.added_on, reverse=True)
    return torrents



get_torrents()

