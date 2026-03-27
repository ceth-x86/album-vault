# Album Library Static Site Generator — Agent-Ready Specification

## 1. Overview

A deterministic + AI-assisted pipeline that converts a local Markdown album library into a static website (Astro), enriches it with album covers, and deploys it via GitHub Pages.

This spec is designed to be executed by a Gemini CLI skill acting as an orchestrator.

---

## 2. Core Design Principles

1. Markdown is the single source of truth
2. All filesystem/network operations are deterministic scripts
3. AI is used only for ambiguity resolution and validation
4. Every step is observable and reproducible
5. No irreversible action without explicit confirmation

---

## 3. Directory Structure

```
/content/albums/
/public/covers/
/scripts/
  scan_albums.py
  match_album.py
  fetch_cover.py
  validate_cover.py
  preview_changes.py
/site/ (Astro project)
/.github/workflows/deploy.yml
/state/
  catalog.json
  decisions.json
  run_log.json
```

---

## 4. Data Contracts (CRITICAL)

### 4.1 Album Record

```json
{
  "source_file": "string",
  "artist": "string",
  "album": "string",
  "year": "number|null",
  "slug": "string",
  "cover_path": "string|null",
  "status": "pending|complete|needs_review"
}
```

---

### 4.2 Candidate Release

```json
{
  "id": "string",
  "title": "string",
  "artist": "string",
  "year": "number|null",
  "cover_url": "string|null",
  "source": "musicbrainz|spotify|lastfm"
}
```

---

### 4.3 AI Decision Output (STRICT FORMAT)

```json
{
  "selected_candidate": "string|null",
  "confidence": "number",
  "reason": "string",
  "needs_review": "boolean"
}
```

Constraints:

* confidence ∈ [0,1]
* must always return valid JSON

---

## 5. CLI Commands (MANDATORY INTERFACE)

### 5.1 Scan Albums

```
python scripts/scan_albums.py --input content/albums --output state/catalog.json
```

---

### 5.2 Match Album

```
python scripts/match_album.py --artist "..." --album "..." --year 1989
```

Output → candidates JSON

---

### 5.3 Fetch Cover

```
python scripts/fetch_cover.py --mbid "..." --output public/covers/{slug}.jpg
```

---

### 5.4 Validate Cover

```
python scripts/validate_cover.py --file public/covers/{slug}.jpg
```

Output:

```json
{
  "valid": true,
  "issues": []
}
```

---

### 5.5 Build Site

```
cd site && npm run build
```

---

### 5.6 Preview Changes

```
python scripts/preview_changes.py --catalog state/catalog.json
```

---

## 6. State Machine (VERY IMPORTANT)

Each album goes through states:

```
pending → matched → cover_downloaded → validated → complete
                               ↓
                        needs_review
```

Rules:

* No skipping states
* Failed validation → retry OR needs_review

---

## 7. Full Pipeline Flow

### STEP 1: Scan

* Generate catalog.json

### STEP 2: Iterate albums

For each album:

#### IF cover exists → mark complete

#### ELSE:

1. Run match_album
2. Send candidates to AI
3. Receive decision

IF decision.selected_candidate == null → needs_review

4. fetch_cover
5. validate_cover

IF validation fails:

* try next candidate (max 3 attempts)

IF still failing:

* mark needs_review

---

## 8. Retry Policy

* Max attempts per album: 3
* If AI confidence < 0.6 → try next candidate
* If no candidates → needs_review

---

## 9. AI Responsibilities (STRICT)

AI MUST:

* Rank candidates
* Provide reasoning
* Respect confidence thresholds

AI MUST NOT:

* Access filesystem directly
* Modify files
* Execute shell commands

---

## 10. Validation Rules

Hard constraints:

* min resolution: 300x300
* aspect ratio: 0.8–1.2
* file size > 5KB

Soft (AI):

* cover matches album semantics

---

## 11. Build & Preview

After processing all albums:

1. Build Astro
2. Generate preview summary

Example:

```
Processed: 10
Downloaded: 8
Needs review: 2
```

---

## 12. Deployment Policy

### SAFE MODE (default)

* Create branch
* Commit changes
* Open PR

### TRUSTED MODE

* Commit directly
* Push

---

## 13. Confirmation Protocol

Before deployment AI MUST ask:

"Do you want to proceed with commit and deploy?"

---

## 14. Logging

All steps logged to:

```
/state/run_log.json
```

Each entry:

```json
{
  "step": "match|fetch|validate",
  "album": "slug",
  "result": "success|fail",
  "details": {}
}
```

---

## 15. Failure Handling

Case → Action:

* No candidates → needs_review
* Download fail → retry
* Validation fail → retry next candidate
* Build fail → STOP

---

## 16. Extensibility Hooks

Future:

* ratings
* artist pages
* search index
* embeddings

---

## 17. Success Criteria

* ≥90% albums auto-resolved
* deterministic output
* no broken builds
* manual review list generated

---

## 18. Final Behavior

Gemini skill executes:

1. scan
2. loop albums
3. resolve covers
4. validate
5. build
6. summarize
7. ask confirmation
8. deploy

---

## END
