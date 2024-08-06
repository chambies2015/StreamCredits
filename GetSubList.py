from urllib.parse import urlencode
from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, InvalidURL, ConnectionError
import json
import TwitchAccessToken
import Credentials

##########################################################
#                Configure your stuff here               #
##########################################################

clientId = Credentials.client_id  # Register a Twitch Developer application and put its client ID here
accessToken = Credentials.subOAuthToken  # Generate an OAuth token with channel_subscriptions scope and insert your token here

channelName = "chambiez"  # Put your channel name here
saveLocation = "subscriberListTest.txt"  # Put the location you'd like to save your list here

###################################################################

def getSubList():
    session = Session()
    channelId = "81822499"

    channelIdUrl = "https://api.twitch.tv/helix/users?login=" + channelName

    retryAdapter = HTTPAdapter(max_retries=2)
    session.mount('https://', retryAdapter)
    session.mount('http://', retryAdapter)

    # Find the Channel ID
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
                if name != 'Chambiez':
                    subList.append(name)
        else:
            break
        return subList

    # if (result):
    #     f = open(saveLocation, 'w')
    #     for sub in subList:
    #         f.write(sub + "\n")
    #     f.close()