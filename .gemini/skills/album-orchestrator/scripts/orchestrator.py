import json
import subprocess
import os
import argparse

VENV_PYTHON = os.path.expanduser("~/venv/cover-api/bin/python3")

def run_script(script_path, args):
    cmd = [VENV_PYTHON, script_path] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return result.stdout

def log_event(step, album_slug, result, details):
    log_path = 'state/run_log.json'
    log_entry = {"step": step, "album": album_slug, "result": result, "details": details}
    logs = []
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            try: logs = json.load(f)
            except: logs = []
    logs.append(log_entry)
    with open(log_path, 'w') as f: json.dump(logs, f, indent=2)

def main():
    catalog_path = 'state/catalog.json'
    if not os.path.exists(catalog_path): return

    with open(catalog_path, 'r') as f:
        catalog = json.load(f)

    for album in catalog:
        if album['status'] == 'complete': continue

        print(f"Processing {album['artist']} - {album['album']}...")
        
        # 1. Fetch (Using updated script that handles MBID search internally)
        cover_filename = f"{album['slug']}.jpg"
        cover_path = os.path.join('public', 'covers', cover_filename)
        
        fetch_output = run_script('scripts/fetch_cover.py', [
            '--artist', album['artist'],
            '--album', album['album'],
            '--output', cover_path
        ])
        
        if not fetch_output:
            album['status'] = 'needs_review'
            log_event('fetch', album['slug'], 'fail', 'Download error or MBID not found')
            continue

        # 2. Validate
        validate_output = run_script('scripts/validate_cover.py', ['--file', cover_path])
        if not validate_output:
            album['status'] = 'needs_review'
            log_event('validate', album['slug'], 'fail', 'Script error')
            continue

        validation = json.loads(validate_output)
        if validation['valid']:
            album['status'] = 'complete'
            album['cover_path'] = f"/covers/{cover_filename}"
            log_event('validate', album['slug'], 'success', {})
        else:
            album['status'] = 'needs_review'
            log_event('validate', album['slug'], 'fail', validation['issues'])

    with open(catalog_path, 'w') as f: json.dump(catalog, f, indent=2)
    print("Orchestration complete.")

if __name__ == '__main__': main()
