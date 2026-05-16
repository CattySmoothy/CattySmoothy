"""
Programmatic SVG pattern generator for CattySmoothy.
Generates two patterns:
  1. Whimsical Winter Swirls  — tileable vector pattern with spirals, stars, snowflakes
  2. Celestial Cosmic Collage — layered collage with celestial elements and particles
"""

import math
import random


# ── SVG helpers ──────────────────────────────────────────────────────────────

def _svg_header(w, h):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'

def _svg_footer():
    return '</svg>'

def _tag(name, attrs, content=""):
    a = " ".join(f'{k}="{v}"' for k, v in attrs.items() if v is not None)
    if content:
        return f"<{name} {a}>{content}</{name}>"
    return f"<{name} {a}/>"

def _rect(x, y, w, h, **kw):
    return _tag("rect", {"x": x, "y": y, "width": w, "height": h, **kw})

def _circle(cx, cy, r, **kw):
    return _tag("circle", {"cx": cx, "cy": cy, "r": r, **kw})

def _ellipse(cx, cy, rx, ry, **kw):
    return _tag("ellipse", {"cx": cx, "cy": cy, "rx": rx, "ry": ry, **kw})

def _line(x1, y1, x2, y2, **kw):
    return _tag("line", {"x1": x1, "y1": y1, "x2": x2, "y2": y2, **kw})

def _path(d, **kw):
    return _tag("path", {"d": d, **kw})

def _polygon(points, **kw):
    d = " ".join(f"{x},{y}" for x, y in points)
    return _tag("polygon", {"points": d, **kw})

def _g(attrs, content):
    return _tag("g", attrs, content)

def _defs(content):
    return _tag("defs", {}, content)

def _linear_gradient(id_, x1, y1, x2, y2, stops):
    s = "".join(
        _tag("stop", {"offset": f"{o}%", "stop-color": c, "stop-opacity": a})
        for o, c, a in stops
    )
    return _tag("linearGradient", {"id": id_, "x1": x1, "y1": y1, "x2": x2, "y2": y2}, s)

def _radial_gradient(id_, stops, cx="50%", cy="50%", r="50%"):
    s = "".join(
        _tag("stop", {"offset": f"{o}%", "stop-color": c, "stop-opacity": a})
        for o, c, a in stops
    )
    return _tag("radialGradient", {"id": id_, "cx": cx, "cy": cy, "r": r}, s)

def _filter(id_, content):
    return _tag("filter", {"id": id_}, content)

def _pattern(id_, w, h, content):
    return _tag("pattern", {"id": id_, "width": w, "height": h, "patternUnits": "userSpaceOnUse"}, content)


# ── Element builders — Pattern 1 ─────────────────────────────────────────────

def _spiral_path(cx, cy, a, b, theta_start, theta_end, steps=120):
    """Archimedean spiral: r = a + b * theta"""
    pts = []
    for i in range(steps + 1):
        t = theta_start + (theta_end - theta_start) * i / steps
        r = a + b * t
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    return "M " + " ".join(f"{x},{y}" for x, y in pts)


def _two_point_star(cx, cy, r):
    """Single thin diamond (one axis of a four-point star)."""
    w = r * 0.12
    return f"M {cx},{cy - r} L {cx + w},{cy} L {cx},{cy + r} L {cx - w},{cy} Z"


def four_point_star(cx, cy, r, **kw):
    """Four-point sparkle: two intersecting thin diamonds at 90°."""
    d1 = _two_point_star(cx, cy, r)
    d2 = _two_point_star(cx, cy, r)
    # rotate second diamond by swapping roles
    d2 = f"M {cx - r},{cy} L {cx},{cy - r * 0.12} L {cx + r},{cy} L {cx},{cy + r * 0.12} Z"
    return _path(d1, **kw) + _path(d2, **kw)


