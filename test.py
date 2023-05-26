import base64
import requests
from secrets_key import client_id, client_secret, refresh_token, token

def refresh_the_token():
    auth_client = client_id + ':' + client_secret
    auth_encode = 'Basic ' + base64.b64encode(auth_client.encode()).decode()
    print(auth_encode)
    headers = {
        'Authorization': auth_encode
    }

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }

    response = requests.post('https://api.spotify.com/api/token', data=data, headers=headers)
    if response.status_code == 200:
        print('The request to went  through we got a status 200; Spotify token refreshed')
        response_json = response.json()
        new_expire = response_json['expires_in']
        print('the time left on new token is: ' + str(new_expire/60) + 'min')
    else:
        print('ERORR! The response we got was: ' + str(response))

refresh_the_token()
