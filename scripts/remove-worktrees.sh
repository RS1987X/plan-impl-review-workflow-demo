#!/bin/bash

set -euo pipefail

# Remove the worktrees created for the AI workflow.
# Safe to run from any worktree; it removes sibling directories.

REPO_DIR="$(pwd)"
REPO_BASENAME=$(basename "$REPO_DIR")
BASE_NAME=${REPO_BASENAME%-plan}
BASE_NAME=${BASE_NAME%-impl}
BASE_NAME=${BASE_NAME%-review}

PLAN_DIR="../${BASE_NAME}-plan"
IMPL_DIR="../${BASE_NAME}-impl"
REVIEW_DIR="../${BASE_NAME}-review"

git worktree remove "$PLAN_DIR" || true
git worktree remove "$REVIEW_DIR" || true
git worktree remove "$IMPL_DIR" || true

echo "Worktrees removed (if they existed):"
echo "- $PLAN_DIR"
echo "- $IMPL_DIR"
echo "- $REVIEW_DIR"