"""Genera los iconos PWA (marcador con dígitos LED '25'). Uso: python make_icons.py"""
import os
from PIL import Image, ImageDraw, ImageFilter

MAP = ['abcdef', 'bc', 'abdeg', 'abcdg', 'bcfg', 'acdfg', 'acdefg', 'abc', 'abcdefg', 'abcdfg']

def hz(x1, x2, cy, h):
    return [(x1, cy), (x1 + h, cy - h), (x2 - h, cy - h), (x2, cy), (x2 - h, cy + h), (x1 + h, cy + h)]

def vt(cx, y1, y2, h):
    return [(cx, y1), (cx + h, y1 + h), (cx + h, y2 - h), (cx, y2), (cx - h, y2 - h), (cx - h, y1 + h)]

SEG = {'a': hz(9, 51, 6, 4.6), 'b': vt(54, 9, 47, 4.6), 'c': vt(54, 53, 91, 4.6), 'd': hz(9, 51, 94, 4.6),
       'e': vt(6, 53, 91, 4.6), 'f': vt(6, 9, 47, 4.6), 'g': hz(11, 49, 50, 4.6)}

def draw_icon(size, safe):
    S = size
    img = Image.new('RGB', (S, S), (10, 13, 19))
    d = ImageDraw.Draw(img)
    # franjas rojo / azul laterales
    d.rectangle([0, 0, S // 2, S], fill=(60, 8, 16))
    d.rectangle([S // 2, 0, S, S], fill=(6, 40, 70))
    glow = Image.new('RGB', (S, S), (0, 0, 0))
    g = ImageDraw.Draw(glow)
    scale = S * safe / 140.0
    ox, oy = (S - 130 * scale) / 2, (S - 100 * scale) / 2
    for digit, dx, col in ((2, 0, (255, 42, 61)), (5, 68, (31, 162, 255))):
        for k, pts in SEG.items():
            p = [(ox + (x + dx) * scale, oy + y * scale) for x, y in pts]
            if k in MAP[digit]:
                g.polygon(p, fill=col)
                d.polygon(p, fill=col)
            else:
                d.polygon(p, fill=tuple(int(c * 0.12) + 8 for c in col))
    blur = glow.filter(ImageFilter.GaussianBlur(S * 0.02))
    img = Image.blend(img, Image.composite(blur, img, blur.convert('L')), 0.0)
    from PIL import ImageChops
    img = ImageChops.add(img, blur)
    return img

os.makedirs('icons', exist_ok=True)
draw_icon(192, 0.8).save('icons/icon-192.png')
draw_icon(512, 0.8).save('icons/icon-512.png')
draw_icon(512, 0.55).save('icons/icon-maskable-512.png')  # zona segura para máscara
print('OK')

