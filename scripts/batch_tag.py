#!/usr/bin/env python3
"""
batch_tag.py
------------
Apply one or more tags to a list of Readwise documents identified by their IDs.

Usage:
    # Tag all day-of articles from the CSV:
    python batch_tag.py --tag DayOf_Oct7 --csv ../day_of_oct7.csv --id-col id

    # Tag specific document IDs:
    python batch_tag.py --tag loc:NovaFestival --ids abc123 def456 ghi789

    # Tag all documents currently tagged 'Hamas' also with 'unit:Nukhba':
    python batch_tag.py --tag unit:Nukhba --source-tag Hamas --dry-run

Requirements:
    pip install requests
"""

import os
import csv
import time
import argparse
import requests

TOKEN = os.environ.get("READWISE_TOKEN")
if not TOKEN:
    raise EnvironmentError("Set READWISE_TOKEN environment variable first.")

BASE_URL = "https://readwise.io/api/v3"
HEADERS = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json"}


def get_documents_by_tag(tag: str) -> list[str]:
    """Return all document IDs with a given tag."""
    ids = []
    params = {"tags": tag, "page_size": 100}
    url = f"{BASE_URL}/documents/"

    while url:
        resp = requests.get(url, headers=HEADERS, params=params)
        resp.raise_for_status()
        data = resp.json()
        ids.extend(doc["id"] for doc in data.get("results", []))
        cursor = data.get("nextPageCursor")
        url = f"{BASE_URL}/documents/" if cursor else None
        params = {"pageCursor": cursor} if cursor else {}
        time.sleep(0.3)

    return ids


def apply_tag(doc_id: str, tag: str, dry_run: bool = False) -> bool:
    """Apply a tag to a single document via PATCH."""
    if dry_run:
        print(f"  [DRY RUN] Would tag {doc_id} with '{tag}'")
        return True

    # First fetch current tags
    resp = requests.get(f"{BASE_URL}/documents/{doc_id}/", headers=HEADERS)
    if resp.status_code != 200:
        print(f"  WARN: Could not fetch {doc_id} — {resp.status_code}")
        return False

    doc = resp.json()
    existing_tags = doc.get("tags", {})
    if isinstance(existing_tags, dict):
        existing_tags = list(existing_tags.keys())

    if tag in existing_tags:
        print(f"  SKIP {doc_id}: already has tag '{tag}'")
        return True

    new_tags = existing_tags + [tag]
    patch_resp = requests.patch(
        f"{BASE_URL}/documents/{doc_id}/",
        headers=HEADERS,
        json={"tags": {t: {} for t in new_tags}},
    )

    if patch_resp.status_code in (200, 204):
        print(f"  OK   {doc_id}: tagged '{tag}'")
        return True
    else:
        print(f"  FAIL {doc_id}: {patch_resp.status_code} — {patch_resp.text[:100]}")
        return False


def load_ids_from_csv(csv_path: str, id_col: str) -> list[str]:
    ids = []
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get(id_col):
                ids.append(row[id_col].strip())
    return ids


def main():
    parser = argparse.ArgumentParser(description="Batch tag Readwise documents")
    parser.add_argument("--tag", required=True, help="Tag to apply")
    parser.add_argument("--csv", help="CSV file with document IDs")
    parser.add_argument("--id-col", default="id", help="Column name for document ID in CSV")
    parser.add_argument("--ids", nargs="+", help="Explicit document IDs to tag")
    parser.add_argument("--source-tag", help="Apply tag to all docs already tagged with this")
    parser.add_argument("--dry-run", action="store_true", help="Preview without making changes")
    args = parser.parse_args()

    doc_ids = []

    if args.csv:
        doc_ids = load_ids_from_csv(args.csv, args.id_col)
        print(f"Loaded {len(doc_ids)} IDs from {args.csv}")

    if args.ids:
        doc_ids.extend(args.ids)

    if args.source_tag:
        print(f"Fetching all docs tagged '{args.source_tag}'...")
        doc_ids.extend(get_documents_by_tag(args.source_tag))
        print(f"  Found {len(doc_ids)} documents")

    if not doc_ids:
        print("No document IDs specified. Use --csv, --ids, or --source-tag.")
        return

    doc_ids = list(set(doc_ids))  # deduplicate
    print(f"\nApplying tag '{args.tag}' to {len(doc_ids)} documents...\n")

    ok = fail = skip = 0
    for doc_id in doc_ids:
        result = apply_tag(doc_id, args.tag, dry_run=args.dry_run)
        if result:
            ok += 1
        else:
            fail += 1
        time.sleep(0.2)  # rate limit courtesy

    print(f"\nDone. OK={ok}  FAIL={fail}")


if __name__ == "__main__":
    main()
