import os
from PIL import Image

def optimize_images():
    source_dir = os.path.abspath("photos")
    target_dir = os.path.abspath(os.path.join("photos", "optimized"))
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"Created target directory: {target_dir}")
        
    print(f"Scanning for images in: {source_dir}")
    
    # Supported extensions
    valid_extensions = ('.jpg', '.jpeg')
    
    # Get all files in the source directory (excluding 'optimized' subdirectory)
    files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
    
    image_files = [f for f in files if f.lower().endswith(valid_extensions)]
    
    print(f"Found {len(image_files)} image(s) to process.")
    
    for filename in image_files:
        src_path = os.path.join(source_dir, filename)
        # Output filename should be lowercase as expected by portfolio.html
        dest_filename = filename.lower()
        dest_path = os.path.join(target_dir, dest_filename)
        
        print(f"Processing '{filename}' -> '{dest_filename}'...")
        try:
            with Image.open(src_path) as img:
                # Calculate new size maintaining aspect ratio
                max_size = 1200
                img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                
                # Save as JPEG with 80% quality
                img.save(dest_path, "JPEG", quality=80, optimize=True)
                
                # Compare sizes
                orig_size = os.path.getsize(src_path) / (1024 * 1024)
                opt_size = os.path.getsize(dest_path) / 1024
                print(f"  Done. Size reduced from {orig_size:.2f} MB to {opt_size:.1f} KB")
        except Exception as e:
            print(f"  Error processing '{filename}': {e}")

if __name__ == "__main__":
    optimize_images()
