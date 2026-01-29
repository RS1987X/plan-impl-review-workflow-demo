#!/bin/bash

# This script automates the creation of Git worktrees for the AI workflow.
# It sets up the necessary directories for the planner, implementer, and reviewer roles.

# Usage: ./create-worktrees.sh <feature-name>

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <feature-name>"
    exit 1
fi

FEATURE=$1

# Define the main repository directory
REPO_DIR=$(pwd)

# Create worktrees
git worktree add "$REPO_DIR/../ai-workflow-worktrees-test-plan" -b plan-$FEATURE
git worktree add "$REPO_DIR/../ai-workflow-worktrees-test-impl" -b feat-$FEATURE
git worktree add "$REPO_DIR/../ai-workflow-worktrees-test-review" -b review-$FEATURE

echo "Worktrees created for feature: $FEATURE"