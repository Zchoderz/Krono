from pathlib import Path
from PIL import Image

source_dir = Path('portfolio photos')
target_dir = Path('photos') / 'optimized'
target_dir.mkdir(parents=True, exist_ok=True)

files_processed = []
for path in sorted(source_dir.iterdir()):
    if path.is_file() and path.suffix.lower() in {'.jpg', '.jpeg', '.png'}:
        target_path = target_dir / path.name
        try:
            with Image.open(path) as img:
                img = img.convert('RGB')
                img.save(target_path, format='JPEG', quality=85, optimize=True, progressive=True)
            files_processed.append(path.name)
        except Exception as exc:
            print(f'ERROR processing {path.name}: {exc}')

print(f'Processed {len(files_processed)} files into {target_dir.resolve()}')
for name in files_processed:
    print(name)
