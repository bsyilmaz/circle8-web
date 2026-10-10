# circle8 OG gorseli (Twitter/X kart onizlemesi) — Pillow
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
img = Image.new("RGB", (W, H), "#f4f5f6")
d = ImageDraw.Draw(img)

TEAL_DARK = (28, 111, 102)

def font(size, bold=False):
    for p in [r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
              r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"]:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()

# logo isareti (sonsuzluk)
import math
def lemniscate(cx, cy, a, n=200):
    pts = []
    for i in range(n + 1):
        t = 2 * math.pi * i / n
        den = 1 + math.sin(t) ** 2
        pts.append((cx + a * math.cos(t) / den, cy + a * math.sin(t) * math.cos(t) / den))
    return pts

pts = lemniscate(170, 200, 70)
d.line([(x + 6, y + 6) for x, y in pts], fill=(200, 208, 211), width=22, joint="curve")
d.line(pts, fill=TEAL_DARK, width=22, joint="curve")
d.text((260, 160), "circle8", font=font(64, bold=True), fill=(20, 24, 26))

d.text((110, 340), "Keep your parents safe.", font=font(58, bold=True), fill=(20, 24, 26))
d.text((110, 415), "Even from miles away.", font=font(58, bold=True), fill=(20, 24, 26))
d.text((110, 510), "Fall detection · Heart rate · Location · First 2,000 signups get a launch discount",
       font=font(27), fill=(92, 100, 104))

img.save("og.png")
print("og.png yazildi")
