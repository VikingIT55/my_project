import base64

USER_NAME = '********'
client_id = '************'
client_secret = '*************'
my_spotify_URI = '***********'
refresh_token = '*********************************************************'
auth_client = client_id + ':' + client_secret
base_64 = 'Basic ' + base64.b64encode(auth_client.encode()).decode()
token = '*******************************************8'

