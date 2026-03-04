"""
image_gen.py — Generate Pinterest pin images using Pillow (FREE, no Canva needed)
Pin size: 1000 x 1500 px (Pinterest optimal vertical format)
"""
from PIL import Image, ImageDraw, ImageFont
import os, textwrap, random

# ── Color themes ─────────────────────────────────────────────────────────────
THEMES = [
    {"bg": "#1a1a2e", "accent": "#e94560", "text": "#ffffff", "sub": "#a8b2d8"},  # dark blue/red
    {"bg": "#0f3460", "accent": "#e94560", "text": "#ffffff", "sub": "#a8d8ea"},  # navy
    {"bg": "#2d2d2d", "accent": "#f5a623", "text": "#ffffff", "sub": "#cccccc"},  # dark/gold
    {"bg": "#1b4332", "accent": "#95d5b2", "text": "#ffffff", "sub": "#b7e4c7"},  # forest green
    {"bg": "#3d0066", "accent": "#ff6ef7", "text": "#ffffff", "sub": "#e0aaff"},  # purple
    {"bg": "#1c1c1c", "accent": "#00f5d4", "text": "#ffffff", "sub": "#aaaaaa"},  # dark/cyan
]

PIN_W, PIN_H = 1000, 1500
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "images")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def _get_font(size: int):
    """Try to load a nice font, fall back to default."""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",  # macOS fallback
    ]
    for path in font_paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def generate_pin_image(title: str, keyword: str, number: int = 10) -> str:
    """
    Creates a Pinterest-optimized vertical pin image.
    Returns the file path of the saved image.
    """
    theme = random.choice(THEMES)
    img = Image.new("RGB", (PIN_W, PIN_H), color=theme["bg"])
    draw = ImageDraw.Draw(img)

    # ── Top accent bar ────────────────────────────────────────────────────────
    draw.rectangle([0, 0, PIN_W, 12], fill=theme["accent"])
    draw.rectangle([0, PIN_H - 12, PIN_W, PIN_H], fill=theme["accent"])

    # ── "TOP 10" badge ────────────────────────────────────────────────────────
    badge_font = _get_font(52)
    badge_text = f"TOP {number}"
    draw.rounded_rectangle([60, 60, 300, 155], radius=20, fill=theme["accent"])
    draw.text((80, 75), badge_text, font=badge_font, fill="#ffffff")

    # ── "PICKS" label ─────────────────────────────────────────────────────────
    label_font = _get_font(28)
    draw.text((320, 90), "BEST PICKS", font=label_font, fill=theme["sub"])

    # ── Year badge ────────────────────────────────────────────────────────────
    year_font = _get_font(30)
    draw.rounded_rectangle([PIN_W - 170, 60, PIN_W - 40, 130], radius=15, fill=theme["sub"])
    draw.text((PIN_W - 160, 72), "2026", font=year_font, fill=theme["bg"])

    # ── Divider ───────────────────────────────────────────────────────────────
    draw.rectangle([60, 175, PIN_W - 60, 180], fill=theme["accent"])

    # ── Main title ────────────────────────────────────────────────────────────
    title_font = _get_font(62)
    title_clean = title.replace("10 Best ", "").replace(" on Amazon India 2026", "")
    wrapped = textwrap.wrap(title_clean.upper(), width=16)
    y = 220
    for line in wrapped:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        w = bbox[2] - bbox[0]
        draw.text(((PIN_W - w) / 2, y), line, font=title_font, fill=theme["text"])
        y += 80

    # ── Subtitle ──────────────────────────────────────────────────────────────
    sub_font = _get_font(36)
    sub_text = "ON AMAZON INDIA"
    bbox = draw.textbbox((0, 0), sub_text, font=sub_font)
    w = bbox[2] - bbox[0]
    draw.text(((PIN_W - w) / 2, y + 20), sub_text, font=sub_font, fill=theme["accent"])

    # ── Decorative dots ───────────────────────────────────────────────────────
    y_dots = y + 100
    for i in range(10):
        cx = 120 + i * 78
        draw.ellipse([cx - 18, y_dots, cx + 18, y_dots + 36], fill=theme["accent"] if i < 5 else theme["sub"])

    # ── Feature bullets ───────────────────────────────────────────────────────
    bullet_font = _get_font(32)
    bullets = [
        "✓  Budget-Friendly Options",
        "✓  Expert Reviewed",
        "✓  Amazon Prime Eligible",
        "✓  Best Value for Money",
        "✓  Updated for 2026",
    ]
    y_b = y_dots + 80
    for b in bullets:
        draw.text((100, y_b), b, font=bullet_font, fill=theme["sub"])
        y_b += 55

    # ── Divider ───────────────────────────────────────────────────────────────
    draw.rectangle([60, y_b + 20, PIN_W - 60, y_b + 25], fill=theme["accent"])

    # ── CTA ───────────────────────────────────────────────────────────────────
    cta_font = _get_font(40)
    cta_text = "🛒 SHOP NOW ON AMAZON"
    bbox = draw.textbbox((0, 0), cta_text, font=cta_font)
    w = bbox[2] - bbox[0]
    draw.rounded_rectangle(
        [(PIN_W - w) / 2 - 30, y_b + 50, (PIN_W + w) / 2 + 30, y_b + 120],
        radius=25, fill=theme["accent"]
    )
    draw.text(((PIN_W - w) / 2, y_b + 58), cta_text, font=cta_font, fill="#ffffff")

    # ── Blog URL watermark ────────────────────────────────────────────────────
    url_font = _get_font(24)
    blog_url = os.environ.get("BLOG_URL", "yourblog.blogspot.com")
    draw.text((60, PIN_H - 80), blog_url, font=url_font, fill=theme["sub"])

    # ── Save ──────────────────────────────────────────────────────────────────
    safe_kw = keyword.replace(" ", "_").replace("/", "_")[:40]
    filename = f"pin_{safe_kw}_{random.randint(1000,9999)}.jpg"
    filepath = os.path.join(OUTPUT_DIR, filename)
    img.save(filepath, "JPEG", quality=92)
    print(f"[image] ✅ Generated: {filename}")
    return filepath


if __name__ == "__main__":
    path = generate_pin_image(
        title="10 Best Coding Desk Gadgets on Amazon India 2026",
        keyword="coding desk gadgets"
    )
    print("Saved to:", path)
