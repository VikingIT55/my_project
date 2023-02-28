import requests
import pandas as pd
from sqlalchemy import create_engine
import json
from datetime import datetime, timedelta
import psycopg2

from tokens import token

DATABASE_LOCATION = 'postgresql+psycopg2://postgres:5555@localhost:5432/postgres'

headers = {"Accept": "application/json",
           "Content-Type": "application/json",
           "Authorization": "Bearer {token}".format(token=token)}

def check_is_valid_data(df: pd.DataFrame) -> bool:
    # check dataframe is empty
    if df.empty:
        raise Exception('Dataframe is empty')

    # Primary key cheking
    if pd.Series(['played_at']).is_unique:
        pass
    else:
        raise Exception('Duplicate data')

    # Check on Null & N/A
    if df.isnull().values.any():
        raise Exception('NULL find')
    if df.isna().values.any():
        raise Exception('Find N/A pleas check code')

    # Check correctly date
    yesterday = datetime.now() - timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

    timestamps = df["timestamps"].tolist()
    for timestamp in timestamps:
        if datetime.strptime(timestamp, '%Y-%m-%d') != yesterday:
            raise Exception("At least one of the returned songs does not have a yesterday's timestamp")

    return True
def run_spotify_etl():
    DATABASE_LOCATION = 'postgresql+psycopg2://postgres:5555@localhost:5432/postgres'

    headers = {"Accept": "application/json",
               "Content-Type": "application/json",
               "Authorization": "Bearer {token}".format(token=token)}

    yesterday = datetime.now() - timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    url_api = 'https://api.spotify.com/v1/me/player/recently-played?limit=10&after={yesterday}'.format(yesterday=yesterday_unix_timestamp)

    request = requests.get(url_api, headers=headers)
    resource = request.json()
    # transformation data
    artist = []
    played_at = []
    name_track = []
    timestamps = []
    for song in resource['items']:
        artist.append(song['track']['album']['artists'][0]['name'])
        played_at.append(song['played_at'])
        timestamps.append(song['played_at'][0:10])
        name_track.append(song['track']['name'])
    song_dict = {
        'played_at': played_at,
        'artist': artist,
        'name_track': name_track,
        'timestamps': timestamps
                }

    spotify_df = pd.DataFrame(song_dict, columns=['played_at', 'artist', 'name_track', 'timestamps'])

    #if check_is_valid_data(spotify_df):
        #print('Data valid, proceed to Load stage')

    engine = create_engine(DATABASE_LOCATION)
    conn = psycopg2.connect(user='postgres',
                            password='5555',
                            host='localhost',
                            port='5432',
                            database='postgres')
    cursor = conn.cursor()

    sql_query = """
        CREATE TABLE IF NOT EXISTS spotify_data(
            played_at VARCHAR(200),
            artist VARCHAR(200),
            name_track VARCHAR(200),
            timestamps VARCHAR(200),
            CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
        )
        """

    cursor.execute(sql_query)
    print("Opened database successfully")
    conn.commit()
    try:
        spotify_df.to_sql("spotify_data", engine, index=False, if_exists='append')
        print('Data add successfully')
    except:
        print("Data already exists in the database")

    conn.close()
    print("Close database successfully")


