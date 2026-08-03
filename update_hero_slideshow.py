from pathlib import Path
import re

index_path = Path('index.html')
opt_dir = Path('photos') / 'optimized'
text = index_path.read_text(encoding='utf-8')

# Gather optimized images sorted by name
images = sorted([p.name for p in opt_dir.iterdir() if p.is_file() and p.suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp'}])
if not images:
    raise SystemExit('No optimized images found.')

# Build slide divs
slide_divs = '\n'.join([f'      <div class="slide slide-{i+1}"></div>' for i in range(len(images))])

# Build slide CSS rules
rules = []
for i, name in enumerate(images):
    delay = i * 6
    rules.append(f"    .slide-{i+1} {{\n      background-image: url(\"photos/optimized/{name}\");\n      animation-delay: {delay}s;\n    }}")
slide_rules = '\n\n'.join(rules) + '\n'

# Replace slide div block
start_marker = '<div class="slideshow">'
end_marker = '    </div>\n    <div class="hero-overlay"></div>'
if start_marker not in text or end_marker not in text:
    raise SystemExit('Hero slideshow block markers not found.')
slideshow_block_start = text.index(start_marker)
slideshow_block_end = text.index(end_marker, slideshow_block_start)
old_slideshow_block = text[slideshow_block_start:slideshow_block_end]
new_slideshow_block = start_marker + '\n' + slide_divs + '\n' + end_marker[:-1]
text = text[:slideshow_block_start] + new_slideshow_block + text[slideshow_block_end:]

# Replace slide CSS animation duration and slide rules
text = text.replace('animation: fadeSlide 42s infinite;', 'animation: fadeSlide 300s infinite;')
# Replace existing slide rules block using regex
pattern = re.compile(r'    \.slide-1 \{.*?\n\}\n\n(?=@keyframes fadeSlide)', re.S)
match = pattern.search(text)
if not match:
    raise SystemExit('Slide rules block not found.')
text = text[:match.start()] + slide_rules + text[match.end():]

# Replace keyframes block to fit 50 slides if needed
keyframes_block = '''    @keyframes fadeSlide {
      0% {
        opacity: 0;
        transform: scale(1.05);
      }

      0.7% {
        opacity: 1;
        transform: scale(1.08);
      }

      2% {
        opacity: 1;
        transform: scale(1.12);
      }

      3% {
        opacity: 0;
        transform: scale(1.12);
      }

      100% {
        opacity: 0;
        transform: scale(1.05);
      }
    }
'''
text = re.sub(r'    @keyframes fadeSlide \{.*?\n    \}\n', keyframes_block, text, flags=re.S)

index_path.write_text(text, encoding='utf-8')
print(f'Updated hero slideshow with {len(images)} slides.')
