# Python 3
import json
import requests as re
import base64
import time
import pprint
"""
https://developer.spotify.com/web-api/authorization-guide/#authorization_code_flow

"""

auth = None
authurl = "https://accounts.spotify.com/api/token"
token = None
BASE_URL = "https://api.spotify.com"

# taken from spotipy
def _make_authorization_headers(client_id, client_secret):
    auth_header = base64.b64encode((client_id + ':' + client_secret).encode('ascii'))
    return {'Authorization': 'Basic %s' % auth_header.decode('ascii')}


def _get_token(client_id, client_secret):
    header = _make_authorization_headers(client_id, client_secret)
    payload = { 'grant_type': 'client_credentials'}
    r = re.post(authurl, headers=header, data=payload, verify=True)

    if r.status_code != 200:
        return None #TODO: should be an error here
    else:
        return r.json()


def _update_token_time(token):
    token['expires_at'] = int(time.time() + token['expires_in'])
    return token

def _auth_header(token):
    if token:
        return {'Authorization': 'Bearer {0}'.format(token['access_token'])}
    else:
        return {}


def _query_my_playlists(token):

    url = "/v1/me/playlists"
    headers = _auth_header(token)
    headers['Content-Type'] = 'application/json'

    test= "https://api.spotify.com/v1/users/iplasmic/playlists/33ilPfrhjOvFnU81vtKMRL/tracks"
    r = re.get(test, headers=headers)

    #TODO: error checking
    return r.json()


def main():
    try:
        settings = open('settings.json', 'r')
        data = json.load(settings)
        auth = (data.get("client_id"), data.get("secret"))
    except IOError:
        print("file not found")

    data = _get_token(auth[0], auth[1])
    _update_token_time(data)

    output = _query_my_playlists(data)
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(len(output['items']))
    # NOTES: can't use the 'me' requests using this authentication method, however you can lookup users.







if __name__ == "__main__":
    main()


