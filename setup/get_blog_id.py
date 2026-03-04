"""
Temporary script to get Blogger Blog ID.
"""

import json, os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds_path = os.path.join(os.path.dirname(__file__), "google_credentials_output.json")
with open(creds_path) as f:
    creds_data = json.load(f)

creds = Credentials(
    token=creds_data["token"],
    refresh_token=creds_data["refresh_token"],
    token_uri=creds_data["token_uri"],
    client_id=creds_data["client_id"],
    client_secret=creds_data["client_secret"],
)
service = build("blogger", "v3", credentials=creds)
blogs = service.blogs().listByUser(userId="self").execute()
for b in blogs.get("items", []):
    print(f"Blog Name : {b['name']}")
    print(f"Blog ID   : {b['id']}")
    print(f"Blog URL  : {b['url']}")
    print()
