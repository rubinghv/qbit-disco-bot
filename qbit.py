import qbittorrentapi

from config import QBITTORRENT_USERNAME, QBITTORRENT_PASSWORD, QBITTORRENT_LOCALHOST, QBITTORRENT_PORT

# instantiate a Client using the appropriate WebUI configuration
qbt_client = qbittorrentapi.Client(
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
    qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)

# display qBittorrent info
print(f'qBittorrent: {qbt_client.app.version}')
print(f'qBittorrent Web API: {qbt_client.app.web_api_version}')
for k,v in qbt_client.app.build_info.items(): print(f'{k}: {v}')

# retrieve and show all torrents
for torrent in qbt_client.torrents_info():
    print(f'{torrent.hash[-6:]}: {torrent.name} ({torrent.state})')