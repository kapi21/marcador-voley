"""Genera los iconos PWA: marcador LED (rojo | azul) con balón de voleibol en el centro.
Uso: python make_icons.py
"""
import math, os
from PIL import Image, ImageDraw, ImageFilter, ImageChops

MAP = ['abcdef', 'bc', 'abdeg', 'abcdg', 'bcfg', 'acdfg', 'acdefg', 'abc', 'abcdefg', 'abcdfg']
def hz(x1, x2, cy, h=4.6): return [(x1, cy), (x1+h, cy-h), (x2-h, cy-h), (x2, cy), (x2-h, cy+h), (x1+h, cy+h)]
def vt(cx, y1, y2, h=4.6): return [(cx, y1), (cx+h, y1+h), (cx+h, y2-h), (cx, y2), (cx-h, y2-h), (cx-h, y1+h)]
SEG = {'a': hz(9, 51, 6), 'b': vt(54, 9, 47), 'c': vt(54, 53, 91), 'd': hz(9, 51, 94), 'e': vt(6, 53, 91), 'f': vt(6, 9, 47), 'g': hz(11, 49, 50)}

RED, BLUE = (255, 42, 61), (31, 162, 255)

def draw_digit(img, digit, ox, oy, sc, col):
    """Dibuja un dígito 7 segmentos con brillo."""
    W = img.size[0]
    glow = Image.new('RGB', img.size, (0, 0, 0))
    g, d = ImageDraw.Draw(glow), ImageDraw.Draw(img)
    for k, pts in SEG.items():
        p = [(ox + x*sc, oy + y*sc) for x, y in pts]
        if k in MAP[digit]:
            g.polygon(p, fill=col); d.polygon(p, fill=col)
        else:
            d.polygon(p, fill=tuple(int(c*0.13) + 6 for c in col))
    blur = glow.filter(ImageFilter.GaussianBlur(W * 0.012))
    return ImageChops.add(img, blur)

