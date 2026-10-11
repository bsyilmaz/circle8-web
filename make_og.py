# circle8 OG gorseli: urun render'i + marka + baslik (Twitter/X kart onizlemesi)
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1200, 630
BG = (233, 242, 240)          # teal-soft panel rengi
INK = (16, 20, 22)
INK2 = (82, 90, 94)
TEAL_DARK = (28, 111, 102)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def font(size, bold=False):
    for p in [r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
              r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"]:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()

# logo: sonsuzluk isareti
def lemniscate(cx, cy, a, n=200):
    pts = []
    for i in range(n + 1):
        t = 2 * math.pi * i / n
        den = 1 + math.sin(t) ** 2
        pts.append((cx + a * math.cos(t) / den, cy + a * math.sin(t) * math.cos(t) / den))
    return pts

pts = lemniscate(120, 105, 46)
d.line(pts, fill=TEAL_DARK, width=15, joint="curve")
d.text((180, 74), "circle8", font=font(46, bold=True), fill=INK)

# baslik
d.text((70, 220), "Keep your parents safe.", font=font(62, bold=True), fill=INK)
d.text((70, 300), "Even from miles away.", font=font(62, bold=True), fill=INK)
d.text((70, 405), "Fall detection  ·  Heart rate  ·  Location", font=font(30), fill=INK2)

# teklif satiri
offer_y = 500
d.rounded_rectangle([70, offer_y, 720, offer_y + 66], radius=14, fill=TEAL_DARK)
d.text((95, offer_y + 17), "First 2,000 signups get a launch discount", font=font(28, bold=True), fill=(255, 255, 255))

# urun render'i (sag taraf)
try:
    prod = Image.open("product.jpg").convert("RGBA")
    target_h = 520
    scale = target_h / prod.height
    prod = prod.resize((int(prod.width * scale), target_h), Image.LANCZOS)
    img.paste(prod, (W - prod.width - 30, 60), prod)
except Exception as e:
    print("urun gorseli alinamadi:", e)

img.save("og.png")
print("og.png yazildi")