def six_blade_snowflake(cx, cy, r, **kw):
    """Six rounded petals at 60° increments."""
    paths = []
    for i in range(6):
        a = math.radians(i * 60)
        tx = cx + r * math.cos(a)
        ty = cy + r * math.sin(a)
        perp = a + math.pi / 2
        pw = r * 0.12
        cp1x = cx + pw * math.cos(perp) + r * 0.35 * math.cos(a)
        cp1y = cy + pw * math.sin(perp) + r * 0.35 * math.sin(a)
        cp2x = cx - pw * math.cos(perp) + r * 0.35 * math.cos(a)
        cp2y = cy - pw * math.sin(perp) + r * 0.35 * math.sin(a)
        paths.append(f"M {cx},{cy} C {cp1x},{cp1y} {tx},{ty} {tx},{ty} C {cp2x},{cp2y} {cx},{cy} {cx},{cy}")
    return _path(" ".join(paths), **kw)


# ── Pattern 1: Whimsical Winter Swirls ───────────────────────────────────────

def generate_winter_swirls(width=600, height=600, seed=None):
    """Tileable Whimsical Winter Swirls pattern as an SVG string."""
    rng = random.Random(seed)
    parts = [_svg_header(width, height)]

    # ── defs ──────────────────────────────────────────────────────────────
    parts.append(_defs(
        _linear_gradient("w-bg", 0, 0, 0, height, [
            (0,   "#85A9DD", 1),
            (100, "#A9C2EC", 1),
        ]) +
        _radial_gradient("w-glow", [
            (0,   "#FFFFFF", 0.5),
            (100, "#FFFFFF", 0),
        ]) +
        _filter("w-glow-filter",
            _tag("feGaussianBlur", {"stdDeviation": "3", "result": "blur"}) +
            _tag("feMerge", {},
                _tag("feMergeNode", {"in": "blur"}) +
                _tag("feMergeNode", {"in": "SourceGraphic"})
            )
        ) +
        _filter("w-soft-glow",
            _tag("feGaussianBlur", {"stdDeviation": "5", "result": "blur"}) +
            _tag("feMerge", {},
                _tag("feMergeNode", {"in": "blur"}) +
                _tag("feMergeNode", {"in": "SourceGraphic"})
            )
        )
    ))

    # ── background ────────────────────────────────────────────────────────
    parts.append(_rect(0, 0, width, height, fill="url(#w-bg)"))

    # ── weave texture (fine grid) ─────────────────────────────────────────
    grid = []
    for x in range(0, width + 1, 12):
        grid.append(_line(x, 0, x, height, stroke="rgba(255,255,255,0.035)", stroke_width="0.5"))
    for y in range(0, height + 1, 12):
        grid.append(_line(0, y, width, y, stroke="rgba(255,255,255,0.035)", stroke_width="0.5"))
    parts.append(_g({}, "".join(grid)))

    # ── micro-dots ────────────────────────────────────────────────────────
    dots = []
    for _ in range(250):
        x = rng.uniform(0, width)
        y = rng.uniform(0, height)
        r = rng.uniform(0.3, 1.5)
        a = rng.uniform(0.08, 0.25)
        c = "#FFFFFF" if rng.random() < 0.6 else "#4A6B8A"
        dots.append(_circle(x, y, r, fill=c, opacity=a))
    parts.append(_g({}, "".join(dots)))

    # ── spirals ───────────────────────────────────────────────────────────
    cols, rows = 3, 3
    cw, ch = width / cols, height / rows
    anchors = []
    for r in range(rows):
        for c in range(cols):
            anchors.append((
                cw * (c + 0.5) + rng.uniform(-cw * 0.15, cw * 0.15),
                ch * (r + 0.5) + rng.uniform(-ch * 0.15, ch * 0.15),
            ))

    spiral_group = []
    for i, (cx, cy) in enumerate(anchors):
        a = rng.uniform(4, 10)
        b = rng.uniform(1.8, 3.5)
        t0 = rng.uniform(0, math.tau)
        t1 = t0 + math.pi * rng.uniform(2, 4)
        d = _spiral_path(cx, cy, a, b, t0, t1)

        # thick soft glow
        spiral_group.append(_path(d, fill="none",
            stroke="rgba(255,255,255,0.06)", stroke_width="8", filter="url(#w-soft-glow)"))
        # bright core
        spiral_group.append(_path(d, fill="none",
            stroke="rgba(255,255,255,0.45)", stroke_width="1.5"))
        # thin blue highlight
        spiral_group.append(_path(d, fill="none",
            stroke="rgba(180,210,255,0.25)", stroke_width="0.5"))

        # connecting curves between anchors
        if i > 0:
            px, py = anchors[(i - 1) % len(anchors)]
            dx, dy = cx - px, cy - py
            if math.hypot(dx, dy) < max(width, height) * 0.55:
                c1x = px + rng.uniform(-40, 40)
                c1y = py + rng.uniform(-40, 40)
                c2x = cx + rng.uniform(-40, 40)
                c2y = cy + rng.uniform(-40, 40)
                cd = f"M {px},{py} C {c1x},{c1y} {c2x},{c2y} {cx},{cy}"
                spiral_group.append(_path(cd, fill="none",
                    stroke="rgba(255,255,255,0.2)", stroke_width="1", filter="url(#w-glow-filter)"))

        # four-point star at anchor
        spiral_group.append(four_point_star(cx, cy, rng.uniform(5, 10),
            fill="#FFFFFF", opacity=rng.uniform(0.5, 0.85)))

    parts.append(_g({}, "".join(spiral_group)))

    # ── scattered four-point stars ────────────────────────────────────────
    extra_stars = []
    for _ in range(18):
        x = rng.uniform(0, width)
        y = rng.uniform(0, height)
        sr = rng.uniform(3, 9)
        extra_stars.append(four_point_star(x, y, sr,
            fill="#FFFFFF", opacity=rng.uniform(0.2, 0.6)))
    parts.append(_g({}, "".join(extra_stars)))

    # ── snowflakes ────────────────────────────────────────────────────────
    flakes = []
    for _ in range(10):
        x = rng.uniform(40, width - 40)
        y = rng.uniform(40, height - 40)
        r = rng.uniform(4, 10)
        a = rng.uniform(0.2, 0.5)
        flakes.append(six_blade_snowflake(x, y, r,
            fill="none", stroke="#FFFFFF", stroke_width="0.7", opacity=a))
    parts.append(_g({}, "".join(flakes)))

    # ── floating orbs ─────────────────────────────────────────────────────
    orbs = []
    for _ in range(8):
        x = rng.uniform(0, width)
        y = rng.uniform(0, height)
        r = rng.uniform(3, 9)
        orbs.append(_circle(x, y, r, fill="#FFFFFF", opacity=rng.uniform(0.1, 0.3)))
    for _ in range(5):
        x = rng.uniform(0, width)
        y = rng.uniform(0, height)
        r = rng.uniform(4, 12)
        orbs.append(_circle(x, y, r, fill="#2C3E6B", opacity=rng.uniform(0.08, 0.18)))
    parts.append(_g({}, "".join(orbs)))

    parts.append(_svg_footer())
    return "".join(parts)


