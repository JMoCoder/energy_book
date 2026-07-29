#!/usr/bin/env python3
"""
Generate PNG icons for PWA manifest (192x192, 512x512, maskable) using PIL
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def draw_icon(size=512, is_maskable=False):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    margin = 0 if is_maskable else int(size * 0.08)
    radius = 0 if is_maskable else int(size * 0.22)

    # 1. Background Gradient / Solid with Rounded Rect
    # Gradient interpolation from #1A5F96 (26, 95, 150) to #0D3F6F (13, 63, 111)
    bg_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bg_draw = ImageDraw.Draw(bg_img)

    for y in range(size):
        ratio = y / size
        r = int(26 * (1 - ratio) + 13 * ratio)
        g = int(95 * (1 - ratio) + 63 * ratio)
        b = int(150 * (1 - ratio) + 111 * ratio)
        bg_draw.line([(0, y), (size, y)], fill=(r, g, b, 255))

    if not is_maskable:
        # Create rounded rectangle mask
        mask = Image.new("L", (size, size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle(
            [margin, margin, size - margin, size - margin],
            radius=radius,
            fill=255
        )
        img.paste(bg_img, (0, 0), mask)
    else:
        img.paste(bg_img, (0, 0))

    # 2. Draw Battery Body and Energy Lightning
    c = size / 2.0
    scale = size / 512.0

    # Draw Inner Glow Ring
    ring_radius = 160 * scale
    draw.ellipse(
        [c - ring_radius, c - ring_radius, c + ring_radius, c + ring_radius],
        outline=(255, 255, 255, 30),
        width=int(10 * scale)
    )

    # Battery Outline
    bw = 180 * scale
    bh = 240 * scale
    bx0 = c - bw / 2
    by0 = c - bh / 2 + 10 * scale
    bx1 = bx0 + bw
    by1 = by0 + bh

    # Battery Cap
    cap_w = 48 * scale
    cap_h = 16 * scale
    draw.rounded_rectangle(
        [c - cap_w / 2, by0 - cap_h + 2 * scale, c + cap_w / 2, by0 + 2 * scale],
        radius=int(4 * scale),
        fill=(226, 232, 240, 255)
    )

    # Battery Outer Shell
    draw.rounded_rectangle(
        [bx0, by0, bx1, by1],
        radius=int(28 * scale),
        outline=(255, 255, 255, 240),
        width=int(16 * scale)
    )

    # Battery Level (Filled Gradient Blue)
    fill_padding = 16 * scale
    fill_h = 130 * scale
    fill_y1 = by1 - fill_padding
    fill_y0 = fill_y1 - fill_h

    draw.rounded_rectangle(
        [bx0 + fill_padding, fill_y0, bx1 - fill_padding, fill_y1],
        radius=int(16 * scale),
        fill=(56, 189, 248, 240)
    )

    # Lightning Bolt (Yellow / Gold)
    # Bolt vertices relative to center
    bolt_pts = [
        (c + 20 * scale, c - 90 * scale),
        (c - 46 * scale, c + 20 * scale),
        (c + 4 * scale, c + 20 * scale),
        (c - 20 * scale, c + 102 * scale),
        (c + 56 * scale, c - 12 * scale),
        (c + 6 * scale, c - 12 * scale)
    ]
    draw.polygon(bolt_pts, fill=(253, 224, 71, 255))

    return img

def main():
    img_192 = draw_icon(192, is_maskable=False)
    img_192.save(os.path.join(OUTPUT_DIR, "pwa-icon-192.png"))
    print("Generated pwa-icon-192.png")

    img_512 = draw_icon(512, is_maskable=False)
    img_512.save(os.path.join(OUTPUT_DIR, "pwa-icon-512.png"))
    print("Generated pwa-icon-512.png")

    img_maskable = draw_icon(512, is_maskable=True)
    img_maskable.save(os.path.join(OUTPUT_DIR, "pwa-icon-maskable-512.png"))
    print("Generated pwa-icon-maskable-512.png")

if __name__ == "__main__":
    main()
