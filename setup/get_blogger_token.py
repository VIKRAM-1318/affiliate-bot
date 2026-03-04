"""
setup/get_blogger_token.py
Run this ONCE locally to get your Google OAuth refresh token for Blogger API.

Steps:
  1. pip install google-auth-oauthlib
  2. python setup/get_blogger_token.py
  3. A browser window will open — log in with your Google account
  4. Copy the printed JSON and save it as GitHub Secret: GOOGLE_CREDENTIALS_JSON
"""

import json, os
from google_auth_oauthlib.flow import InstalledAppFlow

# Path to your downloaded OAuth client secret JSON
CLIENT_SECRET_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "client_secret_528592560194-7q048pqfjlrh315km3870ukg7vuo8cr4.apps.googleusercontent.com.json",
)

SCOPES = ["https://www.googleapis.com/auth/blogger"]


def main():
    print("[*] Starting Google OAuth flow for Blogger API...")
    print(f"   Using credentials file: {CLIENT_SECRET_FILE}\n")

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    creds = flow.run_local_server(port=0)

    output = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "token_uri": creds.token_uri,
    }

    print(
        "\n[SUCCESS] Copy the JSON below and save it as GitHub Secret: GOOGLE_CREDENTIALS_JSON\n"
    )
    print("=" * 60)
    print(json.dumps(output, indent=2))
    print("=" * 60)

    # Also save locally for reference
    out_path = os.path.join(os.path.dirname(__file__), "google_credentials_output.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n[INFO] Also saved locally to: {out_path}")
    print("[WARNING] DO NOT commit this file to GitHub!\n")


if __name__ == "__main__":
    main()
