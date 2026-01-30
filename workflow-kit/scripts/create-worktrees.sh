#!/bin/bash

set -euo pipefail

# This script automates the creation of Git worktrees for the AI workflow.
# It sets up the necessary directories for the planner, implementer, and reviewer roles.

# Usage:
#   ./create-worktrees.sh <feature-name> [--parallel]
#
# Default layout (single lane):
#   ../<repo>-plan, ../<repo>-impl, ../<repo>-review
#
# Parallel layout (multiple lanes):
#   ../<repo>-worktrees/<feature>/{plan,impl,review}

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
    echo "Usage: $0 <feature-name> [--parallel]"
    exit 1
fi

FEATURE="$1"
MODE="${2:-}"
PARALLEL=0
if [ "$MODE" = "--parallel" ]; then
    PARALLEL=1
elif [ -n "$MODE" ]; then
    echo "Unknown option: $MODE" >&2
    echo "Usage: $0 <feature-name> [--parallel]" >&2
    exit 1
fi

REPO_DIR=$(pwd)

# Make this script portable when run from -plan/-impl/-review worktrees.
REPO_BASENAME=$(basename "$REPO_DIR")
BASE_NAME=${REPO_BASENAME%-plan}
BASE_NAME=${BASE_NAME%-impl}
BASE_NAME=${BASE_NAME%-review}

if [ $PARALLEL -eq 1 ]; then
    WORKTREES_ROOT="$REPO_DIR/../${BASE_NAME}-worktrees/$FEATURE"
    PLAN_DIR="$WORKTREES_ROOT/plan"
    IMPL_DIR="$WORKTREES_ROOT/impl"
    REVIEW_DIR="$WORKTREES_ROOT/review"
    mkdir -p "$PLAN_DIR" "$IMPL_DIR" "$REVIEW_DIR"
else
    PLAN_DIR="$REPO_DIR/../${BASE_NAME}-plan"
    IMPL_DIR="$REPO_DIR/../${BASE_NAME}-impl"
    REVIEW_DIR="$REPO_DIR/../${BASE_NAME}-review"
fi

# Create worktrees
git worktree add "$PLAN_DIR"   -b "plan-$FEATURE"
git worktree add "$IMPL_DIR"   -b "feat-$FEATURE"
git worktree add "$REVIEW_DIR" -b "review-$FEATURE"

echo "Worktrees created for feature: $FEATURE"
echo "Planner:     $PLAN_DIR   (plan-$FEATURE)"
echo "Implementer: $IMPL_DIR   (feat-$FEATURE)"
echo "Reviewer:    $REVIEW_DIR (review-$FEATURE)"