import json
import argparse
import requests
import time

def search_musicbrainz(artist, album, year=None):
    base_url = "https://musicbrainz.org/ws/2/release/"
    query = f'release:"{album}" AND artist:"{artist}"'
    if year:
        query += f' AND date:{year}'
    
    params = {
        'query': query,
        'fmt': 'json',
        'limit': 5
    }
    
    # MusicBrainz asks for a User-Agent
    headers = {
        'User-Agent': 'AlbumLibraryStaticSiteGenerator/1.0.0 ( ceth@example.com )'
    }
    
    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        candidates = []
        for release in data.get('releases', []):
            release_id = release.get('id')
            title = release.get('title')
            artist_name = release.get('artist-credit', [{}])[0].get('artist', {}).get('name')
            release_year = release.get('date', '').split('-')[0]
            
            # Cover Art Archive URL
            cover_url = f"https://coverartarchive.org/release/{release_id}/front-500"
            
            candidates.append({
                "id": release_id,
                "title": title,
                "artist": artist_name,
                "year": int(release_year) if release_year.isdigit() else None,
                "cover_url": cover_url,
                "source": "musicbrainz"
            })
            
        return candidates
    except Exception as e:
        print(f"Error searching MusicBrainz: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description='Match album to candidate releases')
    parser.add_argument('--artist', required=True)
    parser.add_argument('--album', required=True)
    parser.add_argument('--year', type=int)
    args = parser.parse_args()

    candidates = search_musicbrainz(args.artist, args.album, args.year)
    print(json.dumps(candidates, indent=2))

if __name__ == '__main__':
    main()
