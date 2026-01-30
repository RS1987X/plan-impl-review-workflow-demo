#!/bin/bash

set -euo pipefail

# Remove the worktrees created for the AI workflow.
# Safe to run from any worktree; it removes sibling directories.
#
# Usage:
#   ./remove-worktrees.sh [<feature-name>] [--parallel]
#
# - Without args: removes the default single-lane siblings (../<repo>-plan/impl/review)
# - With <feature-name> and --parallel: removes ../<repo>-worktrees/<feature>/{plan,impl,review}

REPO_DIR="$(pwd)"
REPO_BASENAME=$(basename "$REPO_DIR")
BASE_NAME=${REPO_BASENAME%-plan}
BASE_NAME=${BASE_NAME%-impl}
BASE_NAME=${BASE_NAME%-review}

FEATURE="${1:-}"
MODE="${2:-}"
PARALLEL=0
if [ "$MODE" = "--parallel" ]; then
	PARALLEL=1
elif [ -n "$MODE" ]; then
	echo "Unknown option: $MODE" >&2
	echo "Usage: $0 [<feature-name>] [--parallel]" >&2
	exit 1
fi

if [ $PARALLEL -eq 1 ]; then
	if [ -z "$FEATURE" ]; then
		echo "Error: feature-name is required with --parallel" >&2
		echo "Usage: $0 <feature-name> --parallel" >&2
		exit 1
	fi
	PLAN_DIR="../${BASE_NAME}-worktrees/${FEATURE}/plan"
	IMPL_DIR="../${BASE_NAME}-worktrees/${FEATURE}/impl"
	REVIEW_DIR="../${BASE_NAME}-worktrees/${FEATURE}/review"
else
	PLAN_DIR="../${BASE_NAME}-plan"
	IMPL_DIR="../${BASE_NAME}-impl"
	REVIEW_DIR="../${BASE_NAME}-review"
fi

git worktree remove "$PLAN_DIR" || true
git worktree remove "$REVIEW_DIR" || true
git worktree remove "$IMPL_DIR" || true

echo "Worktrees removed (if they existed):"
echo "- $PLAN_DIR"
echo "- $IMPL_DIR"
echo "- $REVIEW_DIR"