# circle8 ürün render: STL montajini yumusak isikla PNG'ye bas (landing page icin)
import struct
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

GOVDE = r"..\govde"

def load_stl(path):
    with open(path, "rb") as f:
        data = f.read()
    if data[:5] == b"solid" and b"facet" in data[:2000]:
        verts = []
        for line in data.decode("ascii", "ignore").splitlines():
            line = line.strip()
            if line.startswith("vertex"):
                verts.append([float(x) for x in line.split()[1:4]])
        return np.array(verts, dtype=np.float64).reshape(-1, 3, 3)
    n = struct.unpack("<I", data[80:84])[0]
    rec = np.frombuffer(data, dtype=np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")]),
                        count=n, offset=84)
    return rec["v"].astype(np.float64)

PARTS = [
    # dosya, renk (RGB 0-1)
    ("dostum_kayis.stl",         (0.784, 0.816, 0.827)),   # gümüş bant
    ("dostum_govde_alt.stl",     (0.078, 0.329, 0.302)),   # koyu teal
    ("dostum_govde_ust.stl",     (0.110, 0.435, 0.400)),   # teal gövde
    ("dostum_optik_pencere.stl", (0.055, 0.231, 0.212)),   # optik pencere
    ("dostum_buton.stl",         (0.847, 0.863, 0.875)),   # gümüş buton
    ("dostum_eptfe_membran.stl", (0.910, 0.922, 0.925)),
]

tris = []
cols = []
for fname, rgb in PARTS:
    try:
        t = load_stl(f"{GOVDE}\\{fname}")
    except FileNotFoundError:
        print("yok:", fname)
        continue
    tris.append(t)
    cols.append(np.tile(rgb, (len(t), 1)))
    print(f"{fname}: {len(t)} ucgen")

T = np.concatenate(tris, axis=0)
C = np.concatenate(cols, axis=0)

# --- merkezle ---
center = T.reshape(-1, 3).mean(axis=0)
T = T - center

# --- donus: kamera acisi (yaw + pitch) ---
yaw = np.deg2rad(32)
pitch = np.deg2rad(20)
Rz = np.array([[np.cos(yaw), -np.sin(yaw), 0], [np.sin(yaw), np.cos(yaw), 0], [0, 0, 1]])
Rx = np.array([[1, 0, 0], [0, np.cos(pitch), -np.sin(pitch)], [0, np.sin(pitch), np.cos(pitch)]])
R = Rx @ Rz
T = T @ R.T

# --- isiklandirma ---
light = np.array([-0.45, -0.55, 0.70])
light = light / np.linalg.norm(light)
n = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0])
ln = np.linalg.norm(n, axis=1)
ln[ln == 0] = 1
n = n / ln[:, None]
flip = (n * np.array([0, 0, 1])).sum(axis=1) < 0
n[flip] *= -1
inten = 0.42 + 0.58 * np.clip((n * light).sum(axis=1), 0, 1)
shade = np.clip(C * inten[:, None], 0, 1)

# --- projeksiyon + derinlik sirasi ---
depth = T[:, :, 2].mean(axis=1)
order = np.argsort(depth)      # uzak olan once
pts = T[order][:, :, :2]

fig, ax = plt.subplots(figsize=(9, 9), dpi=140)
ax.set_axis_off()
fig.patch.set_alpha(0)
ax.patch.set_alpha(0)

pc = PolyCollection(pts, facecolors=shade[order], edgecolors="none", antialiaseds=True)
ax.add_collection(pc)
ax.autoscale_view()
ax.set_aspect("equal")
pad = 0.05
xmin, xmax = pts[:, :, 0].min(), pts[:, :, 0].max()
ymin, ymax = pts[:, :, 1].min(), pts[:, :, 1].max()
w, h = xmax - xmin, ymax - ymin
ax.set_xlim(xmin - w * pad, xmax + w * pad)
ax.set_ylim(ymin - h * pad - h * 0.12, ymax + h * pad)

out = "product.png"
plt.savefig(out, transparent=True, bbox_inches="tight", pad_inches=0.05)
print("yazildi:", out)
