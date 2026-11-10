#!/usr/bin/env python3
"""Paint the Emboldened Birth botanical artwork: original watercolour eucalyptus.

Run from the repository root:

    python3 tools/generate-botanicals.py               # writes assets/img/botanical-*.webp
    python3 tools/generate-botanicals.py --preview     # also writes previews on ivory
    python3 tools/generate-botanicals.py --scale 3     # larger masters, e.g. for print

Needs Python 3 with numpy, Pillow (with WebP support) and pycairo.

How it paints
-------------
Every wash, stem and seed pod adds optical density per colour channel (a
Beer-Lambert pigment model), so overlapping washes darken the way real
watercolour glazes do. Each leaf gets an uneven wash, pigment pooled at its
edges, a lifted midrib, paper granulation, and a colour shift from base to
tip. The finished painting is saved as a transparent WebP calibrated for the
site's warm ivory ground (#FAF6EC).

Each piece has a fixed seed, so a run always paints the same pictures.
Change a seed (or a composition below) to paint a new variation.
"""
import argparse
import math
from pathlib import Path

import cairo
import numpy as np
from PIL import Image

PAPER = "#FAF6EC"

# Full-strength pigment colours (what a density of 1.0 looks like on white).
PIGMENT = {
    "blue_green": "#4F7064",
    "sage": "#6C8A6F",
    "pale_sage": "#98AE95",
    "olive": "#66793F",
    "yellow_olive": "#9EA35A",
    "deep": "#3D5948",
    "stem": "#7A5A3F",
    "stem_green": "#5F7350",
    "pod": "#76623F",
    "rose": "#C08479",
    "terracotta": "#B26F57",
    "copper": "#9A5B33",
    "graphite": "#5F574F",
}

ROUND_PAIRS = [
    ("blue_green", "pale_sage"),
    ("sage", "pale_sage"),
    ("blue_green", "sage"),
    ("sage", "yellow_olive"),
    ("deep", "sage"),
]
WILLOW_PAIRS = [
    ("olive", "yellow_olive"),
    ("sage", "yellow_olive"),
    ("olive", "sage"),
    ("blue_green", "olive"),
]


# Colour ---------------------------------------------------------------------

def srgb_to_linear(c):
    c = np.asarray(c, dtype=np.float32)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def linear_to_srgb(c):
    c = np.clip(c, 0.0, 1.0)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * np.power(c, 1 / 2.4) - 0.055)


def hex_rgb(value):
    value = value.lstrip("#")
    return np.array([int(value[i:i + 2], 16) / 255 for i in (0, 2, 4)], dtype=np.float32)


def absorbance(name):
    """Optical density per channel that paints this pigment's colour at density 1."""
    lin = srgb_to_linear(hex_rgb(PIGMENT[name]))
    return (-np.log(np.clip(lin, 1e-4, 1.0))).astype(np.float32)


# Noise and blur -------------------------------------------------------------

def value_noise(h, w, cell, rng):
    gh, gw = int(h / cell) + 4, int(w / cell) + 4
    grid = rng.random((gh, gw), dtype=np.float32)
    size = (max(w, round(gw * cell)), max(h, round(gh * cell)))
    return np.asarray(Image.fromarray(grid).resize(size, Image.BICUBIC), np.float32)[:h, :w]


def fbm(h, w, cell, octaves, rng, gain=0.5):
    total = np.zeros((h, w), np.float32)
    amp, norm = 1.0, 0.0
    for octave in range(octaves):
        total += amp * value_noise(h, w, max(cell / 2 ** octave, 1.2), rng)
        norm += amp
        amp *= gain
    total /= norm
    lo, hi = np.percentile(total, [1, 99])
    return np.clip((total - lo) / (hi - lo + 1e-6), 0, 1)


