import requests
from datetime import datetime, timedelta


def run_spotify_etl(ti):
    token = ti.xcom_pull(task_ids="refresh_token")
    headers = {"Accept": "application/json",
               "Content-Type": "application/json",
               "Authorization": "Bearer {token}".format(token=token)}
    yesterday = datetime.now() - timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    url_api = "https://api.spotify.com/v1/me/player/recently-played?limit=10&after={yesterday}". \
        format(yesterday=yesterday_unix_timestamp)

    request = requests.get(url_api, headers=headers)
    resource = request.json()
    # transformation data
    artist = []
    played_at = []
    name_track = []
    timestamps = []
    for song in resource["items"]:
        artist.append(song["track"]["album"]["artists"][0]["name"])
        played_at.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])
        if "'" in song["track"]["name"]:
            name_track.append(song["track"]["name"].replace("'", "*"))
        else:
            name_track.append(song["track"]["name"])
    song_dict = {
        "played_at": played_at,
        "artist": artist,
        "name_track": name_track,
        "timestamps": timestamps
    }
    return song_dict
