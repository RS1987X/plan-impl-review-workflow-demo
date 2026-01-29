#!/bin/bash

# This script synchronizes the Git worktrees with the latest changes from the main branch.

# Define the base directory for the project
BASE_DIR="$(dirname "$(dirname "$(realpath "$0")")")"

# Define the worktree directories
PLAN_DIR="$BASE_DIR/Thesys-plan"
IMPL_DIR="$BASE_DIR/Thesys-impl"
REVIEW_DIR="$BASE_DIR/Thesys-review"

# Function to sync a worktree
sync_worktree() {
    local dir=$1
    echo "Syncing worktree in $dir..."
    cd "$dir" || exit
    git fetch origin
    git merge origin/main
}

# Sync each worktree
sync_worktree "$PLAN_DIR"
sync_worktree "$IMPL_DIR"
sync_worktree "$REVIEW_DIR"

echo "All worktrees have been synchronized."