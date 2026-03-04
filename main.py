"""
main.py — Master orchestrator
Runs 20 posts/day: keyword → blog → publish → image → pin
"""
import os, time, json, sys
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from keywords import get_trending_keywords
from content  import generate_blog_post
from blogger  import publish_post
from image_gen import generate_pin_image
from pinterest import create_pin

# ── Config ───────────────────────────────────────────────────────────────────
POSTS_PER_DAY   = 20
DELAY_BETWEEN   = 15   # seconds between posts (avoids API rate limits)
ASSOCIATE_ID    = os.environ.get("AMAZON_ASSOCIATE_ID", "YOUR_ASSOCIATE_ID")
PINTEREST_BOARD = os.environ.get("PINTEREST_BOARD_ID", "YOUR_BOARD_ID")
LOG_FILE        = os.path.join(os.path.dirname(__file__), "..", "logs", "run_log.json")

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


def log_result(entry: dict):
    """Append result to log file."""
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE) as f:
                logs = json.load(f)
        except Exception:
            logs = []
    logs.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)


def run_daily():
    """Main daily run — processes POSTS_PER_DAY keywords end-to-end."""
    print(f"\n{'='*60}")
    print(f"🚀 Affiliate Bot Started — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Target: {POSTS_PER_DAY} posts today")
    print(f"{'='*60}\n")

    # ── Step 1: Get keywords ──────────────────────────────────────────────────
    print("📊 Step 1: Fetching trending keywords...")
    keywords = get_trending_keywords(POSTS_PER_DAY)
    print(f"   Got {len(keywords)} keywords\n")

    success_count = 0
    fail_count = 0

    for i, keyword in enumerate(keywords[:POSTS_PER_DAY], 1):
        print(f"\n[{i:2}/{POSTS_PER_DAY}] Processing: '{keyword}'")
        entry = {
            "timestamp": datetime.now().isoformat(),
            "keyword": keyword,
            "status": "failed",
            "blog_url": "",
            "pin_id": ""
        }

        try:
            # ── Step 2: Generate blog post ────────────────────────────────────
            print(f"  ✍️  Generating blog post...")
            post = generate_blog_post(keyword, ASSOCIATE_ID)

            # ── Step 3: Publish to Blogger ────────────────────────────────────
            print(f"  📝  Publishing to Blogger...")
            blog_result = publish_post(
                title=post["title"],
                html_content=post["html_content"],
                seo_description=post["seo_description"],
                labels=["Amazon Finds", "Tech Gadgets", keyword.title()]
            )
            blog_url = blog_result.get("url", "")

            # ── Step 4: Generate pin image ────────────────────────────────────
            print(f"  🖼️   Generating pin image...")
            image_path = generate_pin_image(
                title=post["title"],
                keyword=keyword
            )

            # ── Step 5: Post to Pinterest ─────────────────────────────────────
            print(f"  📌  Pinning to Pinterest...")
            pin_result = create_pin(
                board_id=PINTEREST_BOARD,
                title=post["title"],
                description=post["pin_caption"],
                blog_url=blog_url,
                image_path=image_path
            )

            # ── Cleanup image ─────────────────────────────────────────────────
            if os.path.exists(image_path):
                os.remove(image_path)

            entry["status"]  = "success"
            entry["blog_url"] = blog_url
            entry["pin_id"]  = pin_result.get("id", "")
            success_count += 1
            print(f"  ✅  Done! → {blog_url}")

        except Exception as e:
            print(f"  ❌  Failed: {e}")
            fail_count += 1

        log_result(entry)

        # Delay between posts (avoid rate limits)
        if i < POSTS_PER_DAY:
            print(f"  ⏳  Waiting {DELAY_BETWEEN}s before next post...")
            time.sleep(DELAY_BETWEEN)

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"✅  Run Complete — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Success: {success_count}/{POSTS_PER_DAY}")
    print(f"   Failed:  {fail_count}/{POSTS_PER_DAY}")
    print(f"   Log:     {LOG_FILE}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    run_daily()
