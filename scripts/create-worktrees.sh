#!/bin/bash

set -euo pipefail

# This script automates the creation of Git worktrees for the AI workflow.
# It sets up the necessary directories for the planner, implementer, and reviewer roles.

# Usage: ./create-worktrees.sh <feature-name>

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <feature-name>"
    exit 1
fi

FEATURE=$1

REPO_DIR=$(pwd)

# Make this script portable when run from -plan/-impl/-review worktrees.
REPO_BASENAME=$(basename "$REPO_DIR")
BASE_NAME=${REPO_BASENAME%-plan}
BASE_NAME=${BASE_NAME%-impl}
BASE_NAME=${BASE_NAME%-review}

PLAN_DIR="$REPO_DIR/../${BASE_NAME}-plan"
IMPL_DIR="$REPO_DIR/../${BASE_NAME}-impl"
REVIEW_DIR="$REPO_DIR/../${BASE_NAME}-review"

# Create worktrees
git worktree add "$PLAN_DIR"   -b "plan-$FEATURE"
git worktree add "$IMPL_DIR"   -b "feat-$FEATURE"
git worktree add "$REVIEW_DIR" -b "review-$FEATURE"

echo "Worktrees created for feature: $FEATURE"
echo "Planner:     $PLAN_DIR   (plan-$FEATURE)"
echo "Implementer: $IMPL_DIR   (feat-$FEATURE)"
echo "Reviewer:    $REVIEW_DIR (review-$FEATURE)"