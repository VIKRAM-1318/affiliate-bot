"""
pinterest.py — Auto-pin to Pinterest using Pinterest API v5 (FREE)
"""
import os, requests, base64, time


PINTEREST_API = "https://api.pinterest.com/v5"


def _headers():
    return {
        "Authorization": f"Bearer {os.environ['PINTEREST_ACCESS_TOKEN']}",
        "Content-Type": "application/json"
    }


def _upload_image(image_path: str) -> str:
    """
    Upload image to Pinterest and return media_id.
    Pinterest requires images to be uploaded first via register → upload → done.
    """
    # Step 1: Register upload
    reg_resp = requests.post(
        f"{PINTEREST_API}/media",
        headers=_headers(),
        json={"media_type": "image/jpeg"}
    )
    reg_resp.raise_for_status()
    reg_data = reg_resp.json()
    media_id = reg_data["media_id"]
    upload_url = reg_data["upload_url"]
    upload_params = reg_data.get("upload_parameters", {})

    # Step 2: Upload image to S3
    with open(image_path, "rb") as f:
        files = {"file": ("pin.jpg", f, "image/jpeg")}
        s3_resp = requests.post(upload_url, data=upload_params, files=files)
        s3_resp.raise_for_status()

    # Step 3: Mark as done
    done_resp = requests.patch(
        f"{PINTEREST_API}/media/{media_id}",
        headers=_headers(),
        json={"status": "succeeded"}
    )
    done_resp.raise_for_status()

    # Wait for processing
    time.sleep(3)
    return media_id


def create_pin(
    board_id: str,
    title: str,
    description: str,
    blog_url: str,
    image_path: str
) -> dict:
    """
    Creates a Pinterest pin with uploaded image.
    Returns pin data dict.
    """
    try:
        media_id = _upload_image(image_path)
        pin_data = {
            "board_id": board_id,
            "title": title[:100],
            "description": description[:500],
            "link": blog_url,
            "media_source": {
                "source_type": "media_id",
                "media_id": media_id
            }
        }
        resp = requests.post(
            f"{PINTEREST_API}/pins",
            headers=_headers(),
            json=pin_data
        )
        resp.raise_for_status()
        result = resp.json()
        pin_id = result.get("id", "")
        print(f"[pinterest] ✅ Pinned: {title[:50]}... (id: {pin_id})")
        return result

    except Exception as e:
        print(f"[pinterest] ❌ Error pinning '{title[:40]}': {e}")
        return {}


def get_boards() -> list:
    """List all Pinterest boards (useful to get board_id)."""
    resp = requests.get(f"{PINTEREST_API}/boards", headers=_headers())
    resp.raise_for_status()
    boards = resp.json().get("items", [])
    for b in boards:
        print(f"  Board: {b['name']} → ID: {b['id']}")
    return boards


if __name__ == "__main__":
    print("Your Pinterest boards:")
    get_boards()
