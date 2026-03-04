"""
blogger.py — Auto-publish posts to Blogger using Google Blogger API v3 (FREE)
"""
import os, json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def get_blogger_service():
    """Build Blogger API service from env credentials."""
    creds_json = os.environ["GOOGLE_CREDENTIALS_JSON"]
    creds_data = json.loads(creds_json)
    creds = Credentials(
        token=creds_data["token"],
        refresh_token=creds_data["refresh_token"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=creds_data["client_id"],
        client_secret=creds_data["client_secret"],
    )
    return build("blogger", "v3", credentials=creds)


def publish_post(title: str, html_content: str, seo_description: str, labels: list = None) -> dict:
    """
    Publishes a post to Blogger.
    Returns dict with 'url' and 'id' of the created post.
    """
    service = get_blogger_service()
    blog_id = os.environ["BLOGGER_BLOG_ID"]

    post_body = {
        "title": title,
        "content": html_content,
        "labels": labels or ["Amazon Finds", "Tech Gadgets", "Budget Picks"],
    }

    result = service.posts().insert(
        blogId=blog_id,
        body=post_body,
        isDraft=False
    ).execute()

    post_url = result.get("url", "")
    post_id = result.get("id", "")
    print(f"[blogger] ✅ Published: {title[:50]}...")
    print(f"[blogger]    URL: {post_url}")
    return {"url": post_url, "id": post_id}


if __name__ == "__main__":
    # Test publish
    result = publish_post(
        title="Test Post - 10 Best Gadgets 2026",
        html_content="<p>This is a test post.</p>",
        seo_description="Test description",
        labels=["Test"]
    )
    print(result)
