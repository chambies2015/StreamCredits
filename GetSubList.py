from urllib.parse import urlencode
from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, InvalidURL, ConnectionError
import json
import TwitchAccessToken
import Credentials

clientId = Credentials.client_id
accessToken = Credentials.subOAuthToken
channelName = Credentials.channelName

def getSubList():
    session = Session()
    channelId = Credentials.broadcasterID

    channelIdUrl = "https://api.twitch.tv/helix/users?login=" + channelName

    retryAdapter = HTTPAdapter(max_retries=2)
    session.mount('https://', retryAdapter)
    session.mount('http://', retryAdapter)

    response = session.get(channelIdUrl, headers={
        'Client-ID': clientId,
        'Authorization': f'Bearer {accessToken}',
        'Accept': 'application/vnd.twitchtv.v5+json',
        'Content-Type': 'application/json'
    })
    try:
        result = json.loads(response.text)
    except:
        result = None

    result = None
    response = None

    subList = []

    while (True):
        apiRequestUrl = "https://api.twitch.tv/helix/subscriptions?broadcaster_id=" + channelId + "&first=100"

        # Do the API Lookup
        response = session.get(apiRequestUrl, headers={
            'Client-ID': clientId,
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Authorization': f'Bearer {accessToken}',
            'Content-Type': 'application/json'
        })

        try:
            result = json.loads(response.text)
        except:
            result = None

        if (result):
            for sub in result["data"]:
                name = sub.get('user_name')
                if name != Credentials.channelName:
                    subList.append(name)
        else:
            break
        return subList
