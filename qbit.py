import qbittorrentapi
from datetime import datetime
from enum import Enum
from loguru import logger
from discord import Colour

from config import QBITTORRENT_USERNAME, QBITTORRENT_PASSWORD, QBITTORRENT_LOCALHOST, QBITTORRENT_PORT
from util import human_readable_size

class TorrentStatus(Enum):
    PAUSED = 1
    STALLED = 2
    DOWNLOADING = 3
    COMPLETED = 4
    UNKNOWN = 0

    @classmethod
    def from_status_str(cls, status):
        if status in ('uploading', 'pausedUP', 'checkingUP', 'stalledUP', 'forcedUP', 'missingFiles'):
            return cls.COMPLETED
        elif status in ('downloading'):
            return cls.DOWNLOADING
        elif status in ('pausedDL'):
            return cls.PAUSED
        elif status in ('stalledDL'):
            return cls.STALLED
        else:
            logger.warning(f'Unknown status: ({status})')
            return cls.UNKNOWN

class TorrentItem(object):

    def __init__(self, name, status, added_on, size, completed, completion_on, dlspeed):
        self.name = name
        self.status = TorrentStatus.from_status_str(status)
        self.added_on = datetime.fromtimestamp(added_on)
        self.size = size
        self.completed = completed
        self.completed_on = datetime.fromtimestamp(completion_on)
        self.download_speed = dlspeed

    def get_status_color(self):
        if self.status == TorrentStatus.COMPLETED: 
            return Colour.green()
        elif self.status == TorrentStatus.DOWNLOADING:
            return Colour.blue()
        elif self.status == TorentStatus.PAUSED:
            return Colour.orange()
        elif self.status == TorrentStatus.STALLED:
            return Colour.red()
        else:
            return Colour.grey()

    def get_status_str(self):
        if self.status == TorrentStatus.COMPLETED:
            return '✅ Finished downloading'
        elif self.status == TorrentStatus.DOWNLOADING:
            return f'🚅 Downloading at {human_readable_size(self.download_speed)}/s'
        elif self.status == TorrentStatus.PAUSED:
            return '⏸️ Download paused'
        elif self.status == TorrentStatus.STALLED:
            return '⚠️ Downloading stalled'
        elif self.status == TorrentStatus.UNKNOWN:
            return '⛔ Status unknown, check the logs'

    def get_size_str(self):
        return human_readable_size(self.size)

    def get_completed_str(self):
        return human_readable_size(self.completed)



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
        # logger.except(e)

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
                added_on=torrent.added_on,
                size=torrent.size,
                completed=torrent.completed,
                completion_on=torrent.completion_on,
                dlspeed=torrent.dlspeed
            )
        )
        # print(f'{torrent.completed} / {torrent.size} ({torrent.progress}) - {torrent.eta}')
    
    torrents = sorted(torrents, key=lambda torrent: torrent.added_on, reverse=True)
    return torrents



# get_torrents()