def smooth1d(n, rng, knots=7):
    """Low-frequency wobble in roughly [-1, 1] along n samples."""
    ctrl = rng.uniform(-1, 1, knots)
    x = np.linspace(0, knots - 1, n)
    y = np.interp(x, np.arange(knots), ctrl)
    k = max(1, n // 10)
    return np.convolve(np.pad(y, k, mode="edge"), np.ones(2 * k + 1) / (2 * k + 1), "valid").astype(np.float32)


def _box(a, r, axis):
    pad = [(0, 0)] * a.ndim
    pad[axis] = (r + 1, r)
    c = np.cumsum(np.pad(a, pad, mode="edge"), axis=axis, dtype=np.float64)
    n = a.shape[axis]
    hi = np.take(c, np.arange(2 * r + 1, 2 * r + 1 + n), axis=axis)
    lo = np.take(c, np.arange(0, n), axis=axis)
    return ((hi - lo) / (2 * r + 1)).astype(np.float32)


def blur(a, sigma):
    """Gaussian blur approximated by three box blurs per axis."""
    if sigma < 0.3:
        return a
    r = max(1, int(round((math.sqrt(4 * sigma * sigma + 1) - 1) / 2)))
    for axis in (0, 1):
        for _ in range(3):
            a = _box(a, r, axis)
    return a


# Rasterising ------------------------------------------------------------------

def raster(draw, w, h):
    surface = cairo.ImageSurface(cairo.FORMAT_A8, w, h)
    ctx = cairo.Context(surface)
    ctx.set_antialias(cairo.ANTIALIAS_GOOD)
    draw(ctx)
    surface.flush()
    buf = np.frombuffer(surface.get_data(), np.uint8).reshape(h, surface.get_stride())[:, :w]
    return buf.astype(np.float32) / 255.0


def fill_path(points):
    def draw(ctx):
        ctx.move_to(*points[0])
        for p in points[1:]:
            ctx.line_to(*p)
        ctx.close_path()
        ctx.fill()
    return draw


def stroke_path(points, width, closed=False):
    def draw(ctx):
        ctx.set_line_width(width)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.move_to(*points[0])
        for p in points[1:]:
            ctx.line_to(*p)
        if closed:
            ctx.close_path()
        ctx.stroke()
    return draw


def toward(angle, target, amount):
    diff = (target - angle + math.pi) % (2 * math.pi) - math.pi
    return angle + diff * min(max(amount, 0.0), 1.0)


# Painter --------------------------------------------------------------------

class Painter:
    """A sheet of paper that accumulates pigment density.

    Coordinates are canvas pixels. A margin around the sheet lets branches
    start off-canvas (for corner pieces) and is cropped away on export.
    """

    def __init__(self, width, height, seed, unit=1.0, margin=None):
        self.w, self.h = width, height
        self.u = unit  # scale factor for sizes written at 1x
        self.m = margin if margin is not None else int(420 * unit)
        self.rng = np.random.default_rng(seed)
        H, W = height + 2 * self.m, width + 2 * self.m
        self.D = np.zeros((H, W, 3), np.float32)
        self.low = fbm(H, W, 110 * unit, 3, self.rng)
        self.mid = fbm(H, W, 26 * unit, 3, self.rng)
        self.grain = fbm(H, W, 2.6 * unit, 2, self.rng)

    # -- primitives -------------------------------------------------------

    def _bounds(self, pts, pad):
        H, W = self.D.shape[:2]
        x0 = max(0, int(math.floor(pts[:, 0].min() + self.m - pad)))
        y0 = max(0, int(math.floor(pts[:, 1].min() + self.m - pad)))
        x1 = min(W, int(math.ceil(pts[:, 0].max() + self.m + pad)))
        y1 = min(H, int(math.ceil(pts[:, 1].max() + self.m + pad)))
        return x0, y0, x1, y1

    def wash(self, poly, axis, width, pigments, strength, edge=0.8, shade=0.25,
             vein_line=None, vein=0.0, wet=0.0, grain=0.4, soften=0.7):
        """Lay one watercolour wash inside a polygon."""
        rng = self.rng
        poly = np.asarray(poly, np.float32)
        x0, y0, x1, y1 = self._bounds(poly, int(width * 0.5 + 8))
        if x1 - x0 < 2 or y1 - y0 < 2:
            return
        off = np.array([x0 - self.m, y0 - self.m], np.float32)
        pw, ph = x1 - x0, y1 - y0
        m = raster(fill_path(poly - off), pw, ph)
        if m.max() <= 0:
            return
        m = blur(m, soften * self.u)
        if wet > 0:
            m = (1 - wet) * m + wet * blur(m, 0.05 * width + 1.5 * self.u)
        rim = np.clip(m - blur(m, max(1.2 * self.u, 0.09 * width)), 0, None) * 2.0
        low = self.low[y0:y1, x0:x1]
        mid = self.mid[y0:y1, x0:x1]
        gr = self.grain[y0:y1, x0:x1]
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        bx, by = np.asarray(axis[0], np.float32) + self.m
        tx, ty = np.asarray(axis[1], np.float32) + self.m
        ax, ay = tx - bx, ty - by
        l2 = ax * ax + ay * ay + 1e-6
        t = np.clip(((xx - bx) * ax + (yy - by) * ay) / l2, 0, 1)
        d = m * strength * (0.55 + 0.45 * low + 0.3 * (mid - 0.5))
        if shade:
            side = ((xx - bx) * ay - (yy - by) * ax) / math.sqrt(l2) / (0.5 * width + 1e-6)
            d *= 1 + shade * np.tanh(2.4 * side * rng.choice((-1.0, 1.0)))
        d += m * edge * np.power(rim, 1.25) * (0.5 + mid)
        if vein_line is not None and vein > 0 and len(vein_line) > 1:
            vm = raster(stroke_path(vein_line - off, max(1.0 * self.u, 0.05 * width)), pw, ph)
            d *= 1 - vein * blur(vm, 0.7 * self.u)
        d *= (1 - grain / 2) + grain * gr
        mix = np.clip(t ** 1.1 + 0.3 * (mid - 0.5), 0, 1)[..., None]
        k_a, k_b = absorbance(pigments[0]), absorbance(pigments[1])
        self.D[y0:y1, x0:x1] += d[..., None] * (k_a * (1 - mix) + k_b * mix)

    def line(self, pts, width, pigment, density, broken=0.0, closed=False):
        """A fine pencil or ink line; `broken` opens gaps along it."""
        pts = np.asarray(pts, np.float32)
        x0, y0, x1, y1 = self._bounds(pts, width * 2 + 4)
        if x1 - x0 < 2 or y1 - y0 < 2:
            return
        off = np.array([x0 - self.m, y0 - self.m], np.float32)
        m = blur(raster(stroke_path(pts - off, width, closed), x1 - x0, y1 - y0), 0.45 * self.u)
        if broken:
            m *= np.clip((self.mid[y0:y1, x0:x1] - broken) * 4, 0, 1)
        m *= 0.7 + 0.6 * self.grain[y0:y1, x0:x1]
        self.D[y0:y1, x0:x1] += (m * density)[..., None] * absorbance(pigment)

    def lift(self, center, r, amount):
        """Lift pigment with a damp brush (a soft highlight)."""
        cx, cy = center[0] + self.m, center[1] + self.m
        x0, y0 = int(max(0, cx - 2 * r)), int(max(0, cy - 2 * r))
        x1, y1 = int(min(self.D.shape[1], cx + 2 * r)), int(min(self.D.shape[0], cy + 2 * r))
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        g = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * (0.6 * r) ** 2))
        self.D[y0:y1, x0:x1] *= (1 - amount * g)[..., None]

    # -- botanical elements -------------------------------------------------

    def leaf(self, base, angle, length, width, shape="round", bend=0.0,
             pigments=("blue_green", "pale_sage"), strength=0.55, edge=0.8, shade=0.25,
             vein=0.4, wet=0.0, glaze=0.0, pencil=0.0):
        rng = self.rng
        n = 80
        t = np.linspace(0, 1, n, dtype=np.float32)
        if shape == "round":
            half = 0.5 * width * np.sqrt(np.clip(1 - (2 * t - 1) ** 2, 0, 1)) * (1 - 0.2 * t ** 4)
        elif shape == "oval":
            half = 0.5 * width * np.clip(np.sin(np.pi * t), 0, None) ** 0.8 * (1 - 0.12 * t)
        else:  # lance
            half = 0.5 * width * np.clip(np.sin(np.pi * t ** 0.8), 0, None) ** 0.95 * (1 - 0.32 * t)
        mx = t * length
        my = bend * length * 0.35 * t ** 2
        dx, dy = np.gradient(mx), np.gradient(my)
        ln = np.hypot(dx, dy) + 1e-6
        nx, ny = -dy / ln, dx / ln
        jl = 1 + 0.07 * smooth1d(n, rng)
        jr = 1 + 0.07 * smooth1d(n, rng)
        left = np.stack([mx + nx * half * jl, my + ny * half * jl], 1)
        right = np.stack([mx - nx * half * jr, my - ny * half * jr], 1)
        c, s = math.cos(angle), math.sin(angle)
        rot = np.array([[c, -s], [s, c]], np.float32)
        origin = np.asarray(base, np.float32)

        def to_canvas(p):
            return p @ rot.T + origin

        poly = to_canvas(np.concatenate([left, right[::-1]]))
        midrib = to_canvas(np.stack([mx, my], 1))
        self.wash(poly, (midrib[0], midrib[-1]), width, pigments, strength, edge, shade,
                  vein_line=midrib[3:int(n * 0.86)], vein=vein, wet=wet)
        if glaze > 0:
            k = rng.choice((-1.0, 1.0))
            sel = slice(int(n * 0.1), int(n * 0.9))
            o = k * 0.24 * half
            gl = np.stack([mx + nx * (o + 0.55 * half), my + ny * (o + 0.55 * half)], 1)[sel]
            gr = np.stack([mx + nx * (o - 0.55 * half), my + ny * (o - 0.55 * half)], 1)[sel]
            gpoly = to_canvas(np.concatenate([gl, gr[::-1]]))
            self.wash(gpoly, (midrib[0], midrib[-1]), width * 0.6, pigments[::-1], glaze,
                      edge=0.6, shade=0, wet=0.35)
        if pencil > 0:
            jitter = rng.normal(0, 0.01 * width + 0.6 * self.u, 2).astype(np.float32)
            self.line(poly + jitter, 0.85 * self.u, "graphite", pencil, broken=0.42, closed=True)
            self.line(midrib[2:int(n * 0.8)] + jitter, 0.75 * self.u, "graphite", pencil * 0.7, broken=0.5)

    def stem(self, pts, w0, w1, pigments=("stem", "stem_green"), strength=0.85):
        pts = np.asarray(pts, np.float32)
        n = len(pts)
        if n < 2:
            return
        t = np.linspace(0, 1, n, dtype=np.float32)
        wid = (w0 + (w1 - w0) * t) * (1 + 0.15 * smooth1d(n, self.rng)) * self.u
        d = np.gradient(pts, axis=0)
        ln = np.hypot(d[:, 0], d[:, 1]) + 1e-6
        nrm = np.stack([-d[:, 1] / ln, d[:, 0] / ln], 1)
        poly = np.concatenate([pts + nrm * (wid / 2)[:, None], (pts - nrm * (wid / 2)[:, None])[::-1]])
        self.wash(poly, (pts[0], pts[-1]), max(w0, 2.5) * 3 * self.u, pigments, strength,
                  edge=0.35, shade=0, grain=0.3, soften=0.5)

    def ellipse(self, center, rx, ry, rot):
        n = 44
        th = np.linspace(0, 2 * np.pi, n, endpoint=False)
        r = 1 + 0.07 * smooth1d(n, self.rng)
        x, y = rx * r * np.cos(th), ry * r * np.sin(th)
        c, s = math.cos(rot), math.sin(rot)
        return np.stack([x * c - y * s + center[0], x * s + y * c + center[1]], 1).astype(np.float32)

    def pod(self, center, r, up):
        """A seeded-eucalyptus seed cup: a pale body with a darker rim and mouth."""
        rng = self.rng
        center = np.asarray(center, np.float32)
        body = self.ellipse(center, r, r * rng.uniform(0.85, 1.0), up)
        axis = (center - r * np.array([math.cos(up), math.sin(up)]), center + r * np.array([math.cos(up), math.sin(up)]))
        self.wash(body, axis, 2 * r, ("pod", "olive"), rng.uniform(0.22, 0.32), edge=1.1, shade=0.35, grain=0.5)
        mouth_c = center + 0.45 * r * np.array([math.cos(up), math.sin(up)])
        mouth = self.ellipse(mouth_c, 0.42 * r, 0.3 * r, up + math.pi / 2)
        self.wash(mouth, axis, r, ("pod", "pod"), 0.42, edge=0.5, shade=0, grain=0.3)

    def berry(self, center, r, pigments=("rose", "terracotta")):
        rng = self.rng
        center = np.asarray(center, np.float32)
        body = self.ellipse(center, r, r * rng.uniform(0.9, 1.0), rng.uniform(0, math.pi))
        axis = (center + [-r, -r], center + [r, r])
        self.wash(body, axis, 2 * r, pigments, rng.uniform(0.3, 0.42), edge=0.9, shade=0.3, grain=0.4)
        self.lift(center + np.array([-0.35 * r, -0.35 * r]), 0.45 * r, 0.55)

    def branch(self, start, heading, length, kind="round", curl=0.0, droop=0.0, size=60.0,
               stem_w=(5.0, 1.4), strength=0.55, skip=0.1, pods=0, berries=0, glaze=0.3,
               pencil=0.0, start_u=None, pairs=None, sag=0.0, root=None):
        """A eucalyptus stem with leaves.

        kind: "round" (silver-dollar pairs), "baby" (small round leaves),
        "willow" (alternate narrow leaves) or "seeded" (narrow leaves + seed cups).
        heading: degrees, 0 = right, 90 = down. curl: total degrees of clockwise turn.
        sag: how strongly the stem bends down under its own weight (0-1).
        root: optional function that takes the stem's path and returns the path
        to paint instead, e.g. to run the stem down through a tied bundle. It
        must not use self.rng, so the leaves paint exactly as without it.
        """
        rng = self.rng
        u_ = self.u
        size, length = size * u_, length * u_
        step = 2.5 * u_
        n = max(6, int(length / step))
        a = math.radians(heading)
        wobble = smooth1d(n, rng) * 0.0025
        pts = [np.asarray(start, np.float32)]
        for i in range(n):
            a += math.radians(curl) / n + wobble[i]
            if sag:
                a = toward(a, math.pi / 2, sag * 2.2 / n)
            pts.append(pts[-1] + step * np.array([math.cos(a), math.sin(a)], np.float32))
        pts = np.array(pts)
        self.stem(root(pts) if root is not None else pts, *stem_w)

        def tangent(i):
            i = min(max(i, 1), len(pts) - 2)
            d = pts[i + 1] - pts[i - 1]
            return math.atan2(d[1], d[0])

        def pick(choices):
            return choices[int(rng.integers(len(choices)))]

        if kind in ("round", "baby"):
            u = start_u if start_u is not None else rng.uniform(0.05, 0.1)
            while u < 0.96:
                i = int(u * n)
                sz = size * (1 - 0.6 * u ** 1.3) * rng.uniform(0.86, 1.1)
                tg = tangent(i)
                for side in (-1, 1):
                    if rng.random() < skip:
                        continue
                    spread = rng.uniform(50, 80) if kind == "round" else rng.uniform(60, 95)
                    ang = tg + side * math.radians(spread)
                    ang = toward(ang, math.pi / 2, droop * rng.uniform(0.2, 1.0))
                    pet = sz * (rng.uniform(0.06, 0.18) if kind == "round" else 0.03)
                    base = pts[i] + pet * np.array([math.cos(ang), math.sin(ang)], np.float32)
                    if pet > 3 * u_:
                        self.stem(np.linspace(pts[i], base, 6), 1.6, 1.2, strength=0.7)
                    self.leaf(base, ang, sz * rng.uniform(0.95, 1.12), sz * rng.uniform(0.7, 1.0),
                              "oval" if rng.random() < 0.22 else "round",
                              bend=rng.uniform(-0.3, 0.3), pigments=pick(pairs or ROUND_PAIRS),
                              strength=strength * rng.uniform(0.5, 1.2), edge=rng.uniform(0.5, 0.95),
                              shade=rng.uniform(0.1, 0.35), vein=rng.uniform(0.25, 0.5),
                              wet=rng.uniform(0, 0.5), glaze=glaze * rng.random() * (rng.random() < 0.5),
                              pencil=pencil)
                u += sz * rng.uniform(0.85, 1.15) / length * (0.75 if kind == "baby" else 1.0)
        else:  # willow / seeded: alternate narrow leaves
            u = start_u if start_u is not None else rng.uniform(0.06, 0.12)
            side = rng.choice((-1, 1))
            gap = (0.45, 0.7) if kind == "willow" else (0.7, 1.0)
            while u < 0.95:
                i = int(u * n)
                tg = tangent(i)
                sz = size * (1 - 0.45 * u) * rng.uniform(0.85, 1.12)
                ang = tg + side * math.radians(rng.uniform(22, 42))
                ang = toward(ang, math.pi / 2, droop * rng.uniform(0.3, 1.0))
                if rng.random() >= skip:
                    self.leaf(pts[i], ang, sz * rng.uniform(1.8, 2.4), sz * rng.uniform(0.3, 0.4), "lance",
                              bend=side * rng.uniform(0.05, 0.45), pigments=pick(pairs or WILLOW_PAIRS),
                              strength=strength * rng.uniform(0.7, 1.2), edge=rng.uniform(0.5, 0.9),
                              shade=rng.uniform(0.1, 0.3), vein=rng.uniform(0.3, 0.55),
                              wet=rng.uniform(0, 0.4), glaze=glaze * rng.random() * (rng.random() < 0.4),
                              pencil=pencil)
                side = -side
                u += sz * rng.uniform(*gap) / length

        # Seed cups and berries hang from short side stalks.
        for count, painter in ((pods, "pods"), (berries, "berries")):
            for _ in range(count):
                u = rng.uniform(0.3, 0.88)
                i = int(u * n)
                tg = tangent(i)
                side = rng.choice((-1, 1))
                ang = toward(tg + side * math.radians(rng.uniform(35, 70)), math.pi / 2, 0.35)
                stalk = rng.uniform(14, 26) * u_
                hub = pts[i] + stalk * np.array([math.cos(ang), math.sin(ang)], np.float32)
                self.stem(np.linspace(pts[i], hub, 8), 1.7, 1.2, strength=0.75)
                for _ in range(int(rng.integers(4, 8))):
                    sa = ang + rng.uniform(-1.2, 1.2)
                    sl = rng.uniform(9, 22) * u_
                    tip = hub + sl * np.array([math.cos(sa), math.sin(sa)], np.float32)
                    self.stem(np.linspace(hub, tip, 5), 1.2, 1.0, strength=0.7)
                    r = rng.uniform(7.0, 9.5) * u_ * (1.1 if painter == "berries" else 1.0)
                    if painter == "pods":
                        self.pod(tip, r, sa)
                    else:
                        self.berry(tip, r)

        # A tiny pair of new leaves closes the tip.
        tg = tangent(len(pts) - 2)
        for side in (-1, 1):
            ang = tg + side * math.radians(rng.uniform(18, 35))
            self.leaf(pts[-1], ang, size * 0.28, size * (0.2 if kind in ("round", "baby") else 0.09),
                      "oval", pigments=("sage", "yellow_olive"), strength=strength * 0.9,
                      edge=0.6, shade=0.1, vein=0.0, pencil=pencil * 0.6)
        return pts

    def twine(self, center, radius, wraps=5, pitch=3.9):
        """Copper twine wound tightly round a bundle of stems, knotted at the
        front, with two loose ends. The stems are lifted under each turn first,
        so the twine reads as lying on top of them."""
        rng = self.rng
        u = self.u
        cx, cy = center
        r, pitch = radius * u, pitch * u
        top = cy - wraps * pitch / 2
        xs = np.linspace(-r, r, 28, dtype=np.float32)
        front = np.sqrt(np.clip(1 - (xs / r) ** 2, 0, 1))
        turns = []
        for k in range(wraps):
            # Seen from slightly above, each turn dips at the front of the
            # bundle and climbs gently round it, and narrows where it turns away.
            mid = top + (k + 0.5) * pitch + 0.09 * xs + 1.4 * u * (front - 0.6) + rng.normal(0, 0.25 * u)
            half = 0.46 * pitch * (0.72 + 0.28 * front)
            spine = np.stack([cx + xs, mid], 1)
            outline = np.concatenate([np.stack([cx + xs, mid - half], 1),
                                      np.stack([cx + xs, mid + half], 1)[::-1]])
            turns.append((outline, spine))

        for outline, _ in turns:
            self.lift_under(fill_path, outline, 0.85)
        for outline, spine in turns:
            # The lifted line along each turn is its highlight, so it reads as cord.
            self.wash(outline, (spine[0], spine[-1]), pitch, ("copper", "terracotta"), rng.uniform(0.4, 0.5),
                      edge=0.9, shade=0.3, vein_line=spine - np.array([0, 0.3 * pitch], np.float32),
                      vein=0.5, grain=0.5, soften=0.5)

        knot = np.array([cx + 0.3 * r, top + 0.55 * wraps * pitch], np.float32)
        # Two loose ends: one falls away to the right, clear of the stems; the
        # other hangs in front of them. Each has frayed fibres at its tip.
        for reach, fall, sway in ((26, 56, 1.8), (-13, 68, 2.4)):
            s = np.linspace(0, 1, 40, dtype=np.float32)
            x = knot[0] + reach * u * (0.7 * s + 0.3 * s ** 2) + sway * u * np.sin(3.2 * s)
            y = knot[1] + 2 * u + fall * u * s
            end = np.stack([x, y], 1)
            self.lift_under(lambda pts: stroke_path(pts, 3.2 * u), end, 0.75)
            self.stem(end, 3.1, 2.1, pigments=("copper", "terracotta"), strength=0.58)
            tip, d = end[-1], end[-1] - end[-4]
            a = math.atan2(d[1], d[0])
            for spread in (-0.35, 0.05, 0.4):
                fibre = rng.uniform(3.5, 6) * u
                self.line(np.stack([tip, tip + fibre * np.array([math.cos(a + spread), math.sin(a + spread)],
                                                                np.float32)]), 0.7 * u, "copper", 0.4)
        for dx, dy, rx, ry, rot in ((0, 0, 5.6, 4.3, 0.5), (3.4, 2.9, 4.1, 3.3, -0.4)):
            c = knot + np.array([dx, dy], np.float32) * u
            body = self.ellipse(c, rx * u, ry * u, rot)
            self.lift_under(fill_path, body, 0.7)
            self.wash(body, (c - [rx * u, 0], c + [rx * u, 0]), 2 * rx * u, ("copper", "terracotta"), 0.62,
                      edge=1.0, shade=0.35, grain=0.5, soften=0.5)

    def lift_under(self, shape, pts, amount):
        """Lift pigment under a shape before painting it, so it reads as lying
        on top. `shape` is fill_path or a stroke_path-like function of points."""
        pts = np.asarray(pts, np.float32)
        x0, y0, x1, y1 = self._bounds(pts, 6 * self.u)
        off = np.array([x0 - self.m, y0 - self.m], np.float32)
        cover = blur(raster(shape(pts - off), x1 - x0, y1 - y0), 0.6 * self.u)
        self.D[y0:y1, x0:x1] *= (1 - amount * cover)[..., None]

    # -- output ---------------------------------------------------------------

    def export(self, path, preview=None, quality=88, anchor=None, aspect=None):
        """Save as transparent WebP.

        anchor="tr"/"bl" trims empty space but keeps that corner (for pieces that
        bleed off an edge). aspect=(w, h) crops around the painting with an even
        margin at that aspect ratio (for framed pieces).
        """
        D = self.D[self.m:self.m + self.h, self.m:self.m + self.w]
        ink = np.argwhere(D.max(axis=2) > 0.01)
        (top, left), (bottom, right) = ink.min(0), ink.max(0) + 1
        if anchor:
            pad = int(12 * self.u)
            if anchor == "tr":
                D = D[:min(self.h, bottom + pad), max(0, left - pad):]
            else:
                D = D[max(0, top - pad):, :min(self.w, right + pad)]
        elif aspect:
            margin = 0.07 * max(right - left, (bottom - top) * aspect[0] / aspect[1])
            w = (right - left) + 2 * margin
            h = (bottom - top) + 2 * margin
            if w / h < aspect[0] / aspect[1]:
                w = h * aspect[0] / aspect[1]
            else:
                h = w * aspect[1] / aspect[0]
            cx, cy = (left + right) / 2, (top + bottom) / 2
            x0, y0 = int(round(cx - w / 2)), int(round(cy - h / 2))
            W, H = int(round(w)), int(round(h))
            framed = np.zeros((H, W, 3), np.float32)
            sx0, sy0 = max(0, x0), max(0, y0)
            sx1, sy1 = min(D.shape[1], x0 + W), min(D.shape[0], y0 + H)
            framed[sy0 - y0:sy1 - y0, sx0 - x0:sx1 - x0] = D[sy0:sy1, sx0:sx1]
            D = framed
        # What the painting looks like on ivory paper, in display (sRGB) values.
        T = np.exp(-D)
        target = linear_to_srgb(srgb_to_linear(hex_rgb(PAPER)) * T)
        # Browsers blend transparency in sRGB, so un-blend there: the least alpha
        # (and matching colour) that reproduces the painting over the ivory ground.
        paper = hex_rgb(PAPER)
        alpha = np.clip((1 - target / paper).max(axis=2), 0, 1)
        safe = np.maximum(alpha, 1e-4)[..., None]
        colour = np.clip((target - (1 - alpha[..., None]) * paper) / safe, 0, 1)
        colour[alpha < 1 / 255] = 0
        rgba = np.dstack([colour * 255, alpha * 255]).round().astype(np.uint8)
        Image.fromarray(rgba, "RGBA").save(path, "WEBP", quality=quality, alpha_quality=100, method=6)
        self.size = rgba.shape[1], rgba.shape[0]
        if preview:
            Image.fromarray((target * 255).round().astype(np.uint8), "RGB").save(preview)


