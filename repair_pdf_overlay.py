from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
start_marker = '<div id="pdfOverlay" class="pdf-overlay" aria-hidden="true">'
end_marker = '<!-- Services Section -->'
start = text.find(start_marker)
if start == -1:
    raise SystemExit('overlay start marker not found')
end = text.find(end_marker, start)
if end == -1:
    raise SystemExit('services section marker not found after overlay')

replacement = '''<div id="pdfOverlay" class="pdf-overlay" aria-hidden="true">
    <div class="pdf-overlay-inner" role="dialog" aria-modal="true" aria-labelledby="pdfOverlayTitle">
      <div class="pdf-overlay-header">
        <div>
          <h2 id="pdfOverlayTitle">Krono Property Management Services</h2>
          <p>Preview the brochure below, or download a copy.</p>
        </div>
        <div class="pdf-overlay-header-actions">
          <a href="Krono brochure.pdf" download class="btn btn-navy" style="padding:0.55rem 1.2rem;font-size:0.85rem;">Download PDF</a>
          <button type="button" class="pdf-overlay-close" onclick="closePdfOverlay()" aria-label="Close PDF overlay">×</button>
        </div>
      </div>
      <div class="pdf-overlay-body">
        <div class="pdf-overlay-body-images">
          <img src="brochure-page-1.png" alt="Brochure front page preview">
          <img src="brochure-page-2.png" alt="Brochure back page preview">
        </div>
      </div>
    </div>
  </div>
'''

text = text[:start] + replacement + text[end:]
path.write_text(text, encoding='utf-8')
print('Replaced broken overlay with clean image preview markup.')
