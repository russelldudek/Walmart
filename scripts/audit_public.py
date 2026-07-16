from pathlib import Path
from pypdf import PdfReader
import re

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    'index.html', 'resume.html', 'cover-letter.html', 'interview-brief.html',
    '120-day-plan.html', 'ai-portfolio-review.html', 'styles.css',
    'brand-tokens.css', 'app.js', 'brand-intelligence.md', 'README.md',
    'assets/brand/walmart-wordmark-white-on-true-blue.jpg',
    'assets/brand/walmart-wordmark-cropped.jpg',
    'assets/brand/walmart-spark-true-blue.jpg',
    'assets/brand/walmart-spark-cropped.jpg',
    'docs/resume.pdf', 'docs/cover-letter.pdf', 'docs/interview-brief.pdf',
    'docs/120-day-plan.pdf', 'docs/ai-portfolio-review.pdf',
]
missing = [p for p in REQUIRED if not (ROOT / p).exists() or (ROOT / p).stat().st_size == 0]
if missing:
    raise SystemExit(f'Missing required files: {missing}')

# Construct the private orchestration-name pattern without shipping the literal term.
private_name = ''.join(chr(c) for c in [114, 111, 108, 101, 102, 111, 114, 103, 101])
private_pattern = re.compile(r'role[\s_-]*forge', re.I)
text_ext = {'.html', '.css', '.js', '.mjs', '.ts', '.svg', '.json', '.jsonld', '.md', '.txt', '.xml', '.yml', '.yaml'}
violations = []
for path in ROOT.rglob('*'):
    if not path.is_file() or '.git' in path.parts or path.suffix.lower() not in text_ext:
        continue
    text = path.read_text(encoding='utf-8', errors='ignore')
    if private_name.lower() in text.lower() or private_pattern.search(text):
        violations.append(str(path.relative_to(ROOT)))
if violations:
    raise SystemExit(f'Private-name matches: {violations}')

expected_pages = {'resume.pdf': 2, 'cover-letter.pdf': 1, 'interview-brief.pdf': 3, '120-day-plan.pdf': 4, 'ai-portfolio-review.pdf': 2}
for name, count in expected_pages.items():
    reader = PdfReader(ROOT / 'docs' / name)
    if len(reader.pages) != count:
        raise SystemExit(f'{name}: expected {count} pages, found {len(reader.pages)}')
    text = '\n'.join(page.extract_text() or '' for page in reader.pages)
    metadata = ' '.join(str(v) for v in (reader.metadata or {}).values())
    if private_name.lower() in (text + metadata).lower() or private_pattern.search(text + metadata):
        raise SystemExit(f'Private-name match in {name}')
    if name in {'resume.pdf', 'cover-letter.pdf'}:
        for required in ['412.287.8640', 'russelldudek@gmail.com', 'linkedin.com/in/russelldudek', 'https://russelldudek.github.io/Walmart/']:
            if required not in text:
                raise SystemExit(f'{name}: missing {required}')

resume = (ROOT / 'resume.html').read_text(encoding='utf-8')
cover = (ROOT / 'cover-letter.html').read_text(encoding='utf-8')
if 'View Cover Letter' not in resume or 'cover-letter.html' not in resume:
    raise SystemExit('Resume reciprocal navigation missing')
if 'View Resume' not in cover or 'resume.html' not in cover:
    raise SystemExit('Cover-letter reciprocal navigation missing')
for html in ['resume.html', 'cover-letter.html', 'interview-brief.html', '120-day-plan.html', 'ai-portfolio-review.html']:
    text = (ROOT / html).read_text(encoding='utf-8')
    if 'Download PDF' not in text:
        raise SystemExit(f'{html}: Download PDF missing')
print('Manifest: passed')
print('PDF pagination: passed')
print('Reciprocal navigation: passed')
print('Contact information: passed')
print('Candidate-facing confidentiality: passed')
