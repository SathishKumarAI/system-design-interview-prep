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

# Verdicts, licences and last-push dates for every repo below: github-repos.md.
REPOS=(
  # run something (github-repos.md §3)
  jepsen-io/maelstrom
  ept/hermitage
  # learn a mechanism (§1)
  aphyr/distsys-class
  theanalyst/awesome-distributed-systems
  pingcap/awesome-database-learning
  asatarin/testing-distributed-systems
  ashishps1/awesome-system-design-resources
  # real architectures and real failures (§2)
  danluu/post-mortems
  upgundecha/howtheysre
  eugeneyan/applied-ml
  binhnguyennus/awesome-scalability
  # drill cases (§4)
  donnemartin/system-design-primer
  ByteByteGoHq/system-design-101
  karanpratapsingh/system-design
  alirezadir/AIMLInterviews          # renamed from Machine-Learning-Interviews
  yangshun/front-end-interview-handbook
)

if [[ "${1:-}" == "--clean" ]]; then
  echo "Removing $VENDOR_DIR"
  rm -rf "$VENDOR_DIR"
fi

mkdir -p "$VENDOR_DIR"
cd "$VENDOR_DIR"

# Prune anything no longer in REPOS — this is what removes a dropped repo, and what
# handles an upstream rename (the old directory name simply stops being listed).
for dir in */; do
  name="${dir%/}"
  keep=""
  for repo in "${REPOS[@]}"; do
    [[ "$(basename "$repo")" == "$name" ]] && keep=1 && break
  done
  if [[ -z "$keep" ]]; then
    printf 'pruning  %-42s ' "$name"
    rm -rf -- "$name" && echo "ok"
  fi
done

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