# Compositions -------------------------------------------------------------------

def _bezier(p0, p1, p2, p3, step):
    n = max(4, int(np.hypot(*(p3 - p0)) / step))
    s = np.linspace(0, 1, n, dtype=np.float32)[:, None]
    return (1 - s) ** 3 * p0 + 3 * (1 - s) ** 2 * s * p1 + 3 * (1 - s) * s ** 2 * p2 + s ** 3 * p3


def tied_bundle(stems, tie, scale, waist=9.0, band=22.0):
    """A hand-tied bunch: every stem passes through the tie in its own place.

    Above the twine each stem flares out to its branch; below, it splays a
    little to a cut end of its own length. Returns (roots, ends): `roots` for
    Painter.branch(root=...), and the stem ends below the tie as
    (path, widths) to paint after the branches. The two halves meet under
    the twine, which hides the join. Uses its own random numbers, so the
    branches' leaves paint exactly as they would without it.
    """
    rng = np.random.default_rng(1011)
    step = 2.5 * scale
    order = np.argsort([heading for _, heading, *_ in stems], kind="stable")
    slots = np.linspace(-waist, waist, len(stems)) * scale
    neck_y = tie[1] - (0.5 * band - 2) * scale  # just inside the twine's top edge
    roots, ends = [None] * len(stems), [None] * len(stems)
    for place, i in enumerate(order):
        _, heading, length, _, options = stems[i]
        lean = heading + 90  # degrees from upright; negative leans left
        x = tie[0] + slots[place]
        middle = np.array([x, tie[1]], np.float32)

        # Below the tie: nearly straight, bowed a touch outward, cut at its own length.
        down = math.radians(90 - 0.22 * lean + rng.normal(0, 2.5))
        sink = np.array([math.cos(down), math.sin(down)], np.float32)
        cut = middle + rng.uniform(62, 92) * scale * sink
        outward = np.array([-sink[1], sink[0]], np.float32)
        if outward[0] * lean < 0:
            outward = -outward
        s = np.linspace(0, 1, max(4, int(np.hypot(*(middle - cut)) / step)), dtype=np.float32)[:, None]
        w0 = options.get("stem_w", (5.0, 1.4))[0]
        ends[i] = (middle + s * (cut - middle) + 1.5 * scale * np.sin(np.pi * s) * outward, (0.9 * w0, 0.95 * w0))

        # Above the tie: up out of the twine, then curving into the branch below its first leaves.
        join = 0.8 * options.get("start_u", 0.1) * length * scale
        roots[i] = _tied_root(middle, np.array([x, neck_y], np.float32), lean, join, step)
    return roots, ends


