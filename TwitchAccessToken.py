import requests
import Credentials

client_id = Credentials.client_id
client_secret = Credentials.client_secret
authorization_code = Credentials.followerOAuthToken  # Authorization code from Twitch
redirect_uri = Credentials.redirect_uri

def get_access_token():
    url = 'https://id.twitch.tv/oauth2/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': authorization_code,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        response_json = response.json()
        access_token = response_json.get('access_token')
        return access_token
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

# Example usage
if __name__ == "__main__":
    access_token = get_access_token()
    print("Access Token:", access_token)