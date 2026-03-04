"""
content.py — AI blog post generator using Gemini API (FREE tier)
Free limit: 1500 requests/day — we use 60/day (3 per post × 20 posts)
"""
import google.generativeai as genai
import os, re, time

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")  # free tier model


def _call(prompt: str, retries=3) -> str:
    for attempt in range(retries):
        try:
            resp = model.generate_content(prompt)
            return resp.text.strip()
        except Exception as e:
            print(f"[content] Gemini error (attempt {attempt+1}): {e}")
            time.sleep(3)
    return ""


def generate_blog_post(keyword: str, associate_id: str) -> dict:
    """
    Returns dict with:
      title, html_content, seo_description, pin_caption
    """

    # ── 1. Blog post ─────────────────────────────────────────────────────────
    blog_prompt = f"""
Write a helpful product roundup blog post titled:
"10 Best {keyword.title()} on Amazon India 2026"

Rules:
- Intro paragraph (2-3 sentences, friendly tone)
- List exactly 10 products (make up realistic product names like real Amazon products)
- Each product has:
  * H3 heading: product name
  * 2-3 sentence description (benefits, who it's for)
  * Price estimate in ₹
  * One line: AFFILIATE_LINK_PLACEHOLDER
- Conclusion paragraph (2 sentences)
- Output clean HTML only (use <h2>,<h3>,<p>,<ul>,<li> tags)
- No markdown, no code blocks, just raw HTML
- Include Amazon India affiliate disclosure at top:
  <p><em>Disclosure: This post contains Amazon affiliate links. We earn a small commission at no extra cost to you.</em></p>
"""
    html = _call(blog_prompt)

    # Build actual affiliate search link (no PA-API needed)
    search_link = f"https://www.amazon.in/s?k={keyword.replace(' ', '+')}&tag={associate_id}"
    html = html.replace("AFFILIATE_LINK_PLACEHOLDER",
                        f'<a href="{search_link}" target="_blank" rel="nofollow">👉 Check Price on Amazon India</a>')

    # ── 2. SEO meta description ───────────────────────────────────────────────
    seo_prompt = f"""
Write a Google SEO meta description (max 155 characters) for a blog post about:
"10 Best {keyword.title()} on Amazon India 2026"
Output only the description text, nothing else.
"""
    seo_desc = _call(seo_prompt)[:155]

    # ── 3. Pinterest pin caption ──────────────────────────────────────────────
    pin_prompt = f"""
Write a Pinterest pin description (max 500 characters) for:
"10 Best {keyword.title()} on Amazon India 2026"
- Start with a hook question or statement
- Include 3-5 relevant hashtags at the end
- Friendly, helpful tone
- Output only the caption text, nothing else
"""
    pin_caption = _call(pin_prompt)[:500]

    title = f"10 Best {keyword.title()} on Amazon India 2026"
    return {
        "title": title,
        "html_content": html,
        "seo_description": seo_desc,
        "pin_caption": pin_caption,
        "keyword": keyword,
        "affiliate_link": search_link
    }


if __name__ == "__main__":
    result = generate_blog_post("coding desk gadgets", "YOUR_ASSOCIATE_ID")
    print("Title:", result["title"])
    print("SEO:", result["seo_description"])
    print("Pin:", result["pin_caption"])
    print("HTML length:", len(result["html_content"]))
