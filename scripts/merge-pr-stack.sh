#!/usr/bin/env bash
#
# Publish the whole docs stack to main, oldest first.
#
# Why this is not a plain `gh pr merge` loop
# ------------------------------------------
# The branches form a strictly linear stack: each is an ancestor of the next.
# Squash-merging one gives `main` a commit that exists in no branch's history, so
# the next PR's merge-base goes stale and GitHub reports CONFLICTING even though
# the content has not changed. `git rebase --onto` drops the already-merged prefix
# by its ORIGINAL sha and replays only that batch's own commits. That replay is
# conflict-free because `main` is tree-identical to the commit the batch sits on —
# which the script asserts before touching anything.
#
# Why it is a script and not something Claude ran
# -----------------------------------------------
# `git rebase` and `git push --force-with-lease` are both denied by the Claude Code
# auto-mode classifier. PR #1 was merged from the session; everything above it needs
# this.
#
# Safe to re-run: a step whose PR is already MERGED is skipped.
#
#   bash scripts/merge-pr-stack.sh
#
set -euo pipefail

# branch : original sha of the commit directly below this batch
#
# The shas are the pre-rebase tips and stay valid as the stack is consumed: a later
# branch still carries the earlier branch's original commits in its own history.
STACK=(
  "docs/fundamentals-batch-1:86fc3b4"
  "docs/fundamentals-batch-2:c533b89"
  "docs/fundamentals-batch-3:2caf549"
  "docs/fundamentals-batch-4:1341f9a"
  "docs/fundamentals-batch-5:3e262a5"
  "docs/patterns-batch-6:8e29c94"
  "docs/patterns-batch-7:8b9ec09"
  "docs/comparisons-batch-8:ea0cc86"
  "docs/resources-audit:d9b7aed"
  "docs/applied-sections:bea54ef"
  "docs/status-and-manifest-refresh:fb055cb"
  "docs/readme-front-door:7ac91f0"
  "chore/obsidian-vault-settings:fe21cc3"
  "build/vendor-doc-scripts:b14db6f"
)

start_branch=$(git rev-parse --abbrev-ref HEAD)
cleanup() { git rebase --abort 2>/dev/null || true; git checkout -q "$start_branch" 2>/dev/null || true; }
trap cleanup ERR INT

git diff --quiet && git diff --cached --quiet || {
  echo "ABORT: working tree is dirty. Commit or stash first." >&2; exit 1; }

for entry in "${STACK[@]}"; do
  IFS=: read -r branch base <<<"$entry"
  echo
  echo "=== $branch  (replaying everything above $base) ==="

  git fetch origin -q

  pr=$(gh pr list --head "$branch" --state all --json number,state \
         --jq 'map(select(.state != "CLOSED")) | .[0].number // empty')

  if [ -n "$pr" ] && [ "$(gh pr view "$pr" --json state --jq .state)" = "MERGED" ]; then
    echo "already merged as #$pr, skipping"
    continue
  fi

  # If main already contains this branch's tip, there is nothing left to do.
  if git merge-base --is-ancestor "$branch" origin/main 2>/dev/null; then
    echo "already in main, skipping"
    continue
  fi

  # The replay is only a no-op rebase if main matches the commit this batch sits on.
  if ! git diff --quiet origin/main "$base"; then
    echo "ABORT: origin/main is not tree-identical to $base." >&2
    echo "       The stack moved. Re-derive the bases before re-running." >&2
    exit 1
  fi

  git rebase --onto origin/main "$base" "$branch"
  git push --force-with-lease -u origin "$branch"

  if [ -z "$pr" ]; then
    gh pr create --base main --head "$branch" --fill
    pr=$(gh pr list --head "$branch" --state open --json number --jq '.[0].number')
    echo "opened #$pr"
  fi

  gh pr merge "$pr" --squash --delete-branch

  [ "$(gh pr view "$pr" --json state --jq .state)" = "MERGED" ] || {
    echo "ABORT: #$pr did not merge" >&2; exit 1; }
done

git fetch origin -q
git checkout -q main && git merge --ff-only origin/main

echo
echo "Done. main is now:"
git log --oneline -12 main
echo
echo "Verify:"
echo "  python scripts/gen_backlinks.py .                                  # twice, 0 changed"
echo "  python scripts/check_links.py ."
echo "  expected: 2023 relative links checked, 0 broken, exit 0"
