import requests
import dotenv
import os



dotenv.load_dotenv()

data = {
    'grant_type': 'password',
    'username': os.getenv('REDDIT_USERNAME'),
    'password': os.getenv('REDDIT_PASSWORD')
}
auth = requests.auth.HTTPBasicAuth(
    os.getenv('REDDIT_CLIENT_ID'),
    os.getenv('REDDIT_CLIENT_SECRET')
)

r = requests.post(
    'https://www.reddit.com/api/v1/access_token',
    data=data,
    headers={'User-Agent': 'Editor House by anubhob493'},
    auth=auth
)
d = r.json()
print(d)
access_token = 'bearer ' + d['access_token']
