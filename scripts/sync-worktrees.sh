#!/bin/bash

set -euo pipefail

# Synchronize worktrees using a merge-based workflow (no rebase).
#
# Usage:
#   ./sync-worktrees.sh <feature-name> [<implementer-ref>]
#
# Examples:
#   ./sync-worktrees.sh demo-workflow-1
#   ./sync-worktrees.sh demo-workflow-1 origin/copilot/implement-snake-game-phase-1

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
    echo "Usage: $0 <feature-name> [<implementer-ref>]"
    echo "  <implementer-ref> defaults to origin/feat-<feature-name>"
    exit 1
fi

FEATURE="$1"
REMOTE="origin"
MAIN_REF="$REMOTE/main"
IMPL_REF=${2:-"$REMOTE/feat-$FEATURE"}

# Script directory lives under <repo>/scripts; repo root is one up.
REPO_DIR="$(dirname "$(realpath "$0")")"
REPO_DIR="$(dirname "$REPO_DIR")"

# Make this script portable when run from -plan/-impl/-review worktrees.
REPO_BASENAME=$(basename "$REPO_DIR")
BASE_NAME=${REPO_BASENAME%-plan}
BASE_NAME=${BASE_NAME%-impl}
BASE_NAME=${BASE_NAME%-review}

PLAN_DIR="$REPO_DIR/../${BASE_NAME}-plan"
IMPL_DIR="$REPO_DIR/../${BASE_NAME}-impl"
REVIEW_DIR="$REPO_DIR/../${BASE_NAME}-review"

echo "Fetching $REMOTE once (shared across worktrees)..."
git -C "$REPO_DIR" fetch "$REMOTE" --prune

echo "---"
echo "Sync planner worktree with $MAIN_REF"
git -C "$PLAN_DIR" fetch "$REMOTE" --prune
git -C "$PLAN_DIR" merge "$MAIN_REF"

echo "---"
echo "Sync implementer worktree with $MAIN_REF"
git -C "$IMPL_DIR" fetch "$REMOTE" --prune
git -C "$IMPL_DIR" merge "$MAIN_REF"

echo "---"
echo "Sync reviewer worktree with implementer ref: $IMPL_REF"
git -C "$REVIEW_DIR" fetch "$REMOTE" --prune
git -C "$REVIEW_DIR" merge "$IMPL_REF"

echo "---"
echo "Reviewer next steps (run from $REVIEW_DIR):"
echo "  git diff $MAIN_REF...HEAD"
echo "  npm test"
echo "  npm run build"
echo ""
echo "Note: if the implementer used a different branch (e.g. copilot/*), rerun with:"
echo "  $0 $FEATURE $REMOTE/<that-branch>"