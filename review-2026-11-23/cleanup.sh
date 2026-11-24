#!/bin/sh
# Cleanup: delete superseded _deleted-backup files on the Studio.
# For each row (backup<TAB>canonical<TAB>sha256<TAB>size): verify the canonical
# live copy still exists with the registry sha, THEN delete the backup.
# Never deletes if the canonical is missing or hash-mismatched.
set -u
TSV="${1:-/tmp/cleanup.tsv}"
OUT="${2:-/tmp/cleanup-out.tsv}"
: > "$OUT"
deleted=0; skipped=0; gone=0
while IFS="$(printf '\t')" read -r backup canon sha size; do
  [ -z "$backup" ] && continue
  if [ ! -f "$canon" ]; then
    echo "SKIP canon-missing $backup" >> "$OUT"; skipped=$((skipped+1)); continue
  fi
  actual=$(shasum -a 256 "$canon" | awk '{print $1}')
  if [ "$actual" != "$sha" ]; then
    echo "SKIP canon-hash-mismatch $backup" >> "$OUT"; skipped=$((skipped+1)); continue
  fi
  if [ ! -f "$backup" ]; then
    echo "ALREADY-GONE $backup" >> "$OUT"; gone=$((gone+1)); continue
  fi
  rm -- "$backup"
  if [ -e "$backup" ]; then
    echo "FAIL still-present $backup" >> "$OUT"; skipped=$((skipped+1))
  else
    echo "DELETED $backup" >> "$OUT"; deleted=$((deleted+1))
  fi
done < "$TSV"
echo "SUMMARY deleted=$deleted skipped=$skipped already-gone=$gone" >> "$OUT"
echo "deleted=$deleted skipped=$skipped already-gone=$gone"
