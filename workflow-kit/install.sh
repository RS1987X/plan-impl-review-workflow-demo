#!/bin/bash

set -euo pipefail

FORCE=0
if [[ "${1:-}" == "--force" ]]; then
  FORCE=1
fi

# Resolve kit root (this script lives in workflow-kit/)
KIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Target is current working directory
TARGET_DIR="$(pwd)"

if [[ ! -d "$TARGET_DIR/.git" ]]; then
  echo "Error: run this from the target repo root (must contain .git/)" >&2
  exit 1
fi

copy_file() {
  local src="$1"
  local dst="$2"

  mkdir -p "$(dirname "$dst")"

  if [[ -e "$dst" && $FORCE -ne 1 ]]; then
    echo "Skip (exists): $dst"
    return 0
  fi

  cp "$src" "$dst"
  echo "Installed: $dst"
}

copy_tree() {
  local src_dir="$1"
  local dst_dir="$2"

  # Find all files in src_dir and copy to dst_dir preserving relative paths.
  while IFS= read -r -d '' file; do
    rel="${file#"$src_dir/"}"
    copy_file "$file" "$dst_dir/$rel"
  done < <(find "$src_dir" -type f -print0)
}

# Core workflow doc
copy_file "$KIT_DIR/docs/AI_WORKFLOW_WORKTREES.md" "$TARGET_DIR/docs/AI_WORKFLOW_WORKTREES.md"

# Templates
copy_tree "$KIT_DIR/docs/templates" "$TARGET_DIR/docs/templates"

# ADR template
copy_file "$KIT_DIR/docs/decisions/000-template.md" "$TARGET_DIR/docs/decisions/000-template.md"

# Scripts
copy_tree "$KIT_DIR/scripts" "$TARGET_DIR/scripts"

# Ensure scripts are executable
chmod +x "$TARGET_DIR/scripts/create-worktrees.sh" || true
chmod +x "$TARGET_DIR/scripts/sync-worktrees.sh" || true
chmod +x "$TARGET_DIR/scripts/remove-worktrees.sh" || true
if [[ -f "$TARGET_DIR/scripts/list-worktrees.sh" ]]; then
  chmod +x "$TARGET_DIR/scripts/list-worktrees.sh" || true
fi

echo "---"
echo "Done. Next steps:"
echo "- Read docs/AI_WORKFLOW_WORKTREES.md"
echo "- Start a feature: ./scripts/create-worktrees.sh <feature>"
