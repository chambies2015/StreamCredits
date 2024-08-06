import Credentials
import TwitchAccessToken
import requests

client_id = Credentials.client_id
access_token = Credentials.followerOAuthToken



def get_followers():
    url = 'https://api.twitch.tv/helix/channels/followers'
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    params = {
        'broadcaster_id': Credentials.broadcasterID,  # To get followers of this broadcaster
        'first': 100  # Number of followers to fetch per request (max is 100)
    }
    response = requests.get(url, headers=headers, params=params)
    response_data = response.json()
    followers = []

    if 'data' in response_data:
        for follow in response_data['data']:
            followers.append(follow['user_name'])  # Extract follower names
    return followers


if __name__ == "__main__":
    print(get_followers())