import qbittorrentapi
from datetime import datetime, timedelta
from enum import Enum
from loguru import logger
from discord import Colour

from config import QBITTORRENT_USERNAME, QBITTORRENT_PASSWORD, QBITTORRENT_LOCALHOST, QBITTORRENT_PORT
from util import human_readable_size, time_ago_str, time_ago_timedelta_str

class TorrentStatus(Enum):
    PAUSED = 1
    STALLED = 2
    DOWNLOADING = 3
    COMPLETED = 4
    MOVING = 5
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
        elif status in ('moving'):
            return cls.MOVING
        else:
            logger.warning(f'Unknown status: ({status})')
            return cls.UNKNOWN

class TorrentItem(object):

    def __init__(self, name, status, added_on, size, completed, amount_left,
                 completion_on, dlspeed, progress, eta):
        self.name = name
        self.status = TorrentStatus.from_status_str(status)
        self.status_str = status
        self.added_on = datetime.fromtimestamp(added_on)
        self.size = size
        self.completed = completed
        self.amount_left = amount_left
        self.completed_on = datetime.fromtimestamp(completion_on)
        self.download_speed = dlspeed
        self.progress = progress
        self.time_left = timedelta(seconds=eta)

    def get_status_color(self):
        if self.status == TorrentStatus.COMPLETED: 
            return Colour.green()
        elif self.status == TorrentStatus.DOWNLOADING:
            return Colour.blue()
        elif self.status == TorrentStatus.PAUSED:
            return Colour.orange()
        elif self.status == TorrentStatus.STALLED:
            return Colour.red()
        elif self.status == TorrentStatus.MOVING:
            return Colour.dark_green()
        else:
            return Colour.fuchsia()

    def get_status_str(self):
        if self.status == TorrentStatus.COMPLETED:
            return '✅ Finished downloading'
        elif self.status == TorrentStatus.DOWNLOADING:
            return f'🚅 Downloading at {human_readable_size(self.download_speed)}/s'
        elif self.status == TorrentStatus.PAUSED:
            return '⏸️ Download paused'
        elif self.status == TorrentStatus.STALLED:
            return '⚠️ Downloading stalled'
        elif self.status == TorrentStatus.MOVING:
            return '🚚 Moving completed download'
        elif self.status == TorrentStatus.UNKNOWN:
            return f'⛔ Status unknown {self.status_str}'

    def get_size_str(self):
        return human_readable_size(self.size)

    def get_amount_left_str(self):
        return human_readable_size(self.amount_left)

    def get_progress_str(self):
        return round(self.progress * 100)

    def get_full_status_str(self):
        if self.status == TorrentStatus.COMPLETED:
            return f'Finished {time_ago_str(self.completed_on)}'
        elif self.status == TorrentStatus.DOWNLOADING:
            return time_ago_timedelta_str(self.time_left, suffix=' left')
        elif self.status == TorrentStatus.PAUSED:
            return f'Resume torrent to continue downloading'
        elif self.status == TorrentStatus.STALLED:
            return 'Finding torrent seeders...'
        elif self.status == TorrentStatus.MOVING:
            return 'This can take a few minutes...'
        else:
            return f"Unknown status: {self.status_str}"
            
        



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

    # for k,v in client.app.build_info.items(): print(f'{k}: {v}')

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
                amount_left=torrent.amount_left,
                completion_on=torrent.completion_on,
                dlspeed=torrent.dlspeed,
                progress=torrent.progress,
                eta=torrent.eta,
            )
        )
        # print(f'{torrent.completed} /  {torrent.eta}')
    
    torrents = sorted(torrents, key=lambda torrent: torrent.added_on, reverse=True)
    return torrents



# get_torrents()

