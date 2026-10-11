# Aday acilari yan yana uret (karsilastirma)
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
    ("dostum_kayis.stl",         (0.72, 0.76, 0.78)),
    ("dostum_govde_alt.stl",     (0.078, 0.329, 0.302)),
    ("dostum_govde_ust.stl",     (0.110, 0.435, 0.400)),
    ("dostum_optik_pencere.stl", (0.045, 0.185, 0.170)),
    ("dostum_buton.stl",         (0.80, 0.82, 0.83)),
    ("dostum_eptfe_membran.stl", (0.88, 0.89, 0.90)),
]

tris, cols = [], []
for fname, rgb in PARTS:
    try:
        t = load_stl(f"{GOVDE}\\{fname}")
    except FileNotFoundError:
        continue
    tris.append(t)
    cols.append(np.tile(rgb, (len(t), 1)))

T0 = np.concatenate(tris, axis=0)
C0 = np.concatenate(cols, axis=0)
T0 = T0 - T0.reshape(-1, 3).mean(axis=0)

def render(ax, yaw_deg, pitch_deg, title=""):
    yaw, pitch = np.deg2rad(yaw_deg), np.deg2rad(pitch_deg)
    Rz = np.array([[np.cos(yaw), -np.sin(yaw), 0], [np.sin(yaw), np.cos(yaw), 0], [0, 0, 1]])
    Rx = np.array([[1, 0, 0], [0, np.cos(pitch), -np.sin(pitch)], [0, np.sin(pitch), np.cos(pitch)]])
    T = T0 @ (Rx @ Rz).T

    light = np.array([-0.4, -0.5, 0.75]); light /= np.linalg.norm(light)
    n = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0])
    ln = np.linalg.norm(n, axis=1); ln[ln == 0] = 1
    n = n / ln[:, None]
    flip = (n * np.array([0, 0, 1])).sum(axis=1) < 0
    n[flip] *= -1
    inten = 0.5 + 0.5 * np.clip((n * light).sum(axis=1), 0, 1)
    shade = np.clip(C0 * inten[:, None], 0, 1)

    depth = T[:, :, 2].mean(axis=1)
    order = np.argsort(depth)
    pts = T[order][:, :, :2]
    ax.add_collection(PolyCollection(pts, facecolors=shade[order], edgecolors="none"))
    xmin, xmax = pts[:, :, 0].min(), pts[:, :, 0].max()
    ymin, ymax = pts[:, :, 1].min(), pts[:, :, 1].max()
    w, h = xmax - xmin, ymax - ymin
    ax.set_xlim(xmin - w * 0.10, xmax + w * 0.10)
    ax.set_ylim(ymin - h * 0.12, ymax + h * 0.12)
    ax.set_aspect("equal"); ax.set_axis_off()
    ax.set_title(title, fontsize=11)

ANGLES = [(32, 20), (32, -20), (55, 15), (-25, 15)]
fig, axes = plt.subplots(2, 2, figsize=(11, 11), dpi=110)
for ax, (y, p) in zip(axes.ravel(), ANGLES):
    render(ax, y, p, f"yaw={y} pitch={p}")
plt.tight_layout()
plt.savefig("compare.png", transparent=False, facecolor="#f4f5f6", bbox_inches="tight")
print("compare.png yazildi")
