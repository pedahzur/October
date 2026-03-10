#!/usr/bin/env python3
"""
export_readwise.py
------------------
Export all documents from the October_7_2023 Readwise Reader tag to CSV and JSON.

Usage:
    export READWISE_TOKEN=your_token_here
    python export_readwise.py

Output:
    articles_metadata.csv   — Full export of all tagged documents
    articles_metadata.json  — Same data in JSON format

Requirements:
    pip install requests python-dotenv
"""

import os
import csv
import json
import time
import requests
from datetime import datetime

# ── Config ──────────────────────────────────────────────────────────────────
TOKEN = os.environ.get("READWISE_TOKEN")
if not TOKEN:
    raise EnvironmentError("Set READWISE_TOKEN environment variable first.")

BASE_URL = "https://readwise.io/api/v3"
HEADERS = {"Authorization": f"Token {TOKEN}"}
TARGET_TAG = "October_7_2023"

# CSV column schema
COLUMNS = [
    "id",
    "title",
    "author",
    "source_url",
    "source_domain",
    "published_date",
    "saved_date",
    "language",
    "word_count",
    "reading_progress",
    "tags",
    "category",
    "summary",
    "notes",
    "readwise_url",
]


def fetch_all_documents(tag: str) -> list[dict]:
    """Paginate through all documents with the given tag."""
    documents = []
    params = {
        "tags": tag,
        "page_size": 100,
    }
    url = f"{BASE_URL}/documents/"

    while url:
        resp = requests.get(url, headers=HEADERS, params=params)
        resp.raise_for_status()
        data = resp.json()

        documents.extend(data.get("results", []))
        print(f"  Fetched {len(documents)} documents so far...")

        # Handle pagination
        next_url = data.get("nextPageCursor")
        if next_url:
            url = f"{BASE_URL}/documents/"
            params = {"pageCursor": next_url}
        else:
            url = None

        # Respect rate limits
        time.sleep(0.5)

    return documents


def extract_row(doc: dict) -> dict:
    """Extract and normalize fields from a Readwise document object."""
    tags = doc.get("tags", {})
    tag_names = list(tags.keys()) if isinstance(tags, dict) else tags

    return {
        "id": doc.get("id", ""),
        "title": doc.get("title", "").strip(),
        "author": doc.get("author", ""),
        "source_url": doc.get("source_url", ""),
        "source_domain": doc.get("domain", ""),
        "published_date": doc.get("published_date", ""),
        "saved_date": doc.get("created_at", ""),
        "language": doc.get("language", ""),
        "word_count": doc.get("word_count", ""),
        "reading_progress": doc.get("reading_progress", ""),
        "tags": "; ".join(tag_names),
        "category": doc.get("category", ""),
        "summary": doc.get("summary", "").replace("\n", " "),
        "notes": doc.get("notes", "").replace("\n", " "),
        "readwise_url": f"https://read.readwise.io/read/{doc.get('id', '')}",
    }


def save_csv(rows: list[dict], path: str):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Saved CSV: {path}")


def save_json(docs: list[dict], path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)
    print(f"  Saved JSON: {path}")


def main():
    print(f"Exporting Readwise tag: {TARGET_TAG}")
    print(f"Timestamp: {datetime.now().isoformat()}\n")

    # Fetch
    print("Fetching documents from Readwise API v3...")
    documents = fetch_all_documents(TARGET_TAG)
    print(f"\nTotal documents fetched: {len(documents)}\n")

    # Transform
    rows = [extract_row(doc) for doc in documents]

    # Save
    save_csv(rows, "articles_metadata.csv")
    save_json(documents, "articles_metadata.json")

    # Summary stats
    languages = {}
    for row in rows:
        lang = row["language"] or "unknown"
        languages[lang] = languages.get(lang, 0) + 1

    print("\nLanguage breakdown:")
    for lang, count in sorted(languages.items(), key=lambda x: -x[1]):
        print(f"  {lang}: {count}")

    print(f"\nDone. {len(rows)} documents exported.")


if __name__ == "__main__":
    main()