def _tied_root(middle, neck, lean, join, step):
    rise = math.radians(-90 + 0.6 * lean)
    rise = np.array([math.cos(rise), math.sin(rise)], np.float32)

    def root(pts):
        along = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(pts, axis=0).T))])
        k = int(np.clip(np.searchsorted(along, join), 2, len(pts) - 3))
        tangent = pts[k + 1] - pts[k - 1]
        tangent = tangent / np.linalg.norm(tangent)
        n = max(3, int(np.hypot(*(neck - middle)) / step))
        inside = middle + np.linspace(0, 1, n, dtype=np.float32)[:, None] * (neck - middle)
        span = np.hypot(*(pts[k] - neck))
        flare = _bezier(neck, neck + 0.4 * span * rise, pts[k] - 0.4 * span * tangent, pts[k], step)
        return np.concatenate([inside[:-1], flare[:-1], pts[k:]]).astype(np.float32)

    return root


def bouquet(scale):
    """A small hand-tied bunch: the placeholder print inside the portrait frame."""
    p = Painter(round(1000 * scale), round(1250 * scale), seed=11, unit=scale)
    c = np.array([500, 1065], np.float32) * scale
    # Earlier versions painted four stub stems here first, using 4 x 7 random
    # numbers. Draw them anyway so every branch above keeps its painting.
    p.rng.uniform(-1, 1, 4 * 7)
    stems = [  # (offset from c, heading, length, kind, options)
        ((0, 0), -95, 860, "round", dict(curl=18, size=80, start_u=0.14, stem_w=(5.2, 1.4))),
        ((0, 0), -118, 700, "round", dict(curl=-22, droop=0.1, size=70, start_u=0.15, stem_w=(4.6, 1.3))),
        ((5, 0), -70, 560, "willow", dict(curl=8, droop=0.25, size=70, start_u=0.16, sag=0.04)),
        ((-5, 0), -132, 460, "willow", dict(curl=-14, droop=0.3, size=62, start_u=0.2, sag=0.05)),
        ((0, 0), -82, 620, "seeded", dict(curl=10, droop=0.2, size=58, start_u=0.22)),
        ((0, 0), -104, 560, "baby", dict(curl=-6, size=44, start_u=0.24, stem_w=(3.6, 1.2))),
        ((3, 0), -48, 400, "round", dict(curl=22, droop=0.3, size=52, start_u=0.25, stem_w=(3.4, 1.2))),
        ((-3, 0), -150, 340, "round", dict(curl=-20, droop=0.3, size=50, start_u=0.25, stem_w=(3.2, 1.2))),
    ]
    tie = c + np.array([0, 4], np.float32) * scale
    wraps, pitch = 6, 4.6
    roots, ends = tied_bundle(stems, tie, scale, band=wraps * pitch)
    for (offset, heading, length, kind, options), root in zip(stems, roots):
        p.branch(c + np.array(offset, np.float32) * scale, heading, length, kind, pencil=0.14, root=root,
                 **options)
    for path, widths in ends:
        p.stem(path, *widths, pigments=("stem", "pod"), strength=0.68)
    p.twine(tie, 14, wraps, pitch)
    return p


