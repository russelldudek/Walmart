from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
from pypdf import PdfReader
import base64, mimetypes, urllib.request

ROOT = Path(__file__).resolve().parents[1]
BRAND = ROOT / 'assets' / 'brand'
DOCS = ROOT / 'docs'
BRAND.mkdir(parents=True, exist_ok=True)
DOCS.mkdir(parents=True, exist_ok=True)

ASSETS = {
    'walmart-wordmark-white-on-true-blue.jpg': 'https://corporate.walmart.com/content/dam/corporate/images/newsroom/2025/01/13/walmart-introduces-updated-look-and-feel-a-testament-to-heritage-and-innovation/wordmark-white-on-true-blue.jpg',
    'walmart-spark-true-blue.jpg': 'https://corporate.walmart.com/content/dam/corporate/images/newsroom/2025/01/13/walmart-introduces-updated-look-and-feel-a-testament-to-heritage-and-innovation/spark-true-blue-background.jpg',
}
for name, url in ASSETS.items():
    target = BRAND / name
    if not target.exists() or target.stat().st_size < 1000:
        urllib.request.urlretrieve(url, target)

for src_name, dst_name, box in [
    ('walmart-wordmark-white-on-true-blue.jpg', 'walmart-wordmark-cropped.jpg', (205, 185, 795, 380)),
    ('walmart-spark-true-blue.jpg', 'walmart-spark-cropped.jpg', (340, 110, 660, 450)),
]:
    with Image.open(BRAND / src_name) as image:
        image.crop(box).save(BRAND / dst_name, quality=94)

PAIRS = [
    ('resume.html', 'resume.pdf', 2),
    ('cover-letter.html', 'cover-letter.pdf', 1),
    ('interview-brief.html', 'interview-brief.pdf', 3),
    ('120-day-plan.html', '120-day-plan.pdf', 2),
    ('ai-portfolio-review.html', 'ai-portfolio-review.pdf', 2),
]

def data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
    return f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode()

def inline_html(name: str) -> str:
    html = (ROOT / name).read_text(encoding='utf-8')
    tokens = (ROOT / 'brand-tokens.css').read_text(encoding='utf-8')
    css = (ROOT / 'styles.css').read_text(encoding='utf-8').replace("@import url('./brand-tokens.css');", '')
    html = html.replace('<link rel="stylesheet" href="styles.css">', f'<style>{tokens}\n{css}</style>')
    if '<script src="app.js"></script>' in html:
        html = html.replace('<script src="app.js"></script>', f'<script>{(ROOT / "app.js").read_text(encoding="utf-8")}</script>')
    for rel in [
        'assets/brand/walmart-wordmark-cropped.jpg',
        'assets/brand/walmart-spark-cropped.jpg',
        'assets/brand/walmart-wordmark-white-on-true-blue.jpg',
        'assets/brand/walmart-spark-true-blue.jpg',
    ]:
        path = ROOT / rel
        if path.exists():
            html = html.replace(rel, data_uri(path))
    return html

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True, args=['--no-sandbox', '--disable-dev-shm-usage'])
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    for html_name, pdf_name, expected_pages in PAIRS:
        page.set_content(inline_html(html_name), wait_until='load')
        page.emulate_media(media='print')
        page.pdf(
            path=str(DOCS / pdf_name),
            format='Letter',
            print_background=True,
            margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'},
            prefer_css_page_size=True,
        )
        actual_pages = len(PdfReader(DOCS / pdf_name).pages)
        if actual_pages != expected_pages:
            raise RuntimeError(f'{pdf_name}: expected {expected_pages} pages, found {actual_pages}')
    browser.close()
