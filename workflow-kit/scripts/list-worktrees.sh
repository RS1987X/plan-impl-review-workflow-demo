#!/bin/bash

set -euo pipefail

# List worktrees for the repo, with a hint about parallel-lane layout.

REPO_DIR="$(pwd)"
REPO_BASENAME=$(basename "$REPO_DIR")
BASE_NAME=${REPO_BASENAME%-plan}
BASE_NAME=${BASE_NAME%-impl}
BASE_NAME=${BASE_NAME%-review}

echo "Git worktrees (git worktree list):"
git worktree list

echo "---"
PARALLEL_ROOT="../${BASE_NAME}-worktrees"
if [ -d "$PARALLEL_ROOT" ]; then
  echo "Parallel lanes detected under: $PARALLEL_ROOT"
  find "$PARALLEL_ROOT" -maxdepth 2 -mindepth 2 -type d \( -name plan -o -name impl -o -name review \) -print | sort
else
  echo "No parallel lanes folder found ($PARALLEL_ROOT)."
  echo "Tip: create one with: ./scripts/create-worktrees.sh <feature> --parallel"
fi
