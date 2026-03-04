"""
keywords.py — Trending keyword finder using Google Trends (100% free)
"""
import random
import time
from pytrends.request import TrendReq

# ── Seed keywords per niche ─────────────────────────────────────────────────
SEED_KEYWORDS = [
    # Tech / Coding
    "coding gadgets", "esp32 projects", "raspberry pi accessories",
    "mechanical keyboard", "desk setup accessories", "programmer gifts",
    # Home / Lifestyle
    "home office gadgets", "kitchen gadgets", "smart home devices",
    "budget tech gadgets india", "amazon finds india",
    # IoT / Embedded
    "arduino kits", "iot starter kit", "embedded systems projects",
]

def get_trending_keywords(top_n=20):
    """
    Returns top_n trending keyword variations using Google Trends.
    Falls back to seed list if API is rate-limited.
    """
    try:
        pytrends = TrendReq(hl='en-IN', tz=330, timeout=(10, 25))
        trending = []

        # Pick 5 random seeds and get related queries
        seeds = random.sample(SEED_KEYWORDS, min(5, len(SEED_KEYWORDS)))
        for seed in seeds:
            try:
                pytrends.build_payload([seed], geo='IN', timeframe='now 7-d')
                related = pytrends.related_queries()
                top = related.get(seed, {}).get('top')
                if top is not None and not top.empty:
                    queries = top['query'].tolist()[:4]
                    trending.extend(queries)
                time.sleep(1)  # avoid rate limiting
            except Exception:
                trending.append(seed)

        # Deduplicate and return top_n
        seen = set()
        unique = []
        for kw in trending:
            if kw.lower() not in seen:
                seen.add(kw.lower())
                unique.append(kw)

        if len(unique) >= top_n:
            return unique[:top_n]

        # Pad with seeds if not enough results
        for s in SEED_KEYWORDS:
            if s.lower() not in seen and len(unique) < top_n:
                unique.append(s)
                seen.add(s.lower())

        return unique[:top_n]

    except Exception as e:
        print(f"[keywords] Trends API error: {e} — using seed list")
        shuffled = SEED_KEYWORDS.copy()
        random.shuffle(shuffled)
        return shuffled[:top_n]


if __name__ == "__main__":
    kws = get_trending_keywords(20)
    print(f"Found {len(kws)} keywords:")
    for i, k in enumerate(kws, 1):
        print(f"  {i:2}. {k}")
