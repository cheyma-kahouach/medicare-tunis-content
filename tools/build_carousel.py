#!/usr/bin/env python3
"""Build the 5 Medicare Tunis carousel slides (1080x1350 JPG) from a JSON spec.

Usage: python3 tools/build_carousel.py spec.json

spec.json:
{
  "photo": "photos/grossesse_maman_bebe_01.jpg",   # path inside the repo
  "out": "slides/sopk",                            # output folder inside the repo
  "logo": "auto",                                  # optional on slide 1: "auto" (white when the photo is dark behind the logo), "white" or "dark" (default auto)
  "focus_y": 92,                                   # optional, 0 to 100, vertical focus of the photo (default 92)
  "hook": "SOPK et grossesse : ce que personne ne t'explique",
  "s2": ["paragraph", "paragraph"],
  "s3": ["**MYTHE :** text", "paragraph"],         # **bold** renders bold blue
  "s4": ["paragraph", "paragraph"]
}
Slide 5 is the fixed CTA plus the WhatsApp line, never passed in.
"""
import sys, json, re, os, base64, html, subprocess, asyncio
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = '/tmp/mt_fonts'
CTA1 = "La Tunisie, une destination de choix pour vos soins."
CTA2 = "Contactez-nous dès maintenant et bénéfissiez d'une prise en charge sur mesure."
WA = "+216 29889633 / 98757394"

def ensure_fonts():
    base = f'{FONT_DIR}/node_modules/@fontsource/montserrat/files'
    if not os.path.exists(f'{base}/montserrat-latin-800-normal.woff2'):
        os.makedirs(FONT_DIR, exist_ok=True)
        subprocess.run(['npm', 'i', '--prefix', FONT_DIR, '@fontsource/montserrat'], check=True, capture_output=True)
    return base

def b64(path):
    return base64.b64encode(open(path, 'rb').read()).decode()

def rich(t):
    t = html.escape(t)
    return re.sub(r'\*\*(.+?)\*\*', r'<span style="font-weight:800;color:#3f7fae">\1</span>', t)

def size_for(paras):
    n = sum(len(p) for p in paras)
    return 50 if n <= 260 else 46 if n <= 380 else 42 if n <= 520 else 38

def page(fonts, body):
    ff = ''.join(f"@font-face{{font-family:'Montserrat';font-weight:{w};src:url('file://{fonts}/montserrat-latin-{w}-normal.woff2') format('woff2')}}" for w in (400, 500, 700, 800))
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{ff}body{{margin:0}}</style></head><body>{body}</body></html>'

def build(spec):
    fonts = ensure_fonts()
    photo = 'data:image/jpeg;base64,' + b64(os.path.join(REPO, spec['photo']))
    logo = 'data:image/png;base64,' + b64(os.path.join(REPO, 'assets/logo.png'))
    fy = spec.get('focus_y', 92)
    mode = spec.get('logo', 'auto')
    if mode == 'auto':
        from PIL import Image
        im = Image.open(os.path.join(REPO, spec['photo'])).convert('L')
        w, h = im.size
        # area of the photo that ends up behind the logo (top centre of slide 1)
        box = im.crop((int(w*0.3), 0, int(w*0.7), max(1, int(h*0.12))))
        px = list(box.getdata()); mode = 'white' if sum(px)/len(px) < 110 else 'dark'
    logo1 = 'data:image/png;base64,' + b64(os.path.join(REPO, 'assets/logo_white.png' if mode == 'white' else 'assets/logo.png'))
    root = "position:relative;width:1080px;height:1350px;overflow:hidden;font-family:'Montserrat',sans-serif;"
    def logo_tag(src): return f'<img src="{src}" style="position:absolute;left:390px;top:50px;width:300px;height:109px">'
    def photo_tag(extra): return f'<img src="{photo}" style="position:absolute;left:0;top:0;width:1080px;height:1350px;object-fit:cover;object-position:50% {fy}%;{extra}">'
    slides = []
    slides.append(f'<div style="{root}background:#f3f5f7">{photo_tag("")}'
        '<div style="position:absolute;left:0;top:0;width:1080px;height:1350px;background:linear-gradient(180deg,rgba(97,157,192,0) 0%,rgba(97,157,192,0) 50%,rgba(70,130,175,0.9) 76%,#3f7fae 100%)"></div>'
        f'{logo_tag(logo1)}<div style="position:absolute;left:108px;top:930px;width:864px;color:#fff;font-size:74px;font-weight:800;line-height:1.12;letter-spacing:-1.5px;text-transform:uppercase">{html.escape(spec["hook"])}</div></div>')
    def text_slide(paras, weight=500, extra=''):
        fs = size_for(paras)
        inner = ''.join(f'<div>{rich(p)}</div>' for p in paras) + extra
        return (f'<div style="{root}background:#e8f5ff;color:#1b204d">{photo_tag("opacity:0.1")}{logo_tag(logo)}'
                f'<div style="position:absolute;left:108px;top:230px;width:864px;height:980px;display:flex;flex-direction:column;justify-content:center;gap:36px;font-size:{fs}px;font-weight:{weight};line-height:1.25;letter-spacing:-0.8px">{inner}</div></div>')
    for k in ('s2', 's3', 's4'):
        slides.append(text_slide(spec[k]))
    wa = f'<div style="display:flex;flex-direction:column;gap:8px;padding-top:16px;font-size:40px;font-weight:800;color:#3f7fae"><span>WhatsApp</span><span style="color:#1b204d">{WA}</span></div>'
    slides.append(text_slide([CTA1, CTA2], 700, wa))
    out = os.path.join(REPO, spec['out']); os.makedirs(out, exist_ok=True)
    tmp = '/tmp/mt_render'; os.makedirs(tmp, exist_ok=True)
    from playwright.async_api import async_playwright
    async def run():
        async with async_playwright() as p:
            b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
            for i, s in enumerate(slides, 1):
                f = f'{tmp}/s{i}.html'; open(f, 'w').write(page(fonts, s))
                await pg.goto('file://' + f); await pg.wait_for_timeout(800)
                await pg.screenshot(path=f'{tmp}/s{i}.png')
            await b.close()
    asyncio.run(run())
    for i in range(1, 6):
        subprocess.run(['convert', f'{tmp}/s{i}.png', '-quality', '92', f'{out}/slide_{i}.jpg'], check=True)
    print('built', out)

if __name__ == '__main__':
    build(json.load(open(sys.argv[1])))
