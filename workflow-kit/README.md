# Workflow Kit (Planner / Implementer / Reviewer via Git worktrees)

This folder is a **portable scaffolding bundle** you can copy into any repo to reuse the same development workflow.

## What you get

- `docs/AI_WORKFLOW_WORKTREES.md`: the workflow runbook
- `scripts/`: worktree helpers (`create-worktrees.sh`, `sync-worktrees.sh`, `remove-worktrees.sh`)
- `docs/templates/`: templates for plans, reviews, architecture, and follow-ups
- `docs/decisions/000-template.md`: ADR template

## Install into a new repo

From the **target repo root** (the repo you want to add the workflow to), run the installer from this kit:

```bash
bash workflow-kit/install.sh
```

Add `--force` to overwrite existing files:

```bash
bash workflow-kit/install.sh --force
```

## After install

- Read: `docs/AI_WORKFLOW_WORKTREES.md`
- Start a feature: `./scripts/create-worktrees.sh <feature>`
- Commit the plan from the planner worktree so it’s durable.

## Parallel lanes (multiple features at once)

If you want multiple features in flight without reusing the same `...-plan/impl/review` directories:

```bash
./scripts/create-worktrees.sh <feature> --parallel
./scripts/sync-worktrees.sh <feature> --parallel
./scripts/remove-worktrees.sh <feature> --parallel
```

List what exists:

```bash
./scripts/list-worktrees.sh
```