def ball_layer(size, cx, cy, r):
    """Balón de voleibol: panel crema, costuras en 3 direcciones, franjas amarillo/azul y sombreado."""
    ss = 3
    L = Image.new('RGBA', (size*ss, size*ss), (0, 0, 0, 0))
    R, X, Y = r*ss, cx*ss, cy*ss
    mask = Image.new('L', L.size, 0)
    ImageDraw.Draw(mask).ellipse([X-R, Y-R, X+R, Y+R], fill=255)
    ball = Image.new('RGBA', L.size, (0, 0, 0, 0))
    bd = ImageDraw.Draw(ball)
    bd.ellipse([X-R, Y-R, X+R, Y+R], fill=(250, 246, 232, 255))
    # franjas de color: 3 gajos con arcos desplazados (amarillo y azul) + costuras
    for i, ang in enumerate((90, 210, 330)):
        a = math.radians(ang)
        for off, w, col in ((0.00, 0.045, (24, 36, 70, 255)),
                            (0.17, 0.30, (255, 196, 32, 255) if i != 1 else (30, 110, 220, 255)),
                            (0.34, 0.045, (24, 36, 70, 255))):
            rad = R * 1.15
            ccx = X + math.cos(a) * (R*(1.15 + off - 0.0))
            ccy = Y + math.sin(a) * (R*(1.15 + off - 0.0))
            bd.arc([ccx-rad, ccy-rad, ccx+rad, ccy+rad], 0, 360, fill=col, width=int(R*w))
    # sombreado esférico
    sh = Image.new('RGBA', L.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    for k in range(40):
        t = k/39
        rr = R*(1 - 0.55*t)
        a = int(110*(1-t)**1.5)
        sd.ellipse([X-R*0.18-rr*0.92+R*0.0, Y-R*0.22-rr*0.92, X-R*0.18+rr*0.92, Y-R*0.22+rr*0.92], outline=None)
    shade = Image.new('L', L.size, 0)
    sdd = ImageDraw.Draw(shade)
    sdd.ellipse([X-R, Y-R, X+R, Y+R], fill=95)
    hl = Image.new('L', L.size, 0)
    ImageDraw.Draw(hl).ellipse([X-R*0.75, Y-R*0.85, X+R*0.15, Y-R*0.05], fill=255)
    hl = hl.filter(ImageFilter.GaussianBlur(R*0.25))
    dark = Image.new('L', L.size, 0)
    ImageDraw.Draw(dark).ellipse([X-R*0.95, Y-R*0.95, X+R*1.35, Y+R*1.35], fill=255)
    dark = ImageChops.invert(dark.filter(ImageFilter.GaussianBlur(R*0.35)))
    shadow = Image.new('RGBA', L.size, (10, 12, 30, 255))
    shadow.putalpha(dark.point(lambda v: int(v*0.55)))
    ball = Image.alpha_composite(ball, shadow)
    white = Image.new('RGBA', L.size, (255, 255, 255, 255)); white.putalpha(hl.point(lambda v: int(v*0.45)))
    ball = Image.alpha_composite(ball, white)
    # borde
    ImageDraw.Draw(ball).ellipse([X-R, Y-R, X+R, Y+R], outline=(20, 24, 40, 255), width=max(2, int(R*0.03)))
    L.paste(ball, (0, 0), mask)
    # sombra proyectada
    drop = Image.new('RGBA', L.size, (0, 0, 0, 0))
    ImageDraw.Draw(drop).ellipse([X-R*0.9, Y+R*0.92, X+R*0.9, Y+R*1.08], fill=(0, 0, 0, 150))
    drop = drop.filter(ImageFilter.GaussianBlur(R*0.08))
    out = Image.alpha_composite(drop, L)
    return out.resize((size, size), Image.LANCZOS)

def make(size, k=1.0):
    S = size
    img = Image.new('RGB', (S, S), (10, 13, 19))
    d = ImageDraw.Draw(img)
    # semifondos rojo | azul con degradado
    for x in range(S):
        t = x / S
        base = (60, 8, 18) if t < 0.5 else (6, 40, 72)
        v = 1 - abs(t - 0.5) * 0.9
        d.line([(x, 0), (x, S)], fill=tuple(int(c*(0.5 + v*0.9)) for c in base))
    # rejilla tipo fibra / dot-matrix sutil
    for y in range(0, S, max(3, S//96)):
        d.line([(0, y), (S, y)], fill=(0, 0, 0), width=1)
    img = Image.blend(img, Image.new('RGB', (S, S), (10, 13, 19)), 0.0)
    cx = cy = S / 2
    # dígitos laterales (dentro de zona segura escalada por k)
    sc = S * 0.0037 * k
    dw, dh = 60*sc, 100*sc
    gap = S * 0.315 * k
    ly = cy - dh/2 - S*0.02*k
    img = draw_digit(img, 2, cx - gap - dw*0.55, ly, sc, RED)
    img = draw_digit(img, 5, cx + gap - dw*0.45, ly, sc, BLUE)
    # balón central
    r = S * 0.235 * k
    ball = ball_layer(S, cx, cy + S*0.02*k, r)
    img = Image.alpha_composite(img.convert('RGBA'), ball).convert('RGB')
    # bisel del marcador (marco metálico)
    bez = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bez)
    w = max(2, int(S*0.025))
    bd.rounded_rectangle([w//2, w//2, S-w//2, S-w//2], radius=int(S*0.14), outline=(150, 158, 175, 255), width=w)
    return Image.alpha_composite(img.convert('RGBA'), bez).convert('RGB')

os.makedirs('icons', exist_ok=True)
make(192).save('icons/icon-192.png')
make(512).save('icons/icon-512.png')
make(512, 0.72).save('icons/icon-maskable-512.png')   # zona segura para máscara adaptable
print('OK')

