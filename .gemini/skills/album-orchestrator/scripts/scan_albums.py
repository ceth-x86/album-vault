import os
import re
import json
import argparse

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def parse_header_metadata(content):
    # Pattern to match "# Artist — Album (Year)"
    # Supports both standard dash "-" and long dash "—"
    match = re.search(r'^#\s*(.*?)\s*[—\-]\s*(.*?)\s*\((\d{4})\)', content)
    if match:
        return {
            'artist': match.group(1).strip(),
            'album': match.group(2).strip(),
            'year': int(match.group(3))
        }
    return {}

def main():
    parser = argparse.ArgumentParser(description='Scan albums from markdown files')
    parser.add_argument('--input', required=True, help='Input directory')
    parser.add_argument('--output', required=True, help='Output catalog file')
    args = parser.parse_args()

    catalog = []
    if not os.path.exists(args.input):
        print(f"Error: Input directory {args.input} does not exist.")
        return

    for filename in os.listdir(args.input):
        if filename.endswith('.md'):
            file_path = os.path.join(args.input, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                metadata = parse_header_metadata(content)
                
                if not metadata:
                    print(f"Warning: Could not parse metadata from {filename}. Skipping.")
                    continue

                artist = metadata['artist']
                album = metadata['album']
                year = metadata['year']
                
                slug = slugify(f"{artist}-{album}")
                cover_filename = f"{slug}.jpg"
                cover_path = os.path.join('public', 'covers', cover_filename)
                
                status = 'pending'
                if os.path.exists(cover_path):
                    status = 'complete'
                
                catalog.append({
                    "source_file": file_path,
                    "artist": artist,
                    "album": album,
                    "year": year,
                    "slug": slug,
                    "cover_path": f"/covers/{cover_filename}" if os.path.exists(cover_path) else None,
                    "status": status
                })

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2)

    print(f"Catalog saved to {args.output} ({len(catalog)} albums found)")

if __name__ == '__main__':
    main()
