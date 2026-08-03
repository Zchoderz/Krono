from pathlib import Path
text = Path('index.html').read_text(encoding='utf-8')
start = text.find('<div id="pdfOverlay"')
if start == -1:
    raise SystemExit('overlay start not found')
end = text.find('</div>\n  </div>\n  </div>\n\n', start)
if end == -1:
    end = text.find('</div>\n  </div>\n</div>\n', start)
if end == -1:
    raise SystemExit('overlay end not found')
end += len('</div>\n  </div>\n  </div>\n\n')
segment = text[start:end]
print(segment)
print('\n---SNIPPET-END---')
print('contains iframe', '<iframe' in segment)
print('contains pdf-overlay-body-images', 'pdf-overlay-body-images' in segment)
print('open tags count', segment.count('<img'), 'img count,', segment.count('</div>'), 'div close count')
