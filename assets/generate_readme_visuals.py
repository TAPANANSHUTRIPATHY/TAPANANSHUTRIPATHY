"""Generate the original animated visuals used by the profile README."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
CARD_DIR = HERE / "cards"
CARD_DIR.mkdir(parents=True, exist_ok=True)

PAPER = (244, 241, 232)
WHITE = (255, 254, 248)
INK = (24, 43, 45)
MUTED = (94, 107, 101)
GRID = (222, 218, 207)
TEAL = (38, 124, 113)
ORANGE = (184, 78, 49)
LIME = (147, 165, 67)
BLUE = (77, 115, 137)
NIGHT = (25, 47, 51)
FRAMES = 20
DURATION = 90

FONT_DIR = Path(r"C:\Windows\Fonts")


def font(size: int, *, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont:
    choices = []
    if mono:
        choices.extend([FONT_DIR / "consolab.ttf", FONT_DIR / "consola.ttf"])
    elif bold:
        choices.extend([FONT_DIR / "seguisb.ttf", FONT_DIR / "segoeuib.ttf"])
    else:
        choices.extend([FONT_DIR / "segoeui.ttf", FONT_DIR / "arial.ttf"])
    for candidate in choices:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


FONTS = {
    "title": font(26, bold=True),
    "body": font(13),
    "small": font(11, mono=True),
    "tiny": font(9, mono=True),
    "metric": font(18, bold=True),
    "tag": font(10, mono=True),
    "hero": font(46, bold=True),
    "hero_sub": font(16, mono=True),
}


def mix(a: tuple[int, int, int], b: tuple[int, int, int], amount: float) -> tuple[int, int, int]:
    amount = max(0.0, min(1.0, amount))
    return tuple(round(x + (y - x) * amount) for x, y in zip(a, b))


def paper_grid(draw: ImageDraw.ImageDraw, width: int, height: int, offset: int = 0) -> None:
    for x in range(18 - offset % 24, width, 24):
        for y in range(18, height, 24):
            draw.ellipse((x, y, x + 1, y + 1), fill=GRID)


def draw_text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, which: str, fill=INK) -> None:
    draw.text(xy, text, font=FONTS[which], fill=fill)


def wrap_words(draw: ImageDraw.ImageDraw, text: str, max_width: int, which: str) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textbbox((0, 0), trial, font=FONTS[which])[2] > max_width and current:
            lines.append(current)
            current = word
        else:
            current = trial
    if current:
        lines.append(current)
    return lines


def draw_tags(draw: ImageDraw.ImageDraw, tags: list[str], start_x: int, start_y: int, max_x: int) -> None:
    x, y = start_x, start_y
    for tag in tags:
        box = draw.textbbox((0, 0), tag, font=FONTS["tag"])
        tag_width = box[2] - box[0] + 18
        if x + tag_width > max_x:
            x = start_x
            y += 25
        draw.rounded_rectangle((x, y, x + tag_width, y + 20), radius=8, fill=WHITE, outline=GRID, width=1)
        draw.text((x + 9, y + 4), tag, font=FONTS["tag"], fill=MUTED)
        x += tag_width + 6


def card_base(index: str, category: str, title: str, caption: str, metric: str, tags: list[str], phase: int):
    w, h = 600, 280
    image = Image.new("RGB", (w, h), PAPER)
    draw = ImageDraw.Draw(image)
    paper_grid(draw, w, h, phase)
    draw.rounded_rectangle((5, 5, w - 6, h - 6), radius=18, fill=WHITE, outline=INK, width=2)
    draw.rounded_rectangle((18, 18, w - 19, h - 19), radius=13, outline=GRID, width=1)
    draw_text(draw, (32, 29), f"FIELD {index}  /  {category.upper()}", "small", MUTED)
    draw_text(draw, (32, 57), title, "title", INK)
    for line_no, line in enumerate(wrap_words(draw, caption, 300, "body")[:3]):
        draw_text(draw, (34, 99 + line_no * 20), line, "body", MUTED)

    pulse = (math.sin((phase / FRAMES) * math.tau) + 1) / 2
    accent = mix(TEAL, ORANGE, pulse)
    draw.rounded_rectangle((32, 169, 319, 207), radius=12, fill=NIGHT)
    draw.ellipse((45, 182, 55, 192), fill=accent)
    draw_text(draw, (65, 177), metric.upper(), "metric", WHITE)
    draw_tags(draw, tags, 33, 221, 322)
    draw.rounded_rectangle((351, 66, 568, 240), radius=12, fill=(241, 239, 230), outline=GRID, width=1)
    return image, draw, accent


def draw_crimenetra(phase: int):
    image, draw, accent = card_base(
        "01", "computer vision", "CrimeNetra",
        "Video anomaly analysis, pose estimation, alerts, and evidence logging.",
        "~90%  /  7+ categories",
        ["PYTHON", "OpenCV", "ASTNet", "YOLOv8", "MediaPipe", "Tkinter"], phase,
    )
    x0, y0, x1, y1 = 367, 82, 552, 224
    draw.rounded_rectangle((x0, y0, x1, y1), radius=5, fill=(33, 54, 57))
    for x in range(x0 + 12, x1, 19):
        draw.line((x, y0, x, y1), fill=(44, 68, 70), width=1)
    for y in range(y0 + 12, y1, 19):
        draw.line((x0, y, x1, y), fill=(44, 68, 70), width=1)
    # Abstract camera frame and figures keep the card illustrative without using stock imagery.
    draw.ellipse((407, 111, 432, 136), outline=(210, 213, 196), width=3)
    draw.line((419, 136, 419, 179), fill=(210, 213, 196), width=4)
    draw.line((419, 148, 399, 163), fill=(210, 213, 196), width=3)
    draw.line((419, 149, 439, 162), fill=(210, 213, 196), width=3)
    scan_y = y0 + 8 + (phase * 6) % (y1 - y0 - 16)
    draw.line((x0 + 3, scan_y, x1 - 3, scan_y), fill=accent, width=2)
    bx = 393 + (phase % 4)
    draw.rectangle((bx, 105, 449, 190), outline=accent, width=2)
    for px, py in [(bx, 105), (449, 105), (bx, 190), (449, 190)]:
        draw.ellipse((px - 3, py - 3, px + 3, py + 3), fill=accent)
    draw_text(draw, (371, 207), "FRAME  /  ANALYZE", "tiny", WHITE)
    return image


def draw_elephant(phase: int):
    image, draw, accent = card_base(
        "02", "wildlife monitoring", "Elephant detection",
        "IP-camera monitoring for early warning in live field conditions.",
        "25+ FPS  /  live video",
        ["YOLOv8", "IP CAMERAS", "EARLY WARNING"], phase,
    )
    # Minimal elephant silhouette made from simple vector-like shapes.
    col = (76, 100, 91)
    draw.ellipse((395, 126, 508, 185), fill=col)
    draw.ellipse((480, 112, 532, 165), fill=col)
    draw.ellipse((465, 116, 503, 155), fill=mix(col, PAPER, 0.24))
    draw.rounded_rectangle((490, 148, 512, 206), radius=11, fill=col)
    draw.line((511, 160, 526, 175), fill=WHITE, width=4)
    draw.line((524, 173, 532, 175), fill=WHITE, width=2)
    draw.rectangle((415, 166, 430, 206), fill=col)
    draw.rectangle((446, 166, 461, 206), fill=col)
    draw.rectangle((481, 160, 495, 205), fill=col)
    draw.ellipse((522, 133, 526, 137), fill=INK)
    # Moving range scan and corner marks imply edge inference.
    scan_x = 369 + (phase * 9) % 183
    draw.line((scan_x, 91, scan_x, 216), fill=accent, width=2)
    draw.rectangle((381, 101, 544, 215), outline=accent, width=2)
    draw_text(draw, (387, 87), "IP / LIVE", "tiny", TEAL)
    return image


def draw_traffic(phase: int):
    image, draw, accent = card_base(
        "03", "traffic systems", "Smart traffic",
        "Lane-wise detection turns live traffic into flow data and adaptive signals.",
        "4+ lanes  /  adaptive control",
        ["VEHICLE DETECTION", "FLOW ANALYSIS", "SIGNALS"], phase,
    )
    road = (360, 87, 555, 220)
    draw.rounded_rectangle(road, radius=8, fill=(41, 59, 60))
    for y in (120, 153, 186):
        for x in range(370, 546, 26):
            draw.line((x, y, x + 12, y), fill=(159, 168, 150), width=1)
    for lane in range(4):
        y = 98 + lane * 29
        car_x = 369 + ((phase * 10 + lane * 43) % 152)
        draw.rounded_rectangle((car_x, y, car_x + 25, y + 12), radius=3, fill=[ORANGE, TEAL, LIME, BLUE][lane])
    # Adaptive signal indicator cycles through three states.
    signal_x, signal_y = 535, 78
    draw.rounded_rectangle((signal_x, signal_y, signal_x + 25, signal_y + 61), radius=7, fill=INK)
    lit = phase % 12
    for i, color in enumerate([(203, 85, 58), (211, 174, 70), (61, 152, 106)]):
        on = (lit // 4) == i
        draw.ellipse((signal_x + 7, signal_y + 7 + i * 17, signal_x + 18, signal_y + 18 + i * 17), fill=color if on else (77, 90, 84))
    draw_text(draw, (371, 224), "LANE 01   02   03   04", "tiny", MUTED)
    return image


def draw_iot(phase: int):
    image, draw, accent = card_base(
        "04", "embedded + IoT", "Connected sensing",
        "Three builds connect sensors, appliance control, and live telemetry.",
        "3 systems  /  9-sensor build  /  4 links",
        ["ESP32", "ARDUINO", "OLED", "LORA", "FSO"], phase,
    )
    cx, cy = 456, 151
    # A board at the center with sensor endpoints pulsing around it.
    sensor_points = [(388, 111), (432, 94), (489, 99), (534, 126), (530, 190), (478, 211), (418, 204)]
    for i, (sx, sy) in enumerate(sensor_points):
        draw.line((cx, cy, sx, sy), fill=GRID, width=2)
        p = ((phase + i * 3) % FRAMES) / FRAMES
        px = round(cx + (sx - cx) * p)
        py = round(cy + (sy - cy) * p)
        draw.ellipse((px - 4, py - 4, px + 4, py + 4), fill=accent)
        draw.ellipse((sx - 8, sy - 8, sx + 8, sy + 8), fill=WHITE, outline=TEAL, width=2)
    draw.rounded_rectangle((cx - 33, cy - 23, cx + 33, cy + 23), radius=6, fill=NIGHT, outline=accent, width=2)
    draw_text(draw, (cx - 23, cy - 6), "ESP32", "tiny", WHITE)
    draw_text(draw, (370, 224), "WIFI  /  BT  /  LORA  /  FSO", "tiny", MUTED)
    return image


def draw_attendance(phase: int):
    image, draw, accent = card_base(
        "05", "applied AI", "Face attendance",
        "Webcam recognition logs attendance in an admin dashboard.",
        "manual entries  /  zero",
        ["FLASK", "OPENCV", "MACHINE LEARNING", "WEBCAM"], phase,
    )
    # Face outline and scanning reticle.
    face = (405, 94, 504, 204)
    draw.ellipse(face, outline=TEAL, width=4)
    draw.arc((425, 169, 483, 201), 10, 170, fill=TEAL, width=3)
    draw.ellipse((430, 135, 441, 145), fill=INK)
    draw.ellipse((469, 135, 480, 145), fill=INK)
    draw.arc((440, 147, 471, 173), 10, 170, fill=INK, width=2)
    scan_y = 103 + (phase * 5) % 91
    draw.line((389, scan_y, 520, scan_y), fill=accent, width=2)
    draw.rectangle((393, 86, 516, 212), outline=accent, width=2)
    # Four corner brackets animate in alternating colors.
    for x, y, dx, dy in [(393, 86, 1, 1), (516, 86, -1, 1), (393, 212, 1, -1), (516, 212, -1, -1)]:
        draw.line((x, y, x + dx * 14, y), fill=accent, width=4)
        draw.line((x, y, x, y + dy * 14), fill=accent, width=4)
    draw_text(draw, (384, 224), "FACE MATCH  /  ATTENDANCE LOGGED", "tiny", MUTED)
    return image


def draw_uav(phase: int):
    image, draw, accent = card_base(
        "06", "uav + flight test", "Drone systems",
        "Flight-controller setup, telemetry calibration, and field testing.",
        "3 controllers  /  4 test parameters",
        ["PIXHAWK", "KK2", "APM", "MISSION PLANNER", "CATIA"], phase,
    )
    cx, cy = 459, 150
    # Quad frame, props, landing legs, and moving telemetry arcs.
    rotor = [(394, 106), (524, 106), (394, 193), (524, 193)]
    for i, (rx, ry) in enumerate(rotor):
        draw.line((cx, cy, rx, ry), fill=TEAL, width=5)
        radius = 16 + ((phase + i * 3) % 4)
        draw.ellipse((rx - radius, ry - radius, rx + radius, ry + radius), outline=accent if i == phase % 4 else BLUE, width=2)
    draw.rounded_rectangle((cx - 24, cy - 15, cx + 24, cy + 15), radius=7, fill=NIGHT, outline=accent, width=2)
    draw.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill=WHITE)
    draw.line((cx - 14, cy + 16, cx - 19, cy + 26), fill=INK, width=3)
    draw.line((cx + 14, cy + 16, cx + 19, cy + 26), fill=INK, width=3)
    # GPS/telemetry pulses at the edge of the panel.
    for r in (25, 39, 53):
        draw.arc((cx - r, cy - r, cx + r, cy + r), phase * 18, phase * 18 + 84, fill=LIME, width=2)
    draw_text(draw, (374, 224), "GPS  /  ESC  /  TELEMETRY", "tiny", MUTED)
    return image


def save_gif(path: Path, frames: list[Image.Image]) -> None:
    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=DURATION,
        loop=0,
        optimize=True,
        disposal=2,
    )


def hero_frame(phase: int) -> Image.Image:
    w, h = 1200, 340
    image = Image.new("RGB", (w, h), PAPER)
    draw = ImageDraw.Draw(image)
    paper_grid(draw, w, h, phase)
    draw.rounded_rectangle((6, 6, w - 7, h - 7), radius=20, fill=WHITE, outline=INK, width=2)
    draw_text(draw, (40, 27), "ENGINEERING FIELD NOTES  /  PROFILE 001", "small", MUTED)
    draw.line((40, 53, 1160, 53), fill=GRID, width=2)
    draw_text(draw, (40, 71), "Tapananshu Tripathy", "hero", INK)
    draw_text(draw, (43, 133), "SEE  /  SENSE  /  RESPOND", "hero_sub", ORANGE)
    draw_text(draw, (43, 171), "COMPUTER VISION  ·  CONNECTED HARDWARE  ·  AUTONOMOUS SYSTEMS", "small", MUTED)

    # Animated signal path: camera frame -> edge board -> field response.
    boxes = [(43, 216, 360, 292), (399, 216, 716, 292), (755, 216, 1160, 292)]
    labels = [("01 / PERCEPTION", "Video becomes context"), ("02 / EDGE", "Sensors become signal"), ("03 / RESPONSE", "Decisions become action")]
    colors = [ORANGE, TEAL, LIME]
    for i, (box, label) in enumerate(zip(boxes, labels)):
        draw.rounded_rectangle(box, radius=12, fill=PAPER, outline=GRID, width=2)
        draw.ellipse((box[0] + 17, box[1] + 22, box[0] + 33, box[1] + 38), fill=colors[i])
        draw_text(draw, (box[0] + 47, box[1] + 12), label[0], "tiny", MUTED)
        draw_text(draw, (box[0] + 47, box[1] + 34), label[1], "body", INK)
    for x0, x1 in [(360, 399), (716, 755)]:
        draw.line((x0, 254, x1, 254), fill=MUTED, width=2)
    # Small traveling packet animates left-to-right through the pipeline.
    position = (phase / FRAMES) * 735
    if position <= 355:
        px = 362 + position
    elif position <= 690:
        px = 399 + (position - 355)
    else:
        px = 755 + (position - 690)
    px = min(1156, round(px))
    draw.ellipse((px - 5, 249, px + 5, 259), fill=ORANGE, outline=WHITE, width=2)
    return image


def main() -> None:
    hero = [hero_frame(i) for i in range(FRAMES)]
    save_gif(HERE / "readme-motion.gif", hero)

    projects = [
        ("crimenetra.gif", draw_crimenetra),
        ("elephant-monitor.gif", draw_elephant),
        ("smart-traffic.gif", draw_traffic),
        ("connected-systems.gif", draw_iot),
        ("face-attendance.gif", draw_attendance),
        ("uav-build.gif", draw_uav),
    ]
    for name, render in projects:
        save_gif(CARD_DIR / name, [render(i) for i in range(FRAMES)])
    print(f"Generated 1 animated hero and {len(projects)} animated project cards in {HERE}.")


if __name__ == "__main__":
    main()