# ── Element builders — Pattern 2 ─────────────────────────────────────────────

def _five_point_star_path(cx, cy, r):
    pts = []
    for i in range(10):
        a = math.radians(i * 36 - 90)
        radius = r if i % 2 == 0 else r * 0.38
        pts.append(f"{cx + radius * math.cos(a)},{cy + radius * math.sin(a)}")
    return "M " + " L ".join(pts) + " Z"


def five_point_star(cx, cy, r, **kw):
    return _path(_five_point_star_path(cx, cy, r), **kw)


def crescent_moon(cx, cy, r, **kw):
    d = (f"M {cx - r},{cy} "
         f"A {r},{r} 0 1,1 {cx + r},{cy} "
         f"A {r * 0.55},{r * 0.75} 0 1,0 {cx - r},{cy}")
    return _path(d, **kw)


# ── Pattern 2: Celestial Cosmic Collage ──────────────────────────────────────

def generate_celestial_collage(width=800, height=800, seed=None):
    """Layered Celestial Cosmic Collage pattern as an SVG string."""
    rng = random.Random(seed)
    parts = [_svg_header(width, height)]

    # ── defs ──────────────────────────────────────────────────────────────
    parts.append(_defs(
        _linear_gradient("c-bg", 0, 0, 0, height, [
            (0,   "#6B7D93", 1),
            (50,  "#8B9CB0", 1),
            (100, "#A6B4C9", 1),
        ]) +
        _radial_gradient("c-sun-glow", [
            (0,   "#FFFDE8", 1),
            (30,  "#FFF5C2", 0.5),
            (100, "#FFF5C2", 0),
        ]) +
        _radial_gradient("c-moon-glow", [
            (0,   "#FFFFFF", 0.7),
            (50,  "#FFFFFF", 0.15),
            (100, "#FFFFFF", 0),
        ]) +
        _filter("c-bokeh",
            _tag("feGaussianBlur", {"stdDeviation": "7"})
        ) +
        _filter("c-soft-blur",
            _tag("feGaussianBlur", {"stdDeviation": "2.5"})
        ) +
        _filter("c-heavy-blur",
            _tag("feGaussianBlur", {"stdDeviation": "18"})
        )
    ))

    # ── background ────────────────────────────────────────────────────────
    parts.append(_rect(0, 0, width, height, fill="url(#c-bg)"))

    # ── splatter/distress texture ─────────────────────────────────────────
    splatter = []
    for _ in range(400):
        x = rng.uniform(0, width)
        y = rng.uniform(0, height)
        r = rng.uniform(1, 18)
        shade = rng.choice([
            "rgba(90,100,120,0.08)", "rgba(200,210,230,0.06)",
            "rgba(60,70,90,0.05)",    "rgba(180,190,210,0.04)",
        ])
        splatter.append(_circle(x, y, r, fill=shade))
    parts.append(_g({}, "".join(splatter)))

    # ── central radiant sun ───────────────────────────────────────────────
    cx, cy = width * 0.5, height * 0.35
    sun_r = 60
    parts.append(_circle(cx, cy, sun_r * 3, fill="url(#c-sun-glow)"))
    rays = []
    for i in range(72):
        a = math.radians(i * 5)
        rl = sun_r * rng.uniform(1.4, 3.8)
        x1 = cx + sun_r * 0.75 * math.cos(a)
        y1 = cy + sun_r * 0.75 * math.sin(a)
        x2 = cx + (sun_r + rl) * math.cos(a)
        y2 = cy + (sun_r + rl) * math.sin(a)
        rays.append(_line(x1, y1, x2, y2,
            stroke=f"rgba(255,248,230,{rng.uniform(0.12, 0.38):.2f})",
            stroke_width=f"{rng.uniform(0.4, 1.6):.1f}"))
    parts.append(_g({}, "".join(rays)))
    parts.append(_circle(cx, cy, sun_r, fill="#FFF8E6", opacity=0.9))
    parts.append(_circle(cx, cy, sun_r * 0.55, fill="#FFFFFF", opacity=0.5))

    # ── upper-right moon ──────────────────────────────────────────────────
    cx2, cy2 = width * 0.78, height * 0.2
    mr2 = 35
    parts.append(_circle(cx2, cy2, mr2 * 2.5, fill="url(#c-moon-glow)"))
    rays2 = []
    for i in range(48):
        a = math.radians(i * 7.5 + rng.uniform(0, 5))
        rl = mr2 * rng.uniform(1.2, 3.0)
        x1 = cx2 + mr2 * 0.65 * math.cos(a)
        y1 = cy2 + mr2 * 0.65 * math.sin(a)
        x2 = cx2 + (mr2 + rl) * math.cos(a)
        y2 = cy2 + (mr2 + rl) * math.sin(a)
        rays2.append(_line(x1, y1, x2, y2,
            stroke=f"rgba(255,255,255,{rng.uniform(0.08, 0.28):.2f})",
            stroke_width=f"{rng.uniform(0.3, 1.0):.1f}"))
    parts.append(_g({}, "".join(rays2)))
    parts.append(_circle(cx2, cy2, mr2, fill="#FFFFFF", opacity=0.65))
    parts.append(_circle(cx2, cy2, mr2 * 0.45, fill="#FFFFFF", opacity=0.35))

    # ── crescent moons ────────────────────────────────────────────────────
    crescents = []
    for _ in range(4):
        mcx = rng.uniform(width * 0.05, width * 0.95)
        mcy = rng.uniform(height * 0.05, height * 0.95)
        mr = rng.uniform(25, 55)
        a = rng.uniform(0.06, 0.18)
        crescents.append(crescent_moon(mcx, mcy, mr,
            fill=f"rgba(255,255,255,{a:.2f})", filter="url(#c-soft-blur)"))
    parts.append(_g({}, "".join(crescents)))

    # ── mystical figure (lower-left) ──────────────────────────────────────
    fx, fy = width * 0.2, height * 0.72
    sc = min(width, height) / 800
    hw, hh = 55 * sc, 65 * sc
    sh, bh = 110 * sc, 150 * sc

    figure_d = (
        f"M {fx},{fy - hh * 0.5} "
        f"C {fx + hw * 0.35},{fy - hh * 0.6}  {fx + hw * 0.55},{fy - hh * 0.3}  {fx + hw * 0.55},{fy - hh * 0.05} "
        f"C {fx + hw * 0.65},{fy + hh * 0.05} {fx + hw * 0.58},{fy + hh * 0.15} {fx + hw * 0.48},{fy + hh * 0.15} "
        f"C {fx + hw * 0.55},{fy + hh * 0.22} {fx + hw * 0.48},{fy + hh * 0.32} {fx + hw * 0.42},{fy + hh * 0.32} "
        f"C {fx + hw * 0.32},{fy + hh * 0.42} {fx + hw * 0.15},{fy + hh * 0.52} {fx - hw * 0.08},{fy + hh * 0.55} "
        f"C {fx - hw * 0.18},{fy + hh * 0.62} {fx - sh * 0.25},{fy + hh * 0.72} {fx - sh * 0.15},{fy + bh} "
        f"C {fx + sh * 0.08},{fy + bh * 1.05} {fx + sh * 0.35},{fy + bh * 0.85} {fx + sh * 0.28},{fy + bh * 0.55} "
        f"C {fx + sh * 0.38},{fy + bh * 0.45} {fx + sh * 0.55},{fy + hh * 0.25} {fx + sh * 0.18},{fy - hh * 0.08} "
        f"C {fx + sh * 0.35},{fy - hh * 0.3}  {fx + sh * 0.22},{fy - hh * 0.5}  {fx},{fy - hh * 0.58} "
        f"C {fx - hw * 0.3},{fy - hh * 0.68} {fx - hw * 0.65},{fy - hh * 0.48} {fx - hw * 0.75},{fy - hh * 0.15} "
        f"C {fx - hw * 0.85},{fy + hh * 0.1}  {fx - hw * 0.58},{fy + hh * 0.45} {fx - hw * 0.48},{fy + hh * 0.6} "
        f"C {fx - sh * 0.35},{fy + hh * 0.82} {fx - sh * 0.65},{fy + hh * 0.48} {fx - sh * 0.55},{fy + hh * 0.18} "
        f"C {fx - sh * 0.3},{fy - hh * 0.08}  {fx - hw * 0.18},{fy - hh * 0.28} {fx},{fy - hh * 0.5} Z"
    )
    parts.append(_path(figure_d, fill="rgba(55,65,85,0.25)", filter="url(#c-soft-blur)"))
    parts.append(_path(figure_d, fill="rgba(75,85,105,0.12)"))

    # ── five-point stars — solid ──────────────────────────────────────────
    solid_stars = []
    for _ in range(25):
        sx = rng.uniform(0, width)
        sy = rng.uniform(0, height)
        sr = rng.uniform(2.5, 14)
        a = rng.uniform(0.08, 0.55)
        solid_stars.append(five_point_star(sx, sy, sr,
            fill=f"rgba(255,255,255,{a:.2f})", stroke="none"))
    parts.append(_g({}, "".join(solid_stars)))

    # ── five-point stars — outline ────────────────────────────────────────
    outline_stars = []
    for _ in range(15):
        sx = rng.uniform(0, width)
        sy = rng.uniform(0, height)
        sr = rng.uniform(5, 22)
        a = rng.uniform(0.1, 0.35)
        outline_stars.append(five_point_star(sx, sy, sr,
            fill="none", stroke=f"rgba(255,255,255,{a:.2f})", stroke_width="0.7"))
    parts.append(_g({}, "".join(outline_stars)))

    # ── geometric ring systems ────────────────────────────────────────────
    rings = []
    for _ in range(6):
        rx = rng.uniform(width * 0.1, width * 0.9)
        ry = rng.uniform(height * 0.1, height * 0.9)
        max_r = rng.uniform(22, 50)
        for rr in [max_r * 0.35, max_r * 0.65, max_r]:
            a = rng.uniform(0.04, 0.12)
            rings.append(_circle(rx, ry, rr,
                fill="none", stroke=f"rgba(255,255,255,{a:.2f})", stroke_width="0.4"))
        for angle in [0, math.pi * 0.3, math.pi * 0.7]:
            x1 = rx + max_r * 0.35 * math.cos(angle)
            y1 = ry + max_r * 0.35 * math.sin(angle)
            x2 = rx + max_r * math.cos(angle)
            y2 = ry + max_r * math.sin(angle)
            rings.append(_line(x1, y1, x2, y2,
                stroke="rgba(255,255,255,0.08)", stroke_width="0.4"))
    parts.append(_g({}, "".join(rings)))

    # ── snow particles — sharp focus ──────────────────────────────────────
    sharp = []
    for _ in range(200):
        px = rng.uniform(0, width)
        py = rng.uniform(0, height)
        pr = rng.uniform(0.4, 2.5)
        a = rng.uniform(0.15, 0.8)
        sharp.append(_circle(px, py, pr, fill="#FFFFFF", opacity=a))
    parts.append(_g({}, "".join(sharp)))

    # ── bokeh particles — soft blurred ────────────────────────────────────
    bokeh = []
    for _ in range(40):
        px = rng.uniform(0, width)
        py = rng.uniform(0, height)
        pr = rng.uniform(5, 28)
        a = rng.uniform(0.04, 0.15)
        bokeh.append(_circle(px, py, pr,
            fill="#FFFFFF", opacity=a, filter="url(#c-bokeh)"))
    parts.append(_g({}, "".join(bokeh)))

    # ── splatter clusters ─────────────────────────────────────────────────
    clusters = []
    for _ in range(10):
        c_x = rng.uniform(0, width)
        c_y = rng.uniform(0, height)
        for _ in range(rng.randint(6, 25)):
            px = c_x + rng.uniform(-18, 18)
            py = c_y + rng.uniform(-18, 18)
            pr = rng.uniform(0.3, 3.5)
            a = rng.uniform(0.08, 0.3)
            clusters.append(_circle(px, py, pr, fill="#FFFFFF", opacity=a))
    parts.append(_g({}, "".join(clusters)))

    parts.append(_svg_footer())
    return "".join(parts)
