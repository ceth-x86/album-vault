import os
import re
import requests
import argparse
from pathlib import Path
from typing import Optional

MUSICBRAINZ_SEARCH_URL = "https://musicbrainz.org/ws/2/release/"
COVER_ART_ARCHIVE_URL = "https://coverartarchive.org/release"

class AlbumCoverFetcher:
    def __init__(self, user_agent: str):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})

    def find_release_mbid(self, artist: str, album: str) -> Optional[str]:
        query = f'release:"{album}" AND artist:"{artist}"'
        params = {"query": query, "fmt": "json", "limit": 5}
        try:
            response = self.session.get(MUSICBRAINZ_SEARCH_URL, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            releases = data.get("releases", [])
            return releases[0]["id"] if releases else None
        except Exception as e:
            print(f"Error searching MusicBrainz: {e}")
            return None

    def download_cover(self, mbid: str, output_path: str) -> bool:
        url = f"{COVER_ART_ARCHIVE_URL}/{mbid}/front"
        try:
            response = self.session.get(url, timeout=20, allow_redirects=True)
            if response.status_code != 200:
                return False
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(response.content)
            return True
        except Exception as e:
            print(f"Error downloading cover: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Fetch album cover using MusicBrainz/CAA')
    parser.add_argument('--artist', required=True)
    parser.add_argument('--album', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--mbid', help='Optional MusicBrainz ID')
    args = parser.parse_args()

    fetcher = AlbumCoverFetcher(user_agent="MyAlbumCoverApp/1.0 ( ceth@example.com )")
    
    mbid = args.mbid if args.mbid else fetcher.find_release_mbid(args.artist, args.album)
    
    if not mbid:
        print(f"MBID not found for {args.artist} - {args.album}")
        exit(1)

    if fetcher.download_cover(mbid, args.output):
        print(f"Successfully downloaded to {args.output}")
    else:
        print(f"Failed to download cover for MBID {mbid}")
        exit(1)

if __name__ == '__main__':
    main()