def corner_top_right(scale):
    """Eucalyptus falling in from the top-right corner."""
    p = Painter(round(1100 * scale), round(900 * scale), seed=23, unit=scale)
    o = np.array([1230, -110], np.float32) * scale
    p.branch(o, 166, 1020, "round", curl=-38, droop=0.25, size=78, stem_w=(6, 1.4), sag=0.08)
    p.branch(o + [-10 * scale, 20 * scale], 140, 720, "round", curl=-16, droop=0.3, size=64, stem_w=(5, 1.3))
    p.branch(o, 120, 820, "willow", curl=14, droop=0.45, size=72, sag=0.2)
    p.branch(o + [0, 30 * scale], 176, 640, "willow", curl=-24, droop=0.4, size=62, sag=0.18)
    p.branch(o + [-20 * scale, 0], 103, 600, "seeded", curl=10, droop=0.2, size=60)
    p.branch(o, 154, 640, "baby", curl=-12, size=46, stem_w=(4, 1.2))
    return p


def corner_bottom_left(scale):
    """Eucalyptus rising in from the bottom-left corner."""
    p = Painter(round(1100 * scale), round(800 * scale), seed=37, unit=scale)
    o = np.array([-130, 910], np.float32) * scale
    p.branch(o, -31, 980, "round", curl=22, droop=0.2, size=72, stem_w=(6, 1.4))
    p.branch(o + [10 * scale, 0], -48, 640, "round", curl=-12, droop=0.25, size=62, stem_w=(5, 1.3))
    p.branch(o, -64, 720, "willow", curl=22, droop=0.35, size=70, sag=0.12)
    p.branch(o + [0, -20 * scale], -16, 560, "willow", curl=-14, droop=0.3, size=60, sag=0.1)
    p.branch(o + [20 * scale, 0], -82, 480, "seeded", curl=18, droop=0.15, size=56)
    p.branch(o, -36, 560, "baby", curl=-8, size=44, stem_w=(4, 1.2))
    return p


