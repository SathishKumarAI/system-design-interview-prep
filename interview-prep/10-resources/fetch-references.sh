#!/usr/bin/env bash
# Clone or update the upstream system-design reference repos into ./vendor/.
#
# vendor/ is gitignored and READ-ONLY — never edit anything in it. See ../../CLAUDE.md.
#
#   bash fetch-references.sh           clone missing repos, update existing ones
#   bash fetch-references.sh --clean   delete vendor/ and re-clone everything
#
# Shallow clones (--depth 1): ~100 MB total instead of several GB of history.

set -euo pipefail

VENDOR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/vendor"

REPOS=(
  donnemartin/system-design-primer
  ByteByteGoHq/system-design-101
  ashishps1/awesome-system-design-resources
  karanpratapsingh/system-design
  alirezadir/Machine-Learning-Interviews
  chiphuyen/machine-learning-systems-design
  eugeneyan/applied-ml
  binhnguyennus/awesome-scalability
  yangshun/front-end-interview-handbook
  checkcheckzz/system-design-interview
)

if [[ "${1:-}" == "--clean" ]]; then
  echo "Removing $VENDOR_DIR"
  rm -rf "$VENDOR_DIR"
fi

mkdir -p "$VENDOR_DIR"
cd "$VENDOR_DIR"

for repo in "${REPOS[@]}"; do
  name="$(basename "$repo")"
  if [[ -d "$name/.git" ]]; then
    printf 'updating %-42s ' "$name"
    git -C "$name" fetch --depth 1 origin -q \
      && git -C "$name" reset --hard -q origin/HEAD 2>/dev/null \
      || git -C "$name" reset --hard -q "@{upstream}" 2>/dev/null \
      || true
    echo "ok"
  else
    printf 'cloning  %-42s ' "$name"
    if git clone --depth 1 -q "https://github.com/${repo}.git" "$name"; then
      echo "ok"
    else
      echo "FAILED"
    fi
  fi
done

echo
echo "vendor/ contents:"
du -sh -- */ 2>/dev/null || true
echo
echo "Reminder: vendor/ is gitignored and read-only. Do not edit."
