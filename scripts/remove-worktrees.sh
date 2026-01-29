#!/bin/bash

# Remove the worktrees created for the AI workflow
git worktree remove ../Thesys-plan
git worktree remove ../Thesys-review
git worktree remove ../Thesys-impl

echo "Worktrees removed successfully."