def sprig(scale):
    """A single small stem, for dividers."""
    p = Painter(round(720 * scale), round(300 * scale), seed=5, unit=scale)
    p.branch(np.array([28, 150], np.float32) * scale, -11, 660, "round", curl=24, droop=0.1, size=46,
             stem_w=(3.2, 1.0), skip=0.06)
    return p


PIECES = {
    "botanical-bouquet": (bouquet, "4:5"),
    "botanical-corner-tr": (corner_top_right, "tr"),
    "botanical-corner-bl": (corner_bottom_left, "bl"),
    "botanical-sprig": (sprig, None),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--out", default="assets/img", help="output folder (default: assets/img)")
    parser.add_argument("--scale", type=float, default=1.0, help="size multiplier (default: 1)")
    parser.add_argument("--preview", action="store_true", help="also write previews on ivory")
    parser.add_argument("--only", nargs="*", help="paint only these pieces")
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for name, (compose, anchor) in PIECES.items():
        if args.only and name not in args.only:
            continue
        painter = compose(args.scale)
        target = out / f"{name}.webp"
        preview = out / f"{name}-preview.png" if args.preview else None
        if anchor and ":" in anchor:
            painter.export(target, preview, aspect=tuple(int(v) for v in anchor.split(":")))
        else:
            painter.export(target, preview, anchor=anchor)
        w, h = painter.size
        print(f"{target}  {w}x{h}  {target.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
