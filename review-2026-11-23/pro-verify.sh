#!/bin/sh
# Read-only verification on the Pro: existence, size, sha256 per line of /tmp/pro-verify.tsv
# Input:  path<TAB>sha256<TAB>size
# Output: /tmp/pro-verify-out.tsv  path<TAB>status<TAB>actual_size<TAB>actual_sha
out=/tmp/pro-verify-out.tsv
: > "$out"
TAB=$(printf '\t')
count=0
while IFS="$TAB" read -r path sha size || [ -n "$path" ]; do
  count=$((count + 1))
  if [ ! -e "$path" ]; then
    printf '%s\tmissing\t\t\n' "$path" >> "$out"
  else
    actual_size=$(stat -f %z "$path")
    if [ "$actual_size" != "$size" ]; then
      printf '%s\tpresent-size-mismatch\t%s\t\n' "$path" "$actual_size" >> "$out"
    else
      actual_sha=$(shasum -a 256 "$path" | awk '{print $1}')
      if [ "$actual_sha" = "$sha" ]; then
        printf '%s\tpresent-match\t%s\t%s\n' "$path" "$actual_size" "$actual_sha" >> "$out"
      else
        printf '%s\tpresent-hash-mismatch\t%s\t%s\n' "$path" "$actual_size" "$actual_sha" >> "$out"
      fi
    fi
  fi
done < /tmp/pro-verify.tsv
echo "processed=$count"
wc -l "$out"
