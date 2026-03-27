import json
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description='Preview changes to the catalog')
    parser.add_argument('--catalog', required=True)
    args = parser.parse_args()

    if not os.path.exists(args.catalog):
        print(f"Catalog file not found: {args.catalog}")
        return

    with open(args.catalog, 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    total = len(catalog)
    complete = sum(1 for a in catalog if a['status'] == 'complete')
    pending = sum(1 for a in catalog if a['status'] == 'pending')
    needs_review = sum(1 for a in catalog if a['status'] == 'needs_review')

    print("Pipeline Summary:")
    print(f"Total Albums: {total}")
    print(f"Complete: {complete}")
    print(f"Pending: {pending}")
    print(f"Needs Review: {needs_review}")

    if needs_review > 0:
        print("\nAlbums needing review:")
        for a in catalog:
            if a['status'] == 'needs_review':
                print(f"- {a['artist']} - {a['album']}")

if __name__ == '__main__':
    main()
