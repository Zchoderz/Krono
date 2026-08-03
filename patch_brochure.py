import base64
from pathlib import Path

html_path = Path('index.html')
img1 = Path('brochure-page-1.png')
img2 = Path('brochure-page-2.png')

if not html_path.exists():
    raise SystemExit('index.html not found')
if not img1.exists() or not img2.exists():
    raise SystemExit('Brochure image files missing')

with img1.open('rb') as f:
    data1 = base64.b64encode(f.read()).decode('ascii')
with img2.open('rb') as f:
    data2 = base64.b64encode(f.read()).decode('ascii')

old = '''      <div class="pdf-overlay-body">
        <iframe src="Krono brochure.pdf" frameborder="0" allowfullscreen></iframe>
      </div>'''

new = f'''      <div class="pdf-overlay-body">
        <div class="pdf-preview-scroll">
          <img class="pdf-preview-image" src="data:image/png;base64,{data1}" alt="Brochure front page preview">
          <img class="pdf-preview-image" src="data:image/png;base64,{data2}" alt="Brochure back page preview">
        </div>
      </div>'''

text = html_path.read_text(encoding='utf-8')
if old not in text:
    raise SystemExit('Expected iframe block not found in index.html')

text = text.replace(old, new, 1)
html_path.write_text(text, encoding='utf-8')
print('index.html updated with embedded brochure images')
